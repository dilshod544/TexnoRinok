from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings

class SupabaseMediaStorage(S3Boto3Storage):
    location = ''
    file_overwrite = False
    
    def _clean_name(self, name):
        return name

    def url(self, name):
        # Force the public Supabase URL format
        return f"https://ckzmzsgkuqyuauhwbzdr.supabase.co/storage/v1/object/public/media/{name}"
