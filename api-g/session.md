# Session Persistence (Sticky Sessions) in NGINX Plus API Gateway

## Overview
Session persistence ensures that client requests are always routed to the **same backend server**, maintaining user sessions and improving consistency.

---

## 1. **IP Hash-Based Sticky Sessions**
Routes requests from the same client IP to the same backend server.

```nginx
upstream backend_servers {
    ip_hash;
    server backend1.example.com;
    server backend2.example.com;
}

server {
    listen 443 ssl;
    server_name api.example.com;

    location / {
        proxy_pass http://backend_servers;
    }
}
```

### Explanation:
- **`ip_hash;`** → Ensures requests from the same IP address go to the same backend.

---

## 2. **Cookie-Based Sticky Sessions**
Uses a session cookie to persist user sessions to the same backend.

```nginx
upstream backend_servers {
    server backend1.example.com;
    server backend2.example.com;
    sticky cookie srv_id expires=1h domain=.example.com path=/;
}

server {
    listen 443 ssl;
    server_name api.example.com;

    location / {
        proxy_pass http://backend_servers;
    }
}
```

### Explanation:
- **`sticky cookie srv_id expires=1h;`** → Persists sessions using a cookie.
- Ensures clients always reach the same backend for the duration of the session.

---

## 3. **Route-Based Sticky Sessions**
Assigns backend servers based on a session parameter.

```nginx
upstream backend_servers {
    server backend1.example.com;
    server backend2.example.com;
}

server {
    listen 443 ssl;
    server_name api.example.com;

    location / {
        set $route $cookie_srv_id;
        proxy_pass http://backend_servers;
    }
}
```

### Explanation:
- **Extracts session ID from a cookie** and routes requests accordingly.

---

## Conclusion
NGINX Plus provides **flexible session persistence** options, allowing **IP-based, cookie-based, and route-based sticky sessions** to maintain consistent user experiences across API requests.

