# Configuring NGINX with YAML

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
- [Spec](#spec)
- [spec.host](#spechost)
- [spec.alternative_hosts](#specalternative_hosts)
- [spec.listen](#speclisten)
- [spec.tls](#spec)
- [spec.server_snippets](#specserver_snippets)
- [spec.apiKey](#specapikey)
- [spec.jwt](#specjwt)
- [spec.accessControl](#specaccesscontrol)
- [spec.rateLimit](#specratelimit)
- [spec.upstreams](#specupstreams)
- [spec.upstreams.servers](#specupstreamsservers)
- [spec.upstreams.sessioncookie](#specupstreamssessioncookie)
- [spec.upstreams.healthcheck](#specupstreamshealthcheck)
- [spec.routes](#specroutes)
- [spec.routes.proxy](#specroutesproxy)
- [spec.routes.redirect](#specroutesredirect)
- [spec.routes.return](#specroutesreturn)
- [spec.routes.matches](#specroutesmatches)
- [spec.routes.splits](#specroutessplits)
- [spec.routes.errorpages](#specrouteserrorpages)
- [spec.routes.location_snippets](#specrouteslocation_snippets)


## Root Structure

The Root structure of the YAML consists of three main fields:

| Field              | Description | Type     | Required |
|-------------------|-------------|---------|----------|
|   `name` | This value will be used as the name of the application and needs to be unique across all configurations. | `string` | Yes |
| `template` | This is the name of the JINJA2 template that will be used to convert the values to NGINX configuration. <br> ***Note:*** At the moment only a single template has been developed which is called `vs` | `string` | Yes |
|  [spec](#spec) | This is the main configuration block for the specific applications that is being published. | `object` | Yes |

This is an example of the Root structure YAML:
```yml
name: app1
template: vs
spec:
  ...
  ...
  ...
```

## Spec
The **`spec`** section outlines the high-level configuration of the application. It includes all the key fields used to control routing, security, TLS, upstream settings and more.

| Field      | Description | Type     | Required |
|------------|-------------|---------|----------|
| [spec.host](#spechost)| The hostname (domain name) that the server block is designed to handle. It should be unique across all configurations that are deployed on the same NGINX. The configuration supports also wildcard domains. <br>Expected values: <br>&nbsp;&nbsp; - myapp.example.com<br> &nbsp;&nbsp;&nbsp;- "*.example.com"<br> &nbsp;&nbsp;&nbsp;- myapp | `string` | Yes |
| [spec.alternative_hosts](#specalternative_hosts) | An optional list of additional domain names that the application serves. These domains must also be unique across all configurations that are deployed on the same NGINX. | `array` of `string` | No |
| [spec.listen](#speclisten) | Specifies the port number NGINX should listen on. Defaults to `80` for HTTP and `443` for HTTPS. | `integer` | No |
| [spec.tls](#spectls)  | Defines the TLS termination settings, including the certificate name and supported protocols and ciphers. <br> Defaults to `off` if not set. | object | No |
| [spec.server_snippets](#specserver_snippets) | Allows custom NGINX directives to be added to the server block configuration. | `string` | No |
| [spec.gunzip](#specgunzip)| Controls GZIP decompression on responses. Useful when upstreams send compressed responses and decompression is required for processing or caching. | `object` | No |
| [spec.waf](#specwaf) | Enables NGINX App Protect WAF configuration. Expects the policy references as well as the log settings | `object` | No |
| [spec.apiKey](#specapikey) | Enables API key-based authentication. Allows multiple key definitions and options for supplying them in headers or query parameters. | `object` | No |
| [spec.jwt](#specjwt) | Configures JWT-based authentication. Supports local secret file or remote JWKS URI for token validation. | `object` | No |
| [spec.accessControl](#specaccesscontrol) | Defines IP-based access control rules. Supports `allow` and `deny` lists for fine-grained access policies. | `object` | No |
| [spec.rateLimit](#specratelimit) | Enables rate limiting based on client IP or other variables. Supports burst, delay, dry-run mode, and log customization. | `object` | No |
| [spec.routes](#specroutes) | List of route definitions that specify how incoming requests are processed. Each route can define proxy settings, redirects, static responses, traffic splits, or condition-based routing. | `array` of `object` | Yes |
| [spec.upstreams](#specupstreams) | Defines upstream server pools including load balancing method, timeout settings, health checks, session persistence, and queueing. | `array` of `object` | Yes |

> [!NOTE]
> For full details on each `field`, see their dedicated sections.




## Spec.host

The `host` field specifies the primary fully qualified domain name (FQDN) that this server block is designed to handle. This is a required field and acts as the main identifier for routing traffic. NGINX will match incoming HTTP/HTTPS requests to this value in the Host header and serve the appropriate configuration.
, as the asterisk can be misinterpreted by YAML parsers.


| Field| Description| Type| Required | Examples|
|------|------------|-----|----------|---------|
| `host`  | The primary domain name this server block is designed to handle. Must be a valid FQDN. | `string` | Yes      | `myapp.example.com`, <br>`"*.example.com"` |


> [!IMPORTANT]
> - The `host` must be unique across all server block definitions.
> - If you're using a wildcard domain (e.g. *.example.com), make sure to quote it in YAML (e.g. `host: "*.example.com"`)


**Example:**
```yaml
name: app1
template: vs
spec:
  host: myapp.example.com
```


## Spec.alternative_hosts 
The `alternative_hosts` field defines a list of additional domain names that should be associated with the same server block configuration. These domain names are included in the **server_name** directive along with the primary host, allowing NGINX to handle multiple domain variations using a single configuration block.


| Field | Description | Type | Required | Examples |
|-------|-------------|------|----------|----------|
| `alternative_hosts`| A list of additional domain names that should be included in the same server block configuration. These values are appended to the NGINX `server_name` directive alongside the `host` field. | `array` of `strings` | No       | `cafe1.example.com, cafe2.example.com, "*.api.example.com"` |

> [!IMPORTANT]
> - This field is **optional**.
> - They must be unique across all server block definitions.
> - Wildcard domains like `*.example.com` must be quoted to avoid YAML parsing issues.

**Example:**

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

| Field| Description| Type| Required | Examples|
|------|------------|-----|----------|---------|
| `listen` | Port number to bind the server block configuration to. Defaults to `80` or `443` if omitted. Must be between `1` and `65535`. | integer  | No       | `80`, `443`, `8080` |

> [!IMPORTANT]
> - The value must be an integer between 1 and 65535.
> - You can only configure one port number.
> - If listen is not specified, it defaults to 80 or 443 depending on whether TLS is enabled.
> - TLS-related settings (under spec.tls) determine whether the port is treated as secure.


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


| Field| Description| Type| Required | Examples|
|------|------------|-----|----------|---------|
| `tls.cert_name`      | Name of the certificate and key file (without extension). Files should be located in `/etc/nginx/secrets` or a custom path. | `string`       | Yes      | `"my-cert"`                       |
| `tls.cert_location`  | Optional custom path prefix for the certificate and key files.                                                 | `string`       | No       | `"/custom/path/"`                 |
| `tls.enable`         | Enables or disables TLS termination for this server block.                                                     | `boolean`      | Yes      | `true`, `false`                   |
| `tls.protocols`      | List of allowed TLS protocol versions. <br> **Allowed Values**: SSLv2, SSLv3, TLSv1, TLSv1.1, TLSv1.2, TLSv1.3.       | `array` of `string`| No       | `TLSv1.3`          |
| `tls.ssl_ciphers`    | A string defining supported cipher suites.                                                                     | `string`       | No       | `"HIGH:!aNULL:!MD5"`              |
| `tls.ssl_session_cache` | Configuration for the shared SSL session cache, including cache name and size.                              | `string`       | No       | `"shared:SSL:10m"`                |
| `tls.ssl_session_timeout` | Timeout for cached SSL sessions (e.g., 5m, 10m, 1h).                                                      | `string`       | No       | `"10m"`                           |


> [!IMPORTANT] 
> - When `enable` is **true**, NGINX listens on a secure port (e.g., 443) and serves HTTPS traffic.
> - The specified `cert_name` must match actual files on disk:
>    - `${cert_location}/<cert_name>.crt`
>    - `${cert_location}/<cert_name>.key`
> - If `cert_location` is not defined, it defaults to `/etc/nginx/secrets/`.
> - You can restrict allowed **TLS versions** and define cipher policies to meet compliance (e.g., PCI-DSS).


**Example:**
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


## Spec.server_snippets

The `server_snippets` field allows you to inject custom NGINX directives directly into the generated server block configuration. This is especially useful for advanced or low-level configurations that are not directly supported by the YAML schema.

This field gives operators full control to customize behavior such as logging, headers, variables, or security directives—without modifying the base template or schema.


| Field| Description| Type| Required | Examples|
|------|------------|-----|----------|---------|
| `server_snippets`| Injects raw NGINX directives into the generated server block. Useful for advanced configurations or overrides. | string   | No       | `"access_log /var/log/nginx/custom.log;"`      |

> [!IMPORTANT] 
> - ⚠️ Use with caution: Incorrect or unsupported directives may cause NGINX to fail on reload.
> - Injected snippets appear inside the server block of the generated NGINX configuration.
> - Accepts any raw NGINX directives supported at the server level.
> - Multiple lines can be defined using YAML’s multi-line | syntax.
> - This field is optional and has no default behavior if omitted.

Example:
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

The `apiKey` field enables API key-based authentication by validating client-supplied tokens against a configured list of valid keys. Clients can supply keys via **headers** or **query parameters**.

If a match is found, the request is allowed to proceed; otherwise, it is denied. This mechanism is often used to control access to public APIs or internal services where fine-grained authentication (like **JWT**) is not required.


| Field| Description| Type| Required | Examples|
|------|------------|-----|----------|---------|
| `apiKey.key`               | A list of valid API key name–value pairs.                                                        | `array` of `object`  | Yes      | See example below                     |
| `apiKey.suppliedIn.header` | List of headers from which to extract API keys.                                                  | `array` of `string`  | No       | `["x-api-key", "x-auth-token"]`       |
| `apiKey.suppliedIn.query`  | List of query parameters from which to extract API keys.                                         | `array` of `string`  | No       | `["key", "token"]`                    |

> [!IMPORTANT]
> Each key entry includes a name (for mapping or logging) and a value (used for validation).
> NGINX will search the specified headers and query parameters for a token and check if it matches any known values.
> Tokens are matched using exact string comparison.
> If no match is found, the request is rejected (typically via auth_request).
> This system supports multiple ways to deliver tokens — making it flexible for mobile apps, APIs, and legacy systems.


**Example:**
```yml
spec:
  apiKey:
    key:
      - name: test1
        value: abc1234aa
      - name: test2
        value: abc8976cc
    suppliedIn:
      header:
        - "x-api-key"
        - "x-auth-token"
      query:
        - "access_token"
```


## Spec.jwt
The `jwt` field enables **JWT (JSON Web Token) authentication**, validating incoming tokens for authenticity and access control. This is a robust and modern method of securing APIs, often used in microservices and zero-trust architectures.

NGINX uses a specified **secret** (or a **JWK URI**) to validate the token's signature. If validation fails, the request is denied.

| Field| Description| Type| Required | Examples|
|------|------------|-----|----------|---------|
| `jwt.secret`        | Name of the file containing the secret key (usually mounted at `/etc/nginx/secrets`).           | `string` | Yes*     | `"jwt-secret"`                |
| `jwt.secret_path`   | Path to the directory containing the secret file. Defaults to `/etc/nginx/secrets`.             | `string` | No       | `"/mnt/secrets/"`             |
| `jwt.realm`         | The authentication realm used in the `WWW-Authenticate` header when a token is missing or invalid. | `string` | Yes      | `"My API"`                    |
| `jwt.token`         | Variable from which to extract the JWT (e.g., `$http_authorization`, `$http_token`).            | `string` | Yes      | `"$http_token"`               |
| `jwt.jwksURI`       | Optional URI pointing to a JWKS (JSON Web Key Set) endpoint for dynamic key verification.        | `string` | No       | `"https://auth.example.com/.well-known/jwks.json"` |

> [!IMPORTANT]
> - ⚠️ Either `secret` or `jwksURI` must be specified. Not both
> - If jwksURI is provided, NGINX dynamically fetches public keys to validate tokens signed with asymmetric algorithms.
> - If secret is used, NGINX loads the secret key from the specified path and validates HMAC-signed tokens (e.g., HS256).
> - The token field tells NGINX where to look for the JWT — usually in an HTTP header.
> - When authentication fails, NGINX returns a 401 Unauthorized response and includes the configured realm in the header.
> - Works seamlessly with auth_jwt directives under the hood.

```yml
spec:
  jwt:
    secret: jwt-secret
    secret_path: /etc/nginx/secrets
    realm: "My API"
    token: $http_token
```


## Spec.accessControl

The accessControl field is used to control client IP-based access to the server block configuration. It allows you to define which IPs or CIDR ranges are allowed or denied access to your application.

If allow rules are defined, all other IPs are implicitly denied. If only deny is defined, all others are implicitly allowed. If both are omitted, no IP restrictions are enforced.

| Field| Description| Type| Required | Examples|
|------|------------|-----|----------|---------|
| `accessControl.allow` | List of allowed IPs or CIDR blocks. If specified, all others are denied. | `array` of `string` | No       | `["10.0.0.0/8", "192.168.1.100"]` |
| `accessControl.deny`  | List of denied IPs or CIDR blocks. If specified, all others are allowed. | `array` of `string` | No       | `["203.0.113.0/24"]`              |


> [!IMPORTANT]
> - ⚠️ Either `allow` or `deny` must be specified. In case both are defined, `allow` will supercede `deny`.
> - If allow is set, all IPs not in that list are blocked.
> - If only deny is set, all IPs not in that list are allowed.
> - If both allow and deny are omitted, there is no IP filtering.
> - Applies at the server block level and affects all routes under that host.

Example: 
```yml
spec:
  accessControl:
    allow:
      - 10.0.0.0/8
    deny:
      - 203.0.113.0/24
```

## Spec.rateLimit

The rateLimit field defines a request rate-limiting policy for incoming client traffic. This helps prevent abuse, brute-force attacks, or overload conditions by throttling excessive requests based on an identifier like IP address.

You can configure burst tolerance, delays, dry-run mode, and custom rejection codes.


| Field| Description| Type| Required | Examples|
|------|------------|-----|----------|---------|
| `rateLimit.name`       | Unique name for the rate-limiting zone.                                         | `string` | Yes      | `"default"`               |
| `rateLimit.rate`       | Rate limit expressed in requests per time (e.g., `r/s`, `r/m`).                 | `string` | Yes      | `"1r/s"`                  |
| `rateLimit.id`         | Variable used to identify the client (e.g., `$binary_remote_addr`).            | `string` | Yes      | `"$binary_remote_addr"`   |
| `rateLimit.zoneSize`   | Size of the memory zone allocated for tracking limits (e.g., `10M`).            | `string` | Yes      | `"10M"`                   |
| `rateLimit.delay`      | Time (in seconds) to delay excess requests before rejecting.                   | `integer`| No       | `30`                      |
| `rateLimit.noDelay`    | If `true`, no delay is applied — excess requests are immediately dropped.       | `boolean`| No       | `false`                   |
| `rateLimit.burst`      | Number of requests allowed to exceed the rate in a burst.                      | `integer`| No       | `8`                       |
| `rateLimit.logLevel`   | Log level for rate-limit rejections.                                            | `string` | No       | `"info"`                  |
| `rateLimit.dryRun`     | If `true`, requests are not rejected, but logging occurs as if they were.       | `boolean`| No       | `true`                    |
| `rateLimit.rejectCode` | HTTP status code to return when requests are rejected.                          | `integer`| No       | `429`, `503`, `504`       |


> [!IMPORTANT]
> - Defines a rate-limiting zone using limit_req_zone.
> - Applies throttling based on the id (typically the client IP).
> - If the request rate exceeds the limit:
>   - Burst requests are temporarily allowed (up to `burst` value).
>   - Requests can be delayed or rejected based on `noDelay`.
> - If `dryRun` is `true`, requests are not blocked, but violations are logged.
> - `rejectCode` allows custom HTTP responses when limits are hit (defaults to `503` if not set).


```yml
spec:
  rateLimit:
    name: default
    rate: 1r/s
    id: $binary_remote_addr
    zoneSize: 10M
    delay: 30
    noDelay: false
    burst: 8
    logLevel: info
    dryRun: true
    rejectCode: 504
```



## Spec.upstreams

The upstreams field defines one or more backend server groups that the NGINX server block will forward traffic to. Each upstream contains a list of servers, load balancing settings, timeouts, buffering, queueing, TLS options, health checks, and session persistence.

You can think of each upstream as a named cluster of backend endpoints with its own logic for routing, retries, stickiness, and fault tolerance.

| Field| Description| Type| Required | Examples|
|------|------------|-----|----------|---------|
| `name`                      | Unique name for the upstream group. Referenced by `routes.proxy.upstream`.                      | `string` | Yes  | `"backend_v1"`|
| [servers](#specupstreamsservers)                   | List of backend server addresses and per-server settings.     | `array` of `object`   | Yes  | See `servers` section            |
| `lb_method`             | Load balancing method (e.g., `round_robin`, `least_conn`).                  | `string` | No | `"least_conn"` |
| `connect_timeout`       | Max time to wait for a connection to a backend.                        | `string` | No | `"30s"`|
| `read_timeout`          | Max time to wait for a response from the backend.                       | `string` | No | `"30s"`|
| `send_timeout`          | Max time to wait when sending a request to the backend.                  | `string` | No | `"30s"`|
| `zone_size`             | Shared memory size for load balancing state.                            | `string` or `int` | No | `"512k"` |
| `buffering`             | Enable or disable proxy buffering.                                    | `boolean` | No | `true`, `false`|
| `buffer_size`           | Size of the proxy buffer for reading responses.                     | `string` | No | `"32k"` |
| `buffers.number`        | Number of proxy buffers.                                         | `integer` | No | `4` |
| `buffers.size`          | Size of each proxy buffer.                            | `string` | No | `"8k"` |
| `client_max_body_size`  | Max size of the request body accepted by this upstream.     | `string` | No | `"1m"` |
| `tls.enable`            | If `true`, connect to the upstream using HTTPS.     | `boolean` | No | `false` |
| `queue.size`            | Max number of requests to queue when all upstream servers are busy.   | `integer` | No | `30` |
| `queue.timeout`         | Time a request can wait in the queue before timing out.    | `string` | No | `"60s"` |
| [healthcheck](#specupstreamshealthcheck) | Health check configuration to monitor upstream availability.   | `object` | No | See `healthcheck` section      |
| [sessioncookie](#specupstreamssessioncookie) | Configuration for session stickiness.    | `string` | No | See `sessionCookie`  section|


> [!IMPORTANT]
> - Each upstream defines a **named pool of servers** with rules for how traffic is distributed.
> - Traffic is proxied to these servers based on route configuration (e.g., `proxy.upstream: backend_v1`).
> - Load balancing, timeouts, buffer limits, and body size restrictions can all be tuned here.
> - When `tls.enable: true`, NGINX proxies traffic to the upstream using HTTPS.
> - `sessioncookie` allows session stickiness, ensuring a client consistently hits the same backend.
> - `queue` lets you queue up requests when all upstreams are busy — useful for spike protection.
> - `healthcheck` allows proactive removal of unhealthy servers from the load balancing rotation.
> - DNS `resolve` support with `service` name mapping
> - Upstream servers can have per-server overrides like:
>   - `weight`: traffic weighting
>   - `slow_start`: gradual ramp-up
>   - `fail_timeout`, `max_fails`, `max_conns`
>   - `backup` and `down` flags


```yml
spec:
  upstreams:
    - name: backend_v1
      lb_method: least_conn
      connect_timeout: 30s
      read_timeout: 30s
      send_timeout: 30s
      buffering: true
      buffer_size: 32k
      buffers:
        number: 4
        size: 8k
      client_max_body_size: 1m
      tls:
        enable: false
      sessioncookie:
        name: srv_id
        path: /
        expires: 1h
        domain: .example.com
        httponly: true
        secure: true
        samesite: strict
      queue:
        size: 30
        timeout: 60s
      servers:
        - address: backend1.example.com
        - address: backend2.example.com
```

## Spec.upstreams.servers
The `servers` field defines the individual backend servers within an upstream. Each entry represents a host (or IP) that will receive proxied traffic. You can assign per-server settings like weight, failure handling, backup role, and DNS resolution options.


| Field| Description| Type| Required | Examples|
|------|------------|-----|----------|---------|
| `address`        | Hostname or IP address of the backend server.                              | `string` | Yes | `"backend1.example.com"`           |
| `weight`         | Relative weight used for load balancing.                                   | `integer`| No | `5`                                |
| `slow_start`     | Time period during which traffic ramps up after a server becomes available. | `string` | No | `"60s"`                            |
| `fail_timeout`   | Time to wait before retrying a failed server.                              | `string` | No | `"10s"`                            |
| `max_fails`      | Max number of failed attempts before considering the server unavailable.   | `integer`| No | `3`                                |
| `max_conns`      | Maximum number of concurrent connections allowed to this server.           | `integer`| No | `10`                               |
| `backup`         | If `true`, this server is only used when primary servers are unavailable.  | `boolean`| No | `true`                             |
| `down`           | If `true`, the server is treated as permanently down.                      | `boolean`| No | `true`                             |
| `resolve.enable` | Enables DNS resolution for the server address.                             | `boolean`| No | `true`                             |
| `resolve.service`| DNS SRV service name for dynamic endpoint discovery.                       | `string` | No | `"http.tcp"`                       |

> [!IMPORTANT]
> - Each server in the list is a valid backend endpoint for the upstream.
> - weight impacts how often this server is chosen.
> - slow_start gradually ramps up traffic after recovery to prevent sudden load spikes.
> - fail_timeout + max_fails define failure handling before marking a server as temporarily down.
> - Use backup to designate fallback servers.
> - Use resolve to support DNS-based service discovery (great for service mesh or dynamic backends).

**Example:**

```yml
spec:
  upstreams:
    - name: backend_v1
      servers:
        - address: backend1.example.com
          weight: 5
          slow_start: 60s
          max_fails: 2
          max_conns: 10
        - address: backend2.example.com
          backup: true
        - address: backend3.example.com
          down: true
          resolve:
            enable: true
            service: http.tcp
```

## Spec.upstreams.sessioncookie

The sessioncookie field enables session stickiness, ensuring the same client always connects to the same upstream server during a session. This is useful for maintaining user state in applications that don’t share sessions across nodes.

NGINX accomplishes this using a cookie, which is automatically set on the client side.

| Field         | Description                                                      | Type     | Required | Examples               |
|---------------|------------------------------------------------------------------|----------|----------|------------------------|
| `name`        | Name of the cookie used to persist sessions.                    | `string` | Yes      | `"srv_id"`             |
| `path`        | Cookie path restriction. Defaults to `/` if not set.            | `string` | No       | `"/"`                  |
| `expires`     | Cookie lifetime (e.g., 1h, 30m).                                 | `string` | No       | `"1h"`                 |
| `domain`      | Domain scope for the cookie.                                     | `string` | No       | `".example.com"`       |
| `httponly`    | Prevents client-side JavaScript from reading the cookie.         | `boolean`| No       | `true`                 |
| `secure`      | Ensures the cookie is sent over HTTPS only.                     | `boolean`| No       | `true`                 |
| `samesite`    | Controls cookie sharing across sites (`strict`, `lax`, `none`). | `string` | No       | `"strict"`             |

> [!IMPORTANT]
> - Adds a sticky cookie to client responses (e.g., Set-Cookie: srv_id=abc123).
> - NGINX uses the cookie value to consistently route the client to the same upstream.
> - Improves user experience and reduces cross-server state issues.
> - Set secure, httponly, and samesite for better security posture.

**Example:**
```yml
spec:
  upstreams:
    - name: backend_v1
      sessioncookie:
        name: srv_id
        path: /
        expires: 1h
        domain: .example.com
        httponly: true
        secure: true
        samesite: strict
```

## Spec.upstreams.healthcheck

The `healthcheck` field defines **proactive health monitoring** for upstream servers. It allows NGINX to detect and avoid unhealthy backends by regularly probing a specific URL and checking its response.

This helps improve reliability by routing traffic only to responsive and healthy endpoints.

| Field| Description| Type| Required | Examples|
|------|------------|-----|----------|---------|
| `path`           | URI to probe for health (e.g., `/healthz`).                                      | `string` | No       | `"/healthz"`                |
| `interval`       | How often the health check runs.                                                 | `string` | No       | `"20s"`                     |
| `jitter`         | Adds randomness to health check timing to avoid sync issues.                     | `string` | No       | `"3s"`                      |
| `fails`          | Number of failed checks before marking a server unhealthy.                       | `integer`| No       | `3`                         |
| `passes`         | Number of successful checks to recover a previously failed server.               | `integer`| No       | `2`                         |
| `port`           | Port used for health checks (if different from main traffic).                    | `integer`| No       | `8080`                      |
| `tls.enable`     | Enable TLS for health checks.                                                    | `boolean`| No       | `true`                      |
| `connect_timeout`| Max time to establish a connection for the check.                                | `string` | No       | `"10s"`                     |
| `read_timeout`   | Max time to wait for a response.                                                 | `string` | No       | `"10s"`                     |
| `send_timeout`   | Max time to send the request body (if any).                                      | `string` | No       | `"10s"`                     |
| `headers.name`   | Request header name.                                                             | `string` | No       | `"Host"`                    |
| `headers.value`  | Request header value.                                                            | `string` | No       | `"my.service"`              |
| `match.status`   | Match condition on HTTP status (e.g., `! 500`).                                  | `string` | No       | `"! 500"`                   |
| `match.header`   | Match condition on response header (e.g., `! Refresh;`).                         | `string` | No       | `"! Refresh;"`              |
| `match.body`     | Regex match on response body content.                                            | `string` | No       | `"~ \"OK\""`                |
| `mandatory`      | If `true`, the entire upstream is disabled if check fails.                       | `boolean`| No       | `true`                      |
| `persistent`     | Keeps connection open between checks.                                            | `boolean`| No       | `true`                      |
| `keepalive_time` | Duration to keep connections alive.                                              | `string` | No       | `"60s"`                     |

[!IMPORTANT]
> - Health checks occur at the configured interval.
> - `fails` defines how many times in a row a health check must fail so that it will be marked unhealthy and excluded from load balancing.
> - It must pass `passes` checks to be marked healthy again.
> - Optional `match` rules make checks more precise (e.g., specific response headers or content).
> - `mandatory`: true disables the entire upstream group if health check fails.
> - `persistent` and `keepalive_time` improve performance by reusing connections.

**Example:**
```yml
healthcheck:
  path: /healthz
  interval: 20s
  fails: 3
  passes: 2
  port: 8080
  tls:
    enable: true
  connect_timeout: 10s
  read_timeout: 10s
  send_timeout: 10s
  headers:
    - name: Host
      value: my.service
  match:
    status: "! 500"
    header: "! Refresh;"
    body: "~ \"Service OK\""
  mandatory: true
  persistent: true
  keepalive_time: 60s
```
<br>
<br>

## Spec.routes

The routes field defines a list of path-based routing rules within a server block configuration. Each route determines how NGINX should process requests that match a specific URL path — whether by proxying to an upstream, redirecting, returning a static response, conditionally matching, or splitting traffic.

Each route must include a path, and then one of the supported actions:

> - `proxy` – forward requests to an upstream
> - `redirect` – redirect to another URL
> - `return` – respond directly with a custom message
> - `matches` – apply logic based on headers, cookies, etc.
> - `splits` – divide traffic across upstreams based on weight

| Field| Description| Type| Required | Examples|
|------|------------|-----|----------|---------|
| `path`           | The request URI path to match (e.g., `/api`, `/login`). Must start with `/`.                    | `string`           | Yes      | `"/api"`                   |
| `proxy`          | Defines the upstream and request handling logic for forwarding the request.                     | `object`             | Conditional | See `proxy` section       |
| `redirect`       | Sends an HTTP redirect response to the client.                                                  | `object`             | Conditional | See `redirect` section    |
| `return`         | Immediately returns a custom response to the client.                                            | `object`             | Conditional | See `return` section      |
| `matches`        | Allows routing decisions based on header/cookie/variable conditions.                            | `array` of `objects`   | Conditional | See `matches` section     |
| `splits`         | Enables weighted traffic splitting between upstreams.                                           | `array` of `objects`   | Conditional | See `splits` section      |
| `location_snippets` | Raw NGINX directives to inject inside this location block.                                   | `string`             | No       | `"limit_conn conn 5;"`    |
| `errorpages`     | Custom error response overrides for this route.                                                 | `array` of `objects`   | No       | See `errorpages` section |


> [!IMPORTANT]
> - Every route must define a path — this is the URI prefix that triggers the route logic.
> - A route can only define one action type: `proxy`, `redirect`, `return`, `matches`, or `splits`.
> - Routing precedence is based on the order in which routes are listed.
> - `location_snippets` lets you customize route-level directives (e.g., rate limits, logging).
> - `errorpages` allows defining route-specific error overrides (e.g., custom 404 handler).
> - If multiple routes match a request, only the first match is applied.
<br>
<br>

## Spec.routes.proxy
The proxy field is used to forward incoming requests to an upstream server group defined under spec.upstreams. This is the most common routing action in NGINX configurations and serves as the foundation for reverse proxy behavior.

The proxy object supports additional controls like path rewriting, header manipulation (request/response), and selective visibility of upstream headers.


| Field| Description| Type| Required | Examples|
|------|------------|-----|----------|---------|
| `upstream`                       | Name of the upstream to which the request should be proxied. Must match a `spec.upstreams.name`.        | `string`           | Yes      | `"backend_v1"`                            |
| `rewritepath`                    | Rewrites the request URI before sending it to the upstream.                                              | `string`           | No       | `"/api"` → `"/v1"`                        |
| `requestheaders.pass_origin_headers` | If `true`, passes original client request headers to the upstream.                                      | `boolean`          | No       | `true`                                     |
| `requestheaders.set`            | A list of custom headers to add or override in the request sent to the upstream.                        | `array` of `objects`   | No       | See example below|
| `responseheaders.add`           | A list of custom response headers to add in responses back to the client.                               | `array` of `objects`   | No       |  See example below   |
| `responseheaders.hide`          | A list of upstream response headers to remove before passing to the client.                             | `array` of `objects`   | No       | `name: "X-Powered-By`                |
| `responseheaders.pass`          | A list of upstream response headers to explicitly pass to the client.                                   | `array` of `objects`   | No       | `name: "Content-Type"`                |
| `responseheaders.ignore`        | A list of restricted headers (e.g., `Cache-Control`, `Set-Cookie`) that NGINX should ignore.            | `array` of `objects`   | No       | `name: "Set-Cookie"`                  |


[!IMPORTANT]
> - The `upstream` value must match a defined entry in `spec.upstreams`.
> - `rewritepath` replaces the URI sent to the backend (e.g., `/api` → `/v1`).
> - By default, most original request headers are passed through — but `pass_origin_headers: true` ensures completeness.
> - `set` allows injection of custom headers, like request IDs, auth tokens, or user context.
> - `responseheaders.add` enriches the response with headers (e.g., versioning, flags).
> - `hide` removes potentially sensitive upstream headers before they reach the client.
> - `ignore` suppresses standard NGINX-controlled headers (like Set-Cookie, Cache-Control) if needed.
> -  This configuration gives you full control over **both upstream and downstream header behavior**, making it suitable for internal APIs, secured backends, or third-party integrations.


**Example:**
```yml
spec:
  routes:
    - path: /api
      proxy:
        upstream: backend_v1
        rewritepath: /v1
        requestheaders:
          pass_origin_headers: true
          set:
            - name: X-Request-ID
              value: $request_id
        responseheaders:
          add:
            - name: X-App-Version
              value: "v2"
          hide:
            - name: X-Powered-By
          pass:
            - name: Content-Type
          ignore:
            - name: Set-Cookie
```
<br>
<br>

## Spec.routes.redirect

The `redirect` field configures an **HTTP redirect response** for incoming requests matching the route's `path`. This is useful for rerouting outdated URLs, migrating endpoints, or enforcing trailing slashes or HTTPS.

You can control both the **target URL** and the **status code** used for the redirect.


| Field| Description| Type| Required | Examples|
|------|------------|-----|----------|---------|
| `url`       | The destination URL or path to redirect the request to.                    | `string` | Yes      | `"/new-url"`, `"https://site.com"`|
| `code`      | The HTTP status code for the redirect. Must be one of: 301, 302, 303, 307, 308. | `integer`| No       | `301`, `302`                      |

[!IMPORTANT]
> - `url` can be relative (`/new`) or absolute (`https://example.com/new`).
> - If `code` is omitted, it defaults to 301 (permanent).
> - NGINX uses the `return` directive behind the scenes to issue the redirect.
> - You can use this to implement trailing slash policies, legacy URL rewrites, or protocol upgrades.

**Example:**

```yaml
spec:
  routes:
    - path: /old
      redirect:
        url: /new
        code: 301
```
<br>
<br>


## Spec.routes.return
The `return` field allows the route to **immediately respond with a custom response**, without forwarding or redirecting. This is ideal for status checks (like `/ping`), custom error pages, or mock responses.

You can customize the **status code**, **content type**, **body**, and even **response headers**.


| Field| Description| Type| Required | Examples|
|------|------------|-----|----------|---------|
| `code`         | HTTP status code to return (100–599).                                      | `integer`      | No       | `200`, `404`, `503`          |
| `type`         | MIME type of the response body.                                             | `string`       | No       | `"text/plain"`, `"application/json"` |
| `body`         | The content to return in the response body.                                | `string`       | Yes      | `"pong"`, `"{\"status\": \"ok\"}"` |
| `headers`      | Optional list of headers to include in the response.                       | `array` of `objects` | No       | See examples below |


> [!IMPORTANT]
> - If `code` is not provided, NGINX defaults to 200 OK.
> - `type` sets the Content-Type of the response. If omitted, NGINX will try to infer it.
> - `headers` allows adding custom response headers (e.g., version tags, metadata).
> - No upstream communication or route matching happens — this ends the request immediately.
> - Perfect for health checks, mocking endpoints, under-construction pages, or legal notices.


**Example:**
```yml
spec:
  routes:
    - path: /ping
      return:
        code: 200
        type: text/plain
        body: "pong"
        headers:
          - name: X-Server
            value: nginx
```

## Spec.routes.matches

The `matches` field enables **conditional routing logic** based on request metadata — such as HTTP headers, cookies, or NGINX variables (e.g., method or query parameters). When a match condition is met, the request is handled using the specified `proxy` configuration.

| Field| Description| Type| Required | Examples|
|------|------------|-----|----------|---------|
| `condition.header`  | Name of the HTTP header to match.                              | `string` | Conditional | `"X-User-Type"`               |
| `condition.cookie`  | Name of the cookie to match.                                   | `string` | Conditional | `"session_id"`                |
| `condition.variable`| Name of an NGINX variable to evaluate (e.g., `$request_method`).| `string` | Conditional | `"$request_method"`            |
| `condition.value`   | Expected value to match.                                       | `string` | Yes      | `"admin"`, `"POST"`               |
| [condition.proxy](#specroutesproxy)   | Proxy configuration to apply when the condition matches.       | object   | Yes      | See `routes.proxy` section               |


[!IMPORTANT]
> - Conditions are evaluated in **order**, and the first match is applied.
> - Each condition block must include only one of `header`, `cookie`, or `variable`, plus a `value` and `proxy`.
> - Matching is based on **exact string comparison**.
> - If no conditions match, the route does **not fallback** to another action — the request proceeds with default route behavior (if defined).

**Example:**
```yaml
spec:
  routes:
    - path: /secure
      matches:
        - condition:
            header: X-User-Type
            value: admin
            proxy:
              upstream: admin_backend
        - condition:
            cookie: user_id
            value: 123
            proxy:
              upstream: special_user_backend
```
<br>
<br>


## Spec.routes.splits

The `splits` field allows you to **distribute traffic across multiple upstreams** based on defined weights. This is ideal for **canary deployments**, **A/B testing**, or **progressive rollouts**.


| Field       | Description                                                  | Type     | Required | Examples               |
|-------------|--------------------------------------------------------------|----------|----------|------------------------|
| `weight`    | Percentage of traffic to route to this proxy (0–100).       | integer  | Yes      | `80`, `20`             |
| [proxy](#specroutesproxy)     | The proxy configuration to apply for this weighted split.   | object   | Yes      | See `routes.proxy` section    |

[!IMPROTANT]
> - The total of all weight values should add up to 100.
> - NGINX randomly selects the backend for each request based on the weight.
> - Enables low-risk rollouts and feature experimentation with real traffic.
> - Works well with session stickiness for consistent experiences per user.

**Example:**
```yaml
spec:
  routes:
    - path: /login
      splits:
        - weight: 90
          proxy:
            upstream: stable_backend
        - weight: 10
          proxy:
            upstream: canary_backend
```
<br>
<br>

## Spec.routes.errorpages

The `errorpages` field allows you to **override default error handling** for specific status codes within a route. You can define custom **redirects** or **returns** for one or more HTTP error codes (e.g., `404`, `500`, `502`).

| Field| Description| Type| Required | Examples|
|------|------------|-----|----------|---------|
| `codes`      | List of HTTP status codes this error page applies to.       | array of int    | Yes      | `[404, 500]`                 |
| `redirect.url` | URL to redirect to for the error.                          | string          | Conditional | `"/custom-404"`          |
| `redirect.code`| Redirect status code (301, 302, 303, 307, 308).            | integer         | No       | `302`                        |
| `return.code`  | Status code for static response.                           | integer         | No       | `404`, `503`                 |
| `return.type`  | MIME type of the body.                                     | string          | No       | `"text/plain"`               |
| `return.body`  | Response body to send.                                     | string          | Yes      | `"Page not found"`           |
| `return.headers` | Optional headers to include in the error response.      | array of object | No       | `{ name: "X-Error", value: "true" }` |

> [!IMPORTANT]
> - Each rule applies to one or more status codes.
> - You must define **either** `redirect` or `return`, but not both.
> - `return` can include content and headers — useful for debugging or soft failover.
> - `redirect` points users to a fallback page or external help page.


**Example:**

```yaml
spec:
  routes:
    - path: /demo
      proxy:
        upstream: demo_backend
      errorpages:
        - codes: [404]
          return:
            code: 404
            type: text/plain
            body: "Custom 404 page"
        - codes: [500]
          redirect:
            url: /error
            code: 302
```
<br>
<br>

## Spec.routes.location_snippets

The `location_snippets` field allows you to **inject custom NGINX directives** into a route's generated `location` block. This is useful for fine-tuning settings like rate limiting, logging, connection limits, etc., on a per-route basis.


| Field| Description| Type| Required | Examples|
|------|------------|-----|----------|---------|
| `location_snippets` | NGINX directives to inject directly into the route’s `location` block. | `string` | No       | `"limit_conn addr 10;"` |

> [!IMPORTANT]
> - ⚠️ Use with care. Improper or conflicting directives can break configuration or override default logic.
> - Injects raw text after the location block is opened and before it closes.
> - Accepts any valid NGINX directive allowed in a location context.
> - Should not conflict with what the main schema generates (e.g., duplicate proxy_pass).

**Example:**

```yaml
spec:
  routes:
    - path: /rate-limited
      proxy:
        upstream: backend
      location_snippets: |
        limit_conn addr 10;
        limit_req zone=default burst=5 nodelay;
```




