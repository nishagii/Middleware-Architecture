import socket
import sys


def start_client(server_ip, server_port):
    """Starts the client application."""
    client_socket = None
    try:
        # 1. Create a TCP/IP socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 2. Connect the socket to the server's address and port
        server_address = (server_ip, server_port)
        print(f"Connecting to {server_address[0]} port {server_address[1]}")
        client_socket.connect(server_address)

        while True:
            message = input("Enter message (type 'terminate' to exit): ")
            encoded_message = message.encode("utf-8")
            client_socket.sendall(encoded_message)

            if message.lower() == "terminate":
                print("Client terminating.")
                break

    except ConnectionRefusedError:
        print(
            f"Error: Connection refused. Is the server running on {server_ip}:{server_port}?"
        )
    except socket.gaierror:
        print(f"Error: Could not resolve server IP address '{server_ip}'.")
    except Exception as e:
        print(f"Client error: {e}")
    finally:
        if client_socket:
            print("Closing client socket.")
            client_socket.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python my_client_app.py <Server IP> <Server PORT>")
        sys.exit(1)
    try:
        server_ip = sys.argv[1]
        server_port = int(sys.argv[2])
        if not (1024 <= server_port <= 65535):
            print("Server port number must be between 1024 and 65535.")
            sys.exit(1)
        start_client(server_ip, server_port)
    except ValueError:
        print("Invalid server port number. Please provide an integer.")
        sys.exit(1)
