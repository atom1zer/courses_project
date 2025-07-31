
from storages.backends.s3boto3 import S3Boto3Storage

class ClientDocsStorage(S3Boto3Storage):
    location = 'uploads'
    default_acl = 'private'
    file_overwrite = False