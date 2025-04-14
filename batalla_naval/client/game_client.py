import socket
import sys  
import os

# Add parent directory to path to access modules at the project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client_config import *
from config import *
from utils.classes import *
from utils.helper import clone_boats, isSameAbstractCoord

class GameClient:
    def __init__(self, server_ip, server_port: int, player_name: str):
        self.server_ip = server_ip
        self.server_port: int = server_port
        self.socket = None
        self.connected: bool = False
        self.player: Player = Player(Board(BOARD_SIZE), Board(BOARD_SIZE), player_name, clone_boats(), SHOTS)

    def discover_srvr(self):

        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udp_socket.settimeout(5)
        
        try:
            udp_socket.sendto(DISCOVER_MESSAGE, (NETWORK_BROADCAST_ADDR, UDP_PORT))

            while True:
                try:
                    data, address = udp_socket.recvfrom(1024)
                    print(f"Received {data.decode()} from {address}")

                    if (data.decode() == DISCOVER_RESPONSE):
                        self.server_ip = address[0]  
                        print(f"Server IP: {self.server_ip}")
                        break
                except socket.timeout:
                    print("No response from server, retrying...")
                    break

        finally:
            udp_socket.close()
            print("Closed UDP socket.")

    def connect_to_srvr(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.server_ip, self.server_port))
            self.connected = True
            print(f"Connected to server at {self.server_ip}:{self.server_port}")
            
            self.send_message(f"NAME {self.player.name}")
            response = self.receive_message()
            print(response)
        except Exception as e:
            print(f"Unable to connect: {e}")
            self.connected = False

    def send_message(self, message: str):
        if (self.connected):
            try:
                self.socket.sendall(message.encode())
            except Exception as e:
                print(f"Error sending message: {e}")

    def receive_message(self):
        try:
            return self.socket.recv(1024).decode()
        except Exception as e:
            print(f"Error receiving message: {e}")
            return None

    def process_game_update(self, response: str):
        server_message_split = response.split()
        action = server_message_split[1]

        if (action == "GAME_OVER"):
            print("GANASTE!")

        coord = Coordinate(action[0], int(action[1]) - 1)
        print("Coordsssdsdsds:", coord.letter, coord.number)
        hit, target_boat = self.process_opponent_attack(coord)

        if (hit):
            if (target_boat.__isSunk__()):
                print("El enemigo HUNDIO un barco!")
                self.send_message("CLIENT_RES SUNK")
            self.send_message("CLIENT_RES HIT")

    def process_opponent_attack(self, attack: Coordinate):
        x, y = attack.getMatrixPosition()
        for boat in self.player.ships:
            for coord in boat.coords:
                if (isSameAbstractCoord(coord, attack)):
                    input("ENEMY HIT-- Tu oponente acertó un tiro!")
                    boat.hits += 1
                    self.player.board.place_symbol(x, y, "⨷")
                    return True, boat
        print("El enemigo fallo su tiro!")
        self.player.board.place_symbol(x, y, "O")
        return False, None 

    def process_attack_response(self, response: str, coord: Coordinate) -> bool:
        x, y = coord.getMatrixPosition()

        if (response == "ALREADY_SHOT"):
            print("INVALID-- Ya disparaste aquí!")
            return False
        if (response == "OUT_OF_BOUNDS"):
            print("INVALID-- Disparo inválido!")
            return False
        if (response == "HIT"):
            print("HIT-- Le diste a un barco!")
            self.player.attack_board.place_symbol(x, y, "X")
            return True
        if (response == "MISS"):
            print("MISS-- ")
            self.player.attack_board.place_symbol(x, y, "O")
            return True
        
        return True

    def setup_boats(self):
        allBoats = self.player.ships

        for boat in allBoats:
            self.player.board.place_boat(boat, allBoats) 

    def setup_boats_no_validation(self):
        no_validation_paint_symbols(self.player, self.player.ships)


    def play_turn(self):
        while (self.connected):
            try:

                self.player.board.display()
                self.player.attack_board.display()
                move_string = input("Coordenada a atacar, en formato: A1 (LETRANUMERO): ").strip()
                raw_number = int(move_string[1:])
                coord = Coordinate(move_string[0], raw_number)

                # # Ensure move is valid before sending
                # if (not isInBounds(coord, BOARD_SIZE)):
                #     print("Move is out of bounds. Try again.")
                #     continue

                self.send_message(f"ATTACK {coord.letter}{coord.number}")
                response = self.receive_message()

                if (response == "WAIT"):
                    print("Espera a que termine el turno del oponente...")
                    continue
                
                if (not self.process_attack_response(response, coord)):
                    continue
                
                if (response.startswith("GAME_UPDATE")):
                    self.process_game_update(response)
                
                print(response)

            except KeyboardInterrupt:
                print("Saliendo del juego...")
                break
            except Exception as e:
                print(f"Networking error: {e}")
                break
        self.socket.close()
