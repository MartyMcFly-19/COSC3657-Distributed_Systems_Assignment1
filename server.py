import socket
from concurrent.futures import ThreadPoolExecutor

from protocol import recv_frame, send_frame
from storage import KeyValueStore, TaskQueue

store = KeyValueStore()
tasks = TaskQueue()

def handle_client(conn):
    while True:
        try:
            request = recv_frame(conn)
        except ConnectionError:
            break

        action = request .get("action")

        if action == "PUT":
            store.put(request["key"], request["value"])
            send_frame(conn, {"status": "OK"})

        elif action == "GET":
            value = store.get(request["key"])
            send_frame(conn, {"value": value})
        
        elif action == "ENQUEUE":
            tasks.enqueue(request["task"])
            send_frame(conn, {"status": "OK"})

        elif action == "DEQUEUE":
            task = tasks.dequeue()
            send_frame(conn, {"task": task})

    conn.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind(("0.0.0.0", 9090))
    server.listen()

    print("Server listening on port 9090")

    with ThreadPoolExecutor(max_workers=20) as executor:
        while True:
            conn, address = server.accept()

            print(f"Client connected: {address}")

            executor.submit(handle_client, conn)

if __name__ == "__main__":
    main()
