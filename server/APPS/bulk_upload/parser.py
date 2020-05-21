from configparser import RawConfigParser
from abc import ABCMeta, abstractmethod
from collections import Counter
from io import IOBase, BytesIO

from APPS.bulk_upload.errors import HeaderError, _

class BulkUploadConfig(metaclass=ABCMeta):
    """
    Base Class for reading in the .ini files used to configure headers in files used for bulk uploads.
    There is a 1:1 mapping from db table header to bulk upload file header for mandatory fields specified in the bulk upload config file.
    But all the optional fields in the bulk upload file are aggregated into a single json object within the db.
    """

    def __init__(self, header_config_file, header_section):
        """
        @param str header_config_file:  filepath to .ini file that specifies human readable headers and their corresponding db columns
        @param str header_section:   header config ini section that maps the db field name to the user friendly name displayed in the file
        """
        self.header_config_file = header_config_file
        self.header_section = header_section


    def read_header_config(self):
        """
        Reads in the required column headers from a .ini file
        Expects that the .ini file has a section from which required headers are specified.  Strips any trailing and leading whitespace in human readable header names.
        @return ([human readable headers in same order as defined in .ini], {db header: human readable header}, {human readable header lowercase: db header})
        """

        nice_headers = []
        db_to_nice_header = {}
        nice_to_db_header = {}
        config = RawConfigParser()
        try:
            config.read(self.header_config_file)
            header_section_opts = config.options(self.header_section)

            for db_header in header_section_opts:
                nice_header = config.get(self.header_section, db_header).strip()
                db_to_nice_header[db_header] = nice_header
                nice_to_db_header[nice_header.lower()] = db_header
                nice_headers.append(nice_header)

        except Exception as e:
            raise ValueError("Header Config INI " + str(self.header_config_file) + " is not defined or is not correct. Please contact the coordinator.") from e

        return nice_headers, db_to_nice_header, nice_to_db_header


    def get_nice_headers(self):
        """
        """
        nice_headers = []
        config = RawConfigParser()
        try:
            config.read(self.header_config_file)
            header_section = config.options(self.header_section)

            for db_header in header_section:
                nice_header = config.get(self.header_section, db_header)
                nice_headers.extend([nice_header])

        except Exception as e:
            raise ValueError("Header Configuration INI " + str(self.header_config_file) + " is not defined or is not correct. Please contact the coordinator.") from e

        return nice_headers




class BulkUploadFileParser(metaclass=ABCMeta):
    """
    Base class for parsing data uploaded in bulk via excel, csv, etc.  For configuring the data column headers and how the data should be presented, use BulkUploadConfig.
    """

    def __init__(self, header_config_file, upload_file, header_section):
        """
        @param str header_config_file:  filepath to .ini file that specifies human readable headers and their corresponding db columns
        @param str upload_file:  filepath to csv or xls from which to upload bulk data
        @param str header_section:   header config ini section that maps the db field name to the user friendly name displayed in the file
        """
        self.header_config_file = header_config_file
        self.upload_file = upload_file
        self.header_section = header_section

        self.bulk_upload_config = BulkUploadConfig(header_config_file=header_config_file, header_section=header_section)


    @property
    def config(self):
        """
        The instantiated BulkUploadConfig object
        """
        return self.bulk_upload_config

    @abstractmethod
    def get_data_headers(self):
        """
        Get the headers from the data upload file
        @return [str] :  list of header names as displayed in the data upload file
        """
        raise NotImplementedError("Must override get_headers()")


    def as_handle(self, fileish, mode):
        """
        Returns a file handle if fileish is string, otherwise returns fileish as is.
        """
        if isinstance(fileish, IOBase) and hasattr(fileish, "name"): # regular python3 file handle needs to be opened
            if fileish.closed == False:
                fh =  fileish
            else:  # file handle to closed file
                fh = open(fileish.name, mode)
        elif isinstance(fileish, BytesIO):
            fh = fileish
        elif isinstance(fileish, str):
            fh = open(fileish, mode)
        else:
            raise TypeError("We can only handle io.FileIO and django.core.files.base.File file handles or filenames as string" + str(type(fileish)))
        return fh


    def validate_headers(self):
        """
        Checks that the required column headers exist in the data file.
        You are allowed other column headers that are not in the required header config file,
        but all required columns should exist in the data file.

        Checks that there are no duplicate headers

        @return True if all the required headers exist in the upload file
        @raises ValueError:  if required headers don't all exist in upload file
        """

        req_nice_headers, req_db_to_nice_header, req_nice_to_db_header = self.bulk_upload_config.read_header_config()

        # We want to case insensitive match the headers ignoring leading trailing blanks
        # It's possible that the header row that we found has poorly formatted cells (ie non string).  Convert to string first before comparisons.
        searchable_data_header_to_count = Counter([act_header.lower()  for act_header in self.get_data_headers()])
        searchable_to_req_nice_header = {exp_header.lower() : exp_header for exp_header in req_nice_headers}

        searchable_data_header_set = set(searchable_to_req_nice_header.keys())
        searchable_req_nice_header_set = set(searchable_data_header_to_count.keys())
        missing_nice_header_searchable_set = searchable_data_header_set.difference(searchable_req_nice_header_set)

        if missing_nice_header_searchable_set:
            missing_nice_headers = [searchable_to_req_nice_header[searchable] for searchable in missing_nice_header_searchable_set]
            raise HeaderError(_("Missing header(s): ")+ ";".join(missing_nice_headers),
                              code=HeaderError.MISSING_HEADER)

        # Check for duplicate headers
        dup_data_headers = [header for header, count in searchable_data_header_to_count.items() if count > 1]
        if dup_data_headers:
            raise HeaderError(_("Duplicate header(s): ") + ";".join(dup_data_headers) + ".  " +
                                    _("Note that headers are case insensitive and ignore trailing and leading whitespace."),
                              code=HeaderError.DUP_HEADER)

        return True


    @abstractmethod
    def get_data_row_iter(self):
        """
        Advance row iterator to data (ie just past the header row).
        Yields all cells, even for columns that weren't configured in the header .ini file.
        Skips any columns with blank headers after all trailing and leading white space is stripped.

        EG)  an Excel Parser will return a dict for each row where the values are the openpyxl Cell objects.
        A csv parser will return a dict for each row where the values are the string values for the field.

        @return iterator of dicts: Each row represented by dict mapping {db field name => field value in format specific to the upload file type}

        """


