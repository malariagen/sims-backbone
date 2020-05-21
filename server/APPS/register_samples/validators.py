"""
Validation for Bulk Add Samples File Uploads  aka Manifest File Upload
"""

from abc import ABCMeta, abstractmethod
import csv
import datetime
import json
import mimetypes
import logging
import os

from io import IOBase

from openpyxl.cell import Cell
from openpyxl.cell.cell import TYPE_FORMULA

from APPS.bulk_upload.errors import UploadParseError, HeaderError, _
from APPS.register_samples.errors import FieldError
import APPS.register_samples.helpers as helpers
from APPS.bulk_upload.csv_parser import BulkUploadCSVParser
from APPS.bulk_upload.excel_parser import BulkUploadExcelParser


LOGGER = logging.getLogger(__name__)

class BulkAddSamplesValidatorFactory():
    """
    Creates instance of the BulkAddSamplesValidator based on the manifest file type.

    EG)

    validator = BulkAddSamplesValidatorFactory.create_validator(manifest_file="/path/to/myfile.csv", study_id=2)
    validator.validate_manifest_file()

    """
    CONTENT_TYPE_CSVISH = ['csv', 'text']
    CONTENT_TYPE_XLSXISH = ['excel', 'spreadsheet', 'zip']
    CONTENT_TYPE_ZIPXISH = ['zip']




    @staticmethod
    def is_csv(manifest_file_type):
        manifest_file_type = manifest_file_type.strip().lower()
        for content_type in BulkAddSamplesValidatorFactory.CONTENT_TYPE_CSVISH:
            if content_type in manifest_file_type:
                return True
        return False

    @staticmethod
    def is_excel(manifest_file_type):
        manifest_file_type = manifest_file_type.strip().lower()
        # Technically, an xlsx is a zipped set of xml files.  Allow for zip mimetype.
        # This is particularly true for openpyxl files, which are determined to be zip by libmagic instead of excel.
        for content_type in BulkAddSamplesValidatorFactory.CONTENT_TYPE_XLSXISH :
            if content_type in manifest_file_type:
                return True
        return False


    @staticmethod
    def get_mime_type(manifest_file):
        """
        Attempt to determine mimetype from reading the file contents (using python-magic),
                    or from the filename extension (mimetypes module if python-magic is unavailable).
        Will read in the first 1024B if a file handle is passed in.  It's up to the user to reset the file handle pointer.
        @param manifest_file_name: can only be string full filepath or a file handle with a read method
        """

        manifest_file_type = None
        try:
            import magic
            if isinstance(manifest_file, str):  # filename
                manifest_file_type = magic.from_file(manifest_file, mime=True)
            elif hasattr(manifest_file, "read"): # file handle
                manifest_file_type = magic.from_buffer(manifest_file.read(2048), mime=True)
            else:
                raise TypeError("manifest_file must be string filepath or readable file handle")

        except ImportError:
            LOGGER.warn("Unable to use python-magic to determine mimetype from file contents.  " +
                             "Falling back to mimetypes library to determine mimetype for file name extension")

            if isinstance(manifest_file, str):  # filename
                manifest_file_type, encoding = mimetypes.guess_type(manifest_file)
            elif hasattr(manifest_file, "name"): # Django or IOBase file handle with name attribute
                manifest_file_type, encoding = mimetypes.guess_type(manifest_file.name)
            else:
                raise TypeError("manifest_file_name must be string")

        return manifest_file_type


    @staticmethod
    def create_validator(manifest_file, study, manifest_file_type=None, **kwargs):
        """
        Returns the appropriate CSV or Excel manifest validator based on the file's mime type.


        Be careful with passing in mime types determined by Django through the browser.
        Depending on which browser version, it may yield the wrong type.
        See  https://stackoverflow.com/questions/1201945/how-is-mime-type-of-an-uploaded-file-determined-by-browser and
          https://bugs.chromium.org/p/chromium/issues/detail?id=139105

        @param manifest_file:  String filepath to file or Django File handle or python IOBase readable file handle
        @param str manifest_file_type:  content type (mime type) of the manifest file to upload containing list of samples to associate with study.
                    If not given, then will attempt to determine mimetype from reading the file contents (using python-magic),
                    or from the filename extension (mimetypes module if python-magic is unavailable).
        """

        if not manifest_file_type:
            manifest_file_type = BulkAddSamplesValidatorFactory.get_mime_type(manifest_file)

        # Reset file pointer to beginning
        if hasattr(manifest_file, "read") and hasattr(manifest_file, "seek"):
            manifest_file.seek(0)


        if not isinstance(manifest_file_type, str):
            raise TypeError("manifest_file_type must be string.  Instead got " + str(type(manifest_file_type)) + " value=" + str(manifest_file_type))

        if manifest_file_type == 'application/octet-stream':
            mf_name = None
            mf_content_type = None
            if isinstance(manifest_file, str):
                mf_name = manifest_file
            else:
                mf_content_type = manifest_file.content_type
                mf_name = manifest_file.name

            file_name, file_extension = os.path.splitext(mf_name)
            if file_extension == '.csv':
                manifest_file_type = 'text/csv'
            if file_extension == '.xlsx' or mf_content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                manifest_file_type = 'application/excel'

        if BulkAddSamplesValidatorFactory.is_csv(manifest_file_type):
            return BulkAddSamplesCSVValidator(manifest_file, study, **kwargs)
        elif BulkAddSamplesValidatorFactory.is_excel(manifest_file_type):
            return BulkAddSamplesExcelValidator(manifest_file, study, **kwargs)
        else:
            raise FieldError(_('Unsupported manifest file mime-type "%(mimetype)s".  Please save manifest file as .csv or .xlsx.'),
                                      params={'mimetype': manifest_file_type},
                                      code=FieldError.INVALID_MF)


