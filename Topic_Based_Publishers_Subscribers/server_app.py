import socket
import sys
import threading
import time

# List to keep track of all connected clients and their roles/topics
# Each entry will be a dictionary: {'socket': conn, 'address': addr, 'role': role_str, 'topic': topic_str}
connected_clients = []
client_lock = threading.Lock()  # Lock to protect access to connected_clients list


def handle_client(conn, addr):
    # IMPORTANT: Declare global variable at the very beginning of the function
    # if it's going to be assigned to later in the function.
    global connected_clients
    """
    Handles a single client connection in a separate thread.
    Receives initial role and topic, then processes messages based on role and topic.
    """
    print(f"[SERVER] Handling new connection from {addr}")
    client_role = None
    client_topic = None

    try:
        # First message from client should be its role and topic (e.g., "PUBLISHER:TOPIC_A")
        initial_data = conn.recv(1024)
        if initial_data:
            initial_info = initial_data.decode("utf-8").strip()
            parts = initial_info.split(":", 1)  # Split only on the first colon

            if len(parts) == 2:
                client_role = parts[0].upper()
                client_topic = parts[1].upper()  # Normalize topic to uppercase
            else:
                print(
                    f"[SERVER] Invalid initial format '{initial_info}' from {addr}. Disconnecting."
                )
                return  # Disconnect invalid clients

            if client_role not in ["PUBLISHER", "SUBSCRIBER"] or not client_topic:
                print(
                    f"[SERVER] Invalid role '{client_role}' or topic '{client_topic}' from {addr}. Disconnecting."
                )
                return  # Disconnect invalid clients

            print(
                f"[SERVER] Client {addr} identified as {client_role} on TOPIC: {client_topic}"
            )

            # Add client to our global list
            with client_lock:
                connected_clients.append(
                    {
                        "socket": conn,
                        "address": addr,
                        "role": client_role,
                        "topic": client_topic,
                    }
                )
            print(f"[SERVER] Current active clients: {len(connected_clients)}")

            while True:
                data = conn.recv(1024)
                if data:
                    message_raw = data.decode("utf-8").strip()
                    print(
                        f"[SERVER] Received from {addr} ({client_role}, {client_topic}): {message_raw}"
                    )

                    if message_raw.lower() == "terminate":
                        print(
                            f"[SERVER] Client {addr} ({client_role}, {client_topic}) requested termination."
                        )
                        break  # Exit loop, clean up connection

                    if client_role == "PUBLISHER":
                        # Publishers send messages with their topic prefixed: "TOPIC:MESSAGE_CONTENT"
                        # Extract the topic and content from the incoming message
                        msg_parts = message_raw.split(":", 1)
                        if len(msg_parts) == 2:
                            published_topic = msg_parts[0].upper()
                            published_content = msg_parts[1]
                            print(
                                f"[SERVER] PUBLISHER {addr} publishing on '{published_topic}': '{published_content}'"
                            )

                            subscribers_count = 0
                            with client_lock:
                                for client in connected_clients:
                                    # Forward message only to SUBSCRIBERS on the matching topic
                                    if (
                                        client["role"] == "SUBSCRIBER"
                                        and client["topic"] == published_topic
                                    ):
                                        try:
                                            # Format message for subscribers to see the topic
                                            full_message = f"[PUBLISHED - {published_topic}] {published_content}"
                                            client["socket"].sendall(
                                                full_message.encode("utf-8")
                                            )
                                            subscribers_count += 1
                                        except BrokenPipeError:
                                            print(
                                                f"[SERVER] Subscriber {client['address']} pipe broken, will be removed soon."
                                            )
                                        except Exception as e:
                                            print(
                                                f"[SERVER] Error sending to subscriber {client['address']} on topic {client['topic']}: {e}"
                                            )
                            print(
                                f"[SERVER] Message sent to {subscribers_count} subscriber(s) for topic '{published_topic}'."
                            )
                        else:
                            print(
                                f"[SERVER] Warning: Malformed message from PUBLISHER {addr}: '{message_raw}'. Not routed."
                            )
                else:
                    # Client disconnected without sending "terminate"
                    print(
                        f"[SERVER] Client {addr} ({client_role}, {client_topic}) disconnected unexpectedly."
                    )
                    break

    except ConnectionResetError:
        print(
            f"[SERVER] Client {addr} ({client_role}, {client_topic}) forcibly closed the connection."
        )
    except Exception as e:
        print(f"[SERVER] Error handling client {addr}: {e}")
    finally:
        # Remove client from global list and close socket
        with client_lock:
            # Rebuild the connected_clients list excluding the disconnected client
            connected_clients = [c for c in connected_clients if c["socket"] != conn]
            print(
                f"[SERVER] Removed {addr} ({client_role}, {client_topic}). Active clients: {len(connected_clients)}"
            )
        conn.close()
        print(f"[SERVER] Connection to {addr} closed.")


def start_server(port):
    """Starts the server application, listening for connections."""
    server_socket = None
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1
        )  # Allows reuse of the address

        server_address = ("0.0.0.0", port)
        print(
            f"[SERVER] Starting up server on {server_address[0]} port {server_address[1]}"
        )
        server_socket.bind(server_address)
        server_socket.listen(5)  # Allow up to 5 pending connections

        while True:
            print("\n[SERVER] Waiting for a connection...")
            conn, addr = server_socket.accept()
            # Start a new thread to handle the client
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.daemon = (
                True  # Allow main thread to exit even if client threads are running
            )
            client_thread.start()

    except Exception as e:
        print(f"[SERVER] Server error: {e}")
    finally:
        if server_socket:
            print("[SERVER] Server shutting down.")
            server_socket.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python server_app.py <PORT>")
        sys.exit(1)
    try:
        port = int(sys.argv[1])
        if not (1024 <= port <= 65535):
            print("Port number must be between 1024 and 65535.")
            sys.exit(1)
        start_server(port)
    except ValueError:
        print("Invalid port number. Please provide an integer.")
        sys.exit(1)
