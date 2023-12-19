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
game_state = {'x': 0, 'y': 0, 'snake_list': []}
clients = []

# Function to handle a single client
def handle_client(client_socket):
    global game_state
    try:
        while True:
            client_data = client_socket.recv(1024)
            if not client_data:
                break

            # Unpickle data and update the global game state
            game_state = pickle.loads(client_data)

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
        clients.remove(client_socket)
        client_socket.close()

# Main server loop for accepting clients
def server_loop():
    global clients
    while True:
        client, addr = server.accept()
        clients.append(client)
        print(f"Connection established: {addr}")
        client_handler = Thread(target=handle_client, args=(client,))
        client_handler.start()

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
