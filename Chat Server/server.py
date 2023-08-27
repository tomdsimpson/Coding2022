# Python chat server
# 23/10/22

import threading
import socket

# Setting up socket
PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# Server code

clients = set()
clients_lock = threading.Lock() # Lock ensures that one thread modifies at once

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} Connected")

    try: # Lots of potential disconnect errors to catch
        connected = True
        while connected:
            
            msg = conn.recv(1024).decode(FORMAT)
            
            if not msg: #Error sending
                break

            if msg == DISCONNECT_MESSAGE:
                connected = False
                print(f"[Disconected] [{addr}]")
                break

            print(f"[{addr}] {msg}")
            with clients_lock:
                for c in clients:
                    c.sendall(f"{msg}".encode(FORMAT))
    
    finally:
        with clients_lock:
            clients.remove(conn)
        conn.close()

def start():
    print("[SERVER STARTED]")
    server.listen()
    while True:
        conn, addr = server.accept()
        
        with clients_lock:
            clients.add(conn)

        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

start()
