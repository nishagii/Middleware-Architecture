import socket
import sys


def start_server(port):
    """Starts the server application."""
    server_socket = None
    try:
        # 1. Create a TCP/IP socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1
        )  # Allows reuse of the address

        # 2. Bind the socket to the port
        server_address = ("0.0.0.0", port)  # Listen on all available interfaces
        print(f"Starting up server on {server_address[0]} port {server_address[1]}")
        server_socket.bind(server_address)

        # 3. Listen for incoming connections
        server_socket.listen(
            1
        )  # Allow one client connection at a time for this basic example

        while True:
            print("\nWaiting for a connection...")
            connection, client_address = server_socket.accept()
            try:
                print(f"Connection from {client_address}")

                # 4. Receive data in a loop
                while True:
                    data = connection.recv(1024)  # Receive up to 1024 bytes
                    if data:
                        decoded_data = data.decode("utf-8").strip()
                        print(f"Received from {client_address}: {decoded_data}")
                        if decoded_data.lower() == "terminate":
                            print(f"Client {client_address} requested termination.")
                            break  # Exit inner loop, close connection
                    else:
                        print(f"No more data from {client_address}, disconnecting.")
                        break  # No data, client disconnected

            finally:
                # Clean up the connection
                print(f"Closing connection from {client_address}")
                connection.close()

    except Exception as e:
        print(f"Server error: {e}")
    finally:
        if server_socket:
            print("Server shutting down.")
            server_socket.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python my_server_app.py <PORT>")
        sys.exit(1)
    try:
        port = int(sys.argv[1])
        if not (1024 <= port <= 65535):  # Common range for user-defined ports
            print("Port number must be between 1024 and 65535.")
            sys.exit(1)
        start_server(port)
    except ValueError:
        print("Invalid port number. Please provide an integer.")
        sys.exit(1)
