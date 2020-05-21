from configparser import RawConfigParser
from APPS.bulk_upload.parser import BulkUploadFileParser, BulkUploadConfig
import openpyxl

SECTION_EXCEL = "excel"
PROP_EXCEL_SHEET = "SHEET"

SECTION_HEADER  = "header"

class BulkUploadExcelConfig(BulkUploadConfig):
    """
    Header and worksheet configuration for bulk uploads via excel
    """

    def __init__(self, header_config_file, header_section=SECTION_HEADER):
        """
        @param str header_config_file:  filepath to .ini file that specifies human readable headers and their corresponding db columns
        @param str header_section:   header config ini section that maps the db field name to the user friendly name displayed in the file
        """
        super().__init__(header_config_file=header_config_file, header_section=header_section)


    def get_config_sheet_name(self):
        """
        Reads in the required column headers from a .ini file
        Expects that the .ini file has a "excel" section for required sheets, and "headers" section from which required headers are specified.
        @return (sheet name, {db header: human readable header}, {human readable header: db header})
        """
        sheet_name = ""

        try:

            config = RawConfigParser()
            config.read(self.header_config_file)

            sheet_name = config.get(SECTION_EXCEL, PROP_EXCEL_SHEET)

        except:
            raise ValueError("Header config INI " + str(self.header_config_file) + " is not defined or is not correct. Please contact the coordinator.")

        return sheet_name



# Check if the csv file uploaded is correct.
class BulkUploadExcelParser(BulkUploadFileParser):
    """
    ASSUMES there is only one sheet with data.
    """

    def __init__(self, header_config_file, upload_file):
        """
        @param str header_config_file:  filepath to .ini file that specifies human readable headers and their corresponding db columns
        @param str upload_file:  filepath to xls from which to upload bulk data
        """
        super().__init__(header_config_file=header_config_file, upload_file=upload_file, header_section=SECTION_HEADER)
        self.bulk_upload_config = BulkUploadExcelConfig(header_config_file=header_config_file, header_section=SECTION_HEADER)


    def find_header_row_info(self):
        """
        Returns the first row containing any of required headers.  Does not check for missing headers.
        Skips any columns with empty headers.  Strips trailing and leading whitespace in header names.
        @returns dict, int:  (dict mapping header as displayed in sheet to 1-based column index {nice header : 1based col index},
                              1-based row index of the header row.  None if the header row has not found.)
        """
        # TODO:  it would look nicer if we had a separate class for reading the cells of each row
        header_row_1idx = None

        req_nice_headers, req_db_to_nice_header, req_nice_to_db_header = self.config.read_header_config()

        # Dict mapping the user-friendly header name formatted for searchability => expected user friendly header name
        # we want to search for the required headers using case insensitive and trailing/leading whitespace insensitive sesarch.
        nice_header_searchset = set([nice_header.strip().lower() for nice_header in req_nice_headers])

        nice_header_to_col_1idx = {}
        # Find the header row.  The header row is defined as the first row to contain a cell value that matches one of the mandatory headers.
        sheet = self.get_data_sheet()
        for row in sheet.rows:
            for cell in row:
                if cell.value is None or not isinstance(cell.value, str):
                    continue

                # We've found a cell containing a required header
                if cell.value.strip().lower() in nice_header_searchset:
                    header_row_1idx = cell.row
                    break


            if header_row_1idx:
                for cell in row:
                    if cell.value is not None and str(cell.value).strip() != "":
                        nice_header_to_col_1idx[str(cell.value).strip()] = cell.column
                break

        return nice_header_to_col_1idx, header_row_1idx



    def get_data_row_iter(self):
        """
        Advance iterator to data (ie just past the header row_tuple).
        Yields all cells, even for columns that weren't configured in the header .ini file.
        Skips any columns with blank headers after all trailing and leading white space is stripped.
        @return Iterator:  iterator of dict representing each row  {user friendly header in excel: cell}
        """
        rows_iter = None

        # Get the index of the pertinent columns, index of the header row_tuple
        sheet = self.get_data_sheet()
        nice_header_to_col_1idx, header_row_1idx  = self.find_header_row_info()

        if header_row_1idx:
            rows_iter = sheet.rows
            for row_0idx, row_tuple in enumerate(rows_iter):
                if (row_0idx <= header_row_1idx - 1) or not len(row_tuple):
                    continue

                # openpyxl is 1-based but python is 0based
                row_dict = {nice_header : row_tuple[col_1idx-1] for nice_header, col_1idx in nice_header_to_col_1idx.items() }
                yield row_dict



    def get_data_sheet(self):
        """
        Parses the excel workbook and returns the info required to iterate over the samples.
        @returns (Iterator, dict, dict):  (Iterator over openpyxl rows,
                                            dict mapping {db header name => 0-based index of column within row},
                                            dict mapping {db header name => user friendly header name in excel sheet} )
        @raises ValidationError if the Samples sheet doesn't exist or if the headers don't exist
        """
        wb = openpyxl.load_workbook(self.upload_file, read_only=True,
                                    data_only=True)

        # We want to be flexible in sheet names.  Allow trailing leading spaces, allow case insensitive.
        config_sheetname = self.config.get_config_sheet_name()
        searchable_config_sheetname = config_sheetname.strip().lower()

        data_sheet_names = wb.get_sheet_names()
        searchable_to_data_sheetname = {data_sheetname.strip().lower() : data_sheetname for data_sheetname in data_sheet_names}


        if searchable_config_sheetname in searchable_to_data_sheetname:
            data_sheetname = searchable_to_data_sheetname[searchable_config_sheetname]
            sheet = wb.get_sheet_by_name(data_sheetname)
        else:
            raise ValueError("Missing Worksheet " + str(config_sheetname))

        return sheet


    def get_data_headers(self):
        """
        Get the headers from the data upload file.  Does not do any validation on the headers.
        Does case insensitive search, ignoring leading and trailing blanks.
        Returns any nonempty headers, even those that are not required by the header config ini
        @return [str] :  list of header names as displayed in the data upload file, stripped for leading and trailing whitespace
        """

        # Find the header row and check that all the header columns exist
        # Remove the header from the lookup once we find it
        header_vals = []
        sheet = self.get_data_sheet()
        nice_header_to_col_1idx, header_row_1idx = self.find_header_row_info()
        for row_0idx, row in enumerate(sheet.rows):
            if row_0idx + 1 == header_row_1idx:
                for cell in row:
                    if cell.value:
                        header_vals.append(str(cell.value).strip())
                break


        return header_vals




