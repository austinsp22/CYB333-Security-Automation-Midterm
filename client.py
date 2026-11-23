import socket

# Server connection settings.
HOST = "127.0.0.1"
PORT = 5000


def start_client():
    try:
        # Create a TCP socket and connect to the server.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.settimeout(5)
            client.connect((HOST, PORT))

            print(f"Connected to server at {HOST}:{PORT}")
            print("Type a message or 'exit' to disconnect.")

            while True:
                # Get a message from the user.
                message = input("You: ")

                if not message:
                    print("Please enter a message.")
                    continue

                # Send the message to the server.
                client.sendall(message.encode("utf-8"))

                # Receive the server's response.
                response = client.recv(1024)

                if not response:
                    print("Server closed the connection.")
                    break

                print(f"Server: {response.decode('utf-8')}")

                # Exit after receiving the goodbye message.
                if message.lower() == "exit":
                    print("Disconnecting from server...")
                    break

    except ConnectionRefusedError:
        print("Connection failed: Server is not running.")

    except socket.timeout:
        print("Connection timed out.")

    except OSError as error:
        print(f"Connection error: {error}")

    finally:
        print("Client shutdown complete.")


if __name__ == "__main__":
    start_client()
