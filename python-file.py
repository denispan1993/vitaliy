#!./../../PyEnv/versions/3.6.1/envs/keksik/bin/python

import asyncio
import time
import datetime


async def time_consuming_computation(x):

    print('Computing {0} ** 2...'.format(x, ))

    print('1.1:%s' % time.time(), )
    await asyncio.sleep(0.5)
    print('1.2:%s' % time.time(), )

    return x ** 2


async def process_data(x):

    print('2.1:%s' % time.time(), )
    result = await time_consuming_computation(x)

    print('{0} ** 2 = {1}:{2}'.format(x, result, time.time()))
    print('2.2:%s' % time.time(), )
    return result


async def display_date1(loop):
    end_time = loop.time() + 5.0
    while True:
        print(datetime.datetime.now())
        if (loop.time() + 0.5) >= end_time:
            break
        await asyncio.sleep(0.5)


def display_date2(end_time, loop):
    print('1:', datetime.datetime.now())
    if (loop.time() + 1.0) < end_time:
        loop.call_later(1, display_date2, end_time, loop)
        print('exit2', datetime.datetime.now())
    else:
        loop.stop()


def reader():
    data = rsock.recv(100)
    print("Received:", data.decode())
    # We are done: unregister the file descriptor
    loop.remove_reader(rsock)
    # Stop the event loop
    loop.stop()


if __name__ == '__main__':

    loop = asyncio.get_event_loop()

    res = loop.run_until_complete(process_data(237, ), )
    print(res, )

    loop.close()
    print('...')
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # Blocking call which returns when the hello_world() coroutine is done
    loop.run_until_complete(display_date1(loop))

    loop.close()
    print('...')
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # Schedule the first call to display_date()
    end_time = loop.time() + 5.0
    loop.call_soon(display_date2, end_time, loop)
    print('exit1', datetime.datetime.now())

    # Blocking call interrupted by loop.stop()
    loop.run_forever()
    print('exit - end', datetime.datetime.now())
    loop.close()

    try:
        from socket import socketpair
    except ImportError:
        from asyncio.windows_utils import socketpair

    # Create a pair of connected file descriptors
    rsock, wsock = socketpair()
    print('...')
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Register the file descriptor for read event
    loop.add_reader(rsock, reader)

    # Simulate the reception of data from the network
    loop.call_soon(wsock.send, 'abc'.encode())

    # Run the event loop
    loop.run_forever()

    # We are done, close sockets and the event loop
    rsock.close()
    wsock.close()
    loop.close()
