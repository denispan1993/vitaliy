#!./../../PyEnv/versions/pypy3-v5.10.1-linux32/bin/pypy3
# coding=utf-8


if __name__ == "__main__":
    import os
    import sys
    from django.core.management import execute_from_command_line

    os.environ["DJANGO_SETTINGS_MODULE"] = "proj.settings"
    execute_from_command_line(sys.argv)
