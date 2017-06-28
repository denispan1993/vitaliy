#!./../../PyEnv/versions/3.6.1/envs/keksik/bin/python
# coding=utf-8


if __name__ == "__main__":
    import os
    import sys
    from django.core.management import execute_from_command_line

    os.environ["DJANGO_SETTINGS_MODULE"] = "proj.settings"
    execute_from_command_line(sys.argv)
