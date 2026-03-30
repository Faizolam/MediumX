# Create a new file: app/services/storage.py
from google.cloud import storage
import os
from app.core.config import UPLOAD_BUCKET_NAME

class CloudStorageService:
    def __init__(self):
        self.client = storage.Client()
        self.bucket = self.client.bucket(UPLOAD_BUCKET_NAME)
    
    def upload_file(self, file_data, filename):
        blob = self.bucket.blob(f"images/{filename}")
        blob.upload_from_string(file_data)
        return blob.public_url