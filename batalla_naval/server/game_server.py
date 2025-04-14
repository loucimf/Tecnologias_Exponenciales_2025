import socket
import threading
from server_config import *  # Ensure this imports relevant configurations like DISCOVER_MESSAGE, DISCOVER_RESPONSE, etc.

class GameServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []  # To store client connection information

    def setup_client_connections(self):
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udp_socket.bind((self.host, UDP_PORT))

        print("Server is listening for UDP broadcast messages...")

        while True:
            message, address = udp_socket.recvfrom(1024)
            print(f"Received message: {message.decode()} from {address}")
            if message.decode() == DISCOVER_MESSAGE:
                udp_socket.sendto(DISCOVER_RESPONSE, address)
                print(f"Sent response to {address}")

    def establish_tcp_connection(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

        print(f"Server started on {self.host}:{self.port}")

        while len(self.clients) < 1:  
            conn, addr = self.server_socket.accept()
            client = {
                "player": len(self.clients) + 1,
                "addr": addr, 
                "socket": conn, 
                "name": ""
            }
            self.clients.append(client)
            print(f"Client connected: {addr}")

            client_thread = threading.Thread(target=self.manage_client, args=(client,))
            client_thread.start()

        print("Enough clients connected to the srvr")

    def extract_coords(self, msg: str):
        raw_number = int(msg[1])
        letter = msg[0]
        return [letter, raw_number]
    
    def get_opposing_client(self, current_client):
        for client in self.clients:
            if (client != current_client):
                return client
            return client # just for testing

    def manage_client(self, client):
        conn = client["socket"]
        opposing_client = self.get_opposing_client(client)
        try:
            while True:
                message: str = conn.recv(1024).decode()
                if not message:
                    break 

                print(f"Received from {client['addr']}: {message}")

                if message.startswith("NAME"):
                    name = message.split()[1]
                    client["name"] = name
                    self.send_to_client(f"WELCOME {name}!", client)

                if message.startswith("CLIENT_RES"):
                    print("A response from the opposing client arrived")
                    info = message.split()[1]
                    self.send_to_client(f"{info}", client)

                if message.startswith("ATTACK"):
                    string_coords = message.split()[1]
                    coord = self.extract_coords(string_coords)
                    self.send_to_client(f"GAME_UPDATE {coord[0]}{coord[1]}", opposing_client)
                    
                

        except Exception as e:
            print(f"Error communicating with {client['addr']}: {e}")
        finally:
            print(f"Closing connection with {client['addr']}")
            conn.close()

    def send_to_client(self, message, client):
        try:
            client["socket"].sendall(message.encode())
            print("Sending a msg to client")
        except Exception as e:
            print(f"Error sending to {client['addr']}: {e}")

    def broadcast(self, message):
        for client in self.clients:
            self.send_to_client(message, client)

    def run_server(self):
        discovery_thread = threading.Thread(target=self.setup_client_connections)
        discovery_thread.start()
        self.establish_tcp_connection()

            

