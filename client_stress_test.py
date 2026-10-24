import socket 
from concurrent.futures import ThreadPoolExecutor

from protocol import recv_frame, send_frame

def test_client(client_id):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", 9090))

    send_frame(sock, {
        "action": "PUT",
        "key": f"client_{client_id}",
        "value": f"value_{client_id}"
    })

    response = recv_frame(sock)

    sock.close()

    return response

def main():
    with ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(test_client, range(20)))

    for i, result in enumerate(results):
        print(f"Client {i}: {result}")

if __name__ == "__main__":
    main()
