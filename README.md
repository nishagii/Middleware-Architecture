Middleware Architectures - Assignment 01: Publish/Subscribe Middleware
======================================================================

This repository contains the implementation for **Assignment 01** of the Middleware Architectures course (IS3108 / SCS3203), focusing on a simple **Publish/Subscribe middleware** using client-server socket programming.

🧩 Task 1: The Client-Server Application
----------------------------------------

### 🎯 Objective

Implement a basic client-server socket application where:

*   The **client sends text** to the server.
    
*   The **server displays** the received message.
    
*   The client **disconnects and terminates** upon typing the keyword "terminate".
    

### 🛠️ Language

*   **Python**
    

### 📁 Project Structure (Task 1)

File Name

Description

server\_app.py

The server-side application

client\_app.py

The client-side application

### ▶️ How to Run (Task 1)

#### Step 1: Start the Server (Terminal 1)

1.  Open a terminal.
    
2.  Navigate to the directory containing server\_app.py.
    
3.  python server\_app.py _Example:_ python server\_app.py 5000_Expected Output:_Starting up server on 0.0.0.0 port 5000Waiting for a connection...
    

#### Step 2: Start the Client (Terminal 2)

1.  Open another terminal.
    
2.  Navigate to the directory containing client\_app.py.
    
3.  python client\_app.py _Example (for localhost):_ python client\_app.py 127.0.0.1 5000_Expected Output:_Connecting to 127.0.0.1 port 5000Enter message (type 'terminate' to exit):
    

### 💬 Interaction (Task 1)

*   In the client terminal, type any message and press Enter.
    
*   The server terminal will display the received message.
    

### 🔚 To Terminate (Task 1)

*   Type terminate (case-insensitive) in the client and press Enter.
    
*   The client will disconnect.
    
*   The server will show that the connection has closed and wait for new connections.
    

🧩 Task 2: Publishers and Subscribers
-------------------------------------

### 🎯 Objective

Improve the client-server implementation to:

*   Handle **multiple concurrent client connections** on the server.
    
*   Allow clients to act as either PUBLISHER or SUBSCRIBER via a **third command-line argument**.
    
*   **Echo messages sent by PUBLISHER clients to all SUBSCRIBER clients**.
    
*   Ensure PUBLISHER messages are **only shown on SUBSCRIBER terminals**, not other PUBLISHER terminals.
    

### 🛠️ Language

*   **Python**
    

### 📁 Project Structure (Task 2)

(Same as Task 1: server\_app.py, client\_app.py - updated internally to support new features)

### ▶️ How to Run (Task 2)

#### Step 1: Start the Server (Terminal 1)

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`python server_app.py` 

#### Step 2: Start Multiple Clients (Publishers and Subscribers)

Open additional terminals and run clients specifying their role:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`python client_app.py`   

_Examples:_

*   **Publisher:** python client\_app.py 127.0.0.1 5000 PUBLISHER
    
*   **Subscriber:** python client\_app.py 127.0.0.1 5000 SUBSCRIBER
    

### 💬 Interaction (Task 2)

*   Messages typed by a PUBLISHER will be displayed on all connected SUBSCRIBER terminals.
    
*   PUBLISHER terminals will **not** receive these messages.
    

### 🔚 To Terminate (Task 2)

*   Type terminate (case-insensitive) in any client and press Enter. That client will disconnect. The server will update its active connections, and other clients remain connected.
    

🧩 Task 3: Publishers and Subscribers Filtered on Topics/Subjects
-----------------------------------------------------------------

### 🎯 Objective

Further enhance the implementation from Task 2 to include **"topic/subject" based filtering**:

*   Clients include a **fourth command-line argument for the topic/subject**.
    
*   PUBLISHER clients send messages on a **specific topic**.
    
*   The server routes messages **only to SUBSCRIBER clients interested in the same topic**.
    

### 🛠️ Language

*   **Python**
    

### 📁 Project Structure (Task 3)

(Same as Task 1 & 2: server\_app.py, client\_app.py - updated internally)

### ▶️ How to Run (Task 3)

#### Step 1: Start the Server (Terminal 1)

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`python server_app.py` 

#### Step 2: Start Multiple Clients with Different Roles and Topics

Open additional terminals and run clients specifying their role and topic:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`python client_app.py`    

_Examples:_

*   **Publisher News:** python client\_app.py 127.0.0.1 5000 PUBLISHER NEWS
    
*   **Subscriber News:** python client\_app.py 127.0.0.1 5000 SUBSCRIBER NEWS
    
