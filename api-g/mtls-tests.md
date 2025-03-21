# Client Tests for Validating Mutual TLS (mTLS) Authentication in NGINX Plus

## Overview
These tests ensure that **Mutual TLS (mTLS) authentication** is properly enforced by **NGINX Plus**.

---

## 1. **Valid Client Certificate Test**
Verifies that authenticated clients can access the API.

```sh
curl -v --cert client.crt --key client.key https://api.example.com/
```

### Expected Output:
- **200 OK** if the client certificate is valid.
- Server should verify the certificate and allow access.

---

## 2. **Missing Client Certificate Test**
Ensures requests without a client certificate are rejected.

```sh
curl -v https://api.example.com/
```

### Expected Output:
- **400 Bad Request** or **403 Forbidden**.
- The server should reject unauthenticated clients.

---

## 3. **Invalid Client Certificate Test**
Tests whether an invalid certificate is properly rejected.

```sh
curl -v --cert invalid.crt --key invalid.key https://api.example.com/
```

### Expected Output:
- **400 Bad Request** or **403 Forbidden**.
- NGINX should log an invalid certificate authentication attempt.

---

## 4. **Optional Client Certificate Authentication Test**
Ensures that optional authentication endpoints work correctly.

```sh
curl -v --cert client.crt --key client.key https://api.example.com/public
```

```sh
curl -v https://api.example.com/public
```

### Expected Output:
- Both authenticated and unauthenticated clients should receive **200 OK**.
- Endpoint `/public` should not enforce certificate verification.

---

## 5. **Restricted Certificate Access Test**
Verifies access control based on Subject DN.

```sh
curl -v --cert untrusted_client.crt --key untrusted_client.key https://api.example.com/secure
```

### Expected Output:
- **403 Forbidden** if the client certificate’s Subject DN is not trusted.
- Only certificates with allowed Subject DNs should pass.

---

## 6. **Logging & Monitoring Test**
Ensures mTLS authentication logs are properly captured.

```sh
tail -f /var/log/nginx/access.log | grep mTLS
```

### Expected Output:
- Logs should show **authenticated and rejected** requests.
- Detailed mTLS handshake logs should be available.

---

## Conclusion
These tests validate that **NGINX Plus properly enforces Mutual TLS authentication**, securing API endpoints and ensuring only trusted clients can connect.

