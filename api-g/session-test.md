# Client Tests for Validating Session Persistence in NGINX Plus

## Overview
These tests ensure that **session persistence (sticky sessions)** is functioning correctly in **NGINX Plus**.

---

## 1. **IP Hash-Based Sticky Sessions Test**
Ensures the same IP address is consistently routed to the same backend.

```sh
for i in {1..5}; do curl -s https://api.example.com/; done
```

### Expected Output:
- All responses should come from the **same backend server**.

---

## 2. **Cookie-Based Sticky Sessions Test**
Verifies that session cookies direct traffic to the same backend.

```sh
curl -s -c cookies.txt https://api.example.com/
curl -s -b cookies.txt https://api.example.com/
```

### Expected Output:
- Requests with the same cookie should be routed to the same backend.

---

## 3. **Cross-Session Validation Test**
Ensures different users are assigned different backends.

```sh
curl -s --cookie-jar session1.txt https://api.example.com/
curl -s --cookie-jar session2.txt https://api.example.com/
```

### Expected Output:
- Different users may be routed to different backend servers.

---

## 4. **Failover Test**
Validates what happens when a backend server goes down.

```sh
# Simulate backend failure (shutdown one backend server)
curl -s https://api.example.com/
```

### Expected Output:
- Requests should switch to a healthy backend.
- After the failed backend recovers, new sessions should resume proper routing.

---

## 5. **Logging & Monitoring Test**
Verifies that sticky session routing is logged properly.

```sh
tail -f /var/log/nginx/access.log | grep srv_id
```

### Expected Output:
- Logs should show **consistent session persistence**.

---

## Conclusion
These tests validate that **sticky sessions** (IP-based, cookie-based, and route-based) are working as expected in NGINX Plus, ensuring users maintain consistent backend connections.

