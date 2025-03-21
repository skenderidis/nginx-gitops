# Client Tests for Validating Circuit Breaker & Failover Mechanisms in NGINX Plus

## Overview
These tests ensure that **NGINX Plus circuit breakers and failover mechanisms** are working correctly by limiting failed requests and rerouting traffic to healthy backends.

---

## 1. **Basic Circuit Breaker Test**
Verifies that failed requests trigger circuit breaking.

```sh
for i in {1..5}; do curl -v https://api.example.com/; done
```

### Expected Output:
- After **3 failed requests**, the backend should be marked as **unavailable**.
- Requests should be routed to an alternate backend.

---

## 2. **Rate-Based Circuit Breaker Test**
Ensures request limits prevent API abuse.

```sh
for i in {1..20}; do curl -s -o /dev/null -w "%{http_code}\n" https://api.example.com/; done
```

### Expected Output:
- The first few requests should return **200 OK**.
- Requests exceeding the rate limit should return **429 Too Many Requests**.

---

## 3. **Failover Mechanism Test**
Simulates backend failure and ensures traffic reroutes correctly.

```sh
# Stop primary backend service
systemctl stop backend_service

# Check if requests are routed to the backup backend
curl -v https://api.example.com/
```

### Expected Output:
- Requests should be routed to the **backup server**.
- The failed backend should be removed from the upstream list temporarily.

---

## 4. **Backend Recovery Test**
Ensures traffic resumes normal routing when a failed backend recovers.

```sh
# Restart backend service
systemctl start backend_service

# Check if traffic returns to the primary backend
curl -v https://api.example.com/
```

### Expected Output:
- Requests should be handled by the **primary backend again**.
- Health checks should confirm the backend is available.

---

## 5. **Logging & Monitoring Test**
Ensures that circuit breaker and failover events are properly logged.

```sh
tail -f /var/log/nginx/error.log | grep upstream
```

### Expected Output:
- Logs should indicate **failures, circuit breaking events, and failovers**.

---

## Conclusion
These tests confirm that **NGINX Plus circuit breakers and failover mechanisms** are **preventing cascading failures** and ensuring API reliability.

