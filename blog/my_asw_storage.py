from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    bucket_name = 'social-blog'
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False

class StaticStorage(S3Boto3Storage):
    bucket_name = 'social-blog'
    location = 'static'
    default_acl = 'public-read'
    file_overwrite = False