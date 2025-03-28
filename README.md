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
[host](#spec-host) 

## 'Spec' Field

The **`spec`** field defines the high-level configuration for an application. This includes the following:

| Field              | Description | Type     | Required |
|-------------------|-------------|---------|----------|
| ***[spec.host](#spechost)***| The hostname (domain name) that the application serves. It should be unique across all configurations that are deployed on the same NGINX. The configuration supports also wildcard domains. <br>Expected values: <br>&nbsp;&nbsp; - myapp.example.com<br> &nbsp;&nbsp;&nbsp;-"*.example.com"<br> &nbsp;&nbsp;&nbsp;-myapp | `string` | Yes |
| ***[spec.alternative_hosts](#specalternative_hosts)*** | An optional list of additional domain names that this application serves. These domains must also be unique across all configurations that are deployed on the same NGINX. | `array` of `string` | No |
| ***[spec.listen](#speclisten)*** | Specifies the port number NGINX should listen on. Defaults to `80` for HTTP and `443` for HTTPS. | `integer` | No |
| ***[spec.tls](#spectls)***            | Defines the TLS termination settings, including the certificate name and supported protocols and ciphers. For more details go to the [tls](#spectls) section | object ([tls](#spectls)) | No |
| `server_snippets` | Allows custom NGINX directives to be added to the server block configuration. | `string` | No |
| `gunzip`         | Enables or disables compression responses for clients. Defaults to `off` if not set. | `object` | No |
| `routes`         | Defines URL paths and how requests to those paths are handled, including proxying, redirects, or custom responses. | `array` of `object` | Yes |
| `upstreams`      | Defines backend servers that NGINX will load balance traffic to, including settings like timeouts, load balancing method, and session persistence. | `array` of `object` | Yes |


## Spec.host 
Example:
```yaml
spec:
  host: my-app.example.com
```

## Spec.alternative_hosts 
The `alternative_hosts` field specifies the alternative domains that the application serves. .

Example:
```yaml
spec:
  alternative_hosts:
    - backup.example.com
    - staging.example.com
```

## Spec.listen 
Example:
```yaml
spec:
  listen: 80
```

## Spec.tls
The tls section configures SSL/TLS settings for securing connections. 

| Field                          | Description                      | Type           | Required |
|--------------------------------|----------------------------------|----------------|----------|
| `spec.tls.cert_name`           | The name of the TLS certificate. | `string`       | Yes      |
| `spec.tls.cert_location`       | The filesystem path where the TLS certificate is stored. If you have deployed the certificate with NIM, please check the directory of the certificate. **Default value:** `/etc/nginx/ssl/` | `string`       | Yes      |
| `spec.tls.enable`              | Flag to enable or disable TLS configuration.   | `boolean`      | Yes      |
| `spec.tls.protocols`           | A list of supported TLS protocol versions <br> **Allowed Values**: SSLv2, SSLv3, TLSv1, TLSv1.1, TLSv1.2, TLSv1.3.  <br>    More information can be found on (https://nginx.org/en/docs/http/ngx_http_ssl_module.html#ssl_protocols)     | `list[string]` | No      |
| `spec.tls.ssl_ciphers`         | The ciphers to be used for secure communication, defined in OpenSSL cipher list format. <br> **Examples:** <br> - HIGH:!aNULL:!MD5 <br> - ALL:!aNULL:!EXPORT56:RC4+RSA:+HIGH:+MEDIUM:+LOW:+SSLv2:+EXP;  <br>    More information can be found on (https://nginx.org/en/docs/http/ngx_http_ssl_module.html#ssl_ciphers)  | `string`       | Yes      |
| `spec.tls.ssl_session_cache`   | Configuration for the shared SSL session cache, including cache name and size. <br> **Examples:** <br> - builtin <br> - builtin:1000 <br> - shared:SSL:10m <br> More information can be found on (https://nginx.org/en/docs/http/ngx_http_ssl_module.html#ssl_session_cache) | `string`       | Yes      |
| `spec.tls.ssl_session_timeout` | Specifies a time during which a client may reuse the session parameters. **Examples:** <br> - 5m <br> - 10m <br> - 60m <br> More information can be found on (https://nginx.org/en/docs/http/ngx_http_ssl_module.html#ssl_session_timeout) | `string` | No |


Example of the tls section
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
    ssl_session_timeout: 15m
```

