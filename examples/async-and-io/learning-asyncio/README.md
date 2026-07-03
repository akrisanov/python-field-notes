# Using Asyncio in Python

## Book Notes

Large-scale concurrency is one big reason to learn and use Asyncio, but the other big attraction
of Asyncio over preemptive threading is safety: it will be much easier for you to avoid race
condition bugs with Asyncio.

---

While you wait for a task to complete, work on other tasks can be performed.

---

It can be effective only if every task is short, or at least can be performed in a short period of time.

---

CPUs do work and wait on network I/O.

---

For I/O-bound workloads, there are exactly (only!) two reasons to use async-based concurrency
over thread-based concurrency:

1. Asyncio offers a safer alternative to preemptive multitasking (i.e., using threads),
   thereby avoiding the bugs, race conditions, and other nondeterministic dangers that frequently
   occur in nontrivial threaded applications.
2. Asyncio offers a simple way to support many thousands of simultaneous socket connections,
   including being able to handle many long-lived connections for newer technologies like WebSockets,
   or MQTT for Internet of Things (IoT) applications.

---

Threading—as a programming model—is best suited to certain kinds of computational tasks that are
best executed with multiple CPUs and shared memory for efficient communication between the threads.

---

Falsehoods about async:

- Asyncio will make my code blazing fast
- Asyncio makes threading redundant
- Asyncio removes the problems with the GIL
- Asyncio prevents all race conditions
- Asyncio makes concurrent programming easy

---

Even with Asyncio, there is still a great deal of complexity to deal with. How will your
application support health checks? How will you communicate with a database that may allow only
a few connections—much fewer than your five thousand socket connections to clients?
How will your program terminate connections gracefully when you receive a signal to shut down?
How will you handle (blocking!) disk access and logging? These are just a few of the many complex
design decisions that you will have to answer.

---

The OS decides how to share CPU resources with each of the parts, much as the OS decides to share
CPU resources with all the other different programs (processes) running at the same time.

---

The Python interpreter uses a global lock, called the global interpreter lock (GIL), to protect
the internal state of the interpreter itself.

A side effect of the lock is that it ends up pinning all threads in your program to a single CPU.

---

The best practice for using threads is to use the `ThreadPoolExecutor` class from the
`concurrent.futures` module, passing all required data in through the `submit()` method.

---

Drawbacks of Threading:

- Threading is difficult
- Threads are resource-intensive
- Threading can affect throughput (context-switching)
- Threading is inflexible – a thread may be waiting for data on a socket, but the OS scheduler may
  still switch to and from that thread thousands of times before any actual work needs to be done

For smaller or more finegrained tasks, the overhead that is associated with concurrency can
outweigh the benefit of running the tasks in parallel.

The problem with preemptive multitasking is that any thread busy with some steps can be
interrupted at any time, and a different thread can be given the opportunity to work through
the same steps.

It is not possible to see the race condition by looking at the source code alone. This is because
the source code provides no hints about where execution is going to switch between threads.
That wouldn’t be useful anyway, because the OS can switch between threads just about anywhere.

---

In async programs, we’ll be able to see exactly where context will switch between multiple
concurrent coroutines, because the await keyword indicates such places explicitly.

---

If you’re inside an async def function, you should call `asyncio.get_running_loop()`.

`loop.create_task()` schedules your coroutine to be run on the loop.

---

`loop.run_until_complete(coro)` blocks the current thread, which will usually be the main thread.
`run_until_complete()` will keep the loop running only until the given coro completes — but all
other tasks scheduled on the loop will also run while the loop is running.

`asyncio.run()` will do all of the cancelling, gathering, and waiting for pending tasks to finish up.

`loop.close()` is usually the final action: it must be called on a stopped loop, and it will clear
all queues and shut down the executor.

---

We allow a context switch back to the loop using the keyword `await`.

What happens if executor functions outlive their async counterparts during the shutdown sequence?

`run_in_executor()` does not block the main thread: it only schedules the executor task to run
(it returns a `Future`, which means you can await it if the method is called within another
coroutine function). The executor task will begin executing only after `run_until_complete()`
is called, which allows the event loop to start processing events.

The set of tasks in pending does not include an entry for the call to `blocking()` made in
`run_in_executor()`.

`all_tasks()` really does return only `Tasks`, not `Futures`.

---

Curio and Trio rely only on native coroutines in Python, and nothing whatsoever from the asyncio
library module.

---

asyncio provides both a loop specification, `AbstractEventLoop`, and an implementation, `BaseEventLoop`.

