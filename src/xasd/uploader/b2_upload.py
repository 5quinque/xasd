import logging

from b2sdk.v2 import B2Api, InMemoryAccountInfo, TqdmProgressListener


logger = logging.getLogger(__name__)


class B2Bucket:
    def __init__(self, bucket_name, key, secret):
        info = InMemoryAccountInfo()
        b2_api = B2Api(info)
        b2_api.authorize_account("production", key, secret)

        self.bucket = b2_api.get_bucket_by_name(bucket_name)

    def upload_file(self, local_file, b2_file_name, **file_info):
        self.bucket.upload_local_file(
            local_file=local_file,
            file_name=b2_file_name,
            file_infos=file_info,
            progress_listener=TqdmProgressListener(b2_file_name),
        )

    def list_files(self):
        for file_version, folder_name in self.bucket.ls(latest_only=True):
            print(file_version.file_name, file_version.upload_timestamp, folder_name)