*   **Publisher Sports:** python client\_app.py 127.0.0.1 5000 PUBLISHER SPORTS
    
*   **Subscriber Sports:** python client\_app.py 127.0.0.1 5000 SUBSCRIBER SPORTS
    

### 💬 Interaction (Task 3)

*   Messages from a PUBLISHER will only be received by SUBSCRIBER clients that are subscribed to the **exact same topic**.
    
*   PUBLISHER terminals will still not receive published messages.
    

### 🔚 To Terminate (Task 3)

*   Type terminate (case-insensitive) in any client and press Enter. That client will disconnect. The server will update its active connections, and other clients remain connected.
    

🧩 Task 4: Enhance the Architecture to Gain Improvement in Availability and Reliability
---------------------------------------------------------------------------------------

### 🎯 Objective

Propose a new distributed architecture for the Pub/Sub implementation to gain improved availability and reliability over the single server node failure deficiency. (No implementation expected).

### ✨ Proposed Distributed Architecture: Distributed Broker Cluster with Service Discovery

The current single-server architecture has a **single point of failure (SPOF)**. If the server goes down, the entire messaging system fails. To address this, we propose a distributed architecture that replaces the single server with multiple, interconnected message brokers, coordinated by a service discovery mechanism.

#### 1\. Architecture Components:

*   **Clients (Publishers & Subscribers):**
    
    *   Clients no longer connect to a fixed server IP. Instead, they query a central "Service Discovery" component to find available message brokers.
        
    *   If a connected broker fails, clients can intelligently re-discover and reconnect to another active broker.
        
*   **Message Brokers (e.g., Broker A, Broker B, Broker C):**
    
    *   These are independent instances of the Pub/Sub server logic. Each broker can accept client connections and handle message routing.
        
    *   They collectively manage topics and messages, distributing the workload.
        
*   **Service Discovery / Coordination Service (e.g., Apache ZooKeeper, etcd):**
    
    *   This is a critical, separate component that manages the cluster of message brokers.
        
    *   **Broker Registration:** Each Message Broker registers its IP and port with this service upon startup.
        
    *   **Health Monitoring:** It continuously monitors the health of all registered brokers. Unhealthy brokers are removed from the list of available brokers.
        
    *   **Client Lookup:** Clients query this service to obtain a dynamic list of currently active and healthy Message Brokers.
        

#### 2\. How it Improves Availability and Reliability:

*   **Elimination of Single Point of Failure (SPOF):**
    
    *   If one Message Broker fails, the Service Discovery service detects this. Clients can then seamlessly connect to another healthy broker from the available list. The Pub/Sub system remains operational, ensuring high availability.
        
    *   This redundancy significantly boosts the overall reliability of the messaging infrastructure.
        
*   **Load Balancing & Scalability:**
    
    *   The presence of multiple brokers naturally allows for distributing client connections and message traffic across the cluster, preventing any single node from becoming a bottleneck.
        
    *   New brokers can be added dynamically to handle increased load, providing horizontal scalability.
        
*   **Self-Healing:**
    
    *   Clients are designed to be resilient to broker failures. With the Service Discovery mechanism, they can automatically re-route their connections to another functional broker, minimizing service interruption.
        

#### 3\. Architecture Diagram:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   +------------------+     +------------------+     +------------------+  |                  |     |                  |     |                  |  |   Publisher 1    |     |   Subscriber 1   |     |   Subscriber 2   |  | (Topic: News)    |     | (Topic: News)    |     | (Topic: Sports)  |  |                  |     |                  |     |                  |  +--------+---------+     +--------+---------+     +--------+---------+           |                          |                          |           |                          |                          |  (Client-Broker Connections)           v                          v                          v  +------------------------------------------------------------------+  |                Service Discovery / Coordination Service          |  |                 (e.g., ZooKeeper, etcd)                          |  |                - Broker Registration & Health Check              |  |                - Broker List for Clients                         |  +--------------------------+---------------------------+-----------+           |                   |                          |           |                   |                          |  (Broker Registration & Lookup)           v                   v                          v  +------------------+     +------------------+     +------------------+  |                  |     |                  |     |                  |  |   Message Broker A   | |   Message Broker B   | |   Message Broker C   |  |                  |     |                  |     |                  |  | (Handles Pub/Sub |     | (Handles Pub/Sub |     | (Handles Pub/Sub |  |    Connections)  |     |    Connections)  |     |    Connections)  |  +------------------+     +------------------+     +------------------+   `