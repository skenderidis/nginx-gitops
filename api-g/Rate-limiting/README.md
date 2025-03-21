# Rate Limiting in NGINX Plus API Gateway

## Overview
Rate limiting helps protect APIs from excessive requests, ensuring fair usage and preventing abuse. NGINX Plus provides flexible rate-limiting capabilities using the `limit_req_zone` and `limit_req` directives.

---

## 1. Basic Rate Limiting
Limits requests to **10 requests per second per IP**.

```nginx
http {
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    
    server {
        listen 443 ssl;
        server_name api.example.com;
        
        location / {
            limit_req zone=api_limit burst=20 nodelay;
            proxy_pass http://backend;
        }
    }
}
```

### Explanation:
- `limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;` → Defines a shared memory zone (`api_limit`) storing client IPs, allowing **10 requests per second**.
- `limit_req zone=api_limit burst=20 nodelay;` → Allows a burst of **20 requests**, rejecting excess requests immediately.

---

## 2. Rate Limiting Based on API Key
Limits requests per API key rather than per IP.

```nginx
http {
    limit_req_zone $http_x_api_key zone=api_key_limit:10m rate=5r/s;
    
    server {
        listen 443 ssl;
        server_name api.example.com;
        
        location / {
            limit_req zone=api_key_limit burst=10 nodelay;
            proxy_pass http://backend;
        }
    }
}
```

### Explanation:
- Uses the `X-API-Key` header (`$http_x_api_key`) to track rate limits per key.
- Limits each API key to **5 requests per second** with a **burst of 10**.

---

## 3. Rate Limiting with Delayed Requests
Allows a burst but queues extra requests instead of rejecting them immediately.

```nginx
location / {
    limit_req zone=api_limit burst=20 delay=5;
    proxy_pass http://backend;
}
```

### Explanation:
- `delay=5` → Allows a burst but queues up to **5 extra requests** instead of rejecting them immediately.

---

## 4. Exempting Specific IPs from Rate Limiting
Allows internal IPs to bypass rate limits.

```nginx
set $rate_limit_enabled 1;
if ($remote_addr ~ "192.168.1.100") {
    set $rate_limit_enabled 0;
}

location / {
    if ($rate_limit_enabled) {
        limit_req zone=api_limit burst=20 nodelay;
    }
    proxy_pass http://backend;
}
```

### Explanation:
- The IP `192.168.1.100` is **exempt from rate limits**.
- Other users still face the **10 requests per second** limit.

---

## 5. Logging Rate-Limited Requests
Logs requests that exceed the rate limit.

```nginx
log_format rate_limited '$remote_addr - $http_x_api_key - $status - $request_time';
access_log /var/log/nginx/rate_limit.log rate_limited;

location / {
    limit_req zone=api_limit burst=20 nodelay;
    proxy_pass http://backend;
}
```

### Explanation:
- Logs requests that exceed rate limits to `/var/log/nginx/rate_limit.log`.

---

## Conclusion
Rate limiting in NGINX Plus helps **control API access**, prevent abuse, and optimize performance. Customize these configurations based on your use case to protect your API effectively.

