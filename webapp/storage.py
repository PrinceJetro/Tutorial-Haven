from django.core.files.storage import Storage
from django.conf import settings
from supabase import create_client
from urllib.parse import quote


class SupabaseStorage(Storage):
    def __init__(self):
        self.client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        self.bucket = self.client.storage.from_(settings.SUPABASE_BUCKET,)

    def _open(self, name, mode='rb'):
        pass

    def _save(self, name, content):
        self.bucket.upload(name, content.read())
        return name    

    def delete(self, name):
        """Delete a file from the Supabase bucket."""
        try:
            response = self.bucket.remove([name])  # Remove file using Supabase's API
            if response.get("error") is None:
                print(f"File '{name}' successfully deleted.")
            else:
                print(f"Error deleting file '{name}': {response['error']['message']}")
        except Exception as e:
            print(f"Exception occurred while deleting file '{name}': {e}")

    def exists(self, name):
        pass
        # try:
        #     file = self.bucket.get(name)
        #     return file.get("data") is not None
        # except Exception as e:
        #     print(f"Error checking if file exists: {e}")
        #     return False

    def listdir(self, path):
        pass

    def size(self, name):
        pass

    def url(self, name):
        encoded_name = quote(name)
        return self.bucket.get_public_url(encoded_name)