uvloop simply “plugs into” the hierarchy and replaces only the loop part of the stack.

---

Task is a subclass of Future.

A Future instance represents some sort of ongoing action that will return a result
via notification on the event loop.

A Task represents a coroutine running on the event loop.

A future is “loop-aware,” while a task is both “loop-aware” and “coroutine-aware.”

---

The `Queue` provided by asyncio has a very similar API to the thread-safe Queue in the `queue` module,
except that the asyncio version requires the `await` keyword on `get()` and `put()`.

---

These are the tiers that are most important to focus on when learning how to use the `asyncio`
library module for writing network applications:

- How to write async def functions and use await to call and execute other coroutines
- How to start up, shut down, and interact with the event loop
- Necessary to use blocking code in your async application
- If you need to feed data to one or more long-running coroutines, the best way to do that
  is with `asyncio.Queue`.

---

The streams API gives you the simplest way to handle socket communication over a network.

---

While it is common to refer to async def functions as coroutines, strictly speaking they are
considered by Python to be coroutine functions.

You need to call the async def function to obtain the coroutine object.

A coroutine is an object that encapsulates the ability to resume an underlying function that
has been suspended before completion. Coroutines are very similar to generators.

---

The `send()` and the `StopIteration`, define the start and end of the executing coroutine

---

When you call `task.cancel()`, the event loop will internally use `coro.throw()` to raise
`asyncio.CancelledError` inside your coroutine.

The `throw()` method is used (internally in asyncio) for task cancellation, which we can also
demonstrate quite easily.

The `StopIteration` exception is the normal way that coroutines exit.

Task cancellation is nothing more than regular exception raising (and handling).

If your coroutine receives a cancellation signal, that is a clear directive to do only
whatever cleanup is necessary and exit.

---

The event loop in asyncio handles all of the switching between coroutines, as well as catching
those StopIteration exceptions—and much more, such as listening to sockets and file descriptors for events.

---

The `get_event_loop()` method works only within the same thread.

Because it can be called only within the context of a coroutine, a task, or a function called
from one of those, it always provides the current running event loop.

---

`ensure_future()` was intended only for framework designers, but made the original adoption of
asyncio much more difficult to understand for application developers.

A Future represents a future completion state of some activity and is managed by the loop.
A Task is exactly the same, but the specific “activity” is a coroutine – probably one of yours
that you created with an async def function plus `create_task()`.

Running a function on an executor will return a Future instance, not a Task.

The `Future` class represents a state of something that is interacting with a loop.
You can instead think of a Future instance as a toggle for completion status.
The future completes when its result is set.

---

Coroutines run only when the loop is running.

---

You might wonder what happens if you call set_result() on a Task instance. It was possible to do
this before Python 3.8, but it is no longer allowed. Task instances are wrappers for coroutine
objects, and their result values can be set only internally as the result of the underlying
coroutine function.

---

The API method `asyncio.ensure_future()` is responsible for much of the widespread misunderstanding
about the asyncio library. Much of the API is really quite clear, but there are a few bad
stumbling blocks to learning, and this is one of them.

Here is a (hopefully) clearer description of `ensure_future()`:

- If you pass in a coroutine, it will produce a `Task` instance (and your coroutine will be
scheduled to run on the event loop). This is identical to calling `asyncio.create_task()`
(or `loop.create_task()`) and returning the new `Task` instance.
- If you pass in a `Future` instance (or a `Task` instance, because `Task` is a subclass of `Future`),
you get that very same thing returned, unchanged.

`ensure_future()` is intended to be used by framework authors to provide APIs to end-user
developers that can handle both kinds of parameters.

---

When next you look over the API, everywhere you see a function parameter described
as “awaitable objects,” it is likely that internally `ensure_future()` is being used to coerce
the parameter. For example, the `asyncio.gather()` function has the following signature:

```python
asyncio.gather(*aws, loop=None, ...)
```

The aws parameter means “awaitable objects,” which includes coroutines, tasks, and futures.
Internally, `gather()` is using `ensure_future()` for type coercion: tasks and futures are left
untouched, while tasks are created for coroutines.

The key point here is that as an end-user application developer, you should never need to
use `asyncio.ensure_future()`. It’s more a tool for framework designers.

---

Async generators are async def functions that have yield keywords inside them.

- Coroutines and generators are completely different concepts
- Async generators behave much like ordinary generators
- For iteration, you use `async for` for async generators, instead of the ordinary for used
  for ordinary generators

---

Most async-based programs are long-running, network-based applications.

---

