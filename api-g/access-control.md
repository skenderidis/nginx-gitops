# Access Control Lists (ACLs) in NGINX Plus API Gateway

## Overview
NGINX Plus allows **IP-based access control** to restrict or allow API access using **whitelisting and blacklisting** rules.

---

## 1. **Denying All Except Whitelisted IPs**
Restricts API access to specific trusted IP addresses.

```nginx
server {
    listen 443 ssl;
    server_name api.example.com;

    location / {
        allow 192.168.1.100;
        allow 192.168.1.101;
        deny all;
        proxy_pass http://backend;
    }
}
```

### Explanation:
- Only **192.168.1.100 and 192.168.1.101** can access the API.
- All other IPs are **denied**.

---

## 2. **Blocking Specific IPs (Blacklist)**
Denies requests from certain IPs while allowing others.

```nginx
server {
    listen 443 ssl;
    server_name api.example.com;

    location / {
        deny 203.0.113.5;
        allow all;
        proxy_pass http://backend;
    }
}
```

### Explanation:
- Blocks **203.0.113.5** from accessing the API.
- All other clients are **allowed**.

---

## 3. **Rate Limiting Specific IPs**
Combines **ACLs and rate limiting** for selected clients.

```nginx
limit_req_zone $binary_remote_addr zone=rate_limit:10m rate=5r/s;

server {
    listen 443 ssl;
    server_name api.example.com;

    location / {
        if ($remote_addr = 203.0.113.5) {
            return 403;
        }
        limit_req zone=rate_limit burst=10 nodelay;
        proxy_pass http://backend;
    }
}
```

### Explanation:
- **203.0.113.5 is explicitly blocked**.
- Rate limits are applied to other requests.

---

## Conclusion
NGINX Plus **effectively enforces access control** using IP-based **whitelisting, blacklisting, and rate limiting** to enhance API security.

