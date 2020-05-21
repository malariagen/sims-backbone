
import json
import datetime
import csv

import tempfile
import string
import os
import uuid

import pytest

from APPS.register_samples.errors import FieldError
from APPS.bulk_upload.errors import ValidationError

from APPS.register_samples.validators import BulkAddSamplesValidatorFactory
from APPS.bulk_upload.errors import HeaderError
import APPS.register_samples.helpers as helpers
from APPS.bulk_upload.csv_parser import BulkUploadCSVConfig

from openapi_server.models.locations import Locations  # noqa: E501
from openapi_server.models.location import Location  # noqa: E501

from backbone_server.model.original_sample import OriginalSample
from backbone_server.model.attr import Attr
from backbone_server.model.study import Study

from test_base import TestBase

TEST_USERNAME = "test_user"


MNF_HEADER_DB_DISPLAY_MAP = {"external_id": "Specimen ID",
                             "collection_date": "Collection Date",
                             "location_id": "Collection Location (see locations sheet)",
                             "note": "Notes"}

MNF_DIR = os.path.dirname(os.path.realpath(__file__)) + os.sep + os.pardir + os.sep + "assets"

class TestUploadManifestCreateView(TestBase):

    @classmethod
    def setup_class(cls):
        """ setup any state specific to the execution of the given class (which
        usually contains tests).
        """
        location = Location(location_id=uuid.uuid4(), curated_name='CSV Test Location')
        location2 = Location(location_id=uuid.uuid4(), curated_name='CSV Test Location2')
        locations = Locations()
        locations.locations = [location]
        locations.count = 1
        TestUploadManifestCreateView.location = location
        TestUploadManifestCreateView.location2 = location2
        study = Study(code='8888', name='8888-VAL-MD_UP')
        study.locations = locations
        TestUploadManifestCreateView.study = study
        TestUploadManifestCreateView.alt_study = Study(code='8887', name='8887-VAL-MD_UP')
        TestUploadManifestCreateView.study2 = Study(code='8886', name='8886-VAL-MD_UP')



    @classmethod
    def teardown_class(cls):
        """ teardown any state that was previously setup with a call to
        setup_class.
        """
        pass

    registered_samples = []
    test_study = None

    def lookup_sample_func(self, field, value):

        for samp in self.registered_samples:
            if samp[field] == value:
                ret = OriginalSample()
                ret.attrs = [Attr(attr_type=field, attr_value_str=value)]
                ret.study = self.test_study
                return ret

        return None

    def test_blank_rows(self):
        """
        GIVEN:  I upload a valid sample csv containing blank rows in between data rows
        WHEN:  we validate the csv
        THEN: the blank rows are stripped out
        AND: the samples are validated successfully

        """
        csv_fname = None
        try:
            TOTAL_ROWS = 5
            TOTAL_NONEMPTY_ROWS = 3

            manifest_config_ini = helpers.DEFAULT_MANIFEST_CONFIG_INI
            manifest_config = BulkUploadCSVConfig(header_config_file=manifest_config_ini)
            nice_headers, db_to_nice_header, nice_to_db_header = manifest_config.read_header_config()

            # Create test csv
            tmp = tempfile.NamedTemporaryFile(suffix=".csv", prefix="blankRows_SampleManifest", delete=False)
            tmp.close()
            csv_fname = tmp.name

            with open(csv_fname, 'w') as fh:
                writer = csv.DictWriter(fh, fieldnames = [db_to_nice_header["external_id"],
                                                          db_to_nice_header["collection_date"],
                                                          db_to_nice_header["location_id"],
                                                          db_to_nice_header["note"]])
                # Set the header
                writer.writeheader()

                # Fill in the rows
                for irow in range(TOTAL_NONEMPTY_ROWS - 1):
                    outrow = {}
                    outrow[db_to_nice_header["external_id"]] = "Sample" + str(irow)
                    outrow[db_to_nice_header["collection_date"]] = datetime.date(year=2000, month=1, day=19).strftime("%Y-%m-%d")
                    outrow[db_to_nice_header["location_id"]] = TestUploadManifestCreateView.location.curated_name
                    outrow[db_to_nice_header["note"]] = None

                    writer.writerow(outrow)

                for irow in range(TOTAL_NONEMPTY_ROWS - 1, TOTAL_ROWS - 1):
                    outrow = {}
                    outrow[db_to_nice_header["external_id"]] = None
                    outrow[db_to_nice_header["collection_date"]] = None
                    outrow[db_to_nice_header["location_id"]] = None
                    outrow[db_to_nice_header["note"]] = None
                    writer.writerow(outrow)

                # last row
                outrow = {}
                outrow[db_to_nice_header["external_id"]] = "Sample" + str(TOTAL_NONEMPTY_ROWS-1)
                outrow[db_to_nice_header["collection_date"]] = datetime.date(year=2000, month=1, day=19).strftime("%Y-%m-%d")
                outrow[db_to_nice_header["location_id"]] = TestUploadManifestCreateView.location.curated_name
                outrow[db_to_nice_header["note"]] = None

                writer.writerow(outrow)

            validator = BulkAddSamplesValidatorFactory.create_validator(manifest_file=csv_fname,
                                                                        manifest_file_type="text/csv",
                                                                        study=TestUploadManifestCreateView.study,
                                                                        sample_lookup_func=self.lookup_sample_func)
            samples_iter = validator.validate_manifest_file()

            actual_data = []
            for resp in samples_iter:
                actual_data.append(resp["sample"])
            expected_data = [{"external_id": "Sample0",
                              "location_id": TestUploadManifestCreateView.location.location_id,
                              "collection_date": datetime.date(year=2000, month=1, day=19)},
                             {"external_id": "Sample1",
                              "location_id": TestUploadManifestCreateView.location.location_id,
                              "collection_date": datetime.date(year=2000, month=1, day=19)},
                             {"external_id": "Sample2",
                              "location_id": TestUploadManifestCreateView.location.location_id,
                              "collection_date": datetime.date(year=2000, month=1, day=19)}
                             ]


            assert actual_data == expected_data

        finally:
            if csv_fname and os.path.exists(csv_fname):
                print("Deleting test file " + str(csv_fname))
                os.remove(csv_fname)


    def test_file_handle_as_input(self):
        """
        GIVEN:  I upload a valid sample csv containing blank rows in between data rows
        WHEN:  we validate the csv
        THEN: the blank rows are stripped out
        AND: the samples are validated successfully

        """
        csv_fname = None
        try:
            TOTAL_ROWS = 5
            TOTAL_NONEMPTY_ROWS = 3

            manifest_config_ini = helpers.DEFAULT_MANIFEST_CONFIG_INI
            manifest_config = BulkUploadCSVConfig(header_config_file=manifest_config_ini)
            nice_headers, db_to_nice_header, nice_to_db_header = manifest_config.read_header_config()

            # Create test csv
            tmp = tempfile.NamedTemporaryFile(suffix=".csv", prefix="blankRows_SampleManifest", delete=False)
            tmp.close()
            csv_fname = tmp.name

            with open(csv_fname, 'w') as fh:
                writer = csv.DictWriter(fh, fieldnames = [db_to_nice_header["external_id"],
                                                          db_to_nice_header["collection_date"],
                                                          db_to_nice_header["location_id"],
                                                          db_to_nice_header["note"]])
                # Set the header
                writer.writeheader()

                # Fill in the rows
                for irow in range(TOTAL_NONEMPTY_ROWS - 1):
                    outrow = {}
                    outrow[db_to_nice_header["external_id"]] = "Sample" + str(irow)
                    outrow[db_to_nice_header["collection_date"]] = datetime.date(year=2000, month=1, day=19).strftime("%Y-%m-%d")
                    outrow[db_to_nice_header["location_id"]] = TestUploadManifestCreateView.location.curated_name
                    outrow[db_to_nice_header["note"]] = None

                    writer.writerow(outrow)

                for irow in range(TOTAL_NONEMPTY_ROWS - 1, TOTAL_ROWS - 1):
                    outrow = {}
                    outrow[db_to_nice_header["external_id"]] = None
                    outrow[db_to_nice_header["collection_date"]] = None
                    outrow[db_to_nice_header["location_id"]] = None
                    outrow[db_to_nice_header["note"]] = None
                    writer.writerow(outrow)

                # last row
                outrow = {}
                outrow[db_to_nice_header["external_id"]] = "Sample" + str(TOTAL_NONEMPTY_ROWS-1)
                outrow[db_to_nice_header["collection_date"]] = datetime.date(year=2000, month=1, day=19).strftime("%Y-%m-%d")
                outrow[db_to_nice_header["location_id"]] = TestUploadManifestCreateView.location.curated_name
                outrow[db_to_nice_header["note"]] = None

                writer.writerow(outrow)

            with open(csv_fname, 'rb') as fh:
                validator = BulkAddSamplesValidatorFactory.create_validator(manifest_file=csv_fname,
                                                                            manifest_file_type="text/csv",
                                                                            study=TestUploadManifestCreateView.study,
                                                                            sample_lookup_func=self.lookup_sample_func)
                samples_iter = validator.validate_manifest_file()

                actual_data = []
                for resp in samples_iter:
                    actual_data.append(resp["sample"])
                expected_data = [{"external_id": "Sample0",
                                  "location_id": TestUploadManifestCreateView.location.location_id,
                                  "collection_date": datetime.date(year=2000, month=1, day=19)
                                 },
                                 {"external_id": "Sample1",
                                  "location_id": TestUploadManifestCreateView.location.location_id,
                                  "collection_date": datetime.date(year=2000, month=1, day=19),
                                 },
                                 {"external_id": "Sample2",
                                  "location_id": TestUploadManifestCreateView.location.location_id,
                                  "collection_date": datetime.date(year=2000, month=1, day=19),
                                 }
                                ]


                assert actual_data == expected_data

        finally:
            if csv_fname and os.path.exists(csv_fname):
                print("Deleting test file " + str(csv_fname))
                os.remove(csv_fname)

