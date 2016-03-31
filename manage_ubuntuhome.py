#!/home/user/PycharmProjects/Shop/VirtEnv/bin/python
# -*- coding: utf-8 -*-
import os
import sys

__author__ = 'AlexStarov'

if __name__ == "__main__":
    os.environ["DJANGO_SETTINGS_MODULE"] = "proj.settings"
    from django_jinja.builtins import DEFAULT_EXTENSIONS
    print DEFAULT_EXTENSIONS
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
