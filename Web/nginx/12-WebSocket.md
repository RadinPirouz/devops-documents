# WebSocket and Nginx Reverse Proxy Configuration Guide

## 1. Introduction

**WebSocket** is a **bi-directional, full-duplex communication protocol** that operates over a **single TCP connection**. Unlike traditional HTTP, where the client sends a request and the server responds, WebSocket allows both client and server to send messages to each other at any time during the session.

This makes it highly suitable for **real-time applications** such as chat systems, live dashboards, and streaming services.

---

## 2. How WebSocket Works

### Traditional HTTP

In HTTP:

* The client sends a request.
* The server sends a response.
* The connection is then closed (unless using persistent connections).

### WebSocket

In WebSocket:

* The client initiates an **HTTP request** with special headers to **upgrade** the connection from HTTP to WebSocket.
* The server accepts the upgrade and switches protocols.
* Once established, both sides can exchange data freely over a persistent TCP connection.

---

## 3. Establishing a WebSocket Connection

### Client → Server (Upgrade Request)

The WebSocket connection starts as a standard HTTP request with additional headers:

```http
GET /chat HTTP/1.1
Host: example.com
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Version: 13
```

### Server → Client (Upgrade Response)

If the server supports WebSocket, it responds with:

```http
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
```

---

## 4. Header Explanation

* **Upgrade:**
  Indicates the protocol the client wants to switch to (in this case, `websocket`).

* **Connection:**
  Must include the value `Upgrade` to signal the intention to upgrade the connection.

* **Sec-WebSocket-Key:**
  A randomly generated Base64-encoded value (16 bytes) sent by the client.
  It ensures a unique connection and prevents cross-protocol attacks.

* **Sec-WebSocket-Version:**
  Specifies the WebSocket protocol version the client supports.
  Most servers use **version 13**.
  If not supported, the server responds with:

  ```http
  HTTP/1.1 426 Upgrade Required
  Sec-WebSocket-Version: 13
  ```

* **Sec-WebSocket-Accept:**
  Returned by the server as proof that it successfully accepted the handshake.
  It’s derived from the client’s `Sec-WebSocket-Key` using a predefined GUID.

---

## 5. HTTP Version Requirement

WebSocket requires **HTTP/1.1 or higher** because:

* **HTTP/1.0** opens a new TCP connection for each request, leading to high overhead.
* **HTTP/1.1** introduced **persistent connections (Keep-Alive)**, allowing multiple requests to share a single TCP connection.

For example:

* In HTTP/1.0, downloading 4 images would open 4 separate TCP connections.
* In HTTP/1.1, one TCP connection can handle all 4 requests.

WebSocket leverages this concept to maintain a **single long-lived TCP connection** between the client and server.

---

## 6. Enabling WebSocket Support in Nginx

When using Nginx as a **reverse proxy**, the connection upgrade must be explicitly configured.

### Example Configuration

```nginx
location / {
    proxy_pass http://backend:8080;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_http_version 1.1;
}
```

### Explanation

* **proxy_pass:**
  Forwards the request to the backend service.

* **proxy_set_header Upgrade $http_upgrade;**
  Passes the `Upgrade` header from the client to the backend.

* **proxy_set_header Connection "upgrade";**
  Ensures Nginx forwards the `Connection: Upgrade` header required for WebSocket.

* **proxy_http_version 1.1;**
  Enables HTTP/1.1 support in proxying, required for WebSocket functionality.

---

## 7. Summary

| Feature               | Description                                                                         |
| --------------------- | ----------------------------------------------------------------------------------- |
| Protocol              | Bi-directional, full-duplex                                                         |
| Base Protocol         | HTTP/1.1                                                                            |
| Upgrade Mechanism     | HTTP 101 Switching Protocols                                                        |
| Persistent Connection | Yes                                                                                 |
| Key Headers           | Upgrade, Connection, Sec-WebSocket-Key, Sec-WebSocket-Version, Sec-WebSocket-Accept |
| Nginx Requirement     | Must enable `proxy_http_version 1.1` and pass upgrade headers                       |
