from APPS.bulk_upload.errors import UploadParseError

class FieldError(UploadParseError):
    INVALID_FIELD = "InvalidField"
    MISSING_SAMPLES_TAB = "MissingSamplesTab"
    BAD_HEADER = "BadHeader"  # Generic catch all
    MISSING_FIELD = "MissingField"
    DUP_SAMPLE = "DuplicateSample"
    INVALID_DATE = "InvalidDate"
    INVALID_LOC = "InvalidLocation"
    INVALID_STUDY = "InvalidStudy"
    INVALID_MF = "InvalidMf"
    FORMULA = "InvalidDataFormula"