class BulkAddSamplesValidator(metaclass=ABCMeta):
    """
    Base class for Manifest Sample File validation (ie validating the file with bulk samples to upload)
    """
    def __init__(self, manifest_file, study, header_config_ini_fname=None,
                 is_check_dup_sample=True, is_raise_field_err=True,
                 sample_lookup_func=None):
        """
        @param str manifest_file:  path to excel workbook
        @param Study study:  study id
        @param str header_config_ini_fname:  path to sample manifest header config .ini file. If None, then uses default helper.DEFAULT_MANIFEST_CONFIG_INI
        @param boolean is_check_dup_sample:  whether to check if a sample already exists in the database.  If so, then this causes field validation to fail.
        @param boolean is_raise_field_err:  whether to raise a ValidationError if fail field validation.  If false,
        does the field validation check and only logs an error.  If true,
        then does the field validation check and throws a ValidationError.
        @param function sample_lookup_func: function to look up if the sample exists already outside the manifest
        """
        self.manifest_file = manifest_file
        self.study = study
        self.header_config_ini_fname = header_config_ini_fname
        self.is_check_dup_sample = is_check_dup_sample
        self.sample_ids = {}
        self.is_raise_field_err = is_raise_field_err

        self.search_locname_to_id = None
        self.parser = None
        self.sample_lookup_func = sample_lookup_func
        if not self.header_config_ini_fname:
            self.header_config_ini_fname = helpers.DEFAULT_MANIFEST_CONFIG_INI


    @abstractmethod
    def validate_manifest_file(self):
        """
        Reads sample manifest and validates each sample row entry.

        Fields for optional columns (i.e.  columns with headers not found in the header config .ini) will be combined into a single dict
        in the returned mapping {"tags":  dict containing optional field values}.
        Fields with empty values are not returned in the row dict.

        @returns Iterator samples_iter:  Iterator over list of dicts. Each dict maps {db header name => Sample db field value}
        """
        raise NotImplementedError("Must implement validate_manifest_file()")

    def is_valid_study(self):

        if not self.study:
            raise FieldError(_("No study specified"),
                             code=FieldError.INVALID_STUDY)


    def is_dup_sample_intra_manifest(self, field, value, cell=None):

        if value in self.sample_ids:
            raise FieldError(_("Sample with external id %(external_id)s already exists in the manifest"),
                             params={'external_id': value},
                             code=FieldError.DUP_SAMPLE)
        else:
            self.sample_ids[value] = field
            return False


    def is_dup_sample_extra_manifest(self, field, value, cell=None):

        # Rule applies across all studies
        # use self.study if want to make it within study

        sample = self.sample_lookup_func(field, value)

        if self.is_check_dup_sample and sample:
            raise FieldError(_("Sample with external id %(external_id)s is already registered in study %(study)s"),
                             params={
                                 'external_id': value,
                                 'study': sample.study.name
                             },
                             code=FieldError.DUP_SAMPLE)
        else:
            return False

    def load_location_cache(self):
        if not self.search_locname_to_id:
            locs = self.study.locations.locations
            self.search_locname_to_id = {}
            self.search_locname_to_id = {str(loc.curated_name).strip().lower() : loc.location_id for loc in locs}

            for loc in locs:
                self.search_locname_to_id[loc.curated_name.strip().lower()] = loc.location_id

    def is_study_location(self, value):

        # cache
        self.load_location_cache()
        search_value = str(value).strip().lower()
        if search_value not in self.search_locname_to_id:
            raise FieldError(_("%(value)s is not a location registered with study project code %(study_project_code)s. If you want to add this location, please contact the Coordinator."),
                             params={"value": value,
                                     "study_project_code": self.study.name},
                             code=FieldError.INVALID_LOC)

        validated_value = self.search_locname_to_id[search_value]

        return validated_value

    def validate_field(self, field, value, cell=None):
        """
        collection date is expected to be in format %Y-%m-%d if it is not formatted as Date Cell in excel.
        If the field is optional (i.e.  not one of helpers.MANIFEST_DB_COL_EXT_ID, helpers.MANIFEST_DB_COL_COLLECT_DATE, helpers.MANIFEST_DB_COL_LOC_ID)
        then it gets returned as is with whitespace stripped.
        @param str field:  fieldname as it appears in the database under Samples table
        @param value:  can be any type
        """


        if not self.study:
            raise ValueError(_("We can only validate bulk uploaded samples for a given study.  Please specify study"))

        if isinstance(value, str):
            value = value.strip()

        validated_value = value

        if field == helpers.MANIFEST_DB_COL_EXT_ID:
            if not value:
                req_nice_headers, req_db_to_nice_header, req_nice_to_db_header = self.parser.config.read_header_config()
                nice_header = req_db_to_nice_header.get(helpers.MANIFEST_DB_COL_EXT_ID)
                raise FieldError(_('Mandatory field "%(field)s" is missing'),
                                 params={"field": nice_header},
                                 code=FieldError.MISSING_FIELD)

            else:
                self.is_dup_sample_intra_manifest(field, value, cell)
                self.is_dup_sample_extra_manifest(field, value, cell)

        # If the user formats the cell as date, it doesn't really matter which format they use
        # since openpyxl will convert to datetime.datetime accordingly.
        # But if the user formats the cell as string, they MUST use YYYY-MM-DD format,
        # otherwise we have no way of knowing which is month and day for things like January 1, 2000.
        # We don't support numeric representations of date (e.g.  seconds since Epoch), since epoch varies from OS to OS
        # and we have no control or knowlege of where the excel sheets are created.
        elif field == helpers.MANIFEST_DB_COL_COLLECT_DATE:
            if not value:
                req_nice_headers, req_db_to_nice_header, req_nice_to_db_header = self.parser.config.read_header_config()
                nice_header = req_db_to_nice_header.get(helpers.MANIFEST_DB_COL_COLLECT_DATE)
                raise FieldError(_('Mandatory field "%(field)s" is missing'),
                                 params={"field": nice_header},
                                 code=FieldError.MISSING_FIELD)

            if isinstance(value, str):
                try:
                    validated_value = datetime.datetime.strptime(value, '%Y-%m-%d').date()
                except ValueError as e:
                    raise FieldError(_("Collection Date '%(value)s' does not match format YYYY-MM-DD"),
                                     params={"value": value},
                                     code=FieldError.INVALID_DATE) from e

            elif isinstance(value, (datetime.date, datetime.datetime)):
                validated_value = value.date()
            else:
                raise FieldError(_("Collection Date '%(value)s' does not match format YYYY-MM-DD"),
                                 params={"value": value},
                                 code=FieldError.INVALID_DATE)

            present = datetime.datetime.date(datetime.datetime.now())

            if validated_value > present:
                raise FieldError(_("Collection Date '%(value)s' is in the future"),
                                 params={"value": value},
                                 code=FieldError.INVALID_DATE)


        elif field == helpers.MANIFEST_DB_COL_LOC_ID:
            if not value:
                req_nice_headers, req_db_to_nice_header, req_nice_to_db_header = self.parser.config.read_header_config()
                nice_header = req_db_to_nice_header.get(helpers.MANIFEST_DB_COL_LOC_ID)
                raise FieldError(_('Mandatory field "%(field)s" is missing'),
                                 params={"field": nice_header},
                                 code=FieldError.MISSING_FIELD)


            validated_value = self.is_study_location(value)


