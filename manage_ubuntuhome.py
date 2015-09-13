#!/home/user/PycharmProjects/Shop/VirtEnv/bin/python
# coding=utf-8

import os
import sys
# import django

if __name__ == "__main__":
    # cwd = os.path.dirname(__file__)
    # sys.path.append(os.path.join(os.path.abspath(os.path.dirname(cwd)), '../'))
    #os.putenv('DJANGO_SETTINGS_MODULE', 'proj.settings')
    #os.system('bash')
    # os.environ.setdefault(key="DJANGO_SETTINGS_MODULE", failobj="proj.settings", )
    # os.environ.setdefault(key="DJANGO_SETTINGS_MODULE", failobj="proj.settings")
    # from django.core.management import execute_from_command_line
    # execute_from_command_line(sys.argv)

    os.environ["DJANGO_SETTINGS_MODULE"] = "proj.settings"
    # django.setup()
    #DJANGO_SETTINGS_MODULE = os.getenv(key='DJANGO_SETTINGS_MODULE', )
    #print DJANGO_SETTINGS_MODULE
    from django.core.management import execute_from_command_line
    # print 1
    # from proj.settings import DATABASES
    # print(DATABASES)
    # print(os.environ.get("DJANGO_SETTINGS_MODULE", ))
    # print(sys.argv)
    #print 1
    execute_from_command_line(sys.argv)
    #print 2
#    print /home/user/PycharmProjects/Shop/VirtualEnv/bin/python
