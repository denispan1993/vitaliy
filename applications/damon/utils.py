import asyncio
import logging
import multiprocessing

from django.conf import settings

import asterisk.manager
from redis_collections import Dict


logger = multiprocessing.log_to_stderr(logging.INFO)


def _connect_to_ami() -> asterisk.manager.Manager:
    """
    Connecting to asterisk(AMI)
    """
    while True:
        manager = asterisk.manager.Manager()
        try:
            manager.connect(settings.AS_MANAGER_IP)
            manager.login(settings.AS_MANAGER_LOGIN,
                          settings.AS_MANAGER_PASSWORD)
        except asterisk.manager.ManagerException as e:
            logger.error("connect to ami Error: %s" % e)

        if manager.connected():
            return manager


def _do_command_safety(manager: asterisk.manager.Manager,
                       command_to_asterisk: str) -> tuple:
    """
    Trying send command to an asterisk and receiving an answer,
        if got error will create new connection to the asterisk and do same

    :return: tuple : where
        0 - asterisk.manager.Manager;
        1 - result of executing command by asterisk
    """
    while True:
        try:
            if manager.connected():
                response = manager.command(command_to_asterisk)

                return manager, response

        except asterisk.manager.ManagerException as e:
            logger.error("command safety Error: %s" % e)
            try:
                manager.logoff()
            except asterisk.manager.ManagerException as e:
                logger.error("logoff Error: %s" % e)
            finally:
                manager.close()
                logger.info('manager.close()')
                manager = _connect_to_ami()
                logger.info('new manager')


@asyncio.coroutine
def _get_response_to_command(manager: asterisk.manager.Manager,
                             command_to_manager: str,
                             key: str,
                             loop: asyncio.events.BaseDefaultEventLoopPolicy):
    """
    Getting an answer from an asterisk, and put it to a redis storage
    """
    asyncio.sleep(1, loop=loop)
    manager, response = _do_command_safety(manager, command_to_manager)
    monitor = Dict(key=settings.MONITORING_KEY)
    monitor[key] = response.data
    asyncio.async(_get_response_to_command(manager, command_to_manager,
                                           response, loop), loop=loop)


def _send_command_to_asterisk(command_to_asterisk: str, key: str):
    """
    Sending command to asterisk through AMI in an async loop
    """
    manager = _connect_to_ami()
    loop = asyncio.new_event_loop()
    asyncio.async(
        _get_response_to_command(manager, command_to_asterisk, key, loop),
        loop=loop
    )
    try:
        logger.info('loop.run_forever with command - "%s"' %
                    command_to_asterisk)
        loop.run_forever()
    finally:
        logger.info('loop.close()')
        loop.close()


def create_daemons(keys_with_command: list):
    """
    Creating processes daemons and asked in each of them an asterisk

    :param keys_with_command: list of tuples, where each tuple consist with
        0 - str: command;
        1 - str: key in redis dict.
    :return: list of multiprocessing.Process
    """
    processes = []
    for command, key in keys_with_command:
        process = multiprocessing.Process(
                target=_send_command_to_asterisk,
                kwargs={'command_to_asterisk': command, 'key': key}
        )
        process.daemon = True
        processes.append(
            process
        )
        process.start()

    for process in processes:
        logger.info('join %s' % process.name)
        process.join(timeout=1)
