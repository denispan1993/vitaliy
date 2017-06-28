#!./../../PyEnv/versions/3.6.1/envs/keksik/bin/python
# -*- coding: utf-8 -*-

__author__ = 'AlexStarov'

if __name__ == "__main__":
    import sys
    import os
    os.environ["DJANGO_SETTINGS_MODULE"] = "proj.settings"
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
