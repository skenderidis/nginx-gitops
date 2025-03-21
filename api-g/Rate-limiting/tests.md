# Client Tests for Validating NGINX Plus Rate Limiting

## Overview
These tests help verify that the **rate limiting** configurations in NGINX Plus are working as expected. The tests use `curl`, `ab` (Apache Bench), and `hey` to simulate different request scenarios.

---

## 1. **Basic Rate Limiting Test**
Validates that requests beyond the configured limit are blocked.

```sh
# Send 15 requests in quick succession
for i in {1..15}; do curl -s -o /dev/null -w "%{http_code}\n" https://app.f5k8s.net/; done
```

### Expected Output:
- The first **10 requests** should return **200 OK**.
- The remaining **requests** should return **429 Too Many Requests**.

---

## 2. **Testing Rate Limiting with Bursting**
Ensures the burst capacity is working.

```sh
ab -n 25 -c 1 https://api.example.com/
```

### Expected Output:
- The first **10 requests** should be served immediately.
- The next **10 requests** should be queued if `burst=10` is set.
- Any additional requests should return **429 Too Many Requests**.

---

## 3. **Testing API Key-Based Rate Limiting**
Verifies that rate limiting is applied per API key.

```sh
for i in {1..15}; do curl -s -H "X-API-Key: test123" -o /dev/null -w "%{http_code}\n" https://api.example.com/; done
```

### Expected Output:
- If `rate=5r/s`, the **first 5 requests per second** should return **200 OK**.
- The rest should return **429 Too Many Requests**.

---

## 4. **Testing Delayed Requests Handling**
Ensures queued requests are processed gradually.

```sh
hey -n 30 -c 5 https://api.example.com/
```

### Expected Output:
- Requests should be served **with some delay** if `delay=5` is configured.
- No requests should be immediately rejected unless exceeding the burst limit.

---

## 5. **Exempted IP Test**
Verifies that whitelisted IPs bypass rate limits.

```sh
curl -s -o /dev/null -w "%{http_code}\n" --interface 192.168.1.100 https://api.example.com/
```

### Expected Output:
- Requests from **192.168.1.100** should not be rate-limited.
- Other clients should still experience rate limits.

---

## 6. **Logging & Monitoring Test**
Checks if rate-limited requests are being logged properly.

```sh
tail -f /var/log/nginx/rate_limit.log
```

### Expected Output:
- Requests exceeding limits should be logged.
- Log format should include **IP, API key, status code, and request time**.

---

## Conclusion
These tests help validate that NGINX Plus is correctly enforcing **rate limiting policies**. Adjust thresholds as needed and analyze logs to fine-tune configurations for optimal API performance.