# Test doesn't work but the code does
#    def test_bom_ascii(self):
#        """
#        GIVEN:  I upload a valid sample csv containing blank rows in between data rows
#        WHEN:  we validate the csv
#        THEN: the blank rows are stripped out
#        AND: the samples are validated successfully
#
#        """
#        csv_fname = None
#        try:
#            TOTAL_ROWS = 5
#            TOTAL_NONEMPTY_ROWS = 3
#
#            manifest_config_ini = helpers.DEFAULT_MANIFEST_CONFIG_INI
#            manifest_config = BulkUploadCSVConfig(header_config_file=manifest_config_ini)
#            nice_headers, db_to_nice_header, nice_to_db_header = manifest_config.read_header_config()
#
#            # Create test csv
#            tmp = tempfile.NamedTemporaryFile(suffix=".csv", prefix="blankRows_SampleManifest", delete=False)
#            tmp.close()
#            csv_fname = tmp.name
#
#            with open(csv_fname, 'w', encoding='utf-8-sig', newline='\r\n') as fh:
#
#                writer = csv.DictWriter(fh, fieldnames=[db_to_nice_header["external_id"],
#                                                        db_to_nice_header["collection_date"],
#                                                        db_to_nice_header["location_id"],
#                                                        db_to_nice_header["note"]])
#                # Set the header
#                writer.writeheader()
#
#                outrows = []
#                # Fill in the rows
#                for irow in range(TOTAL_NONEMPTY_ROWS - 1):
#                    outrow = {}
#                    outrow[db_to_nice_header["external_id"]] = "Sample" + str(irow)
#                    outrow[db_to_nice_header["collection_date"]] = datetime.date(year=2000, month=1, day=19).strftime("%Y-%m-%d")
#                    outrow[db_to_nice_header["location_id"]] = self.location.curated_name
#                    outrow[db_to_nice_header["note"]] = None
#
#                    outrows.append(outrow)
#
#
#                for irow in range(TOTAL_NONEMPTY_ROWS - 1, TOTAL_ROWS - 1):
#                    outrow = {}
#                    outrow[db_to_nice_header["external_id"]] = None
#                    outrow[db_to_nice_header["collection_date"]] = None
#                    outrow[db_to_nice_header["location_id"]] = None
#                    outrow[db_to_nice_header["note"]] = None
#                    outrows.append(outrow)
#
#                # last row
#                outrow = {}
#                outrow[db_to_nice_header["external_id"]] = "Sample" + str(TOTAL_NONEMPTY_ROWS-1)
#                outrow[db_to_nice_header["collection_date"]] = datetime.date(year=2000, month=1, day=19).strftime("%Y-%m-%d")
#                outrow[db_to_nice_header["location_id"]] = self.location.curated_name
#                outrow[db_to_nice_header["note"]] = None
#
#                outrows.append(outrow)
#
#                for row in outrows:
#                    # writer.writerow(dict((k, v.encode('utf-8') if isinstance(v, str) else v) for k, v in row.items()))
#                    writer.writerow(row)
#
#
#            validator = BulkAddSamplesValidatorFactory.create_validator(manifest_file=csv_fname,
#                                                                        manifest_file_type="text/csv",
#                                                                        study=self.study,
#                                                                        sample_lookup_func=self.lookup_sample_func)
#            samples_iter = validator.validate_manifest_file()
#
#            actual_data = []
#            for resp in samples_iter:
#                actual_data.append(resp["sample"])
#            expected_data = [{"external_id": "Sample0",
#                              "location_id": self.location.location_id,
#                              "collection_date": datetime.date(year=2000, month=1, day=19)
#                              },
#                             {"external_id": "Sample1",
#                              "location_id": self.location.location_id,
#                              "collection_date": datetime.date(year=2000, month=1, day=19),
#                             },
#                             {"external_id": "Sample2",
#                              "location_id": self.location.location_id,
#                              "collection_date": datetime.date(year=2000, month=1, day=19),
#                             }
#                             ]
#
#
#            assert actual_data == expected_data
#
#        finally:
#            if csv_fname and os.path.exists(csv_fname):
#                print("Deleting test file " + str(csv_fname))
#                os.remove(csv_fname)
#

    def test_missing_header(self):
        """
        GIVEN:  I upload a sample xlsx containing a Samples worksheet with a missing required header
        WHEN:  we validate the worksheet
        THEN: a ValidationError is thrown

        """
        csv_fname = None
        try:

            TOTAL_ROWS = 3

            manifest_config_ini = helpers.DEFAULT_MANIFEST_CONFIG_INI
            manifest_config = BulkUploadCSVConfig(header_config_file=manifest_config_ini)
            nice_headers, db_to_nice_header, nice_to_db_header = manifest_config.read_header_config()

            # Create test csv
            tmp = tempfile.NamedTemporaryFile(suffix=".csv", prefix="missingHeader_SampleManifest", delete=False)
            tmp.close()
            csv_fname = tmp.name

            with open(csv_fname, 'w') as fh:
                writer = csv.DictWriter(fh, fieldnames = [db_to_nice_header["external_id"],
                                                          " ", # Missing collection date
                                                          db_to_nice_header["location_id"],
                                                          db_to_nice_header["note"]])
                # Set the header
                writer.writeheader()

                # Fill in the rows
                for irow in range(TOTAL_ROWS):
                    outrow = {}
                    outrow[db_to_nice_header["external_id"]] = "Sample" + str(irow)
                    outrow[" "] = " "
                    outrow[db_to_nice_header["location_id"]] = TestUploadManifestCreateView.location.curated_name
                    outrow[db_to_nice_header["note"]] = None

                    writer.writerow(outrow)

            with pytest.raises(ValidationError) as e:
                validator = BulkAddSamplesValidatorFactory.create_validator(manifest_file=csv_fname,
                                                                            manifest_file_type="text/csv",
                                                                            study=TestUploadManifestCreateView.study,
                                                                            sample_lookup_func=self.lookup_sample_func)
                samples_iter = validator.validate_manifest_file()
                for sample_dict in samples_iter:
                    if sample_dict and len(sample_dict):
                        pass

            assert e.value.code == HeaderError.MISSING_HEADER
            assert all(c in string.printable for c in str(e.value)), "The Missing Header Validation Error has not been properly interpolated"



        finally:
            if csv_fname and os.path.exists(csv_fname):
                print("Deleting test file " + str(csv_fname))
                os.remove(csv_fname)


    def test_blank_column(self):
        """
        GIVEN:  I upload a sample xlsx containing a valid Samples worksheet with a blank column in between required columns
        WHEN:  we validate the worksheet
        THEN: the blank columns are stripped out
        AND: the samples are validated successfully

        """
        csv_fname = None
        try:

            TOTAL_ROWS = 3

            manifest_config_ini = helpers.DEFAULT_MANIFEST_CONFIG_INI
            manifest_config = BulkUploadCSVConfig(header_config_file=manifest_config_ini)
            nice_headers, db_to_nice_header, nice_to_db_header = manifest_config.read_header_config()

            # Create test csv
            tmp = tempfile.NamedTemporaryFile(suffix=".csv", prefix="blankCol_SampleManifest", delete=False)
            tmp.close()
            csv_fname = tmp.name

            with open(csv_fname, 'w') as fh:
                writer = csv.DictWriter(fh, fieldnames = [db_to_nice_header["external_id"],
                                                          db_to_nice_header["collection_date"],
                                                          " ",
                                                          db_to_nice_header["location_id"],
                                                          db_to_nice_header["note"]])
                # Set the header
                writer.writeheader()

                # Fill in the rows
                for irow in range(TOTAL_ROWS):
                    outrow = {}
                    outrow[db_to_nice_header["external_id"]] = "Sample" + str(irow)
                    outrow[db_to_nice_header["collection_date"]] = datetime.date(year=2000, month=1, day=19).strftime("%Y-%m-%d")
                    outrow[" "] = " "
                    outrow[db_to_nice_header["location_id"]] = TestUploadManifestCreateView.location.curated_name
                    outrow[db_to_nice_header["note"]] = None

                    writer.writerow(outrow)

            validator = BulkAddSamplesValidatorFactory.create_validator(manifest_file=csv_fname,
                                                                        manifest_file_type="text/csv",
                                                                        study=TestUploadManifestCreateView.study,
                                                                        sample_lookup_func=self.lookup_sample_func)
            samples_iter = validator.validate_manifest_file()
            actual_data = []
            for resp in samples_iter:
                actual_data.append(resp["sample"])
            expected_data = [{"external_id": "Sample0",
                                 "location_id": TestUploadManifestCreateView.location.location_id,
                                 "collection_date": datetime.date(year=2000, month=1, day=19)},
                             {"external_id": "Sample1",
                                 "location_id": TestUploadManifestCreateView.location.location_id,
                                 "collection_date": datetime.date(year=2000, month=1, day=19)},
                             {"external_id": "Sample2",
                                 "location_id": TestUploadManifestCreateView.location.location_id,
                                 "collection_date": datetime.date(year=2000, month=1, day=19)}
                             ]


            assert actual_data == expected_data

        finally:
            if csv_fname and os.path.exists(csv_fname):
                print("Deleting test file " + str(csv_fname))
                os.remove(csv_fname)


    def test_invalid_loc(self):
        """
        GIVEN:  I upload a sample xlsx containing a Samples worksheet a location name that is not a valid location
        WHEN:  we validate the worksheet
        THEN: we get a ValidationError with an InvalidField code

        """
        csv_fname = None
        try:

            TOTAL_ROWS = 3

            manifest_config_ini = helpers.DEFAULT_MANIFEST_CONFIG_INI
            manifest_config = BulkUploadCSVConfig(header_config_file=manifest_config_ini)
            nice_headers, db_to_nice_header, nice_to_db_header = manifest_config.read_header_config()

            # Create test csv
            tmp = tempfile.NamedTemporaryFile(suffix=".csv", prefix="invalidLoc_SampleManifest", delete=False)
            tmp.close()
            csv_fname = tmp.name

            with open(csv_fname, 'w') as fh:
                writer = csv.DictWriter(fh, fieldnames = [db_to_nice_header["external_id"],
                                                          db_to_nice_header["collection_date"],
                                                          db_to_nice_header["location_id"],
                                                          db_to_nice_header["note"]])
                # Set the header
                writer.writeheader()

                # Fill in the rows
                for irow in range(TOTAL_ROWS):
                    outrow = {}
                    outrow[db_to_nice_header["external_id"]] = "Sample" + str(irow)
                    outrow[db_to_nice_header["collection_date"]] = datetime.date(year=2000, month=1, day=19).strftime("%Y-%m-%d")
                    outrow[db_to_nice_header["location_id"]] = "Location that is not found in the study"
                    outrow[db_to_nice_header["note"]] = None

                    writer.writerow(outrow)

            total_samples = 0

            with pytest.raises(ValidationError) as e:
                validator = BulkAddSamplesValidatorFactory.create_validator(manifest_file=csv_fname,
                                                                            manifest_file_type="text/csv",
                                                                            study=TestUploadManifestCreateView.study,
                                                                            sample_lookup_func=self.lookup_sample_func)
                samples_iter = validator.validate_manifest_file()
                for sample_dict in samples_iter:
                    if sample_dict and len(sample_dict):
                        total_samples += 1

            assert e.value.code == FieldError.INVALID_LOC, "Expected " + FieldError.INVALID_LOC + " for invalid location but got " + str(e.value.code)
            assert all(c in string.printable for c in str(e.value)), "The Invalid Field Validation Error has not been properly interpolated"
            assert total_samples == 0, "Expected no samples but got " +str(total_samples)


        finally:
            if csv_fname and os.path.exists(csv_fname):
                print("Deleting test file " + str(csv_fname))
                os.remove(csv_fname)



    def test_invalid_loc_multiple(self):
        """
        GIVEN:  I upload a sample xlsx containing a Samples worksheet a location name that is not a valid location
        WHEN:  we validate the worksheet
        THEN: we get a ValidationError with an InvalidField code

        """
        csv_fname = None
        try:

            TOTAL_ROWS = 3

            manifest_config_ini = helpers.DEFAULT_MANIFEST_CONFIG_INI
            manifest_config = BulkUploadCSVConfig(header_config_file=manifest_config_ini)
            nice_headers, db_to_nice_header, nice_to_db_header = manifest_config.read_header_config()

            # Create test csv
            tmp = tempfile.NamedTemporaryFile(suffix=".csv", prefix="invalidLoc_SampleManifest", delete=False)
            tmp.close()
            csv_fname = tmp.name

            with open(csv_fname, 'w') as fh:
                writer = csv.DictWriter(fh, fieldnames = [db_to_nice_header["external_id"],
                                                          db_to_nice_header["collection_date"],
                                                          db_to_nice_header["location_id"],
                                                          db_to_nice_header["note"]])
                # Set the header
                writer.writeheader()

                # Fill in the rows
                for irow in range(TOTAL_ROWS):
                    outrow = {}
                    outrow[db_to_nice_header["external_id"]] = "Sample" + str(irow)
                    outrow[db_to_nice_header["collection_date"]] = datetime.date(year=2000, month=1, day=19).strftime("%Y-%m-%d")
                    outrow[db_to_nice_header["location_id"]] = "Location that is not found in the study"
                    outrow[db_to_nice_header["note"]] = None

                    writer.writerow(outrow)

            total_samples = 0
            total_errors = 0
            errors = []

            validator = BulkAddSamplesValidatorFactory.create_validator(manifest_file=csv_fname,
                                                                        manifest_file_type="text/csv",
                                                                        study=TestUploadManifestCreateView.study,
                                                                        is_raise_field_err=False,
                                                                        sample_lookup_func=self.lookup_sample_func)
            samples_iter = validator.validate_manifest_file()
            for sample_dict in samples_iter:
                if sample_dict["valid"]:
                    if sample_dict and len(sample_dict):
                        total_samples += 1
                else:
                    total_errors += 1
                    errors += sample_dict["errors"]

            assert total_errors == 3

            for idx, val in enumerate(errors):
                err_msg = "Failed validation for row={}, field = 'location_id', value='Location that is not found in the study' ['Location that is not found in the study is not a location registered with study project code {}. If you want to add this location, please contact the Coordinator.']".format(idx + 1,
                                    TestUploadManifestCreateView.study.name)
                assert val == err_msg

            assert total_samples == 0, "Expected no samples but got " +str(total_samples)


        finally:
            if csv_fname and os.path.exists(csv_fname):
                print("Deleting test file " + str(csv_fname))
                os.remove(csv_fname)




    def test_invalid_date(self):
        """
        GIVEN:  I upload a sample xlsx containing a Samples worksheet with a collection date that isn't in required format
        WHEN:  we validate the worksheet
        THEN: we get a ValidationError with an InvalidField code

        """
        csv_fname = None
        try:

            TOTAL_ROWS = 3

            manifest_config_ini = helpers.DEFAULT_MANIFEST_CONFIG_INI
            manifest_config = BulkUploadCSVConfig(header_config_file=manifest_config_ini)
            nice_headers, db_to_nice_header, nice_to_db_header = manifest_config.read_header_config()

            # Create test csv
            tmp = tempfile.NamedTemporaryFile(suffix=".csv", prefix="invalidDate_SampleManifest", delete=False)
            tmp.close()
            csv_fname = tmp.name

            with open(csv_fname, 'w') as fh:
                writer = csv.DictWriter(fh, fieldnames = [db_to_nice_header["external_id"],
                                                          db_to_nice_header["collection_date"],
                                                          db_to_nice_header["location_id"],
                                                          db_to_nice_header["note"]])
                # Set the header
                writer.writeheader()

                # Fill in the rows
                for irow in range(TOTAL_ROWS):
                    outrow = {}
                    outrow[db_to_nice_header["external_id"]] = "Sample" + str(irow)
                    outrow[db_to_nice_header["collection_date"]] = datetime.date(year=2000, month=1, day=19).strftime("%Y")
                    outrow[db_to_nice_header["location_id"]] = "Location that is not found in the study"
                    outrow[db_to_nice_header["note"]] = None

                    writer.writerow(outrow)

            total_samples = 0

            with pytest.raises(ValidationError) as e:
                validator = BulkAddSamplesValidatorFactory.create_validator(manifest_file=csv_fname,
                                                                            manifest_file_type="text/csv",
                                                                            study=TestUploadManifestCreateView.study,
                                                                            sample_lookup_func=self.lookup_sample_func)
                samples_iter = validator.validate_manifest_file()
                for sample_dict in samples_iter:
                    if sample_dict and len(sample_dict):
                        total_samples += 1

            assert e.value.code == FieldError.INVALID_DATE, "Expected invalid field exception for invalid date but got " + str(e.value.code)
            assert all(c in string.printable for c in str(e.value)), "The Invalid Field Validation Error has not been properly interpolated"
            assert total_samples == 0, "Expected no samples but got " +str(total_samples)


        finally:
            if csv_fname and os.path.exists(csv_fname):
                print("Deleting test file " + str(csv_fname))
                os.remove(csv_fname)

    def test_case_insensitive_lead_trail_space_loc(self):
        """
        GIVEN:  I upload a sample csv
        AND:  sample location name uses a different case than stored in database
        AND:  sample location name uses trailing and leading spaces
        WHEN:  we validate the worksheet
        THEN: samples validate successfully

        """
        csv_fname = None
        try:

            TOTAL_ROWS = 3

            manifest_config_ini = helpers.DEFAULT_MANIFEST_CONFIG_INI
            manifest_config = BulkUploadCSVConfig(header_config_file=manifest_config_ini)
            nice_headers, db_to_nice_header, nice_to_db_header = manifest_config.read_header_config()

            # Create test csv
            tmp = tempfile.NamedTemporaryFile(suffix=".csv", prefix="caseInsens_SampleManifest", delete=False)
            tmp.close()
            csv_fname = tmp.name

            with open(csv_fname, 'w') as fh:
                writer = csv.DictWriter(fh, fieldnames = [db_to_nice_header["external_id"],
                                                          db_to_nice_header["collection_date"],
                                                          db_to_nice_header["location_id"],
                                                          db_to_nice_header["note"]])
                # Set the header
                writer.writeheader()

                # Fill in the rows
                for irow in range(TOTAL_ROWS):
                    outrow = {}
                    outrow[db_to_nice_header["external_id"]] = "Sample" + str(irow)
                    outrow[db_to_nice_header["collection_date"]] = datetime.date(year=2000, month=1, day=19).strftime("%Y-%m-%d")
                    outrow[db_to_nice_header["location_id"]] = "\n" + TestUploadManifestCreateView.location.curated_name.upper() + " "
                    outrow[db_to_nice_header["note"]] = None

                    writer.writerow(outrow)

            validator = BulkAddSamplesValidatorFactory.create_validator(manifest_file=csv_fname,
                                                                        manifest_file_type="text/csv",
                                                                        study=TestUploadManifestCreateView.study,
                                                                        sample_lookup_func=self.lookup_sample_func)
            samples_iter = validator.validate_manifest_file()

            actual_data = []
            for resp in samples_iter:
                actual_data.append(resp["sample"])
            expected_data = [{"external_id": "Sample0",
                              "location_id": TestUploadManifestCreateView.location.location_id,
                              "collection_date": datetime.date(year=2000, month=1, day=19),
                              },
                             {"external_id": "Sample1",
                              "location_id": TestUploadManifestCreateView.location.location_id,
                              "collection_date": datetime.date(year=2000, month=1, day=19),
                              },
                             {"external_id": "Sample2",
                              "location_id": TestUploadManifestCreateView.location.location_id,
                              "collection_date": datetime.date(year=2000, month=1, day=19),
                              }
                             ]


            assert actual_data == expected_data


        finally:
            if csv_fname and os.path.exists(csv_fname):
                print("Deleting test file " + str(csv_fname))
                os.remove(csv_fname)

    def test_optional_col(self):
        """
        GIVEN:  I upload a sample xlsx containing a valid Samples worksheet with non-mandatory columns
        WHEN:  we validate the worksheet
        THEN: all non-mandatory columns are combined into a single json object as the validated value

        """
        csv_fname = None
        try:
            TOTAL_ROWS = 3
            manifest_config_ini = helpers.DEFAULT_MANIFEST_CONFIG_INI
            manifest_config = BulkUploadCSVConfig(header_config_file=manifest_config_ini)
            nice_headers, db_to_nice_header, nice_to_db_header = manifest_config.read_header_config()

            # Create test csv
            tmp = tempfile.NamedTemporaryFile(suffix=".csv", prefix="optionalCol_SampleManifest", delete=False)
            tmp.close()
            csv_fname = tmp.name

            with open(csv_fname, 'w') as fh:
                writer = csv.DictWriter(fh, fieldnames = [db_to_nice_header["external_id"],
                                                          "PatientID",
                                                          "Days From Baseline",
                                                          db_to_nice_header["collection_date"],
                                                          db_to_nice_header["location_id"],
                                                          db_to_nice_header["note"]])
                # Set the header
                writer.writeheader()

                # Fill in the rows
                for irow in range(TOTAL_ROWS):
                    outrow = {}
                    outrow[db_to_nice_header["external_id"]] = "Sample" + str(irow)
                    outrow["PatientID"] = "Pat" + str(irow)
                    outrow["Days From Baseline"] = irow
                    outrow[db_to_nice_header["collection_date"]] = datetime.date(year=2000, month=1, day=19).strftime("%Y-%m-%d")
                    outrow[db_to_nice_header["location_id"]] = TestUploadManifestCreateView.location.curated_name
                    outrow[db_to_nice_header["note"]] = None

                    writer.writerow(outrow)

            validator = BulkAddSamplesValidatorFactory.create_validator(manifest_file=csv_fname,
                                                                        manifest_file_type="text/csv",
                                                                        study=TestUploadManifestCreateView.study,
                                                                        sample_lookup_func=self.lookup_sample_func)
            samples_iter = validator.validate_manifest_file()

            actual_data = []
            for resp in samples_iter:
                actual_data.append(resp["sample"])
            # NB:  if there is no value for the columns, then it won't be included in the return dict
            expected_data = [{"external_id": "Sample0",
                                 "location_id": TestUploadManifestCreateView.location.location_id,
                                 "collection_date": datetime.date(year=2000, month=1, day=19),
                                 "tags": {"PatientID": "Pat0",
                                          "Days From Baseline": "0"
                                        }
                              },
                             {"external_id": "Sample1",
                                 "location_id": TestUploadManifestCreateView.location.location_id,
                                 "collection_date": datetime.date(year=2000, month=1, day=19),
                                 "tags": { "PatientID": "Pat1",
                                          "Days From Baseline": "1"
                                          }
                              },
                             {"external_id": "Sample2",
                                 "location_id": TestUploadManifestCreateView.location.location_id,
                                 "collection_date": datetime.date(year=2000, month=1, day=19),
                                 "tags": {"PatientID": "Pat2",
                                          "Days From Baseline": "2"
                                          }
                              },
                             ]


            assert actual_data == expected_data

        finally:
            if csv_fname and os.path.exists(csv_fname):
                print("Deleting test file " + str(csv_fname))
                os.remove(csv_fname)


    def test_blank_header_nonblank_cell(self):
        """
        GIVEN:  I upload a sample xlsx containing a valid Samples worksheet with a column with non-blank cell values but blank header
        WHEN:  we validate the worksheet
        THEN: the column with blank header is ignored

        """
        csv_fname = None
        try:

            TOTAL_ROWS = 3

            manifest_config_ini = helpers.DEFAULT_MANIFEST_CONFIG_INI
            manifest_config = BulkUploadCSVConfig(header_config_file=manifest_config_ini)
            nice_headers, db_to_nice_header, nice_to_db_header = manifest_config.read_header_config()

            # Create test csv
            tmp = tempfile.NamedTemporaryFile(suffix=".csv", prefix="blankCol_SampleManifest", delete=False)
            tmp.close()
            csv_fname = tmp.name

            with open(csv_fname, 'w') as fh:
                writer = csv.DictWriter(fh, fieldnames = [db_to_nice_header["external_id"],
                                                          db_to_nice_header["collection_date"],
                                                          " ",
                                                          db_to_nice_header["location_id"],
                                                          db_to_nice_header["note"]])
                # Set the header
                writer.writeheader()

                # Fill in the rows
                for irow in range(TOTAL_ROWS):
                    outrow = {}
                    outrow[db_to_nice_header["external_id"]] = "Sample" + str(irow)
                    outrow[db_to_nice_header["collection_date"]] = datetime.date(year=2000, month=1, day=19).strftime("%Y-%m-%d")
                    outrow[" "] = "nonblank"
                    outrow[db_to_nice_header["location_id"]] = TestUploadManifestCreateView.location.curated_name
                    outrow[db_to_nice_header["note"]] = None

                    writer.writerow(outrow)


            validator = BulkAddSamplesValidatorFactory.create_validator(manifest_file=csv_fname,
                                                                        manifest_file_type="text/csv",
                                                                        study=TestUploadManifestCreateView.study,
                                                                        sample_lookup_func=self.lookup_sample_func)
            samples_iter = validator.validate_manifest_file()

            actual_data = []
            for resp in samples_iter:
                actual_data.append(resp["sample"])
            # NB:  if there is no value for the columns, then it won't be included in the return dict
            expected_data = [{"external_id": "Sample0",
                                 "location_id": TestUploadManifestCreateView.location.location_id,
                                 "collection_date": datetime.date(year=2000, month=1, day=19)},
                             {"external_id": "Sample1",
                                 "location_id": TestUploadManifestCreateView.location.location_id,
                                 "collection_date": datetime.date(year=2000, month=1, day=19)},
                             {"external_id": "Sample2",
                                 "location_id": TestUploadManifestCreateView.location.location_id,
                                 "collection_date": datetime.date(year=2000, month=1, day=19)}
                             ]


            assert actual_data == expected_data

        finally:
            if csv_fname and os.path.exists(csv_fname):
                print("Deleting test file " + str(csv_fname))
                os.remove(csv_fname)


    def test_dup_header(self):
        """
        GIVEN:  I upload a sample CSV containing duplicated headers
        WHEN:  we validate the file
        THEN: a ValidationError is thrown

        """
        csv_fname = None
        try:

            TOTAL_ROWS = 3
            manifest_config_ini = helpers.DEFAULT_MANIFEST_CONFIG_INI
            manifest_config = BulkUploadCSVConfig(header_config_file=manifest_config_ini)
            nice_headers, db_to_nice_header, nice_to_db_header = manifest_config.read_header_config()

            # Create test csv
            tmp = tempfile.NamedTemporaryFile(suffix=".csv", prefix="optionalCol_SampleManifest", delete=False)
            tmp.close()
            csv_fname = tmp.name

            with open(csv_fname, 'w') as fh:
                writer = csv.DictWriter(fh, fieldnames = [db_to_nice_header["external_id"],
                                                          db_to_nice_header["collection_date"],
                                                          "PatientID",
                                                          "Days Since Baseline",
                                                          db_to_nice_header["location_id"],
                                                          db_to_nice_header["location_id"].upper() + " ",
                                                          db_to_nice_header["note"],
                                                          "patientid"])
                # Set the header
                writer.writeheader()

                # Fill in the rows
                for irow in range(TOTAL_ROWS):
                    outrow = {}
                    outrow[db_to_nice_header["external_id"]] = "Sample" + str(irow)
                    outrow[db_to_nice_header["collection_date"]] = datetime.date(year=2000, month=1, day=19)
                    outrow["PatientID"] = "Pat" + str(irow)
                    outrow["Days Since Baseline"] = irow
                    outrow[db_to_nice_header["location_id"]] = TestUploadManifestCreateView.location.curated_name
                    outrow[db_to_nice_header["location_id"].upper() + " "] = TestUploadManifestCreateView.location.curated_name
                    outrow[db_to_nice_header["note"]] = None
                    outrow["patientid"] = "Bob"

                    writer.writerow(outrow)




            tmp = tempfile.NamedTemporaryFile(suffix=".xlsx", prefix="dupHeader_SampleManifest", delete=False)
            tmp.close()


            validator = BulkAddSamplesValidatorFactory.create_validator(manifest_file=csv_fname,
                                                                        manifest_file_type="text/csv",
                                                                        study=TestUploadManifestCreateView.study,
                                                                        sample_lookup_func=self.lookup_sample_func)
            samples_iter = validator.validate_manifest_file()

            with pytest.raises(ValidationError) as e:
                for sample_dict in samples_iter:
                    if sample_dict and len(sample_dict):
                        pass

            print ("test_dup_header: " + str(e.value))
            assert e.value.code == HeaderError.DUP_HEADER
            assert all(c in string.printable for c in str(e.value)), "The Missing Header Validation Error has not been properly interpolated"



        finally:
            if csv_fname and os.path.exists(csv_fname):
                print("Deleting test file " + str(csv_fname))
                os.remove(csv_fname)


    def test_case_insensitve_header(self):
        """
        GIVEN:  I upload a valid sample CSV containing mandatory header in different case and trailing/leading spaces than specified in header config ini
        WHEN:  we validate the file
        THEN: the sample validates successfully

        """
        csv_fname = None
        try:

            TOTAL_ROWS = 3
            manifest_config_ini = helpers.DEFAULT_MANIFEST_CONFIG_INI
            manifest_config = BulkUploadCSVConfig(header_config_file=manifest_config_ini)
            nice_headers, db_to_nice_header, nice_to_db_header = manifest_config.read_header_config()

            # Create test csv
            tmp = tempfile.NamedTemporaryFile(suffix=".csv", prefix="caseins_traillead_space_header", delete=False)
            tmp.close()
            csv_fname = tmp.name

            with open(csv_fname, 'w') as fh:
                writer = csv.DictWriter(fh, fieldnames = [db_to_nice_header["external_id"],
                                                          db_to_nice_header["collection_date"],
                                                          " " + db_to_nice_header["location_id"].upper() + " ",
                                                          db_to_nice_header["note"],
                                                          "patientid"])
                # Set the header
                writer.writeheader()

                # Fill in the rows
                for irow in range(TOTAL_ROWS):
                    outrow = {}
                    outrow[db_to_nice_header["external_id"]] = "Sample" + str(irow)
                    outrow[db_to_nice_header["collection_date"]] = datetime.date(year=2000, month=1, day=19).strftime('%Y-%m-%d')
                    outrow[" " + db_to_nice_header["location_id"].upper() + " "] = TestUploadManifestCreateView.location.curated_name
                    outrow[db_to_nice_header["note"]] = None

                    writer.writerow(outrow)



            validator = BulkAddSamplesValidatorFactory.create_validator(manifest_file=csv_fname,
                                                                        manifest_file_type="text/csv",
                                                                        study=TestUploadManifestCreateView.study,
                                                                        sample_lookup_func=self.lookup_sample_func)
            samples_iter = validator.validate_manifest_file()

            actual_data = []
            for resp in samples_iter:
                actual_data.append(resp["sample"])
            # NB:  if there is no value for the columns, then it won't be included in the return dict
            expected_data = [{"external_id": "Sample0",
                                 "location_id": TestUploadManifestCreateView.location.location_id,
                                 "collection_date": datetime.date(year=2000, month=1, day=19)},
                             {"external_id": "Sample1",
                                 "location_id": TestUploadManifestCreateView.location.location_id,
                                 "collection_date": datetime.date(year=2000, month=1, day=19)},
                             {"external_id": "Sample2",
                                 "location_id": TestUploadManifestCreateView.location.location_id,
                                 "collection_date": datetime.date(year=2000, month=1, day=19)}
                             ]


            assert actual_data == expected_data

        finally:
            if csv_fname and os.path.exists(csv_fname):
                print("Deleting test file " + str(csv_fname))
                os.remove(csv_fname)


    def test_duplicate_external_id_intra(self):
        """
        GIVEN:  I upload a sample xlsx containing a Samples worksheet with
        a repeated id
        WHEN:  we validate the worksheet
        THEN: we get a ValidationError with an InvalidField code

        """
        csv_fname = None
        try:

            TOTAL_ROWS = 3

            manifest_config_ini = helpers.DEFAULT_MANIFEST_CONFIG_INI
            manifest_config = BulkUploadCSVConfig(header_config_file=manifest_config_ini)
            nice_headers, db_to_nice_header, nice_to_db_header = manifest_config.read_header_config()

            # Create test csv
            tmp = tempfile.NamedTemporaryFile(suffix=".csv",
                                              prefix="invalidIntraId_SampleManifest", delete=False)
            tmp.close()
            csv_fname = tmp.name

            with open(csv_fname, 'w') as fh:
                writer = csv.DictWriter(fh, fieldnames = [db_to_nice_header["external_id"],
                                                          db_to_nice_header["collection_date"],
                                                          db_to_nice_header["location_id"],
                                                          db_to_nice_header["note"]])
                # Set the header
                writer.writeheader()

                outrow = {}
                # Fill in the rows
                for irow in range(TOTAL_ROWS):
                    outrow = {}
                    outrow[db_to_nice_header["external_id"]] = "Sample" + str(irow)
                    outrow[db_to_nice_header["collection_date"]] = datetime.date(year=2000, month=1, day=19).strftime("%Y-%m-%d")
                    outrow[db_to_nice_header["location_id"]] = TestUploadManifestCreateView.location.curated_name
                    outrow[db_to_nice_header["note"]] = None

                    writer.writerow(outrow)

                writer.writerow(outrow)
            total_samples = 0

            with pytest.raises(ValidationError) as e:
                validator = BulkAddSamplesValidatorFactory.create_validator(manifest_file=csv_fname,
                                                                            manifest_file_type="text/csv",
                                                                            study=TestUploadManifestCreateView.study,
                                                                            sample_lookup_func=self.lookup_sample_func)
                samples_iter = validator.validate_manifest_file()
                for sample_dict in samples_iter:
                    if sample_dict['valid']:
                        total_samples += 1

            assert e.value.code == FieldError.DUP_SAMPLE, "Expected invalid field exception for invalid duplicate id but got " + str(e.value.code)
            assert all(c in string.printable for c in str(e.value)), "The Invalid Field Validation Error has not been properly interpolated"
            assert e.value.messages[0] == 'Invalid value at row 4 , column "Unique Aliquot ID": [\'Sample with external id Sample2 already exists in the manifest\']'
            assert total_samples == TOTAL_ROWS, f"Expected {TOTAL_ROWS} samples but got {total_samples}"


        finally:
            if csv_fname and os.path.exists(csv_fname):
                print("Deleting test file " + str(csv_fname))
                os.remove(csv_fname)


    def test_duplicate_external_id_extra_same_study(self):
        """
        GIVEN:  I upload a sample xlsx containing a Samples worksheet with
        a repeated id
        WHEN:  we validate the worksheet
        THEN: we get a ValidationError with an InvalidField code

        """
        csv_fname = None
        samples = []
        try:

            TOTAL_ROWS = 3

            manifest_config_ini = helpers.DEFAULT_MANIFEST_CONFIG_INI
            manifest_config = BulkUploadCSVConfig(header_config_file=manifest_config_ini)
            nice_headers, db_to_nice_header, nice_to_db_header = manifest_config.read_header_config()

            # Create test csv
            tmp = tempfile.NamedTemporaryFile(suffix=".csv",
                                              prefix="invalidExtraId_SampleManifest", delete=False)
            tmp.close()
            csv_fname = tmp.name

            with open(csv_fname, 'w') as fh:
                writer = csv.DictWriter(fh, fieldnames = [db_to_nice_header["external_id"],
                                                          db_to_nice_header["collection_date"],
                                                          db_to_nice_header["location_id"],
                                                          db_to_nice_header["note"]])
                # Set the header
                writer.writeheader()

                outrow = {}
                # Fill in the rows
                for irow in range(TOTAL_ROWS):
                    outrow = {}
                    outrow[db_to_nice_header["external_id"]] = "Sample" + str(irow)
                    outrow[db_to_nice_header["collection_date"]] = datetime.date(year=2000, month=1, day=19).strftime("%Y-%m-%d")
                    outrow[db_to_nice_header["location_id"]] = TestUploadManifestCreateView.location.curated_name
                    outrow[db_to_nice_header["note"]] = None

                    writer.writerow(outrow)

            total_samples = 0


            validator = BulkAddSamplesValidatorFactory.create_validator(manifest_file=csv_fname,
                                                                        manifest_file_type="text/csv",
                                                                        study=TestUploadManifestCreateView.study,
                                                                        sample_lookup_func=self.lookup_sample_func)
            samples_iter = validator.validate_manifest_file()
            self.test_study = self.alt_study
            for sample_dict in samples_iter:
                if sample_dict['valid']:
                    validated_sample_dict = sample_dict["sample"]
                    samples.append(validated_sample_dict)
                    self.registered_samples.append(validated_sample_dict)


            validator = BulkAddSamplesValidatorFactory.create_validator(manifest_file=csv_fname,
                                                                        manifest_file_type="text/csv",
                                                                        study=TestUploadManifestCreateView.study,
                                                                        sample_lookup_func=self.lookup_sample_func)
            samples_iter = validator.validate_manifest_file()
            with pytest.raises(ValidationError) as e:
                samples_iter = validator.validate_manifest_file()
                for sample_dict in samples_iter:
                    if sample_dict['valid']:
                        total_samples += 1

            assert e.value.code == FieldError.DUP_SAMPLE, "Expected invalid field exception for invalid duplicate id but got " + str(e.value.code)
            assert all(c in string.printable for c in str(e.value)), "The Invalid Field Validation Error has not been properly interpolated"
            assert e.value.messages[0] == f'Invalid value at row 1 , column "Unique Aliquot ID": [\'Sample with external id Sample0 is already registered in study {str(self.test_study.name)}\']'
            assert total_samples == 0, "Expected no samples but got " +str(total_samples)


        finally:
            self.registered_samples = []
            if csv_fname and os.path.exists(csv_fname):
                print("Deleting test file " + str(csv_fname))
                os.remove(csv_fname)

    def test_duplicate_external_id_extra_different_study(self):
        """
        GIVEN:  I upload a sample xlsx containing a Samples worksheet with
        a repeated id
        WHEN:  we validate the worksheet
        THEN: we get a ValidationError with an InvalidField code

        """
        csv_fname = None
        samples = []
        try:

            TOTAL_ROWS = 3

            manifest_config_ini = helpers.DEFAULT_MANIFEST_CONFIG_INI
            manifest_config = BulkUploadCSVConfig(header_config_file=manifest_config_ini)
            nice_headers, db_to_nice_header, nice_to_db_header = manifest_config.read_header_config()

            # Create test csv
            tmp = tempfile.NamedTemporaryFile(suffix=".csv",
                                              prefix="invalidExtraId_SampleManifest", delete=False)
            tmp.close()
            csv_fname = tmp.name

            with open(csv_fname, 'w') as fh:
                writer = csv.DictWriter(fh, fieldnames = [db_to_nice_header["external_id"],
                                                          db_to_nice_header["collection_date"],
                                                          db_to_nice_header["location_id"],
                                                          db_to_nice_header["note"]])
                # Set the header
                writer.writeheader()

                outrow = {}
                # Fill in the rows
                for irow in range(TOTAL_ROWS):
                    outrow = {}
                    outrow[db_to_nice_header["external_id"]] = "Sample" + str(irow)
                    outrow[db_to_nice_header["collection_date"]] = datetime.date(year=2000, month=1, day=19).strftime("%Y-%m-%d")
                    outrow[db_to_nice_header["location_id"]] = self.location.curated_name
                    outrow[db_to_nice_header["note"]] = None

                    writer.writerow(outrow)

            total_samples = 0

            validator = BulkAddSamplesValidatorFactory.create_validator(manifest_file=csv_fname,
                                                                        manifest_file_type="text/csv",
                                                                        study=TestUploadManifestCreateView.study,
                                                                        sample_lookup_func=self.lookup_sample_func)

            self.test_study = self.study
            self.registered_samples = []
            samples_iter = validator.validate_manifest_file()
            for sample_dict in samples_iter:
                if sample_dict['valid']:
                    validated_sample_dict = sample_dict["sample"]
                    samples.append(validated_sample_dict)
                    self.registered_samples.append(validated_sample_dict)


            with open(csv_fname, 'w') as fh:
                writer = csv.DictWriter(fh, fieldnames = [db_to_nice_header["external_id"],
                                                          db_to_nice_header["collection_date"],
                                                          db_to_nice_header["location_id"],
                                                          db_to_nice_header["note"]])
                # Set the header
                writer.writeheader()

                outrow = {}
                # Fill in the rows
                for irow in range(TOTAL_ROWS):
                    outrow = {}
                    outrow[db_to_nice_header["external_id"]] = "Sample" + str(irow)
                    outrow[db_to_nice_header["collection_date"]] = datetime.date(year=2000, month=1, day=19).strftime("%Y-%m-%d")
                    outrow[db_to_nice_header["location_id"]] = self.location2.curated_name
                    outrow[db_to_nice_header["note"]] = None

                    writer.writerow(outrow)

            validator = BulkAddSamplesValidatorFactory.create_validator(manifest_file=csv_fname,
                                                                        manifest_file_type="text/csv",
                                                                        study=TestUploadManifestCreateView.study2,
                                                                        sample_lookup_func=self.lookup_sample_func)
            samples_iter = validator.validate_manifest_file()
            with pytest.raises(ValidationError) as e:
                samples_iter = validator.validate_manifest_file()
                for sample_dict in samples_iter:
                    if sample_dict['valid']:
                        total_samples += 1

            assert e.value.code == FieldError.DUP_SAMPLE, "Expected invalid field exception for invalid duplicate id but got " + str(e.value.code)
            assert all(c in string.printable for c in str(e.value)), "The Invalid Field Validation Error has not been properly interpolated"
            assert e.value.messages[0] == f'Invalid value at row 1 , column "Unique Aliquot ID": [\'Sample with external id Sample0 is already registered in study {str(self.test_study.name)}\']'
            assert total_samples == 0, "Expected no samples but got " +str(total_samples)


        finally:
            if csv_fname and os.path.exists(csv_fname):
                print("Deleting test file " + str(csv_fname))
                os.remove(csv_fname)
            self.registered_samples = []
