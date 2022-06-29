import enum


class TransferTypes(str, enum.Enum):
    BEFORE = "before"
    AFTER = "after"


class FileSchemes(str, enum.Enum):
    File = "file"
    S3 = "s3"
    Globus = "globus"
    HTTP = ("http",)
    HTTPS = "https"


class FileTransferStrategyTypes(str, enum.Enum):
    Rsync = "rsync"
    HTTP = "http"
    S3 = "s3"
    FTP = "ftp"
    GLOBUS = "globus"


SchemeToStrategyMap = {
    "file": FileTransferStrategyTypes.Rsync,
    "http": FileTransferStrategyTypes.HTTP,
    "https": FileTransferStrategyTypes.HTTP,
    "s3": FileTransferStrategyTypes.S3,
    "ftp": FileTransferStrategyTypes.FTP,
    "globus": FileTransferStrategyTypes.GLOBUS,
}
