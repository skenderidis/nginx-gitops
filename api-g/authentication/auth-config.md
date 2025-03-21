# Authentication & Authorization in NGINX Plus API Gateway

## Overview
Authentication & Authorization ensures secure access to APIs by validating **API keys, JWT tokens, and OAuth2 credentials** before processing requests.

---

## 1. **Basic Authentication (Username & Password)**
Restrict access using **Basic Auth**.

```nginx
server {
    listen 443 ssl;
    server_name api.example.com;

    location /secure-api/ {
        auth_basic "Restricted Area";
        auth_basic_user_file /etc/nginx/.htpasswd;
        proxy_pass http://backend;
    }
}
```

### **Setup Credentials:**
```sh
htpasswd -c /etc/nginx/.htpasswd user1
```

---

## 2. **API Key Authentication**
Validate requests using an **X-API-Key** header.

```nginx
map $http_x_api_key $valid_api_key {
    default 0;
    "test123" 1;
    "apikey456" 1;
}

server {
    listen 443 ssl;
    server_name api.example.com;

    location /secure-api/ {
        if ($valid_api_key = 0) {
            return 403 "Forbidden: Invalid API Key";
        }
        proxy_pass http://backend;
    }
}
```

---

## 3. **JWT Authentication**
Validate JWT tokens in requests.

```nginx
server {
    listen 443 ssl;
    server_name api.example.com;

    location /secure-api/ {
        auth_jwt "Restricted";
        auth_jwt_key_file /etc/nginx/jwt-key.pem;
        proxy_pass http://backend;
    }
}
```

### **Generate JWT Key:**
```sh
openssl genrsa -out /etc/nginx/jwt-key.pem 2048
```

---

## 4. **OAuth2 Authentication (NGINX as Reverse Proxy to OAuth Server)**
Validate requests with an OAuth2 token.

```nginx
server {
    listen 443 ssl;
    server_name api.example.com;

    location /secure-api/ {
        set $auth_header $http_authorization;
        proxy_set_header Authorization "$auth_header";
        proxy_pass http://oauth-backend;
    }
}
```

---

## 5. **LDAP Authentication**
Use LDAP for centralized authentication.

```nginx
server {
    listen 443 ssl;
    server_name api.example.com;

    location /secure-api/ {
        auth_ldap "Restricted";
        auth_ldap_servers ldap_backend;
        proxy_pass http://backend;
    }
}

ldap_server ldap_backend {
    url "ldap://ldap.example.com/ou=users,dc=example,dc=com?uid?sub";
    binddn "cn=admin,dc=example,dc=com";
    binddn_passwd "password";
}
```

---

## Conclusion
NGINX Plus can enforce authentication and authorization using multiple methods, including **Basic Auth, API Keys, JWT, OAuth2, and LDAP**. Choose the approach that best fits your API security requirements.

