# (c) Copyright 2014 Synapse Wireless, Inc.
"""
EchoTestFutures.py - a simple benchmark used to determine how fast SNAP Connect can
communicate with a directly connected bridge. We use this to evaluate different
Python platforms, implementations, and serial drivers.

This example demonstrates one way to maximize throughput without choking the network.

Refer to comments throughout this file, plus the accompanying README.txt.
"""

import apy
import logging
import asyncore
from snapconnect import snap
from future_snap_connect import FutureSnapConnect
import time
import tornado
from tornado.gen import coroutine

log = logging.getLogger('EchoTestFutures')
# Note the hardcoded COM1 usage.
# You should set these to match YOUR available hardware
SERIAL_TYPE = snap.SERIAL_TYPE_RS232
#SERIAL_TYPE = snap.SERIAL_TYPE_SNAPSTICK100
#SERIAL_TYPE = snap.SERIAL_TYPE_SNAPSTICK200

# If you're on a unix platform, you'll need to specify the interface type differently than windows
# An example for a typical interface device is shown below
SERIAL_PORT = 0 # COM1
#SERIAL_PORT = '/dev/ttyUSB0'

NUMBER_OF_QUERIES = 100 # More polls == longer test
TIMEOUT = 1.0 # (in seconds) You might need to increase this if:
# 1) You change the RPC call being made
# If you are invoking some custom function of your own, and it takes longer for the
# nodes to respond - for example, some function that performs multiple analog readings
# and then computes a result.
# 2) You are benchmarking a remote node, and it is so many hops away that 1 second is too short.

# You could experiment with various size payloads.
# Note that PAYLOAD is just one of several parameters to the actual RPC call
#PAYLOAD = "A"
#PAYLOAD = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
#PAYLOAD = "ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOP"
PAYLOAD = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890-=<({[]})=-!@#$"

@coroutine
def main():
    replies = 0
    """Simple benchmark. Create a SNAP Connect instance, and use it to send a batch of RPC calls"""
    tornado.ioloop.PeriodicCallback(asyncore.poll, 5).start()
    scheduler = apy.ioloop_scheduler.IOLoopScheduler.instance()
    # Create a SNAP Connect object to do communications (comm) for us
    comm = snap.Snap(scheduler=scheduler, funcs={})
    tornado.ioloop.PeriodicCallback(comm.poll_internals, 5).start()
    # Get a future snapconnect object
    fsc = FutureSnapConnect(comm)

    bridge_address = yield fsc.open_serial(SERIAL_TYPE, SERIAL_PORT)
    log.info("Bridge connection opened to %s", bridge_address)
    start_time = time.time()
    for queries in range(NUMBER_OF_QUERIES):
        result = yield fsc.callback_rpc(bridge_address, 'str', args=(PAYLOAD,), retries=3, timeout=TIMEOUT)
        if result != (PAYLOAD,):
            log.error("we did not receive the correct response %r" % result)
        else:
            replies += 1
    end_time = time.time()
    delta = end_time - start_time
    delta *= 1000
    log.info("%d queries, %d responses in %d milliseconds" % (queries+1, replies, delta))
    my_loop.stop()


if __name__ == "__main__":
    global my_loop
    # Notice that because this is a benchmark, we have set logging to of the lowest verbose levels
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    main()
    my_loop = tornado.ioloop.IOLoop.instance()
    my_loop.start()

