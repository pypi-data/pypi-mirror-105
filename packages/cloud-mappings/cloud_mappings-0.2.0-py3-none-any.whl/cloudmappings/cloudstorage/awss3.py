from typing import Dict

import boto3

from .cloudstorage import CloudStorage, KeyCloudSyncError


class AWSS3(CloudStorage):
    def __init__(
        self,
        bucket_name: str,
    ) -> None:
        self._client = boto3.client("s3")
        self._bucket_name = bucket_name

    def _get_s3_object(self, key: str):
        return boto3.resource("s3").Object(self._bucket_name, key)

    def create_if_not_exists(self, metadata: Dict[str, str]):
        bucket = boto3.resource("s3").Bucket(self._bucket_name)
        try:
            bucket.create()
        except bucket.meta.client.exceptions.BucketAlreadyExists:
            return True
        return False

    def download_data(self, key: str, etag: str) -> bytes:
        obj = boto3.resource("s3").Object(self._bucket_name, key)
        obj.reload()
        
        try:
            obj = self._client.get_object(key)
        except self._client.meta.client.exceptions.NoSuchKey:
            raise KeyCloudSyncError(key=key, etag=etag)
        if etag is not None and etag != obj["ETag"]:
            raise KeyCloudSyncError(key=key, etag=etag)
        return obj["Body"].read()

    def upload_data(self, key: str, etag: str, data: bytes) -> str:
        try:
            obj = self._client.get_object(key)
        except self._client.meta.client.exceptions.NoSuchKey:
            raise KeyCloudSyncError(key=key, etag=etag)
        if etag is not None and etag != obj["ETag"]:
        obj = boto3.resource("s3").Object(self._bucket_name, key)
        return obj.put(
            Body=data,
            # TODO: check that etag is MD5 hash at least most of the time?
            # TODO: figure out something else the rest of the time?
            ContentMD5=etag,
        )["Etag"]

    def delete_data(self, key: str, etag: str) -> None:
        obj = boto3.resource("s3").Object(self._bucket_name, key)
        obj.delete(
            # TODO: somewhere to check etag here?
        )

    def list_keys_and_ids(self, key_prefix: str) -> Dict[str, str]:
        bucket = boto3.resource("s3").Bucket(self._bucket_name)
        return {
            o.key: o.e_tag
            for o in bucket.objects.filter(
                Prefix=key_prefix,
            )
        }
