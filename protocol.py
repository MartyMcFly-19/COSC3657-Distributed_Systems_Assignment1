import socket
import struct
import json

def recv_exact(sock, n):
    data = b""

    while len(data) < n:
        chunk = sock.recv(n - len(data))

        if not chunk:
            raise ConnectionError("Connection closed while receiving data")
        
        data += chunk
    
    return data

def recv_frame(sock):
    header = recv_exact(sock, 4)

    length = struct.unpack("!I", header)[0]

    payload = recv_exact(sock, length)

    return json.loads(payload.decode("utf-8"))

def send_frame(sock, message):
    payload = json.dumps(message).encode("utf-8")

    header = struct.pack("!I", len(payload))

    sock.sendall(header + payload)
