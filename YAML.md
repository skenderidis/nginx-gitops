# Using the NGINX YAML Configuration

This document is a guide on how to use the custom YAML files to define a complete NGINX configuration with routing, upstreams, authentication, rate limiting, and much more.

In terms of NGINX configuration, each YAML file represents a single **server** and multiple **upstream** blocks. An example of a typical is shown below.
 
```yaml 
name: app1
template: vs
spec: 
  host: example.com
  alternative_hosts:
    - cafe.example.com
  listen: 443
  tls: 
    cert_name: example
    enable: true
    protocols:
      - TLSv1.2
  routes:
  - path: /
    proxy: 
      upstream: pool_1
  upstreams:
  - name: pool_1
    lb_method: least_conn
    servers:
      - address: 10.1.20.23:80
      - address: 10.1.20.34:8080

```

## Table of Contents

- [Root Structure](#root-structure)
- [Spec.host](#host)
- [Spec.tls](#team)
- [Spec.jwt](#faq)
- [Spec.accessControl](#support)
- [Spec.License](#license)



## Root Structure

The Root structure of the YAML consists of three main fields:

| Field              | Description | Type     | Required |
|-------------------|-------------|---------|----------|
|   name | This value will be used as the name of the application and needs to be unique across all configurations. | `string` | Yes |
| template | This is the name of the JINJA2 template that will be used to convert the values to NGINX configuration. <br> ***Note:*** At the moment only a single template has been developed which is called `vs` | `string` | Yes |
|  [spec](#spec) | This is the main configuration block for the specific applications that is being published. | `object` | Yes |

This is an example of the Root structure YAML:
```yml
name: app1
template: vs
spec:
  host: cafe.example.com
  tls: ...
  ...
  ...
```

## Spec
The **`spec`** section outlines the high-level configuration of the application. It includes all the key fields used to control routing, security, TLS, upstream settings, and more.
You can click on any `field` name in the table below to jump to its detailed description.

| Field              | Description | Type     | Required |
|-------------------|-------------|---------|----------|
| ***[spec.host](#spechost)***| The hostname (domain name) that the application serves. It should be unique across all configurations that are deployed on the same NGINX. The configuration supports also wildcard domains. <br>Expected values: <br>&nbsp;&nbsp; - myapp.example.com<br> &nbsp;&nbsp;&nbsp;- "*.example.com"<br> &nbsp;&nbsp;&nbsp;- myapp | `string` | Yes |
| ***[spec.alternative_hosts](#specalternative_hosts)*** | An optional list of additional domain names that this application serves. These domains must also be unique across all configurations that are deployed on the same NGINX. | `array` of `string` | No |
| ***[spec.listen](#speclisten)*** | Specifies the port number NGINX should listen on. Defaults to `80` for HTTP and `443` for HTTPS. | `integer` | No |
| ***[spec.tls](#spectls)***  | Defines the TLS termination settings, including the certificate name and supported protocols and ciphers. <br> Defaults to `off` if not set. | object ([tls](#spectls)) | No |
| ***[spec.server_snippets](#specserver_snippets)*** | Allows custom NGINX directives to be added to the server block configuration. | `string` | No |
| ***[spec.gunzip](#specgunzip)*** | Controls GZIP decompression on responses. Useful when upstreams send compressed responses and decompression is required for processing or caching. | `object` | No |
| ***[spec.waf](#specwaf)*** | Enables NGINX App Protect WAF configuration. Expects the policy references as well as the log settings | `object` | No |
| ***[spec.apiKey](#specapikey)*** | Enables API key-based authentication. Allows multiple key definitions and options for supplying them in headers or query parameters. | `object` | No |
| ***[spec.jwt](#specjwt)*** | Configures JWT-based authentication. Supports local secret file or remote JWKS URI for token validation. | `object` | No |
| ***[spec.accessControl](#specaccesscontrol)*** | Defines IP-based access control rules. Supports `allow` and `deny` lists for fine-grained access policies. | `object` | No |
| ***[spec.rateLimit](#specratelimit)*** | Enables rate limiting based on client IP or other variables. Supports burst, delay, dry-run mode, and log customization. | `object` | No |
| ***[spec.routes](#specroutes)*** | List of route definitions that specify how incoming requests are processed. Each route can define proxy settings, redirects, static responses, traffic splits, or condition-based routing. | `array` of `object` | Yes |
| ***[spec.upstreams](#specupstreams)*** | Defines upstream server pools including load balancing method, timeout settings, health checks, session persistence, and queueing. | `array` of `object` | Yes |


```yml
name: app1
template: vs
spec:
  host: cafe.example.com
  tls: ...
  ...
  ...
```


## Spec.host

The `host` field specifies the primary fully qualified domain name (FQDN) that this server block is designed to handle. This is a required field and acts as the main identifier for routing traffic. NGINX will match incoming HTTP/HTTPS requests to this value in the Host header and serve the appropriate configuration.
If you're using a wildcard domain (e.g., *.example.com), make sure to quote it in YAML, as the asterisk can be misinterpreted by YAML parsers.

**Key Notes:**
- The host must be unique across all server block definitions.
- The value must follow valid domain name syntax (RFC 1035).

| Field   | Description                                                                                                                    | Type     | Required | Examples                    |
|---------|--------------------------------------------------------------------------------------------------------------------------------|----------|----------|-----------------------------|
| `host`  | The primary domain name this server block is designed to handle. Must be a valid FQDN. If using wildcard (e.g., `*.nginx.com`), it must be quoted. This value must be unique across all server blocks. | `string` | Yes      | `myapp.nginx.com`<br>`"*.nginx.com"` |


Example:
```yaml
name: app1
template: vs
spec:
  host: my-app.example.com
  ...
  ...
```

## Spec.alternative_hosts 
The `alternative_hosts` field defines a list of additional domain names that should be associated with the same server block configuration. These domain names are included in the **server_name** directive along with the primary host, allowing NGINX to handle multiple domain variations using a single configuration block.

- This field is **optional**.
- Wildcard domains like `*.example.com` must be quoted to avoid YAML parsing issues.

| Field               | Description                                                                                                         | Type            | Required | Examples                                                  |
|--------------------|---------------------------------------------------------------------------------------------------------------------|------------------|----------|-----------------------------------------------------------|
| `alternative_hosts`| A list of additional domain names that should be included in the same server block configuration. These values are appended to the NGINX `server_name` directive alongside the `host` field. | array of strings | No       | `["cafe1.example.com", "cafe2.example.com"]`<br>`["*.api.example.com"]` |


Example:
```yaml
name: app1
template: vs
spec:
  host: www.example.com
  alternative_hosts:
    - cafe1.example.com
    - cafe2.example.com
    - "*.api.example.com"
```


## Spec.listen 
The `listen` field defines the **port number** that NGINX should bind to for incoming connections in this server block configuration. It controls whether NGINX listens on HTTP (typically port 80) or HTTPS (port 443), or on a custom port for specific use cases (e.g., 8080 for internal apps).

⚠️ Considerations: 
- The value must be an integer between 1 and 65535.
- If listen is not specified, it defaults to 80 or 443 depending on whether TLS is enabled.
- TLS-related settings (under spec.tls) determine whether the port is treated as secure.

This field provides flexibility when multiple configurations need to run on different ports on the same server.


| Field    | Description                                                                                   | Type     | Required | Examples        |
|----------|-----------------------------------------------------------------------------------------------|----------|----------|-----------------|
| `listen` | Port number to bind the server block configuration to. Defaults to `80` or `443` if omitted. Must be between `1` and `65535`. | integer  | No       | `80`, `443`, `8080` |


Example:
```yaml
name: app1
template: vs
spec:
  host: api.example.com
  listen: 8080
```

> 💡 **Tip:** When using listen: 443, make sure TLS is enabled and a valid certificate is provided under spec.tls.

## Spec.tls
The `tls` field defines the TLS (Transport Layer Security) settings for this server block configuration. When enabled, NGINX will listen for **HTTPS** traffic on the configured port (commonly 443) and terminate SSL using the specified certificate.

This field allows you to control what protocols and ciphers are allowed, where certificates are stored, and how session handling is configured.


| Field                 | Description                                                                                                    | Type           | Required | Examples                          |
|----------------------|----------------------------------------------------------------------------------------------------------------|----------------|----------|-----------------------------------|
| `tls.cert_name`      | Name of the certificate and key file (without extension). Files should be located in `/etc/nginx/secrets` or a custom path. | `string`       | Yes      | `"my-cert"`                       |
| `tls.cert_location`  | Optional custom path prefix for the certificate and key files.                                                 | `string`       | No       | `"/custom/path/"`                 |
| `tls.enable`         | Enables or disables TLS termination for this server block.                                                     | `boolean`      | Yes      | `true`, `false`                   |
| `tls.protocols`      | List of allowed TLS protocol versions. <br> **Allowed Values**: SSLv2, SSLv3, TLSv1, TLSv1.1, TLSv1.2, TLSv1.3.       | `array` of `string`| No       | `["TLSv1.2", "TLSv1.3"]`          |
| `tls.ssl_ciphers`    | A string defining supported cipher suites.                                                                     | `string`       | No       | `"HIGH:!aNULL:!MD5"`              |
| `tls.ssl_session_cache` | Configuration for the shared SSL session cache, including cache name and size.                              | `string`       | No       | `"shared:SSL:10m"`                |
| `tls.ssl_session_timeout` | Timeout for cached SSL sessions (e.g., 5m, 10m, 1h).                                                      | `string`       | No       | `"10m"`                           |

> [!NOTE] 
> Note: More information can be found on https://nginx.org/en/docs/http/ngx_http_ssl_module.html


Example of the tls section
```yaml
name: app1
template: vs
spec:
  tls:
    cert_name: my-cert
    cert_location: /etc/ssl/nginx
    enable: true
    protocols:
      - TLSv1.2
      - TLSv1.3
    ssl_ciphers: ALL:!aNULL:!EXPORT56:RC4+RSA:+HIGH:+MEDIUM:+LOW:+SSLv2:+EXP
    ssl_session_cache: shared:SSL:10m
    ssl_session_timeout: 15m
```

> [!IMPORTANT] 
> - When `enable` is **true**, NGINX listens on a secure port (e.g., 443) and serves HTTPS traffic.
> - The specified `cert_name` must match actual files on disk:
>    - `${cert_location}/<cert_name>.crt`
>    - `${cert_location}/<cert_name>.key`
> - If `cert_location` is not defined, it defaults to `/etc/nginx/secrets/`.
> - You can restrict allowed **TLS versions** and define cipher policies to meet compliance (e.g., PCI-DSS).



## Spec.server_snippets

The `server_snippets` field allows you to inject custom NGINX directives directly into the generated server block configuration. This is especially useful for advanced or low-level configurations that are not directly supported by the YAML schema.

This field gives operators full control to customize behavior such as logging, headers, variables, or security directives—without modifying the base template or schema.

💡 Considerations: 
- Injected snippets appear inside the server block of the generated NGINX configuration.
- Accepts any raw NGINX directives supported at the server level.
- Multiple lines can be defined using YAML’s multi-line | syntax.
- This field is optional and has no default behavior if omitted.


> ⚠️ Use with caution: Incorrect or unsupported directives may cause NGINX to fail on reload.

| Field            | Description                                                                                                   | Type     | Required | Examples                                      |
|------------------|---------------------------------------------------------------------------------------------------------------|----------|----------|-----------------------------------------------|
| `server_snippets`| Injects raw NGINX directives into the generated server block. Useful for advanced configurations or overrides. | string   | No       | `"access_log /var/log/nginx/custom.log;"`      |

Example of the tls section
```yaml
name: app1
template: vs
spec:
  host: example.com
  listen: 443
  server_snippets: |
    access_log /var/log/nginx/access.log combined;
    error_log /var/log/nginx/error.log warn;
    add_header X-Server-ID $hostname;
```


## Spec.gunzip  TO FIX
The `gunzip` field enables or disables decompression of gzipped responses before they are delivered to the client. This is useful when upstream services return gzipped content, but the client (e.g., older browsers or debugging tools) expects uncompressed data.

When enabled, NGINX will decode responses compressed with gzip (based on their MIME type) and send them to the client as plain content.


| Field                | Description                                                                                      | Type            | Required | Examples                                 |
|---------------------|--------------------------------------------------------------------------------------------------|------------------|----------|------------------------------------------|
| `gunzip.enable`     | Enables or disables automatic decompression of gzip-encoded responses.                           | `boolean`        | Yes      | `true`, `false`                          |
| `gunzip.gzip_types` | A list of MIME types that should be decompressed if gzipped by the upstream.                    | array of string  | No       | `["text/html", "application/json"]`      |
| `gunzip.gzip_proxied` | A list of proxy-related conditions under which gunzip should apply (e.g., `expired`, `no-cache`). | array of string  | No       | `["expired", "no-cache"]`                |
| `gunzip.gzip_min_length` | Minimum response size in bytes for decompression to be applied.                            | integer          | No       | `256`, `1024`                            |




Example of the tls section
```yaml
name: app1
template: vs
spec:
  gunzip:
    enable: true
    gzip_types:
      - text/html
      - application/json
    gzip_proxied:
      - expired
      - no-cache
    gzip_min_length: 256
```

> [!IMPORTANT] 
>  When enable is true, NGINX automatically decompresses gzipped responses if they match the MIME types in gzip_types.
>  Use gzip_proxied to control when decompression applies, based on proxy response headers (e.g., apply only to expired or cached responses).
>  If gzip_min_length is set, only responses larger than the specified size are decompressed.

If no gzip_types are specified, NGINX uses a default set (but best practice is to define it explicitly for clarity).



## Spec.apiKey

The apiKey field enables API key-based authentication by validating client-supplied tokens against a configured list of valid keys. Clients can supply keys via headers or query parameters.

If a match is found, the request is allowed to proceed; otherwise, it is denied. This mechanism is often used to control access to public APIs or internal services where fine-grained authentication (like JWT) is not required.


| Field                       | Description                                                                                      | Type             | Required | Examples                              |
|----------------------------|--------------------------------------------------------------------------------------------------|------------------|----------|---------------------------------------|
| `apiKey.key`               | A list of valid API key name–value pairs.                                                        | array of object  | Yes      | See example below                     |
| `apiKey.suppliedIn.header` | List of headers from which to extract API keys.                                                  | array of string  | No       | `["x-api-key", "x-auth-token"]`       |
| `apiKey.suppliedIn.query`  | List of query parameters from which to extract API keys.                                         | array of string  | No       | `["key", "token"]`                    |

Example:
```yml
spec:
  apiKey:
    key:
      - name: test1
        value: 123123123123
      - name: test2
        value: 123123123
    suppliedIn:
      header:
        - "x-api-key"
        - "x-auth-token"
      query:
        - "access_token"
```


> [!IMPORTANT]
> Each key entry includes a name (for mapping or logging) and a value (used for validation).
> NGINX will search the specified headers and query parameters for a token and check if it matches any known values.
> Tokens are matched using exact string comparison.
> If no match is found, the request is rejected (typically via auth_request).
> This system supports multiple ways to deliver tokens — making it flexible for mobile apps, APIs, and legacy systems.


## spec.jwt
The jwt field enables JWT (JSON Web Token) authentication, validating incoming tokens for authenticity and access control. This is a robust and modern method of securing APIs, often used in microservices and zero-trust architectures.

NGINX uses a specified secret (or a JWK URI) to validate the token's signature. If validation fails, the request is denied.

| Field               | Description                                                                                      | Type     | Required | Examples                      |
|--------------------|--------------------------------------------------------------------------------------------------|----------|----------|-------------------------------|
| `jwt.secret`        | Name of the file containing the secret key (usually mounted at `/etc/nginx/secrets`).           | `string` | Yes*     | `"jwt-secret"`                |
| `jwt.secret_path`   | Path to the directory containing the secret file. Defaults to `/etc/nginx/secrets`.             | `string` | No       | `"/mnt/secrets/"`             |
| `jwt.realm`         | The authentication realm used in the `WWW-Authenticate` header when a token is missing or invalid. | `string` | Yes      | `"My API"`                    |
| `jwt.token`         | Variable from which to extract the JWT (e.g., `$http_authorization`, `$http_token`).            | `string` | Yes      | `"$http_token"`               |
| `jwt.jwksURI`       | Optional URI pointing to a JWKS (JSON Web Key Set) endpoint for dynamic key verification.        | `string` | No       | `"https://auth.example.com/.well-known/jwks.json"` |

> [!CAUTION]
> Either secret or jwksURI must be specified.


```yml
spec:
  jwt:
    secret: jwt-secret
    secret_path: /etc/nginx/secrets
    realm: "My API"
    token: $http_token
```

> [!NOTE]
> - If jwksURI is provided, NGINX dynamically fetches public keys to validate tokens signed with asymmetric algorithms.
> - If secret is used, NGINX loads the secret key from the specified path and validates HMAC-signed tokens (e.g., HS256).
> - The token field tells NGINX where to look for the JWT — usually in an HTTP header.
> - When authentication fails, NGINX returns a 401 Unauthorized response and includes the configured realm in the header.
> - Works seamlessly with auth_jwt directives under the hood.



## spec.accessControl

The accessControl field is used to control client IP-based access to the server block configuration. It allows you to define which IPs or CIDR ranges are allowed or denied access to your application.

If allow rules are defined, all other IPs are implicitly denied. If only deny is defined, all others are implicitly allowed. If both are omitted, no IP restrictions are enforced.


| Field               | Description                                                         | Type           | Required | Examples                          |
|--------------------|---------------------------------------------------------------------|----------------|----------|-----------------------------------|
| `accessControl.allow` | List of allowed IPs or CIDR blocks. If specified, all others are denied. | array of string | No       | `["10.0.0.0/8", "192.168.1.100"]` |
| `accessControl.deny`  | List of denied IPs or CIDR blocks. If specified, all others are allowed. | array of string | No       | `["203.0.113.0/24"]`              |

> [!CAUTION]
> Either `allow` or `deny` must be specified. In case both are defined, `allow` will supercede `deny`.

```yml
spec:
  accessControl:
    allow:
      - 10.0.0.0/8
    deny:
      - 203.0.113.0/24
```


> [!IMPORTANT]
> - If allow is set, all IPs not in that list are blocked.
> - If only deny is set, all IPs not in that list are allowed.
> - If both allow and deny are omitted, there is no IP filtering.
> - Applies at the server block level and affects all routes under that host.