The idiomatic shutdown procedure is to collect all unfinished tasks, cancel them, and then
let them all finish before closing the loop.

`asyncio.run()` does all of these steps for you, but it is important to understand the process
in detail so that you will be able to handle more complex situations.

As a general rule of thumb, try to avoid creating new tasks inside `CancelledError` exception
handlers. If you must, be sure to also await the new task or future inside the scope of
the same function.

If you’re using a library or framework, make sure to follow its documentation on how you should
perform startup and shutdown.

---

`asyncio.run()` uses `gather()` and `return_exceptions=True` internally.

the default is `gather(..., return_exceptions=False)`. This default is problematic for most
situations, including the shutdown process:

- `run_until_complete()` operates on a future; during shutdown, it’s the future returned by `gather()`
- If that future raises an exception, the exception will also be raised out of `run_until_complete()`,
  which means that the loop will stop.
- If `run_until_complete()` is being used on a group future, any exception raised inside any of
  the subtasks will also be raised in the “group” future if it isn’t handled in the subtask.
  Note this includes CancelledError.
- If only some tasks handle `CancelledError` and others don’t, the ones that don’t will cause
  the loop to stop. This means that the loop will be stopped before all the tasks are done.
- For shutdown, we really don’t want this behavior. We want `run_until_complete()` to finish only
  when all the tasks in the group have finished, regardless of whether some of
  the tasks raise exceptions.
- Hence we have `gather(*, return_exceptions=True)`: that setting makes the “group” future treat
  exceptions from the subtasks as returned values, so that they don’t bubble out and interfere
  with run_until_complete().

An undesirable consequence of capturing exceptions in this way is that some errors may escape
your attention because they’re now (effectively) being handled inside the group task.
If this is a concern, you can obtain the output list from `run_until_complete()` and scan it for
any subclasses of `Exception`, and then write log messages appropriate for your situation.

Without `return_exceptions=True`, the `ZeroDivisionError` would be raised
from `run_until_complete()`, stopping the loop and thus preventing the other tasks from finishing.

---

`KeyboardInterrupt` corresponds to the `SIGINT` signal. In network services, the more common
signal for process termination is actually `SIGTERM`, and this is also the default signal when
you use the kill command in a Unix shell.

The kill command on Unix systems is deceptively named: all it does it send signals to a process.
Without arguments, kill `<PID>` will send a `TERM` signal: your process can receive the signal
and do a graceful shutdown, or simply ignore it! That’s a bad idea, though, because if your
process doesn’t stop eventually, the next thing the would-be killer usually does is `kill -s KILL <PID>`,
which sends the `KILL` signal. This will shut you down, and there’s nothing your program can
do about it. Receiving the `TERM` (or `INT`) signal is your opportunity to shut down in a controlled way.

`asyncio` has built-in support for handling process signals.

Your app must not do weird things if you’re sent signals multiple times
(such as rerunning any shutdown steps); after you receive the first shutdown signal,
you want to simply ignore any new signals until exit.

---

Application lifetime management is a core consideration for using async programming correctly.

---

The streams API is the high-level interface offered for async socket programming.

---

Sending and receiving data might be best handled in separate coroutines, depending on the use case.
In such instances, queues can be very useful for moving data between those different coroutines
and for providing buffering to decouple them.

---

The design of asyncio has been heavily influenced by Twisted and the extensive experience
of its leaders and maintainers.

Twisted includes high-quality implementations of a huge number of internet protocols,
including not only the usual HTTP but also XMPP, NNTP, IMAP, SSH, IRC, and FTP
(both servers and clients). And the list goes on: DNS? Check. SMTP? Check. POP3? Check.
The availability of these excellent internet protocol implementations continues to make Twisted compelling.

---

`aiofiles` provides a convenient wrapper for performing disk access in a thread.
This works because Python releases the GIL during file operations so your main thread
(running the asyncio loop) is unaffected.

## Sync, Blocking, and Async Code

- Sync – usual Python code we write
- Blocking – code that can block the entire thread
- Async – tasks, futures, etc.

## Loop

Application may spin event loop at will (say get and close a loop inside a single function),
to perform IO heavy computations:

- scraping
- concurrent uploads
- ...

Application may delegate IO heavy tasks to dedicated loop in separate thread.

## ThreadPool

- No way to kill thread if task stuck inside
- C extensions could consumer alot of virtual memory due to thread arena
- Convenient workaround for blocking calls

## ProcessPool

- Easy to terminate
- Consumes a lot of memory
- Process should be created and warmed as soon as possible in order not to copy memory due to `fork()`

## Graceful Shutdown

...
