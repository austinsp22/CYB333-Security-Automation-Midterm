import socket

# Configure the server to listen on localhost.
HOST = "127.0.0.1"
PORT = 5000


def start_server():
    try:
        # Create a TCP socket.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((HOST, PORT))
            server.listen(1)

            print(f"Server listening on {HOST}:{PORT}")
            print("Waiting for a client to connect...")

            # Accept an incoming client connection.
            connection, address = server.accept()

            with connection:
                print(f"Client connected: {address}")

                while True:
                    # Receive a message from the client.
                    data = connection.recv(1024)

                    if not data:
                        print("Client disconnected.")
                        break

                    message = data.decode("utf-8")
                    print(f"Client says: {message}")

                    if message.lower() == "exit":
                        connection.sendall(b"Goodbye!")
                        print("Closing client connection.")
                        break

                    # Send a response back to the client.
                    response = f"Server received: {message}"
                    connection.sendall(response.encode("utf-8"))

    except OSError as error:
        print(f"Server error: {error}")

    finally:
        print("Server shutdown complete.")


if __name__ == "__main__":
    start_server()
