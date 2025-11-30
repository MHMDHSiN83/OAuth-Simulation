# OAuth 2.0 Flow Simulation

A lightweight, educational simulation of the OAuth 2.0 authorization framework.

This project isolates and demonstrates the mechanics of the OAuth 2.0 protocol (specifically the Authorization Code Grant flow). It abstracts away complex backend infrastructure—such as persistent databases—to provide a clear, focused view of how Tokens, Client IDs, and Redirect URIs interact during an authentication handshake.

---

## 🎯 Purpose

The primary goal of this repository is to demonstrate how OAuth 2.0 works under the hood.

Real-world OAuth implementations often obscure the protocol details behind complex database schemas and security layers. This simulation:

* **Simplifies the Data Layer:** Uses in-memory storage instead of a complex database.
* **Decouples the Actors:** Distinctly separates the Client Application (e.g., a shopping site) from the Authorization Server (the identity provider).
* **Visualizes the Flow:** Allows you to inspect the redirects, parameters (scope, state), and token exchanges as they happen.

---

## 🏗 Architecture

The simulation runs **two separate Flask applications simultaneously** to mimic a real-world scenario:

* **Auth Server (`auth_server_app.py`)**: Runs on port 5000. Acts like "Google" or "Facebook," handling user credentials and issuing access tokens.
* **Client App (`client_app.py`)**: Runs on port 5001. Acts like a third-party application (e.g., an online shop) that wants to access user data without seeing their password.

---

## 🚀 Getting Started

### Prerequisites

* Python 3.x
* Git

### Installation

Clone the repository:

```bash
git clone https://github.com/MHMDHSiN83/OAuth-Simulation.git
cd OAuth-Simulation
```

Install dependencies:

```bash
pip install flask requests
```

---

## 💻 Usage

To run the simulation, you need **two terminal windows**.

### Terminal 1: Authorization Server

```bash
cd logic
flask --app auth_server_app.py --debug run -h localhost -p 5000
```

Access at: [http://localhost:5000](http://localhost:5000)

### Terminal 2: Client Application

```bash
cd logic
flask --app client_app.py --debug run -h localhost -p 5001
```

Access at: [http://localhost:5001](http://localhost:5001)

### Start the Flow

1. Open your browser and visit [http://localhost:5001](http://localhost:5001).
2. Click the **Login** button.
3. You will be redirected to the Auth Server (Port 5000) to grant permission.
4. Once approved, you will be redirected back to the Client App (Port 5001) with an authorization code, which is immediately exchanged for an Access Token to retrieve your user profile.

---

## 📂 Project Structure

```
OAuth-Simulation/
├── logic/
│   ├── auth_server_app.py   # The Authorization Server (Provider)
│   ├── client_app.py        # The Client Application (Consumer)
│   ├── client.py            # Helper class for client operations
│   └── ...
├── templates/               # HTML files for the UI
├── static/                  # CSS and assets
└── README.md
```
