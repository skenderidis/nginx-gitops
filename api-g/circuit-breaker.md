# Circuit Breaker & Failover Mechanisms in NGINX Plus API Gateway

## Overview
Circuit breakers and failover mechanisms prevent **cascading failures** by limiting failed requests and ensuring traffic is rerouted to healthy backends.

---

## 1. **Basic Circuit Breaker Configuration**
Limits failed requests per upstream server before marking it as unavailable.

```nginx
upstream backend {
    zone backend 64k;
    server backend1.example.com;
    server backend2.example.com;

    health_check interval=5s fails=3 passes=2;
}

server {
    listen 443 ssl;
    server_name api.example.com;

    location / {
        proxy_pass http://backend;
        proxy_next_upstream error timeout http_500 http_502 http_503 http_504;
    }
}
```

### Explanation:
- **Health checks** detect failures every 5 seconds.
- A backend is marked **unhealthy after 3 failed requests**.
- **`proxy_next_upstream`** redirects failed requests to another backend.

---

## 2. **Rate-Based Circuit Breaker**
Prevents excessive retries on failing servers by **limiting connection attempts**.

```nginx
limit_conn_zone $binary_remote_addr zone=conn_limit:10m;
limit_conn conn_limit 10;
limit_req_zone $binary_remote_addr zone=req_limit:10m rate=5r/s;

server {
    listen 443 ssl;
    server_name api.example.com;

    location / {
        limit_conn conn_limit 10;
        limit_req zone=req_limit burst=10 nodelay;
        proxy_pass http://backend;
    }
}
```

### Explanation:
- **Limits concurrent connections** per client to `10`.
- **Rate-limits** requests to `5 per second` to prevent excessive retries.

---

## 3. **Failover Mechanism**
Automatically reroutes traffic to healthy backends when a failure is detected.

```nginx
upstream backend {
    server backend1.example.com max_fails=3 fail_timeout=10s;
    server backup.example.com backup;
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
- If a backend fails **3 times within 10 seconds**, it is temporarily removed.
- Traffic is rerouted to the **backup server**.

---

## Conclusion
NGINX Plus ensures **reliable API availability** by implementing **circuit breakers and failover mechanisms**, preventing cascading failures and improving system resilience.

