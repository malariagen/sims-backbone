import csv
from io import TextIOWrapper, StringIO, FileIO
from APPS.bulk_upload.parser import BulkUploadFileParser, BulkUploadConfig
from codecs import EncodedFile
SECTION_CSV = "csv"

class BulkUploadCSVConfig(BulkUploadConfig):
    """
    Reads csv header config .ini
    """



    def __init__(self, header_config_file, header_section=SECTION_CSV):
        """
        @param str header_config_file:  filepath to .ini file that specifies human readable headers and their corresponding db columns
        @param str header_section:   header config ini section that maps the db field name to the user friendly name displayed in the file
        """
        super().__init__(header_config_file=header_config_file, header_section=header_section)


class TextIOWrapperNoclose(TextIOWrapper):
    """
    TextIOWrapper will close the file handle once its out of scope during garbage collection.
    Override the TextIOWrapper so that the underlying file handle from this TextIOWrapper is always open.
    If you want to close the underlying file handle, you must use the reference to the underlying file handle.

    See http://stackoverflow.com/questions/30993816/prevent-textiowrapper-from-closing-on-gc-in-a-py2-py3-compatible-way
    http://stackoverflow.com/questions/2404430/does-filehandle-get-closed-automatically-in-python-after-it-goes-out-of-scope
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def close(self):
        self.closed = True


# Check if the csv file uploaded is correct.
class BulkUploadCSVParser(BulkUploadFileParser):
    """
    There is a 1:1 mapping from db table header to bulk upload file header for mandatory fields specified in the bulk upload config file.
    But all the optional fields in the bulk upload file are aggregated into a single json object within the db.
    """



    def __init__(self, header_config_file, upload_file):
        """
        @param str header_config_file:  filepath to .ini file that specifies human readable headers and their corresponding db columns
        @param str upload_file:  filepath to upload file. Or file handle to binary stream of file
        """
        super().__init__(header_config_file=header_config_file, upload_file=upload_file, header_section=SECTION_CSV)
        self.bulk_upload_config = BulkUploadCSVConfig(header_config_file=header_config_file, header_section=SECTION_CSV)
        self.__csv_dictreader = None



    def __make_csv_dict_reader(self):
        """
        Finds the csv/tsv dialect and sets the internal csv dictreader handle to the beginning of the file just past the header row.
        """

        fh = self.as_handle(fileish=self.upload_file, mode='rb')
        textio_fh = TextIOWrapperNoclose(fh, "ascii")


        # Only sniff the header line to determine the delimiter
        # http://stackoverflow.com/questions/35756682/getting-csv-sniffer-to-work-with-quoted-values
        textio_fh.seek(0)
        sniffstring = None
        try:
            sniffstring = textio_fh.readline()
        except UnicodeDecodeError as ude:
            fh = self.as_handle(fileish=self.upload_file, mode='r')
            textio_fh = TextIOWrapperNoclose(fh, "utf-8-sig")
            textio_fh.seek(0)
            sniffstring = textio_fh.readline()

        sniffdialect = csv.Sniffer().sniff(sniffstring, delimiters='\t,')  #we can manage TAB too.

        textio_fh.seek(0)
        self.__csv_dictreader = csv.DictReader(textio_fh, dialect=sniffdialect)

        # Rename the headers so that they are whitestripped
        self.__csv_dictreader.fieldnames = [nice_header.strip() for nice_header in self.__csv_dictreader.fieldnames]






    def get_data_row_iter(self):
        """
        Advance row iterator to data (ie just past the header row).
        Yields all cells, even for columns that weren't configured in the header .ini file.
        Skips any columns with blank headers after all trailing and leading white space is stripped.

        Checks if delimiter is tab or comma.  Allows both.

        @return iterator: data row iterator, where each row is represented by dict mapping {db field name => field value}
        """

        self.__make_csv_dict_reader()

        # Find the columns that are nonblank after stripping trailing and leading whitespace.
        nonblank_colnames = self.get_data_headers()
        for row in self.__csv_dictreader:
            yield dict((colname, row[colname]) for colname in nonblank_colnames)





    def get_data_headers(self):
        """
        Get the headers from the data upload file.
        Skips any columns with blank headers after all trailing and leading white space is stripped.


        NB:  This will reset the file iterator to just past the headers!
        @return [str] :  list of header names as displayed in the data upload file
        """
        self.__make_csv_dict_reader()
        nonblank_colnames = [nice_header.strip() for nice_header in self.__csv_dictreader.fieldnames if nice_header.strip() != ""]
        return nonblank_colnames





