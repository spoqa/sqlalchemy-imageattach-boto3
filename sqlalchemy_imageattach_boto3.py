import io
from typing import Optional, Union

from boto3 import client
from sqlalchemy_imageattach.store import Store
from sqlalchemy_imageattach.stores.fs import guess_extension
from sqlalchemy_imageattach.stores.s3 import (
    BASE_REGION_URL_FORMAT, BASE_URL_FORMAT, DEFAULT_MAX_AGE,
)


class Boto3S3Store(Store):
    def __init__(
        self,
        bucket,  # type: str
        access_key=None,  # type: Optional[str]
        secret_key=None,  # type: Optional[str]
        max_age=DEFAULT_MAX_AGE,  # type: int
        prefix='',  # type: str
        public_base_url=None,  # type: Optional[str]
        region=None,  # type: Optional[str]
    ):
        self.bucket = bucket
        self.s3_client = client(
            's3',
            region_name=region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )
        self.max_age = max_age
        self.prefix = prefix.strip()
        if self.prefix.endswith('/'):
            self.prefix = self.prefix.rstrip('/')
        if public_base_url is None:
            if region is None:
                self.public_base_url = BASE_URL_FORMAT.format(bucket)
            else:
                self.public_base_url = BASE_REGION_URL_FORMAT.format(
                    bucket,
                    region=region
                )
        elif public_base_url.endswith('/'):
            self.public_base_url = public_base_url.rstrip('/')
        else:
            self.public_base_url = public_base_url

    def get_key(
        self,
        object_type,  # type: str
        object_id,  # type: str
        width,  # type: int
        height,  # type: int
        mimetype,  # type: str
    ):
        # type: (...) -> str
        extension = guess_extension(mimetype)
        key = f'{object_type}/{object_id}/{width}x{height}{extension}'
        if self.prefix:
            return f'{self.prefix}/{key}'
        return key

    def upload_file(
        self,
        key,  # type: str
        data,  # type: Union[bytes, io.IOBase]
        content_type,  # type: str
        rrs,  # type: bool
        acl='public-read',  # type: str
    ):
        self.s3_client.put_object(
            ACL=acl,
            Body=data,
            Bucket=self.bucket,
            CacheControl=f'max-age={self.max_age!s}',
            ContentType=content_type,
            StorageClass='REDUCED_REDUNDANCY' if rrs else 'STANDARD',
            Key=key,
        )

    def put_file(
        self,
        file,  # type: io.IOBase
        object_type,  # type: str
        object_id,  # type: str
        width,  # type: int
        height,  # type: int
        mimetype,  # type: str
        reproducible,  # type: bool
    ):
        key = self.get_key(object_type, object_id, width, height, mimetype)
        self.upload_file(key, file, mimetype, reproducible)

    def delete_file(
        self,
        object_type,  # type: str
        object_id,  # type: str
        width,  # type: int
        height,  # type: int
        mimetype,  # type: str
    ):
        key = self.get_key(object_type, object_id, width, height, mimetype)
        self.s3_client.delete_object(
            Bucket=self.bucket,
            Key=key,
        )

    def get_file(
        self,
        object_type,  # type: str
        object_id,  # type: str
        width,  # type: int
        height,  # type: int
        mimetype,  # type: str
    ):
        # type: (...) -> io.IOBase
        key = self.get_key(object_type, object_id, width, height, mimetype)
        resp = self.s3_client.get_object(
            Bucket=self.bucket,
            Key=key,
        )
        return resp['Body']._raw_stream

    def get_url(
        self,
        object_type,  # type: str
        object_id,  # type: str
        width,  # type: int
        height,  # type: int
        mimetype,  # type: str
    ):
        # type: (...) -> str
        key = self.get_key(object_type, object_id, width, height, mimetype)
        return f'{self.public_base_url}/{key}'
