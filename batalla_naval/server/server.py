import socket

TCP_PORT: int = 60000
UDP_PORT: int = 50000

def start_server():  
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
    udp_socket.bind(('', UDP_PORT))

    print("Server is listening for UPD broadcast messages..")

    client_ip = None

    while True:  
        message, address = udp_socket.recvfrom(1024)  
        print(f"Received message: {message.decode()} from {address}")

        decoded_message = message.decode()

        if decoded_message != "DISCOVER_SERVER_REQUEST":
            print("Message is not the same")

        if message.decode() == "DISCOVER_SERVER_REQUEST":  
            client_ip = address

            udp_socket.sendto(b"DISCOVER_SERVER_RESPONSE", client_ip)  
            print("Sent response to client")  
            establish_tcp_conn(client_ip)


def establish_tcp_conn(client_ip):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
        tcp_socket.bind(("", TCP_PORT))
        tcp_socket.listen()

        print(f"Listening for TCP connections on port 60000")

        conn, addr = tcp_socket.accept()

        while conn: 
            print(f"Connection OK with {addr}")
            while True:
                data = conn.recv(1024)
                if (not data):
                    break
                print(f"Received from client: {data.decode()}")
                conn.sendall(data.upper())



start_server()
