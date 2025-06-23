# Middleware Architectures - Assignment 01: Publish/Subscribe Middleware

This repository contains the implementation for **Assignment 01** of the Middleware Architectures course (`IS3108 / SCS3203`), focusing on a simple **Publish/Subscribe middleware** using client-server socket programming.

---

## 🧩 Task 1: The Client-Server Application

### 🎯 Objective

Implement a basic client-server socket application where:
- The **client sends text** to the server.
- The **server displays** the received message.
- The client **disconnects and terminates** upon typing the keyword `"terminate"`.

---

### 🛠️ Language

- **Python**

---

## 📁 Project Structure (Task 1)

| File Name       | Description                     |
|-----------------|---------------------------------|
| `server_app.py` | The server-side application     |
| `client_app.py` | The client-side application     |

---

## ▶️ How to Run

### Step 1: Start the Server (Terminal 1)

1. Open a terminal.
2. Navigate to the directory containing `server_app.py`.
3. Run the server with a port number:

```bash
python server_app.py <PORT> 
```

### Step 2: Start the Client (Terminal 2)
Open another terminal.

1.Navigate to the directory containing my_client_app.py.
2.Run the client by specifying the server IP and port:

```bash
python my_client_app.py <SERVER_IP> <SERVER_PORT>
```

Example (for localhost):
```bash
python my_client_app.py 127.0.0.1 5000
```

Expected Output:

Connecting to 127.0.0.1 port 5000
Enter message (type 'terminate' to exit):

## 💬 Interaction
In the client terminal, type any message and press Enter.
The server terminal will display the received message.

## 🔚 To Terminate:
Type terminate (case-insensitive) in the client and press Enter.
The client will disconnect.

The server will show that the connection has closed and wait for new connections.


