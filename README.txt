"""
(c) Copyright 2015 Synapse Wireless, Inc.

EchoTestFutures.py - A simple throughput benchmark.

=== Background ===

Many SNAP Connect applications want to gather data from the remote nodes as quickly
as possible.

Here are some naive approaches that DON'T work well.

1) Blindly enqueueing RPC calls

Since the packets have to be transferred "out" via either a serial or TCP/IP link,
blindly enqueueing lots of RPC calls just queues them up INSIDE your PC.

2) Queueing RPC calls based on HOOK_RPC_SENT, but with no regard for incoming replies

If you are sending COMMANDS (no return RPC call), triggering their transmission off
off the HOOK_RPC_SENT event is sufficient. However, if those outbound RPC calls are
going to result in INCOMING RPC calls, you need to give the remote nodes a chance to 
"get a word in edgewise".

=== Running EchoTestFutures.py ===

All configuration for this example is done by changing hardcoded values near the top
of the source file, for example:
 
    What is the address of the SNAP Node you want to test against?
        This could be your bridge node if you only want to see the effects of the
        serial interface, or it could be a *remote* SNAP node if you also want to
        include the effects of Over-The-Air (OTA) radio communications too.

    What serial interface do you want to use to reach it?
        Or in the remote node case, what serial interface to reach the bridge?

    How many test RPC calls do you want to make?
        Using a higher number of RPC calls will "average out" the time taken to 
        perform route lookups to the node. This will make the "per-packet"
        timing more accurate.
    
Once you have edited EchoTestFutures.py for your available hardware, simply do:

python EchoTestFutures.py

The specified number of queries will be made, incoming responses will be counted,
and final results displayed. Here is an example:

    Permanent license created on 2012-02-14 14:14:45.343000 for 000020
    100 queries, 100 responses in 6903 milliseconds

For more details, refer to source file EchoTestFutures.py
"""
