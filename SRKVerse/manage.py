#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path


def main():
    """Run administrative tasks."""
    #Get the absolute path of the current file's directory
    current_path = Path(__file__).resolve().parent

    #Add both the current directory and its parent to Python Path
    sys.path.append(str(current_path))
    sys.path.append(str(current_path.parent))

    #Print paths for debugging
    print("Current directory:", current_path)
    print("Python path: ", sys.path)

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SRKVerse.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
