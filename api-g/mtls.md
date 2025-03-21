# Mutual TLS (mTLS) Authentication in NGINX Plus API Gateway

## Overview
Mutual TLS (mTLS) ensures that both the **client and server authenticate each other** using certificates, providing a secure communication channel between API clients and backend services.

---

## 1. **Basic mTLS Authentication Configuration**
Requires clients to present a valid certificate for authentication.

```nginx
server {
    listen 443 ssl;
    server_name api.example.com;

    ssl_certificate /etc/nginx/ssl/api.crt;
    ssl_certificate_key /etc/nginx/ssl/api.key;

    ssl_client_certificate /etc/nginx/ssl/ca.crt;
    ssl_verify_client on;

    location / {
        proxy_pass http://backend;
    }
}
```

### Explanation:
- **`ssl_client_certificate`** → Specifies the CA that issued client certificates.
- **`ssl_verify_client on`** → Requires client authentication.

---

## 2. **Optional Client Certificate Authentication**
Allows optional authentication for specific endpoints.

```nginx
server {
    listen 443 ssl;
    server_name api.example.com;

    ssl_certificate /etc/nginx/ssl/api.crt;
    ssl_certificate_key /etc/nginx/ssl/api.key;

    ssl_client_certificate /etc/nginx/ssl/ca.crt;
    ssl_verify_client optional;

    location /public {
        proxy_pass http://backend;
    }
    
    location /secure {
        if ($ssl_client_verify != SUCCESS) {
            return 403;
        }
        proxy_pass http://backend;
    }
}
```

### Explanation:
- Clients **may** present a certificate for `/public`.
- Clients **must** authenticate for `/secure`.

---

## 3. **Restrict Access Based on Client Certificate**
Allow access only to specific certificates based on Subject DN.

```nginx
if ($ssl_client_s_dn !~ "CN=TrustedClient, O=MyOrg") {
    return 403;
}
```

### Explanation:
- Only requests from **CN=TrustedClient, O=MyOrg** are allowed.

---

## Conclusion
Mutual TLS (mTLS) in NGINX Plus provides **strong authentication and encryption** for securing APIs and backend services.

