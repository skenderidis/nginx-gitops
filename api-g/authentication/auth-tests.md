# Client Tests for Validating Authentication & Authorization in NGINX Plus

## Overview
These tests validate that authentication and authorization configurations in **NGINX Plus** are correctly enforcing security policies. The tests use `curl` to verify different authentication mechanisms.

---

## 1. **Basic Authentication Test**
Ensures access is restricted to authenticated users.

```sh
curl -u user1:password123 -s -o /dev/null -w "%{http_code}\n" https://api.example.com/secure-api/
```

### Expected Output:
- **200 OK** → If valid credentials are provided.
- **401 Unauthorized** → If authentication fails.

---

## 2. **API Key Authentication Test**
Validates access using an `X-API-Key` header.

```sh
curl -H "X-API-Key: test123" -s -o /dev/null -w "%{http_code}\n" https://api.example.com/secure-api/
```

### Expected Output:
- **200 OK** → If a valid API key is used.
- **403 Forbidden** → If the API key is missing or invalid.

---

## 3. **JWT Authentication Test**
Ensures JWT tokens are required for access.

```sh
curl -H "Authorization: Bearer valid.jwt.token" -s -o /dev/null -w "%{http_code}\n" https://api.example.com/secure-api/
```

### Expected Output:
- **200 OK** → If a valid JWT is provided.
- **401 Unauthorized** → If the token is missing or invalid.

---

## 4. **OAuth2 Authentication Test**
Tests if OAuth2 tokens are correctly passed and validated.

```sh
curl -H "Authorization: Bearer oauth_token_123" -s -o /dev/null -w "%{http_code}\n" https://api.example.com/secure-api/
```

### Expected Output:
- **200 OK** → If the token is valid.
- **401 Unauthorized** → If the token is missing or expired.

---

## 5. **LDAP Authentication Test**
Ensures users authenticated via LDAP can access the API.

```sh
curl -u ldap_user:ldap_password -s -o /dev/null -w "%{http_code}\n" https://api.example.com/secure-api/
```

### Expected Output:
- **200 OK** → If the LDAP credentials are correct.
- **401 Unauthorized** → If authentication fails.

---

## 6. **Logging & Monitoring Test**
Checks if authentication failures are logged properly.

```sh
tail -f /var/log/nginx/error.log
```

### Expected Output:
- Failed authentication attempts should be logged with details on **IP, timestamp, and failure reason**.

---

## Conclusion
These tests ensure that **authentication mechanisms** (Basic Auth, API Key, JWT, OAuth2, LDAP) are enforced correctly, preventing unauthorized access to the API. Logs should be monitored for security auditing.

