# VirtualServer Template 

This document describes the YAML structure used to configure NGINX virtual servers. The structure is designed to be similar to the NGINX VirtualServer resource in Kubernetes, ensuring ease of configuration while allowing for direct deployment in traditional environments.

Key Features

- Traffic Routing: Define routes based on URL paths, headers, cookies, and request methods.
- Load Balancing: Support for various load balancing methods, including round-robin and least connections.
- TLS Termination: Enable SSL/TLS security with certificate configuration.
- Gzip Compression: Optimize response delivery with compression settings.
- Health Checks: Define health monitoring for upstream services.
- Flexible Response Handling: Return custom responses or perform redirections.


The `vs` YAML defines load balancing configuration for a domain name, such as example.com. Below is an example of such a configuration:

```yml

name: app1
template: vs
spec: 
  host: cafe.example.com
  alternative_hosts:
    - cafe1.example.com
    - cafe2.example.com  
  listen: 443
  tls: 
    cert_name: test
    enable: true
    protocols:
      - TLSv1.2
  upstreams:
  - name: backend-1
    servers:
      - address: 10.1.10.10:80
      - address: 10.1.10.12:80
        backup: true
  - name: backend-2
    lb_method: least_conn
    servers:
      - address: 10.1.20.20:80
      - address: 10.1.20.21:80
  routes:
  - path: /abc
    proxy: 
      upstream: backend-1
  - path: /api
    proxy: 
      upstream: backend-2
  - path: ~ ^/images/.*\\.jpg$
    action:
      pass: backend-2
  - path: = /img/test
    action:
      pass: backend-1
```

## Root Structure

The Root structure of the YAML consists of three main fields:

| Field              | Description | Type     | Required |
|-------------------|-------------|---------|----------|
| `name`            | This value will be used as the name of the application and needs to be unique across all configurations. | `string` | Yes |
| `template` | The template that will be used to convert the values to NGINX configuration. | `string` | Yes |
| `spec` | Main configuration specification. | `string` | Yes |

```yml
name: app1                  <--- Name of the app
template: vs                <--- Template used
spec:                       <--- Main Configuration 
  host: cafe.example.com
  ...
  ...
```


## 'Spec' Field

The **`spec`** field defines the high-level configuration for an application. This includes the following:

| Field              | Description | Type     | Required |
|-------------------|-------------|---------|----------|
| `host`            | The host (domain name) of the server. Must be a valid subdomain. If using a wildcard domain like `*.example.com`, it must be quoted. This value should be unique across configurations. | `string` | Yes |
| `alternative_hosts` | An optional list of additional domain names that this VirtualServer should respond to. | `array` of `string` | No |
| `listen`          | Specifies the port number NGINX should listen on. Defaults to `80` for HTTP and `443` for HTTPS. | `integer` | No |
| `tls`            | Defines TLS termination settings, including the certificate name and supported protocols. | `object` | No |
| `server_snippets` | Allows custom NGINX directives to be added to the server block configuration. | `string` | No |
| `gunzip`         | Enables or disables compression responses for clients. Defaults to `off` if not set. | `object` | No |
| `routes`         | Defines URL paths and how requests to those paths are handled, including proxying, redirects, or custom responses. | `array` of `object` | Yes |
| `upstreams`      | Defines backend servers that NGINX will load balance traffic to, including settings like timeouts, load balancing method, and session persistence. | `array` of `object` | Yes |


## spec.host and spec.alternative_hosts
The `host` field specifies the primary domain that the application serves, while `alternative_hosts` allows additional domains to be mapped to the same configuration.

```yaml
spec:
  host: my-app.example.com
  alternative_hosts:
    - backup.example.com
    - staging.example.com
```

| Field              | Description | Type     | Required |
|-------------------|-------------|---------|----------|
| `host` |The primary domain name for the server. It should be unique across configurations. Supports wildcard domains (e.g., *.example.com).|`string` | Yes |
|`alternative_hosts`|A list of additional domain names that this VirtualServer should respond to. These domains will share the same routing and upstream rules | `array` of `string` | Yes |


## Spec.listen

The listen field determines the port on which NGINX listens for incoming connections. If omitted, NGINX defaults to port 80 (HTTP) or port 443 (HTTPS with TLS enabled).

```yaml
spec:
  listen: 8080
  ```

| Field              | Description | Type     | Required |
| `listen` |Specifies the port number NGINX should listen on. Defaults to `80` for HTTP and `443` for HTTPS (when `tls`.`enable` is **true**).|`integer` | false |


## Spec.tls

The tls section configures SSL/TLS settings for securing connections. If enabled, NGINX will require a certificate and private key.
```yaml
spec:
  tls:
    cert_name: my-cert
    cert_location: /etc/ssl/nginx
    enable: true
    protocols:
      - TLSv1.2
      - TLSv1.3
    ssl_ciphers: HIGH:!aNULL:!MD5
    ssl_session_cache: shared:SSL:10m
    ssl_session_timeout: 10m
```

