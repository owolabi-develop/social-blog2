from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    bucket_name = 'social-blogers'
    location = 'mediafiles'
    default_acl = 'public-read'
    file_overwrite = False

class StaticStorage(S3Boto3Storage):
    bucket_name = 'social-blogers'
    location = 'staticfiles'
    default_acl = 'public-read'
    file_overwrite = False