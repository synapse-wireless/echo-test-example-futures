[![](https://cloud.githubusercontent.com/assets/1317406/12406044/32cd9916-be0f-11e5-9b18-1547f284f878.png)](http://www.synapse-wireless.com/)

# Echo Test Example Futures - Basic echo example using SNAPconnect Futures

`Echo Test Example Futures` is a straight-forward example project that sends message payloads to a node
and expects to get those messages echoed back.

## Background

Many SNAPconnect applications tend to follow a standard format:

1. A SNAP Node has some kind of valuable data that needs to be collected. 
1. Create a callback method to handle collected/polled data from a node.
1. Send callback rpc to the node and wait for a response.
1. Response triggers the callback method which kicks off subsequent events.
1. Repeat ad infinitum.

Problem: It can be confusing as to what is actually happening, especially if you 
are viewing source code that you didn't write.  Traditional implementations are
very reliant on state-machines since everything has to be event-driven, as well.
In most cases, as soon as you get past the simplest applications, the complexity 
of your applications will begin to expand drastically.  Once you add in other
mechanisms such as retries/timeouts and dropped package handling, it's easy to 
see how even relatively simple applications can become more complex over time.

Solution: Use Futures to simulate a synchronous environment where you can 
simply wait for data to be returned.  SNAPconnect Futures also has built-in 
retry/timeout mechanisms to help provide more reliable communications with less 
overhead. This lends itself to creating much more straight-forward code which, 
in turn, means faster iteration and easier bug-fixes in the future.

Many SNAPconnect applications are built to gather data from the remote nodes as quickly
as possible.

Here are some approaches that **don't** work well.

#### Blindly enqueueing RPC calls

Since the packets have to be transferred "out" via either a serial or TCP/IP link,
blindly enqueueing lots of RPC calls just queues them up INSIDE your PC.

#### Queueing RPC calls based on HOOK_RPC_SENT, but with no regard for incoming replies

If you are sending COMMANDS (no return RPC call), triggering their transmission off
of the HOOK_RPC_SENT event is sufficient. However, if those outbound RPC calls are
going to result in INCOMING RPC calls, you need to give the remote nodes a chance to 
"get a word in edgewise".

## Installation

First, download the example, either by cloning the repo with git, or by downloading the zip archive.
Then, using pip, install the required Python packages for the example, which include SNAPconnect Futures:

```bash
pip install -r requirements.txt
```

## Running This Example

All configuration for this example is done by changing hardcoded values near the top
of the `EchoTestFutures.py`, for example:
 
#### What is the address of the SNAP Node you want to test against?

This could be your bridge node if you only want to see the effects of the
serial interface, or it could be a *remote* SNAP node if you also want to
include the effects of Over-The-Air (OTA) radio communications too.

```python
BRIDGE_NODE = "627d43" # <- Replace this with the address of your bridge node
```

#### What serial interface do you want to use to reach it?

Or in the remote node case, what serial interface to reach the bridge?

```python
# You should set these to match YOUR available hardware
SERIAL_TYPE = snap.SERIAL_TYPE_RS232
...
SERIAL_PORT = 0  # COM1
```

#### How many test RPC calls do you want to make?

Using a higher number of RPC calls will "average out" the time taken to 
perform route lookups to the node. This will make the "per-packet"
timing more accurate.

```python
NUMBER_OF_QUERIES = 100  # More polls == longer test
```
    
Once you have edited EchoTestFutures.py for your available hardware, run the example:

```bash
python EchoTestFutures.py 
```

The specified number of queries will be made, incoming responses will be counted,
and final results displayed. Here is an example:

```
Permanent license created on 2012-02-14 14:14:45.343000 for 000020
100 queries, 100 responses in 6903 milliseconds
SUCCESS!
```

For more details, refer to source file `EchoTestFutures.py`

## License

Copyright © 2016 [Synapse Wireless](http://www.synapse-wireless.com/), licensed under the [Apache License v2.0](LICENSE.md).

<!-- meta-tags: vvv-snapconnect, vvv-python, vvv-example -->
