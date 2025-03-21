
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