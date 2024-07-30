from google.cloud import storage
from pathlib import Path
import os, uuid, time
from datetime import datetime, timedelta, timezone

BASE_DIR = Path(__file__).resolve().parent.parent

class CloudStorageManager:
    def __init__(self):
        self.storage_client = storage.Client.from_service_account_json(os.path.join(BASE_DIR, "mediasaver.json"))
        self.bucket = self.storage_client.bucket('mediasaver')

    def delete_file(self, file_path):
        if file_path:
            blob = self.bucket.blob(file_path)
            blob.delete()
            return True
        return False

    def delete_old_files(self):
        while True:
            for blob in self.bucket.list_blobs():
                blob_age = datetime.now(timezone.utc) - blob.time_created
                if blob_age > timedelta(minutes=3):
                    print(f"Deleting {blob.name}, Age: {blob_age}")
                    self.delete_file(blob.name)
            time.sleep(60)  # Check every 60 seconds

manager = CloudStorageManager()
manager.delete_old_files()
