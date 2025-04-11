
import socket

TCP_PORT: int = 60000
UDP_PORT: int = 50000

def discover_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client_socket.settimeout(5)  

    message = b"DISCOVER_SERVER_REQUEST"
    network_broadcast_adress = "<broadcast>"
    server_ip = None

    try: 
        client_socket.sendto(message, (network_broadcast_adress, UDP_PORT))

        while True:
            try:
                data, adress = client_socket.recvfrom(1024)
                print(f"Received message: {data.decode()} from {adress}")

                if (data.decode() == "DISCOVER_SERVER_RESPONSE"):
                    server_ip = adress[0]
                break
            except socket.timeout:
                print("No response from server, retrying...")
                break
    finally:
        client_socket.close()
        print("Client socket closed.")

    if server_ip:
        tcp_connect(server_ip)
    else:
        print("No server_ip found:", server_ip)


def tcp_connect(server_ip):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:

        tcp_socket.connect((server_ip, TCP_PORT))
        print(f"Connected to server at {server_ip}")

        while True:
            try:
                message = input("Message to send: ")
                tcp_socket.sendall(message.encode())
                data = tcp_socket.recv(1024)
                print(f"Received from server: {data.decode()}")
            except KeyboardInterrupt:
                print("Closing connection")
                break



discover_server()