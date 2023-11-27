import socket
import threading
import pickle
from flask import Flask, render_template

# Flask configuration
app = Flask(__name__)

# Define constants
SERVER_IP = "127.0.0.1"
SERVER_PORT = 5555
BUFFER_SIZE = 2048

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen()

# List to store client connections
clients = []


def handle_client(client_socket, player_id):
    global clients

    while True:
        try:
            # Receive player input from the client
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                break

            # Deserialize the received data
            player_input = pickle.loads(data)

            # Broadcast the player input to all clients
            for client in clients:
                if client != client_socket:
                    try:
                        # Serialize and send the player input
                        client.sendall(pickle.dumps((player_id, player_input)))
                    except socket.error:
                        # Remove disconnected clients
                        clients.remove(client)

        except Exception as e:
            print(f"Error handling client: {e}")
            break

    # Remove the disconnected client
    clients.remove(client_socket)
    client_socket.close()


# Flask route for the web interface
@app.route('/')
def index():
    return render_template('index.html')


# Accept incoming connections
def accept_connections():
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")

        # Assign a player ID to the client
        player_id = len(clients)
        clients.append(client_socket)

        # Create a thread to handle the client
        client_handler = threading.Thread(target=handle_client, args=(client_socket, player_id))
        client_handler.start()


if __name__ == '__main__':
    # Start a separate thread to handle connections
    connection_thread = threading.Thread(target=accept_connections)
    connection_thread.start()

    # Run the Flask app
    app.run(debug=True, port=SERVER_PORT)
