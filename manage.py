#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import json
from pathlib import Path


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mygalley.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Load port from config.json when running runserver
    if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
        try:
            config_file = Path(__file__).resolve().parent / 'config.json'
            with open(config_file, 'r') as f:
                config = json.load(f)
                port = config.get('port', 8000)
            
            # If no port specified in command line, use config port
            if len(sys.argv) == 2:
                sys.argv.append(str(port))
        except FileNotFoundError:
            pass  # Use Django's default port if config.json doesn't exist
    
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
