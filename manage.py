#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault(key="DJANGO_SETTINGS_MODULE", failobj="proj.settings", )

    from django.core.management import execute_from_command_line
    print 1
    from proj.settings import DATABASES
    print(DATABASES)
    print(os.environ.get("DJANGO_SETTINGS_MODULE", ))
    print(sys.argv)
    execute_from_command_line(sys.argv)