# In theory data_only=True means this shouldn't be possible
        if cell and cell.data_type == TYPE_FORMULA:
            raise FieldError(_('Field  contains a formula {value}'),
                             params={"value": value},
                             code=FieldError.FORMULA)



        return validated_value



class BulkAddSamplesCSVValidator(BulkAddSamplesValidator):
    """
    Validates CSV Manifest Files (aka File of Samples to register with study)
    """

    def __init__(self, manifest_file, study, header_config_ini_fname=None,
                 is_check_dup_sample=True, is_raise_field_err=True,
                 sample_lookup_func=None):
        """
        @param str manifest_file:  path to excel workbook
        @param dict study:  study id
        @param str header_config_ini_fname:  path to sample manifest header config .ini file. If None, then uses default helper.DEFAULT_MANIFEST_CONFIG_INI
        @param boolean is_check_dup_sample:  whether to check if a sample already exists in the database.  If so, then this causes field validation to fail.
        @param boolean is_raise_field_err:  whether to raise a ValidationError if fail field validation.  If false,
        does the field validation check and only logs an error.  If true,
        then does the field validation check and throws a ValidationError.
        @param function sample_lookup_func: function to look up if the sample exists already outside the manifest
        """
        super().__init__(manifest_file=manifest_file, study=study,
                         header_config_ini_fname=header_config_ini_fname,
                         is_check_dup_sample=is_check_dup_sample,
                         is_raise_field_err=is_raise_field_err,
                         sample_lookup_func=sample_lookup_func)
        self.parser = BulkUploadCSVParser(header_config_file=self.header_config_ini_fname, upload_file=self.manifest_file)


    def validate_manifest_file(self):
        """
        Reads sample manifest and validates each sample row entry.

        Fields for optional columns (i.e.  columns with headers not found in the header config .ini) will be combined into a single dict
        in the returned mapping {"tags":  dict containing optional field values}.
        Fields with empty values are not returned in the row dict.

        If BulkAddSamplesCSVValidator.is_check_dup_sample==True, then doesn't check if the sample already in db.
        If BulkAddSamplesCSVValidator.is_raise_field_err==True, then doesn't raise a ValidationError when a field fails validation and just logs an exception.

        @returns Iterator samples_iter:  Iterator over list of dicts. Each dict maps {db header name => Sample db field value}
        """
        if not self.header_config_ini_fname:
            header_config_ini_fname = helpers.DEFAULT_MANIFEST_CONFIG_INI

        self.is_valid_study()

        try:
            self.parser.validate_headers()
        except HeaderError as e:
            raise e
        except Exception as e:
                raise HeaderError(_('%(msg)s'),
                                  code=FieldError.BAD_HEADER,
                                  params={'msg': str(e)}) from e

        nice_header_name = ""
        row_1idx = -1
        try:
            req_nice_headers, req_db_to_nice_header, req_nice_to_db_header = self.parser.config.read_header_config()
            for row_0idx, row in enumerate(self.parser.get_data_row_iter()):
                row_1idx = row_0idx + 1

                # If the entire row is empty, skip it. But if some fields are filled but not others, complain about missing fields.
                nonempty_values = [value for value in row.values() if len(str(value).strip()) > 0]
                if not nonempty_values:
                    continue

                validated_sample_dict = {}
                tags = {}
                field_errors = []
                for nice_header_name, val in row.items():
                    db_header_name = req_nice_to_db_header.get(nice_header_name.lower(), helpers.DB_HEADER_TAGS)
                    if val is not None and val != "":  # We allow cell value == 0
                        try:
                            if db_header_name == helpers.DB_HEADER_TAGS:
                                tags[nice_header_name] = self.validate_field(db_header_name, val)
                            else:
                                validated_sample_dict[db_header_name] = self.validate_field(db_header_name, val)
                        except FieldError as e:
                            if self.is_raise_field_err:
                                raise e
                            else:
                                err_msg = "Failed validation for row={}, field = '{}', value='{}' {}".format(row_1idx,
                                                                                                             db_header_name,
                                                                                                             val,
                                                                                                             str(e))
                                LOGGER.exception(err_msg)
                                field_errors.append(err_msg)

                if tags:
                    validated_sample_dict[helpers.DB_HEADER_TAGS] = tags

                if validated_sample_dict:
                    response = {
                        "valid": not field_errors,
                        "errors": field_errors,
                        "sample": validated_sample_dict
                    }
                    yield response
        except FieldError as e:
            if row_1idx and nice_header_name:
                # If the row and column info is available, then wrap the exception with another ValidationError to give the row + col info.
                msg = str(e)
                raise FieldError(_('Invalid value at row %(row_1idx)d , column "%(col)s": %(msg)s'),
                                      code=e.code,
                                      params={
                                          'row_1idx': row_1idx,
                                          'col': nice_header_name,
                                          'msg': msg
                                      }) from e
            else:
                raise e
        except Exception as e:  # Wrap unexpected exceptions with a nicer validationError with a nice message that we can display direclty to user.
            if row_1idx and nice_header_name:
                # If the row and column info is available, then wrap the exception with another ValidationError to give the row + col info.
                raise FieldError(_('Invalid value at row %(row_1idx)d , column "%(col)s": %(msg)s'),
                                      code=FieldError.INVALID_FIELD,
                                      params={'row_1idx': row_1idx, 'col': nice_header_name, 'msg':  str(e), "field": db_header_name, "value": val}) from e
            else:
                raise e



