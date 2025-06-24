import socket
import sys
import threading
import time


def receive_messages(client_socket):
    """
    Function for a subscriber client to continuously receive messages from the server.
    Runs in a separate thread.
    """
    while True:
        try:
            data = client_socket.recv(1024)
            if data:
                message = data.decode("utf-8").strip()
                # Print received message clearly, especially for subscribers
                print(
                    f"\n[RECEIVED] {message}\nEnter message (type 'terminate' to exit): ",
                    end="",
                    flush=True,
                )
            else:
                # Server disconnected
                print("\n[CLIENT] Server disconnected. Exiting receiver thread.")
                break
        except ConnectionResetError:
            print(
                "\n[CLIENT] Server closed the connection unexpectedly. Exiting receiver thread."
            )
            break
        except Exception as e:
            print(f"\n[CLIENT] Error in receiver thread: {e}. Exiting.")
            break
    # Signal the main thread that receiver is done (if needed for graceful shutdown)


def start_client(server_ip, server_port, client_role):
    """Starts the client application as a Publisher or Subscriber."""
    client_socket = None
    client_role = client_role.upper()  # Normalize role to uppercase

    if client_role not in ["PUBLISHER", "SUBSCRIBER"]:
        print(
            f"[CLIENT] Invalid client role: {client_role}. Must be PUBLISHER or SUBSCRIBER."
        )
        sys.exit(1)

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (server_ip, server_port)

        print(
            f"[CLIENT] Connecting to {server_address[0]} port {server_address[1]} as {client_role}..."
        )
        client_socket.connect(server_address)

        # Send the role to the server immediately after connecting
        client_socket.sendall(client_role.encode("utf-8"))
        print(f"[CLIENT] Connected successfully as {client_role}.")

        receiver_thread = None
        if client_role == "SUBSCRIBER":
            # For subscribers, start a separate thread to receive messages
            receiver_thread = threading.Thread(
                target=receive_messages, args=(client_socket,)
            )
            receiver_thread.daemon = True  # Allow main thread to exit
            receiver_thread.start()

        # Main loop for sending messages (for Publishers) or termination signal
        while True:
            user_input = input("Enter message (type 'terminate' to exit): ")

            if not user_input.strip():  # Don't send empty messages
                continue

            encoded_message = user_input.encode("utf-8")
            client_socket.sendall(encoded_message)

            if user_input.lower() == "terminate":
                print("[CLIENT] Termination command sent. Disconnecting.")
                break  # Exit sending loop

            # Add a small delay for better readability in rapid message exchanges
            # time.sleep(0.1)

    except ConnectionRefusedError:
        print(
            f"[CLIENT] Error: Connection refused. Is the server running on {server_ip}:{server_port}?"
        )
    except socket.gaierror:
        print(f"[CLIENT] Error: Could not resolve server IP address '{server_ip}'.")
    except Exception as e:
        print(f"[CLIENT] An unexpected error occurred: {e}")
    finally:
        if client_socket:
            print("[CLIENT] Closing client socket.")
            client_socket.close()
        # If there's a receiver thread, it will terminate once the socket is closed or server disconnects.
        # No explicit join needed for daemon threads on program exit.


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python client_app.py <Server IP> <Server PORT> <ROLE>")
        print("Roles: PUBLISHER or SUBSCRIBER")
        sys.exit(1)
    try:
        server_ip = sys.argv[1]
        server_port = int(sys.argv[2])
        client_role = sys.argv[3]

        if not (1024 <= server_port <= 65535):
            print("Server port number must be between 1024 and 65535.")
            sys.exit(1)

        start_client(server_ip, server_port, client_role)
    except ValueError:
        print("Invalid server port number. Please provide an integer.")
        sys.exit(1)
