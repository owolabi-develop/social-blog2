from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    bucket_name = 'developer-news-porter'
    location = 'media'

class StaticStorage(S3Boto3Storage):
    bucket_name = 'developer-news-porter'
    location = 'static'