# Client Tests for Validating NGINX Plus Reverse Proxy & Load Balancing

## Overview
These tests ensure that **reverse proxying and load balancing** configurations in NGINX Plus function correctly. We use `curl`, `ab` (Apache Bench), and `hey` to simulate different request scenarios and validate behavior.

---

## 1. **Basic Reverse Proxy Test**
Ensures requests are properly forwarded to the backend servers.

```sh
curl -v -s https://api.example.com/
```

### Expected Output:
- Response headers should include `Server: nginx`.
- Backend response should be successfully proxied.

---

## 2. **Load Balancing Distribution Test**
Ensures requests are distributed among backend servers.

```sh
for i in {1..10}; do curl -s -o /dev/null -w "%{http_code} -> %{remote_ip}\n" https://api.example.com/; done
```

### Expected Output:
- Requests should be routed to different backend servers.
- The backend IPs in the response should **alternate** based on the load balancing method.

---

## 3. **Least Connections Load Balancing Test**
Verifies that requests are routed to the backend with the fewest active connections.

```sh
ab -n 50 -c 10 https://api.example.com/
```

### Expected Output:
- Requests should be distributed in a way that minimizes active connections per backend server.
- Faster responses from less-loaded servers.

---

## 4. **Session Persistence (Sticky Sessions) Test**
Ensures the same client always hits the same backend.

```sh
for i in {1..5}; do curl -s -b "SESSIONID=test123" -o /dev/null -w "%{remote_ip}\n" https://api.example.com/; done
```

### Expected Output:
- All requests should be routed to the **same backend server**.
- If `sticky` is correctly configured, there should be no changes in backend assignment.

---

## 5. **Weighted Load Balancing Test**
Ensures traffic is routed based on defined weights.

```sh
ab -n 100 -c 5 https://api.example.com/
```

### Expected Output:
- Higher-weighted servers should receive **more requests** compared to lower-weighted ones.
- The proportion of traffic should match the configured weight distribution.

---

## 6. **Failover & Health Check Test**
Verifies that unhealthy backends are automatically removed from rotation.

```sh
# Temporarily shut down one backend, then run:
ab -n 50 -c 5 https://api.example.com/
```

### Expected Output:
- NGINX should **detect the failure** and route traffic to the remaining healthy servers.
- Failed backend should not receive requests until it recovers.

---

## 7. **Dynamic Service Discovery Test**
Verifies that backends are updated dynamically when using DNS resolution.

```sh
dig +short api-service.example.com
```

### Expected Output:
- The list of backend IPs should reflect the **current available instances**.
- Requests should be routed to **new instances** when they come online.

---

## 8. **Logging & Monitoring Test**
Ensures that proxied requests are being logged properly.

```sh
tail -f /var/log/nginx/access.log
```

### Expected Output:
- Requests should be logged with backend response times and status codes.
- Log format should include details such as **client IP, upstream response time, and backend server**.

---

## Conclusion
These tests validate **NGINX Plus reverse proxying and load balancing functionality**, ensuring high availability, efficient traffic distribution, and proper failover handling. Modify the tests based on your specific setup and requirements.

