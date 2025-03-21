# Service Discovery & Dynamic Upstreams in NGINX Plus API Gateway

## Overview
NGINX Plus supports **dynamic service discovery**, allowing API services to be automatically detected and updated via **DNS resolution** or the **NGINX Plus API**.

---

## 1. **DNS-Based Dynamic Upstreams**
Resolves upstream servers dynamically using DNS.

```nginx
resolver 8.8.8.8 valid=30s;
upstream backend {
    zone backend 64k;
    server api-service.example.com resolve;
}

server {
    listen 443 ssl;
    server_name api.example.com;

    location / {
        proxy_pass http://backend;
    }
}
```

### Explanation:
- **`resolver 8.8.8.8;`** → Configures an external DNS resolver.
- **`server api-service.example.com resolve;`** → Dynamically resolves the service name.
- Updates backend IPs **every 30 seconds**.

---

## 2. **NGINX Plus API for Service Discovery**
Automatically update backends using the **NGINX Plus API**.

```nginx
upstream backend {
    zone backend 64k;
    server localhost:8080;
    server localhost:8081;
}

server {
    listen 443 ssl;
    server_name api.example.com;

    location / {
        proxy_pass http://backend;
    }
}
```

### Update Upstreams Dynamically:
```sh
curl -X POST -d '{"server": "localhost:8082"}' http://nginx-plus-api/upstreams/backend/servers/
```

### Explanation:
- Dynamically **adds or removes upstream servers** without reloading NGINX.
- Uses the **NGINX Plus API** for real-time updates.

---

## 3. **Health Checks for Dynamic Backends**
Enable **active health checks** to ensure backends are available.

```nginx
upstream backend {
    zone backend 64k;
    server api-service.example.com resolve;
    health_check interval=5s fails=3 passes=2;
}
```

### Explanation:
- **Active health checks** monitor the backend's health every **5 seconds**.
- A server is marked **down after 3 failures** and reinstated **after 2 successes**.

---

## Conclusion
NGINX Plus enables **automated service discovery** using **DNS resolution, dynamic APIs, and health checks**, ensuring API services remain resilient and highly available.

