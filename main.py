import os
import sys
from django.core.management import execute_from_command_line

if __name__ == "__main__":
    # Set the required environment variables
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Project.settings")

    # Add the Django project's root directory to sys.path
    django_project_path = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(django_project_path)

    # Run the Django application
    execute_from_command_line(sys.argv)
