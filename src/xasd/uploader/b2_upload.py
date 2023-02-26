import logging

from b2sdk.v2 import B2Api, InMemoryAccountInfo, TqdmProgressListener


logger = logging.getLogger(__name__)


class B2Bucket:
    """
    A class representing a B2 bucket, providing methods for interacting with the bucket.

    Attributes:
        bucket (b2sdk.v2.Bucket): The B2 bucket associated with this B2Bucket object.

    Methods:
        __init__(self, bucket_name: str, key: str, secret: str) -> None:
            Initializes a new B2Bucket object.

        upload_file(self, local_file: str, b2_file_name: str, **file_info: dict) -> None:
            Uploads a file to the B2 bucket associated with this B2Bucket object.

        list_files(self) -> None:
            Lists the files in the B2 bucket associated with this B2Bucket object.
    """

    def __init__(self, bucket_name: str, key: str, secret: str) -> None:
        """
        Initializes a new B2Bucket object.

        Args:
            bucket_name (str): The name of the B2 bucket to interact with.
            key (str): The B2 application key to use for authentication.
            secret (str): The B2 application secret to use for authentication.
        """
        info = InMemoryAccountInfo()
        b2_api = B2Api(info)
        b2_api.authorize_account("production", key, secret)

        self.bucket = b2_api.get_bucket_by_name(bucket_name)

    def upload_file(
        self, local_file: str, b2_file_name: str, **file_info: dict
    ) -> None:
        """
        Uploads a file to the B2 bucket associated with this B2Bucket object.

        Args:
            local_file (str): The path to the local file to upload.
            b2_file_name (str): The desired name for the file in the B2 bucket.
            **file_info (dict): Additional information to associate with the file.

        Returns:
            None
        """
        self.bucket.upload_local_file(
            local_file=local_file,
            file_name=b2_file_name,
            file_infos=file_info,
            progress_listener=TqdmProgressListener(b2_file_name),
        )

    def list_files(self) -> None:
        """
        Lists the files in the B2 bucket associated with this B2Bucket object.

        Returns:
            None
        """
        for file_version, folder_name in self.bucket.ls(latest_only=True):
            print(file_version.file_name, file_version.upload_timestamp, folder_name)
