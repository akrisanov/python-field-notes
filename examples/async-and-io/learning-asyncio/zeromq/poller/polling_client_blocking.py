# https://zguide.zeromq.org/#Handling-Multiple-Sockets

import zmq

context = zmq.Context()

# a receive-only kind of socket that will be fed by some other send-only socket, which will be a PUSH type
receiver = context.socket(zmq.PULL)
receiver.connect("tcp://localhost:5557")

# another kind of receive-only socket, and it will be fed a PUB socket which is send-only
subscriber = context.socket(zmq.SUB)
subscriber.connect("tcp://localhost:5556")
subscriber.setsockopt_string(zmq.SUBSCRIBE, "")

# If you need to move data between multiple sockets in a threaded ØMQ application,
# you’re going to need a poller. This is because these sockets are not thread-safe,
# so you cannot recv() on different sockets in different threads:
poller = zmq.Poller()
poller.register(receiver, zmq.POLLIN)
poller.register(subscriber, zmq.POLLIN)

while True:
    try:
        socks = dict(poller.poll())  # works similarly to the select() system call
    except KeyboardInterrupt:
        break

    # Using a poller loop plus an explicit socket-selection block makes the code look a little
    # clunky, but this approach avoids thread-safety problems by guaranteeing the same socket
    # is not used from different threads.
    if receiver in socks:
        message = receiver.recv_json()
        print(f"Via PULL: {message}")

    if subscriber in socks:
        message = subscriber.recv_json()
        print(f"Via SUB: {message}")
