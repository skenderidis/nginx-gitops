# Client Tests for Validating Request & Response Modification in NGINX Plus

## Overview
These tests ensure that **request modifications (headers, URL rewrites)** and **response modifications (headers, content filters)** work as expected in **NGINX Plus API Gateway**.

---

## 1. **Request Header Modification Test**
Validates that custom request headers are being set.

```sh
curl -v -H "X-Test: Sample" https://api.example.com/
```

### Expected Output:
- Backend should receive **X-Client-IP** and **Authorization** headers.
- Headers should be modified as per configuration.

---

## 2. **Response Header Modification Test**
Verifies that response headers are modified correctly.

```sh
curl -I https://api.example.com/
```

### Expected Output:
- `Server: API-Gateway` should be present.
- `X-Frame-Options: DENY` should be set.

---

## 3. **URL Rewrite Test**
Ensures requests to old endpoints are redirected.

```sh
curl -v https://api.example.com/old-endpoint/test
```

### Expected Output:
- Should return **301 Moved Permanently**.
- Redirect to `/new-endpoint/test`.

---

## 4. **Response Content Modification Test**
Verifies that specific text in API responses is replaced.

```sh
curl -s https://api.example.com/ | grep "Modified Text"
```

### Expected Output:
- **Original Text** should be replaced with **Modified Text**.

---

## 5. **Logging & Monitoring Test**
Ensures logs capture modifications.

```sh
tail -f /var/log/nginx/access.log
```

### Expected Output:
- Requests and modifications should be logged with timestamps.

---

## Conclusion
These tests confirm **request header injection, response modifications, URL rewriting, and response filtering**, ensuring API Gateway modifications function correctly.

