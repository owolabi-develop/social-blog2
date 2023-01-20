from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    bucket_name = 'developer-news-porter'
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False

class StaticStorage(S3Boto3Storage):
    bucket_name = 'developer-news-porter'
    location = 'static'