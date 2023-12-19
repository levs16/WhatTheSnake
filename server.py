import socket
import pickle
from threading import Thread

# Server configuration
server_ip = "127.0.0.1"
server_port = 5555
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((server_ip, server_port))
server.listen()

# Global game state
game_state = {'players': {}}
clients = []

# Function to handle a single client
def handle_client(client_socket, client_id):
    global game_state
    try:
        while True:
            client_data = client_socket.recv(1024)
            if not client_data:
                break

            # Unpickle data and update the global game state
            player_data = pickle.loads(client_data)
            game_state['players'][client_id] = player_data

            # Send updated game state to all clients
            for c in clients:
                try:
                    c.send(pickle.dumps(game_state))
                except socket.error as e:
                    print(f"Error sending data to a client: {e}")

    except Exception as e:
        print(f"Error handling client: {e}")

    finally:
        # Remove the disconnected client
        del game_state['players'][client_id]
        clients.remove(client_socket)
        client_socket.close()

# Main server loop for accepting clients
def server_loop():
    global clients
    client_id = 0
    while True:
        client, addr = server.accept()
        clients.append(client)
        print(f"Connection established: {addr}")
        client_handler = Thread(target=handle_client, args=(client, client_id))
        client_handler.start()
        client_id += 1

# Start the server loop in a separate thread
server_thread = Thread(target=server_loop)
server_thread.start()

# Keep the main thread running to maintain the server
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Server shutting down...")
finally:
    server.close()
