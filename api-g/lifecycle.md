# Canary Deployments & Blue-Green Deployments in NGINX Plus

## Overview
NGINX Plus enables **Canary and Blue-Green Deployments** for **gradual rollouts** and **zero-downtime releases**.

---

## 1. **Canary Deployment Configuration**
Routes a percentage of traffic to a new version while keeping the existing version live.

```nginx
upstream app_backend {
    server app-v1.example.com weight=80;
    server app-v2.example.com weight=20;
}

server {
    listen 443 ssl;
    server_name api.example.com;

    location / {
        proxy_pass http://app_backend;
    }
}
```

### Explanation:
- **80% of traffic goes to `app-v1`**, while **20% goes to `app-v2`**.
- Gradually shift weight to `app-v2` before fully transitioning.

---

## 2. **Blue-Green Deployment Configuration**
Switches between two environments with zero downtime.

```nginx
upstream blue {
    server blue-app.example.com;
}

upstream green {
    server green-app.example.com;
}

server {
    listen 443 ssl;
    server_name api.example.com;

    set $backend blue;

    location / {
        proxy_pass http://$backend;
    }
}
```

### Switching Environments:
```sh
# Switch traffic to Green environment
echo 'set $backend green;' > /etc/nginx/conf.d/deployment.var
nginx -s reload
```

### Explanation:
- All traffic initially goes to `blue-app`.
- **Switches to `green-app` instantly by modifying a variable**.
- Ensures **zero downtime** when switching environments.

---

## Conclusion
NGINX Plus enables **controlled rollouts and instant environment switches**, ensuring **safe API deployments** with **minimal risk**.

