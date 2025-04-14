from game_server import *

game_server = GameServer(HOST, TCP_PORT)

def main():
    game_server.run_server()
    

if (__name__ == "__main__"):
	main()

