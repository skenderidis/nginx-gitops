# Request & Response Modification in NGINX Plus API Gateway

## Overview
NGINX Plus can modify requests and responses dynamically using `sub_filter`, `headers_more`, and `rewrite` to adjust headers and content before passing them to backend services or clients.

---

## 1. **Modifying Request Headers**
Customize request headers before passing them to the backend.

```nginx
server {
    listen 443 ssl;
    server_name api.example.com;

    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Client-IP $remote_addr;
        proxy_set_header Authorization "Bearer static-token";
    }
}
```

---

## 2. **Modifying Response Headers**
Use `headers_more` to modify response headers before sending them to the client.

```nginx
server {
    listen 443 ssl;
    server_name api.example.com;

    location / {
        proxy_pass http://backend;
        more_set_headers "Server: API-Gateway";
        more_set_headers "X-Frame-Options: DENY";
    }
}
```

---

## 3. **Rewriting Request URLs**
Modify request URLs dynamically.

```nginx
server {
    listen 443 ssl;
    server_name api.example.com;

    location /old-endpoint/ {
        rewrite ^/old-endpoint/(.*)$ /new-endpoint/$1 permanent;
    }
}
```

---

## 4. **Modifying Response Body Content**
Change response content dynamically using `sub_filter`.

```nginx
server {
    listen 443 ssl;
    server_name api.example.com;

    location / {
        proxy_pass http://backend;
        sub_filter 'Original Text' 'Modified Text';
        sub_filter_once off;
    }
}
```

---

## Conclusion
Using **request and response modification** features, NGINX Plus enables flexible adjustments to API communication, ensuring compatibility, security, and performance enhancements.

