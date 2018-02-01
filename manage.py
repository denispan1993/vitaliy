#!./../../PyEnv/versions/shop/bin/pypy3
# -*- coding: utf-8 -*-

import os
import sys
from django.core.management import execute_from_command_line

__author__ = 'AlexStarov'

if __name__ == "__main__":

    os.environ["DJANGO_SETTINGS_MODULE"] = "proj.settings"
    execute_from_command_line(sys.argv)
