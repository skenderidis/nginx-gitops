# NGINX Plus Configuration Examples

This document provides 10 configuration examples for NGINX Plus. Each example demonstrates a different feature or use case.

## Basic HTTP Reverse Proxy Configuration
 
This setup forwards API requests to an upstream API backend.
```
  server {
    listen 80;
    server_name api.f5k8s.net;

    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
  }

  upstream backend {
      server  10.1.20.21:30880;
      server  10.1.20.22:30880;
  }

```

## Weighted Load Balancing
Distributes traffic based on assigned weights on the upstream.

```nginx
upstream backend {

    server  10.1.20.21:30880 weight=3;
    #server  10.1.20.22:30880 weight=1;

}
```

## Backup services
The group consists of two servers of the same application, one of them is a running instance while the second is a backup server.

```nginx
upstream backend {

    server  10.1.20.21:30880;
    #server  10.1.20.22:30880 backup;

}
```

## Dynamic Service Discovery
Automatically resolves backend services via DNS.

```nginx
  resolver 8.8.8.8 valid=30s;
  upstream backend {

    zone backend 32k;
    server  dns-resolve.f5k8s.net:30880;
  }
```


## Choosing the right LB method
NGINX Open Source supports four load‑balancing methods, and NGINX Plus adds two more methods (**random** and **least_time**)

```nginx
  upstream backend {
    # no load balancing method is specified for Round Robin
    least_conn;
    #ip_hash;
    #least_time header;
    #hash $request_uri consistent;
    server  10.1.20.21:30880;
    #server  10.1.20.22:30880;
  }
```

## Cookie-Based Sticky Sessions
Uses a session cookie to persist user sessions to the same backend.

```
  upstream backend {
      server  10.1.20.21:30880;
      #server  10.1.20.22:30880;
      sticky cookie srv_id expires=1h domain=.f5k8s.net path=/;
  }
```


## Health checks
NGINX Plus can periodically check the health of upstream servers by sending special health‑check requests to each server and verifying the correct response.

To enable active health checks:
  - In the location that passes requests (proxy_pass) to an upstream group, include the health_check directive:
  - In the upstream server group, define a shared memory zone with the zone directive:

```
  server {
      location / {
          proxy_pass http://backend;
          health_check;
      }
  }
```


The defaults for active health checks can be overridden with parameters to the health_check directive:

```
server {
    location / {
        proxy_pass   http://backend;
        health_check port=8080;
        health_check uri=/some/path;
        health_check interval=10 fails=3 passes=2;
        health_check interval=1 keepalive_time=60s;
    }
}
```


## Defining custom Health conditions
You can set custom conditions that the response must satisfy for the server to pass the health check. The conditions are defined in a match block, which is referenced in the match parameter of the health_check directive.
  - On the http {} level, specify the match {} block and name it, for example, server_ok.
  - Refer to the block from the health_check directive by specifying the match parameter and the name of the match block.

```nginx
  match server_ok {
      #status 200-399;
      body   ~ "My Echo Project";
  }

  server {
      listen 443 ssl;
      listen 80;
      server_name api.f5k8s.net;

      ssl_certificate /etc/nginx/f5k8s.crt;
      ssl_certificate_key /etc/nginx/f5k8s.key;

      location / {
          proxy_pass http://backend;
          proxy_set_header Host $host;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          health_check interval=5s fails=1 passes=1 match=server_ok;

      }
  }

  upstream backend {
      zone backend 64k;
      server  10.1.20.21:30880;
      #server  10.1.20.22:30880;
  }
```


## Basic TLS/SSL Termination
Terminate TLS and forward traffic to an upstream API service.

```nginx
server {
    listen 443 ssl;
    server_name api.f5k8s.net;

      ssl_certificate /etc/nginx/f5k8s.crt;
      ssl_certificate_key /etc/nginx/f5k8s.key;

    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

## Enforcing Strong TLS Security
Enhance security with modern TLS versions and ciphers.

```nginx
server {
    listen 443 ssl;
    server_name api.f5k8s.net;

    ssl_certificate /etc/nginx/f5k8s.crt;
    ssl_certificate_key /etc/nginx/f5k8s.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers "EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH";
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    location / {
        proxy_pass http://backend;
    }
}
```


## Redirect HTTP to HTTPS
Ensure all traffic is securely encrypted.

```nginx
server {
    listen 80;
    server_name api.f5k8s.net;
    return 301 https://$host$request_uri;
}
```


## Mutual TLS (mTLS) Authentication
Require client certificates for authentication.

```nginx
server {
    listen 443 ssl;
    server_name api.f5k8s.net;

    ssl_certificate /etc/nginx/f5k8s.crt;
    ssl_certificate_key /etc/nginx/f5k8s.key;
    ssl_client_certificate /etc/nginx/ssl/ca.crt;
    ssl_verify_client on;

    location / {
        proxy_pass http://backend;
    }
}
```



