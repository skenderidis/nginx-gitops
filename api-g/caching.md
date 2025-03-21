# Caching in NGINX Plus API Gateway

## Overview
NGINX Plus enables **API response caching** to improve performance, reduce backend load, and enhance user experience.

---

## 1. **Basic API Response Caching**
Caches GET requests for 10 minutes.

```nginx
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=api_cache:10m max_size=1g inactive=10m;

server {
    listen 443 ssl;
    server_name api.example.com;

    location / {
        proxy_cache api_cache;
        proxy_cache_valid 200 10m;
        proxy_cache_key "$scheme$proxy_host$request_uri";
        add_header X-Cache-Status $upstream_cache_status;
        proxy_pass http://backend;
    }
}
```

### Explanation:
- Stores responses in `/var/cache/nginx`.
- **Cache expires in 10 minutes**.
- Adds `X-Cache-Status` header to indicate cache hits/misses.

---

## 2. **Caching Specific API Responses**
Cache responses only for specific endpoints.

```nginx
location /public-api/ {
    proxy_cache api_cache;
    proxy_cache_valid 200 5m;
    proxy_pass http://backend;
}
```

### Explanation:
- Caches only requests under `/public-api/`.
- Cache expires after **5 minutes**.

---

## 3. **Bypassing Cache for Authentication Headers**
Avoids caching responses when `Authorization` header is present.

```nginx
location / {
    proxy_cache api_cache;
    proxy_cache_bypass $http_authorization;
    proxy_pass http://backend;
}
```

### Explanation:
- Requests with `Authorization` are **not cached**.

---