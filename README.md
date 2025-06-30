# Middleware Architectures - Assignment 01: Publish/Subscribe Middleware

This repository contains the implementation for **Assignment 01** of the Middleware Architectures course (**IS3108 / SCS3203**), focusing on a simple **Publish/Subscribe middleware** using client-server socket programming.

---

## 🧹 Task 1: The Client-Server Application

### 🌟 Objective
Implement a basic client-server socket application where:

- The client sends text to the server.
- The server displays the received message.
- The client disconnects and terminates upon typing the keyword `terminate`.

### 🛠️ Language
- Python

### 📁 Project Structure (Task 1)
| File Name      | Description             |
|----------------|-------------------------|
| `server_app.py` | The server-side application |
| `client_app.py` | The client-side application |

### ▶️ How to Run (Task 1)

#### Step 1: Start the Server (Terminal 1)
```bash
python server_app.py <PORT>
# Example:
python server_app.py 5000
```
**Expected Output:**
```
Starting up server on 0.0.0.0 port 5000
Waiting for a connection...
```

#### Step 2: Start the Client (Terminal 2)
```bash
python client_app.py <SERVER_IP> <SERVER_PORT>
# Example:
python client_app.py 127.0.0.1 5000
```
**Expected Output:**
```
Connecting to 127.0.0.1 port 5000
Enter message (type 'terminate' to exit):
```

### 💬 Interaction (Task 1)
- Type a message in the client terminal.
- Server displays the received message.

### 🖚️ To Terminate (Task 1)
- Type `terminate` (case-insensitive) in the client and press Enter.
- Client disconnects; server shows connection closed and waits for new clients.

---

## 🧹 Task 2: Publishers and Subscribers

### 🌟 Objective
Enhance the basic implementation to:
- Handle **multiple clients** concurrently.
- Accept a **role** (PUBLISHER or SUBSCRIBER) as a third argument.
- **Echo messages from PUBLISHERS** only to SUBSCRIBERS.

### 🛠️ Language
- Python

### 📁 Project Structure (Task 2)
(Same files as Task 1, updated internally)

### ▶️ How to Run (Task 2)

#### Step 1: Start the Server
```bash
python server_app.py <PORT>
```

#### Step 2: Start Multiple Clients
```bash
python client_app.py <SERVER_IP> <SERVER_PORT> <ROLE>
# Examples:
python client_app.py 127.0.0.1 5000 PUBLISHER
python client_app.py 127.0.0.1 5000 SUBSCRIBER
```

### 💬 Interaction (Task 2)
- PUBLISHER messages are displayed only on SUBSCRIBER clients.
- PUBLISHERS do not receive messages.

### 🖚️ To Terminate
- Type `terminate` in any client.
- Server updates active connections; others stay connected.

---

## 🧹 Task 3: Topic-Based Filtering

### 🌟 Objective
Enhance Task 2 with **topic/subject-based filtering**:
- Clients include a **topic** as a fourth argument.
- Server routes messages to SUBSCRIBERS interested in the same topic.

### 🛠️ Language
- Python

### 📁 Project Structure (Task 3)
(Same files as before)

### ▶️ How to Run (Task 3)
```bash
python client_app.py <SERVER_IP> <SERVER_PORT> <ROLE> <TOPIC>
# Examples:
python client_app.py 127.0.0.1 5000 PUBLISHER NEWS
python client_app.py 127.0.0.1 5000 SUBSCRIBER NEWS
python client_app.py 127.0.0.1 5000 PUBLISHER SPORTS
python client_app.py 127.0.0.1 5000 SUBSCRIBER SPORTS
```

### 💬 Interaction (Task 3)
- SUBSCRIBERS receive only messages for their subscribed topic.
- PUBLISHERS do not receive messages.

### 🖚️ To Terminate
- Type `terminate` in the client terminal to disconnect.

---

## 🧹 Task 4: Improved Architecture for Availability & Reliability

### 🌟 Objective
Propose a **distributed architecture** to address the single point of failure (SPOF).

### ✨ Proposed Architecture: Distributed Broker Cluster with Service Discovery

#### 1. Architecture Components:

**Clients (Publishers & Subscribers)**
- Query a central **Service Discovery** component to find available brokers.
- Automatically reconnect to another broker if current one fails.

**Message Brokers (Broker A, B, C)**
- Accept connections, manage topics, route messages.
- Share load across the cluster.

**Service Discovery (e.g., ZooKeeper, etcd)**
- Brokers register themselves here.
- Clients get broker lists.
- Handles broker health checks.

#### 2. Benefits:

- **No SPOF**: If one broker fails, clients switch to another.
- **Scalability**: Add brokers as needed.
- **Self-healing**: Clients auto-connect to healthy brokers.

#### 3. Architecture Diagram:
```
+------------------+     +------------------+     +------------------+
|   Publisher 1    |     |   Subscriber 1   |     |   Subscriber 2   |
| (Topic: News)    |     | (Topic: News)    |     | (Topic: Sports)  |
+--------+---------+     +--------+---------+     +--------+---------+
         |                          |                          |
         v                          v                          v
+------------------------------------------------------------------+
|         Service Discovery / Coordination Service                 |
|         (e.g., ZooKeeper, etcd)                                  |
+--------------------------+---------------------------+-----------+
         |                   |                          |
         v                   v                          v
+------------------+     +------------------+     +------------------+
| Message Broker A |     | Message Broker B |     | Message Broker C |
| (Handles Pub/Sub)|     | (Handles Pub/Sub)|     | (Handles Pub/Sub)|
+------------------+     +------------------+     +------------------+
```

---

