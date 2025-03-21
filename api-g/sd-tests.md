# Client Tests for Validating Service Discovery & Dynamic Upstreams in NGINX Plus

## Overview
These tests ensure that **NGINX Plus service discovery and dynamic upstreams** are working correctly by verifying **DNS-based resolution, API updates, and health checks**.

---

## 1. **DNS-Based Dynamic Upstream Test**
Verifies that DNS-based service discovery is resolving correctly.

```sh
dig +short api-service.example.com
curl -v https://api.example.com/
```

### Expected Output:
- `dig` should return a list of backend IPs.
- The request should successfully **resolve and connect** to a backend server.

---

## 2. **NGINX Plus API Upstream Update Test**
Ensures new upstream servers can be added dynamically.

```sh
curl -X POST -d '{"server": "localhost:8082"}' http://nginx-plus-api/upstreams/backend/servers/
curl -v https://api.example.com/
```

### Expected Output:
- The new server should be added to the upstream list.
- API requests should be load-balanced to the newly added server.

---

## 3. **Health Check Failure Simulation**
Tests if an unhealthy backend is removed from the upstream list.

```sh
# Stop a backend server
systemctl stop backend_service

# Check if the unhealthy server is marked as down
grep 'backend' /var/log/nginx/access.log
```

### Expected Output:
- The unhealthy server should no longer receive traffic.
- Health check logs should indicate failure detection.

---

## 4. **Dynamic Upstream Recovery Test**
Validates that a recovered backend is reinstated.

```sh
# Restart the backend server
systemctl start backend_service

# Check logs for health check success
tail -f /var/log/nginx/access.log
```

### Expected Output:
- The previously failed server should resume receiving traffic after recovery.

---

## 5. **Logging & Monitoring Test**
Ensures that service discovery updates are properly logged.

```sh
tail -f /var/log/nginx/error.log | grep upstream
```

### Expected Output:
- Logs should show updates related to **dynamic upstreams and health checks**.

---

## Conclusion
These tests validate that **NGINX Plus dynamic service discovery and upstream health checks** ensure seamless API availability and automatic failover handling.

