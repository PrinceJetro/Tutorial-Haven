import os
import json
from pathlib import Path
import django

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from django.core.serializers import serialize
from webapp.models import Course, PastQuestionsObj, PastQuestionsTheory, Topic  # Import only the required models

# Specify the backup file path
backup_file = Path(__file__).parent / "backup.json"

# Function to serialize and save data
def backup_data():
    try:
        # Fetch the required data
        models_to_backup = {
            "topics": Topic.objects.all(),
            "courses": Course.objects.all(),
            "past_questions_obj": PastQuestionsObj.objects.all(),
            "past_questions_theory": PastQuestionsTheory.objects.all(),
        }

        # Serialize the data
        data = {key: json.loads(serialize("json", queryset)) for key, queryset in models_to_backup.items()}

        # Save to file
        with open(backup_file, "w") as file:
            json.dump(data, file, indent=4)

        print(f"Backup completed successfully! Data saved to {backup_file}")
    except Exception as e:
        print(f"An error occurred during the backup: {e}")

# Execute the backup
if __name__ == "__main__":
    backup_data()
