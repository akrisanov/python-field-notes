# ØMQ

ØMQ (or ZeroMQ) is a popular language-agnostic library for networking applications:
it provides “smart” sockets. When you create ØMQ sockets in code, they resemble regular sockets,
with recognizable method names like recv() and send() and so on—but internally these sockets
handle some of the more annoying and tedious tasks required for working with conventional sockets.

One of the features it provides is management of message passing, so you don’t have to invent
your own protocol and count bytes on the wire to figure out when all the bytes for a particular
message have arrived—you simply send whatever you consider to be a “message,” and the whole thing
arrives on the other end intact.

Another great feature is automatic reconnection logic. If the server goes down and comes back
up later, the client ØMQ socket will automatically reconnect. And even better, messages your code
sends into the socket will be buffered during the disconnected period, so they will all still
be sent out when the server returns. These are some of the reasons ØMQ is sometimes referred to
as [brokerless messaging](http://wiki.zeromq.org/whitepapers:brokerless): it provides some of
the features of message broker software directly in the socket objects themselves.

ØMQ sockets are already implemented as asynchronous internally (so they can maintain many
thousands of concurrent connections, even when used in threaded code), but this is hidden
from us behind the ØMQ API.

If ØMQ provides sockets that are already asynchronous, in a way that is usable with threading,
what is the point of using ØMQ with asyncio? The answer is cleaner code.

---

In real production code with lots of ØMQ sockets, the coro‐ utine handlers for each could even be
in separate files, providing more opportunities for better code structure. And even for programs
with a single read/write socket, it is very easy to use separate coroutines for reading and
writing, if necessary.
