import socket
import sys
import threading
import time  # For slight delays if needed

# List to keep track of all connected clients and their roles
# Each entry will be a dictionary: {'socket': conn, 'address': addr, 'role': role_str}
connected_clients = []
client_lock = threading.Lock()  # Lock to protect access to connected_clients list


def handle_client(conn, addr):
    """
    Handles a single client connection in a separate thread.
    Receives initial role, then processes messages based on role.
    """
    print(f"[SERVER] Handling new connection from {addr}")
    client_role = None

    try:
        # First message from client should be its role (PUBLISHER/SUBSCRIBER)
        role_data = conn.recv(1024)
        if role_data:
            client_role = role_data.decode("utf-8").strip().upper()
            if client_role not in ["PUBLISHER", "SUBSCRIBER"]:
                print(
                    f"[SERVER] Invalid role '{client_role}' from {addr}. Disconnecting."
                )
                return  # Disconnect invalid clients
            print(f"[SERVER] Client {addr} identified as {client_role}")

            # Add client to our global list
            with client_lock:
                connected_clients.append(
                    {"socket": conn, "address": addr, "role": client_role}
                )
            print(f"[SERVER] Current active clients: {len(connected_clients)}")

            while True:
                data = conn.recv(1024)
                if data:
                    message = data.decode("utf-8").strip()
                    print(f"[SERVER] Received from {addr} ({client_role}): {message}")

                    if message.lower() == "terminate":
                        print(
                            f"[SERVER] Client {addr} ({client_role}) requested termination."
                        )
                        break  # Exit loop, clean up connection

                    if client_role == "PUBLISHER":
                        # If this client is a Publisher, echo message to all Subscribers
                        print(
                            f"[SERVER] Broadcasting message from PUBLISHER {addr} to Subscribers..."
                        )
                        subscribers_count = 0
                        with client_lock:
                            for client in connected_clients:
                                if (
                                    client["role"] == "SUBSCRIBER"
                                    and client["socket"] != conn
                                ):  # Don't send back to self if somehow subscriber (safety)
                                    try:
                                        # Prefix message to indicate it's a published message
                                        published_msg = f"[PUBLISHED] {message}"
                                        client["socket"].sendall(
                                            published_msg.encode("utf-8")
                                        )
                                        subscribers_count += 1
                                    except BrokenPipeError:
                                        print(
                                            f"[SERVER] Subscriber {client['address']} pipe broken, will be removed."
                                        )
                                        # Mark for removal or remove directly (careful with iteration)
                                    except Exception as e:
                                        print(
                                            f"[SERVER] Error sending to subscriber {client['address']}: {e}"
                                        )
                        print(
                            f"[SERVER] Message sent to {subscribers_count} subscriber(s)."
                        )
                else:
                    # Client disconnected without sending "terminate"
                    print(
                        f"[SERVER] Client {addr} ({client_role}) disconnected unexpectedly."
                    )
                    break

    except ConnectionResetError:
        print(f"[SERVER] Client {addr} ({client_role}) forcibly closed the connection.")
    except Exception as e:
        print(f"[SERVER] Error handling client {addr}: {e}")
    finally:
        # Remove client from global list and close socket
        if conn in [c["socket"] for c in connected_clients]:  # Check if still in list
            with client_lock:
                # Find and remove the correct client entry
                connected_clients[:] = [
                    c for c in connected_clients if c["socket"] != conn
                ]
                print(
                    f"[SERVER] Removed {addr} ({client_role}). Active clients: {len(connected_clients)}"
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
