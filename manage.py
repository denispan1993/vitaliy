#!./../../PyEnv/versions/3.6.1/envs/keksik/bin/python
#1!/home/sergey/PycharmProjects/Env/bin/python
#1!/home/user/PycharmProjects/Shop/VirtEnv/bin/python
# coding=utf-8

import os
import sys
from django.core.management import execute_from_command_line

if __name__ == "__main__":
    # cwd = os.path.dirname(__file__)
    # sys.path.append(os.path.join(os.path.abspath(os.path.dirname(cwd)), '../'))
    #os.putenv('DJANGO_SETTINGS_MODULE', 'proj.settings')
    #os.system('bash')
    # os.environ.setdefault(key="DJANGO_SETTINGS_MODULE", failobj="proj.settings", )

    os.environ["DJANGO_SETTINGS_MODULE"] = "proj.settings"
    #DJANGO_SETTINGS_MODULE = os.getenv(key='DJANGO_SETTINGS_MODULE', )
    #print DJANGO_SETTINGS_MODULE
    # print 1
    # from proj.settings import DATABASES
    # print(DATABASES)
    # print(os.environ.get("DJANGO_SETTINGS_MODULE", ))
    # print(sys.argv)
    execute_from_command_line(sys.argv)
