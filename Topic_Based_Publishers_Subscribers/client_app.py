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
                # Print received message clearly, ensuring it doesn't interfere with input prompt
                sys.stdout.write(f"\n[RECEIVED] {message}\n")
                sys.stdout.write("Enter message (type 'terminate' to exit): ")
                sys.stdout.flush()
            else:
                # Server disconnected or no more data
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


def start_client(server_ip, server_port, client_role, client_topic):
    """Starts the client application as a Publisher or Subscriber with a specific topic."""
    client_socket = None
    client_role = client_role.upper()  # Normalize role
    client_topic = client_topic.upper()  # Normalize topic

    if client_role not in ["PUBLISHER", "SUBSCRIBER"]:
        print(
            f"[CLIENT] Invalid client role: {client_role}. Must be PUBLISHER or SUBSCRIBER."
        )
        sys.exit(1)
    if not client_topic:
        print("[CLIENT] Topic cannot be empty. Please provide a topic.")
        sys.exit(1)

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (server_ip, server_port)

        print(
            f"[CLIENT] Connecting to {server_address[0]} port {server_address[1]} as {client_role} on TOPIC: {client_topic}..."
        )
        client_socket.connect(server_address)

        # Send the role and topic to the server immediately after connecting
        initial_info = f"{client_role}:{client_topic}"
        client_socket.sendall(initial_info.encode("utf-8"))
        print(
            f"[CLIENT] Connected successfully as {client_role} on TOPIC: {client_topic}."
        )

        receiver_thread = None
        if client_role == "SUBSCRIBER":
            # For subscribers, start a separate thread to receive messages
            receiver_thread = threading.Thread(
                target=receive_messages, args=(client_socket,)
            )
            receiver_thread.daemon = True  # Allow main thread to exit
            receiver_thread.start()

        # Main loop for sending messages (prepending topic for Publishers) or termination signal
        while True:
            user_input = input("Enter message (type 'terminate' to exit): ")

            if (
                not user_input.strip() and user_input.lower() != "terminate"
            ):  # Don't send empty messages unless it's terminate
                continue

            message_to_send = user_input
            if client_role == "PUBLISHER" and user_input.lower() != "terminate":
                # For publishers, prepend the topic to the message content
                message_to_send = f"{client_topic}:{user_input}"

            encoded_message = message_to_send.encode("utf-8")
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
        # The receiver thread for SUBSCRIBERS will naturally exit when the socket is closed or server disconnects.


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python client_app.py <Server IP> <Server PORT> <ROLE> <TOPIC>")
        print("Roles: PUBLISHER or SUBSCRIBER")
        print("Topics: Any string (e.g., NEWS, WEATHER, SPORTS)")
        sys.exit(1)
    try:
        server_ip = sys.argv[1]
        server_port = int(sys.argv[2])
        client_role = sys.argv[3]
        client_topic = sys.argv[4]

        if not (1024 <= server_port <= 65535):
            print("Server port number must be between 1024 and 65535.")
            sys.exit(1)

        start_client(server_ip, server_port, client_role, client_topic)
    except ValueError:
        print("Invalid server port number. Please provide an integer.")
        sys.exit(1)
