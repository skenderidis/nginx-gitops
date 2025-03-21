# Client Tests for Validating Canary & Blue-Green Deployments in NGINX Plus

## Overview
These tests ensure that **NGINX Plus properly routes traffic** in **canary and blue-green deployments**.

---

## 1. **Canary Deployment Traffic Split Test**
Verifies that traffic is correctly distributed between versions.

```sh
for i in {1..20}; do curl -s -o /dev/null -w "%{http_code} -> %{redirect_url}\n" https://api.example.com/; done
```

### Expected Output:
- **80% of requests** should hit `app-v1`.
- **20% of requests** should hit `app-v2`.

---

## 2. **Full Transition to New Version (Canary Deployment)**
Gradually increase traffic to the new version.

```sh
# Modify weight to fully transition to v2
echo 'server app-v2.example.com weight=100;' > /etc/nginx/conf.d/upstream.conf
nginx -s reload
```

```sh
for i in {1..10}; do curl -s -o /dev/null -w "%{http_code}\n" https://api.example.com/; done
```

### Expected Output:
- **100% of requests** should now hit `app-v2`.

---

## 3. **Blue-Green Deployment Switch Test**
Ensures environment switching works without downtime.

```sh
# Switch traffic from blue to green
echo 'set $backend green;' > /etc/nginx/conf.d/deployment.var
nginx -s reload
```

```sh
curl -v https://api.example.com/
```

### Expected Output:
- Traffic should now be served by `green-app`.

---

## 4. **Rollback Test (Blue-Green)**
Verifies that rollback to the previous version works instantly.

```sh
# Switch back to blue
echo 'set $backend blue;' > /etc/nginx/conf.d/deployment.var
nginx -s reload
```

```sh
curl -v https://api.example.com/
```

### Expected Output:
- Traffic should return to `blue-app`.

---

## 5. **Logging & Monitoring Test**
Ensures deployment transitions are logged correctly.

```sh
tail -f /var/log/nginx/access.log | grep api.example.com
```

### Expected Output:
- Logs should show traffic shifting between versions.

---

## Conclusion
These tests validate that **NGINX Plus successfully manages canary deployments and blue-green rollouts**, ensuring smooth version transitions with minimal risk.


