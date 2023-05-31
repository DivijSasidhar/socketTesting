import socket

# https://realpython.com/python-sockets/

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65535  # Port to listen on

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)  # will receive at most 1024 bytes (if empty byte will break loop)
            if not data:
                break
            conn.sendall(data)
