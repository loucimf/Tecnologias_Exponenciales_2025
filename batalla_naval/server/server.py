import socket

def start_server():  
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
    server_socket.bind(('', 50000))

    print("Server is listening for broadcast messages..")

    while True:  
        message, address = server_socket.recvfrom(1024)  
        print(f"Received message: {message.decode()} from {address}")

        decoded_message = message.decode()

        if decoded_message != "DISCOVER_SERVER_REQUEST":
            print("Message is not the same")

        if message.decode() == "DISCOVER_SERVER_REQUEST":  
            server_socket.sendto(b"Hellooo!", address)  
            print("Sent response to client")  

start_server()
