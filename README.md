# Distributed Systems - Unit 1

## Project Overview

This project implements a concurrent networked server using raw TCP sockets in Python.

The server provides four operations:

- `PUT` - stores a key-value pair
- `GET` - retrieves a value
- `ENQUEUE` - adds a task to a queue
- `DEQUEUE` - removes a task from a queue

The project uses a custom length-prefixed protocol where each message contains a 4-byte length header followed by a UTF-8 encoded JSON message.

The server uses a thread pool to handle multiple clients concurrently. A lock protects the shared key-value store, while a condition variable is used to coordinate access to the task queue.

## Project Structure

```text
Distributed Systems/
├── .devcontainer/
│   └── devcontainer.json
├── protocol.py
├── storage.py
├── server.py
├── client_stress_test.py
└── README.md
```

### File Descriptions

- `protocol.py` - Handles message framing, JSON encoding and decoding, and partial TCP reads.
- `storage.py` - Contains the thread-safe key-value store and condition-backed task queue.
- `server.py` - Runs the TCP server and handles client requests using a 20-worker thread pool.
- `client_stress_test.py` - Creates 20 concurrent clients to test the server.
- `README.md` - Contains project documentation and instructions.
- `.devcontainer/devcontainer.json` - Contains the development container configuration.

## Protocol

The server communicates using TCP on port `9090`.

Each message uses the following format:

```text
[4-byte big-endian unsigned length][UTF-8 JSON payload]
```

The 4-byte header tells the receiver how many bytes are contained in the JSON payload.

The protocol supports four actions:

| Action | Purpose |
|---|---|
| `PUT` | Store a key-value pair |
| `GET` | Retrieve a value using a key |
| `ENQUEUE` | Add a task to the task queue |
| `DEQUEUE` | Remove a task from the task queue |

The `recv_exact()` function handles TCP stream fragmentation by continuing to receive data until the required number of bytes has been collected.

## Concurrency and Synchronization

The server uses `ThreadPoolExecutor` with a maximum of 20 worker threads. This allows multiple client connections to be processed concurrently.

The key-value store uses `threading.Lock` to protect shared data from concurrent access.

The task queue uses `threading.Condition`. When the queue is empty, a worker waits until another client adds a task. When a task is added, `notify()` wakes a waiting worker.

This prevents multiple threads from modifying shared data at the same time and demonstrates mutual exclusion and condition-variable synchronization.

## Running the Server

Make sure Python 3 is installed.

Start the server with:

```bash
python3 server.py
```

The server should display:

```text
Server listening on port 9090
```

The server listens for TCP connections on port `9090`.

## Running the Stress Test

With the server running, open another terminal and run:

```bash
python3 client_stress_test.py
```

The stress test creates 20 clients using a thread pool.

A successful test produces results similar to:

```text
Client 0: {'status': 'OK'}
Client 1: {'status': 'OK'}
Client 2: {'status': 'OK'}
...
Client 19: {'status': 'OK'}
```

All 20 clients should receive an `OK` response.

## Testing the Task Queue

An `ENQUEUE` request can be tested with:

```bash
python3 -c "import socket; from protocol import send_frame, recv_frame; s=socket.socket(); s.connect(('127.0.0.1',9090)); send_frame(s, {'action':'ENQUEUE','task':'test_task'}); print(recv_frame(s)); s.close()"
```

Expected result:

```text
{'status': 'OK'}
```

A `DEQUEUE` request can then be tested with:

```bash
python3 -c "import socket; from protocol import send_frame, recv_frame; s=socket.socket(); s.connect(('127.0.0.1',9090)); send_frame(s, {'action':'DEQUEUE'}); print(recv_frame(s)); s.close()"
```

Expected result:

```text
{'task': 'test_task'}
```

## Testing GET

The stress test stores values using `PUT`. A stored value can be retrieved using `GET`.

For example:

```bash
python3 -c "import socket; from protocol import send_frame, recv_frame; s=socket.socket(); s.connect(('127.0.0.1',9090)); send_frame(s, {'action':'GET','key':'client_5'}); print(recv_frame(s)); s.close()"
```

Expected result:

```text
{'value': 'value_5'}
```

## Test Results

The following tests were successfully completed:

- `PUT` operation - Passed
- `GET` operation - Passed
- `ENQUEUE` operation - Passed
- `DEQUEUE` operation - Passed
- Custom TCP message framing - Passed
- Partial TCP reads using `recv_exact()` - Implemented
- Thread-safe key-value storage - Passed
- Condition-backed task queue - Passed
- 20 concurrent clients - Passed
- 20-worker thread pool - Passed

The stress test successfully completed with all 20 clients receiving:

```text
{'status': 'OK'}
```

## Technologies Used

- Python 3
- TCP sockets
- JSON
- POSIX-style socket programming
- `threading.Lock`
- `threading.Condition`
- `ThreadPoolExecutor`
- `collections.deque`
