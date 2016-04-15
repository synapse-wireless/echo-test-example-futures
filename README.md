[![](https://cloud.githubusercontent.com/assets/1317406/12406044/32cd9916-be0f-11e5-9b18-1547f284f878.png)](http://www.synapse-wireless.com/)

# Echo Test Example Futures — Basic echo example using SNAP Connect Futures

`Echo Test Example Futures` is a straight-forward example project that sends message payloads to a node
and expects to get those messages echoed back.

## Background

Many SNAP Connect applications tend to follow a standard format:

1. A SNAP Node has some kind of valuable data that needs to be collected.
1. Create a method on the node to collect and return polled data.
1. Send callback RPC to the node and wait for a response.
1. The node's callback response triggers the SNAP Connect method, which 
kicks off subsequent events.
1. Repeat ad infinitum.

There are two significant challenges with this:

 * The first is that maximizing throughput is difficult, since having 
your host send messages out to poll your nodes as quickly as it can 
doesn't leave any bandwidth available for receiving replies from the 
nodes it is polling. Queueing RPC calls to query nodes as quickly as the 
host can generate them gets the messages queued for output (until you 
run out of buffers), but doesn't send the messages efficiently. 
Triggering the sending of RPC calls from the RPC_SENT hook improves the 
system efficiency, but still leaves no bandwidth for the host to receive 
replies from the nodes it is polling.
 * The second is that managing the sending and receiving of messages 
typically requires setting up event-driven state machines, which can 
make your code complex, difficult to understand, and even harder to
maintain. By the time you add in other mechanisms, such as retries or 
timeouts, or recovery from dropped packets, even relatively simple
applications can grow unwieldy very quickly.

The Futures package for SNAP Connect solves these problems by simulating 
a synchronous environment when you can simply wait for data to be 
returned. SNAP Connect Futures also has built-in retry/timeout 
mechanisms to help provide more reliable communications with less
overhead. This lends itself to creating much more straight-forward code 
which, in turn, means faster development and easier bug-fixes in the 
future.

This demonstration script, `EchoTestFutures.py`, gives an example of 
using the SNAP Connect Futures library to query a node (or several 
nodes) repeatedly as quickly as your host can.

## Installation

First, download the example, either by cloning the repository with Git, or by downloading and unzipping the zip archive.
Then, using pip, install the required Python packages for the example, which include SNAP Connect Futures:

```bash
pip install -r requirements.txt
```

## Running This Example

All configuration for this example is done by changing hardcoded values near the top
of the `EchoTestFutures.py`, for example:

#### What serial interface do you want to use to reach your bridge node?

You will need to modify `SERIAL_TYPE` and `SERIAL_PORT` based on which type of bridge node you have:

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

The nature and configuration of your network will affect the rate at 
which you can process polls in your environment. But using SNAP Connect 
Futures should keep your application as efficient as possible, and it 
should keep your code easy to understand and easy to maintain.

For more details, refer to source file `EchoTestFutures.py`

## License

Copyright © 2016 [Synapse Wireless](http://www.synapse-wireless.com/), licensed under the [Apache License v2.0](LICENSE.md).

<!-- meta-tags: vvv-snapconnect, vvv-python, vvv-example -->