class BulkAddSamplesExcelValidator(BulkAddSamplesValidator):
    """
    Validates CSV Manifest Files (aka File of Samples to register with study)
    """
    def __init__(self, manifest_file, study, header_config_ini_fname=None,
                 is_check_dup_sample=True, is_raise_field_err=True,
                 sample_lookup_func=None):
        """
        @param str manifest_file:  path to excel workbook
        @param dict study:  study id
        @param str header_config_ini_fname:  path to sample manifest header config .ini file. If None, then uses default helper.DEFAULT_MANIFEST_CONFIG_INI
        @param boolean is_check_dup_sample:  whether to check if a sample already exists in the database.  If so, then this causes field validation to fail.
        @param boolean is_raise_field_err:  whether to raise a ValidationError if fail field validation.  If false,
        does the field validation check and only logs an error.  If true,
        then does the field validation check and throws a ValidationError.
        @param function sample_lookup_func: function to look up if the sample exists already outside the manifest
        """
        super().__init__(manifest_file=manifest_file, study=study,
                         header_config_ini_fname=header_config_ini_fname,
                         is_check_dup_sample=is_check_dup_sample,
                         is_raise_field_err=is_raise_field_err,
                         sample_lookup_func=sample_lookup_func)
        self.parser = BulkUploadExcelParser(header_config_file=self.header_config_ini_fname, upload_file=self.manifest_file)


    def validate_manifest_file(self, is_raise_field_err=True):
        """
        Reads excel sheet of sample manifest and validates each sample entry.

        Fields for optional columns (i.e.  columns with headers not found in the header config .ini) will be combined into a single json object
        in the returned mapping {"tags":  python dict object containing optional field values}.
        Fields with empty values are not returned in the row dict.

        If BulkAddSamplesExcelValidator.is_check_dup_sample==True, then doesn't check if the sample already in db.
        If BulkAddSamplesExcelValidator.is_raise_field_err==True, then doesn't raise a ValidationError when a field fails validation and just logs an exception.

        @returns Iterator samples_iter:  Iterator over list of dicts. Each dict maps {db header name => Sample db field value}

        """

        self.is_valid_study()

        try:
            config_sheet_name = self.parser.config.get_config_sheet_name()
            sample_sheet = self.parser.get_data_sheet()
        except ValueError as e:
            raise UploadParseError(_("Required worksheet '%(expected_sample_sheet_name)s' doesn't exist"),
                                  code=FieldError.MISSING_SAMPLES_TAB,
                                  params={'expected_sample_sheet_name': config_sheet_name}) from e
        except Exception as e:
            raise UploadParseError(_("Invalid manifest file.  Please save your manifest as .csv or .xlsx format.  %(msg)s"),
                                  code=FieldError.INVALID_MF,
                                  params={'msg': str(e)}) from e

        try:
            self.parser.validate_headers()
        except HeaderError as e:
            raise e
        except Exception as e:
                raise HeaderError(_('Unable to parse header.  %(msg)s'),
                                  code=FieldError.BAD_HEADER,
                                  params={'msg': str(e)}) from e



        nice_header_name = ""
        coord = "?"
        try:
            req_nice_headers, req_db_to_nice_header, req_nice_to_db_header = self.parser.config.read_header_config()
            for row in self.parser.get_data_row_iter():
                if not len(row):
                    continue  # skip empty rows

                validated_sample_dict = {}
                tags = {}
                field_errors = []
                for nice_header_name, cell in row.items():
                    db_header_name = req_nice_to_db_header.get(nice_header_name.lower(), helpers.DB_HEADER_TAGS)
                    val = cell.value
                    if isinstance(val, str):
                        val = val.strip()
                    if val is not None and val != "":  # We allow cell value == 0
                        coord = cell.coordinate  # coordinate only exists if cell is nonempty
                        try:
                            if db_header_name == helpers.DB_HEADER_TAGS:
                                tags[nice_header_name] = self.validate_field(db_header_name, val, cell)
                            else:
                                validated_sample_dict[db_header_name] = self.validate_field(db_header_name, val, cell)
                        except FieldError as e:
                            field_error = True
                            if self.is_raise_field_err:
                                raise e
                            else:
                                err_msg = "Failed validation for coord = {}, field='{}', value='{}' {}".format(coord, db_header_name, val, str(e))
                                LOGGER.exception(err_msg)
                                field_errors.append(err_msg)

                if tags:
                    validated_sample_dict[helpers.DB_HEADER_TAGS] = tags

                if validated_sample_dict:
                    response = {
                        "valid": not field_errors,
                        "errors": field_errors,
                        "sample": validated_sample_dict
                    }
                    yield response
        except FieldError as e:
            if coord and nice_header_name:
                # If the row and column info is available, then wrap the exception with another ValidationError to give the row + col info.
                if len(e.messages) == 1:  # ValidationError.messages is a list of error messages.  If there's only 1, we don't need the enclosing brackets.
                    msg = e.messages[0]
                else:
                    msg = e.messages
                raise FieldError(_('Error at worksheet "%(config_sheet_name)s", coordinate %(coord)s,  column "%(col)s": %(msg)s'),
                                      code=e.code,
                                      params={'config_sheet_name': config_sheet_name, 'coord': coord, 'col': nice_header_name, 'msg': msg, "field": db_header_name, "value": val}) from e
            else:
                raise e
        except Exception as e:
            import traceback
            traceback.print_exc()
            if coord and nice_header_name:
                # If the row and column info is available, then wrap the exception with another ValidationError to give the row + col info.
                raise FieldError(_('Error at worksheet "%(config_sheet_name)s", coordinate %(coord)s,  column "%(col)s": %(msg)s'),
                                      code=FieldError.INVALID_FIELD,
                                      params={'config_sheet_name': config_sheet_name, 'coord': coord, 'col': nice_header_name, 'msg': str(e), "field": db_header_name, "value": val}) from e
            else:
                raise e
