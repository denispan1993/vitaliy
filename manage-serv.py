#!/usr/www/envs/keksik_com_ua/bin/python
# -*- coding: utf-8 -*-
__author__ = 'AlexStarov'

import os
import sys

if __name__ == "__main__":
    os.environ["DJANGO_SETTINGS_MODULE"] = "proj.settings"
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
