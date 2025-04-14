from game_client import *

def main():
    player_name = input("Cual es tu nombre? ")
    game_client = GameClient("", TCP_PORT, player_name)

    # UDP
    game_client.discover_srvr()

    # TCP
    game_client.connect_to_srvr()

    if game_client.connected:
        game_client.setup_boats_no_validation()
        game_client.play_turn()
    else:
        print("Failed to connect to server.")

if __name__ == "__main__":
    main()
