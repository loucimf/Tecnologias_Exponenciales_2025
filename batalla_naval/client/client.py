
import socket

def discover_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client_socket.settimeout(5)  

    message = b"DISCOVER_SERVER_REQUEST"
    network_broadcast_adress = "<broadcast>"

    try: 
        client_socket.sendto(message, (network_broadcast_adress, 50000))

        while True:
            try:
                data, adress = client_socket.recvfrom(1024)
                print(f"Received message: {data.decode()} from {adress}")
                break
            except socket.timeout:
                print("No response from server, retrying...")
                break
    finally:
        client_socket.close()
        print("Client socket closed.")

discover_server()