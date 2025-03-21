# Client Tests for Validating Caching in NGINX Plus

## Overview
These tests verify that **NGINX Plus API caching** is working as expected by checking cache hits, bypassing cache, and purging cached responses.

---

## 1. **Basic API Caching Test**
Ensures API responses are cached for the configured duration.

```sh
curl -v https://api.example.com/
```

### Expected Output:
- Response should include:
  ```
  X-Cache-Status: HIT
  ```
  if cached.
- `MISS` on the first request and `HIT` on subsequent requests.

---

## 2. **Cache Expiry Test**
Validates cache expiration after a defined time.

```sh
curl -v https://api.example.com/
# Wait for 10 minutes (or configured expiry time)
curl -v https://api.example.com/
```

### Expected Output:
- `HIT` on second request before expiration.
- `MISS` after the cache expires.

---

## 3. **Bypassing Cache for Authorization Headers**
Ensures authenticated requests bypass caching.

```sh
curl -v -H "Authorization: Bearer test-token" https://api.example.com/
```

### Expected Output:
- `X-Cache-Status: BYPASS` for requests with authentication.

---

## 4. **Purging Cached Responses**
Tests manual cache purging.

```sh
curl -X GET https://api.example.com/ > /dev/null
curl -X PURGE https://api.example.com/purge/
curl -X GET https://api.example.com/ > /dev/null
```

### Expected Output:
- `MISS` on the first request after purge.

---

## 5. **Logging & Monitoring Test**
Ensures cache hits/misses are logged properly.

```sh
tail -f /var/log/nginx/access.log | grep X-Cache-Status
```

### Expected Output:
- Cache hits/misses should appear in logs.

---

## Conclusion
These tests validate that **NGINX Plus caching** is working efficiently and correctly managing API responses based on cache rules.

