# Client Tests for Validating Access Control Lists (ACLs) in NGINX Plus

## Overview
These tests ensure that **NGINX Plus correctly enforces ACL rules** using **IP whitelisting, blacklisting, and rate limiting**.

---

## 1. **Whitelisted IP Test**
Verifies that only allowed IPs can access the API.

```sh
curl -v --interface 192.168.1.100 https://api.example.com/
```

### Expected Output:
- **200 OK** if the IP is whitelisted.

```sh
curl -v --interface 192.168.1.200 https://api.example.com/
```

### Expected Output:
- **403 Forbidden** if the IP is not whitelisted.

---

## 2. **Blacklisted IP Test**
Ensures blocked IPs cannot access the API.

```sh
curl -v --interface 203.0.113.5 https://api.example.com/
```

### Expected Output:
- **403 Forbidden** if the IP is blacklisted.

---

## 3. **Rate Limiting Test**
Verifies that excessive requests are throttled.

```sh
for i in {1..10}; do curl -s -o /dev/null -w "%{http_code}\n" https://api.example.com/; done
```

### Expected Output:
- First **5 requests return 200 OK**.
- Additional requests return **429 Too Many Requests**.

---

## 4. **Logging & Monitoring Test**
Ensures access control violations are logged properly.

```sh
tail -f /var/log/nginx/access.log | grep '403'
```

### Expected Output:
- Logs should capture **denied and rate-limited requests**.

---

## Conclusion
These tests validate that **NGINX Plus enforces ACL policies correctly**, blocking unauthorized access and limiting API abuse.

