# HTTP Status Codes Table

| Status Code | Category               | Description                                                                           |
|-------------|------------------------|---------------------------------------------------------------------------------------|
| **100**     | Informational (1xx)     | Continue: The client should continue with its request.                                |
| **101**     | Informational (1xx)     | Switching Protocols: Server is switching protocols.                                   |
| **102**     | Informational (1xx)     | Processing (WebDAV): Server has received and is processing the request.               |
| **200**     | Success (2xx)           | OK: The request was successful.                                                       |
| **201**     | Success (2xx)           | Created: The request was successful and a resource was created.                       |
| **202**     | Success (2xx)           | Accepted: The request has been accepted for processing.                               |
| **203**     | Success (2xx)           | Non-Authoritative Information: The server is a proxy, not the original.               |
| **204**     | Success (2xx)           | No Content: The server successfully processed the request, but no content is returned.|
| **205**     | Success (2xx)           | Reset Content: The client should reset the view.                                      |
| **206**     | Success (2xx)           | Partial Content: The server is delivering part of the resource (range requests).       |
| **300**     | Redirection (3xx)       | Multiple Choices: Multiple options for the resource are available.                    |
| **301**     | Redirection (3xx)       | Moved Permanently: The resource has moved permanently to a new URI.                   |
| **302**     | Redirection (3xx)       | Found: The resource is temporarily at a different URI.                                |
| **303**     | Redirection (3xx)       | See Other: The response is at another URI.                                            |
| **304**     | Redirection (3xx)       | Not Modified: The resource has not been modified since the last request.              |
| **305**     | Redirection (3xx)       | Use Proxy: The requested resource is available only through a proxy.                  |
| **307**     | Redirection (3xx)       | Temporary Redirect: The resource resides temporarily at a different URI.              |
| **308**     | Redirection (3xx)       | Permanent Redirect: The resource has moved permanently, and this URI should be used.  |
| **400**     | Client Errors (4xx)     | Bad Request: The server could not understand the request due to invalid syntax.       |
| **401**     | Client Errors (4xx)     | Unauthorized: Authentication is required and has failed.                              |
| **402**     | Client Errors (4xx)     | Payment Required: Reserved for future use.                                            |
| **403**     | Client Errors (4xx)     | Forbidden: The request was understood but refuses to authorize it.                    |
| **404**     | Client Errors (4xx)     | Not Found: The resource could not be found.                                           |
| **405**     | Client Errors (4xx)     | Method Not Allowed: The request method is not supported for the resource.             |
| **406**     | Client Errors (4xx)     | Not Acceptable: The resource cannot produce content acceptable to the client.         |
| **407**     | Client Errors (4xx)     | Proxy Authentication Required: The client must authenticate with the proxy first.     |
| **408**     | Client Errors (4xx)     | Request Timeout: The server timed out waiting for the request.                        |
| **409**     | Client Errors (4xx)     | Conflict: The request could not be processed because of a conflict.                   |
| **410**     | Client Errors (4xx)     | Gone: The resource is no longer available.                                            |
| **411**     | Client Errors (4xx)     | Length Required: The request did not specify the length.                              |
| **412**     | Client Errors (4xx)     | Precondition Failed: The preconditions set by the client were not met.                |
| **413**     | Client Errors (4xx)     | Payload Too Large: The request is too large to process.                               |
| **414**     | Client Errors (4xx)     | URI Too Long: The URI provided was too long for the server to process.                |
| **415**     | Client Errors (4xx)     | Unsupported Media Type: The media type of the request is not supported.               |
| **416**     | Client Errors (4xx)     | Range Not Satisfiable: The client requested a portion that cannot be supplied.        |
| **417**     | Client Errors (4xx)     | Expectation Failed: The server cannot meet the expectation of the request.            |
| **418**     | Client Errors (4xx)     | I'm a teapot (RFC 2324): An April Fools' joke code.                                   |
| **421**     | Client Errors (4xx)     | Misdirected Request: The request was directed at a wrong server.                      |
| **422**     | Client Errors (4xx)     | Unprocessable Entity (WebDAV): The request was well-formed but semantic errors exist. |
| **423**     | Client Errors (4xx)     | Locked (WebDAV): The resource being accessed is locked.                               |
| **424**     | Client Errors (4xx)     | Failed Dependency (WebDAV): A previous request failed, causing this one to fail.      |
| **425**     | Client Errors (4xx)     | Too Early: The server is unwilling to process this request yet.                       |
| **426**     | Client Errors (4xx)     | Upgrade Required: The client needs to switch to a different protocol.                 |
| **428**     | Client Errors (4xx)     | Precondition Required: The server requires the request to be conditional.             |
| **429**     | Client Errors (4xx)     | Too Many Requests: Too many requests sent in a given amount of time.                  |
| **431**     | Client Errors (4xx)     | Request Header Fields Too Large: The request's header fields are too large.           |
| **451**     | Client Errors (4xx)     | Unavailable For Legal Reasons: The resource is unavailable for legal reasons.         |
| **500**     | Server Errors (5xx)     | Internal Server Error: An unexpected server error occurred.                           |
| **501**     | Server Errors (5xx)     | Not Implemented: The server lacks the ability to fulfill the request.                 |
| **502**     | Server Errors (5xx)     | Bad Gateway: Received an invalid response from the upstream server.                   |
| **503**     | Server Errors (5xx)     | Service Unavailable: The server is overloaded or down for maintenance.                |
| **504**     | Server Errors (5xx)     | Gateway Timeout: No timely response from the upstream server.                         |
| **505**     | Server Errors (5xx)     | HTTP Version Not Supported: The server does not support the HTTP version.             |
| **506**     | Server Errors (5xx)     | Variant Also Negotiates: Internal configuration error.                                |
| **507**     | Server Errors (5xx)     | Insufficient Storage (WebDAV): The server cannot store the representation.            |
| **508**     | Server Errors (5xx)     | Loop Detected (WebDAV): The server detected an infinite loop while processing.        |
| **510**     | Server Errors (5xx)     | Not Extended: Extensions are required for the server to fulfill the request.          |
| **511**     | Server Errors (5xx)     | Network Authentication Required: Client must authenticate to gain network access.     |

---

# Docker Image Layers

A **Docker image** is composed of multiple layers that work together to create a fully functional container. Each layer represents a step in the build process, and layers are stacked on top of one another to form the complete image.

### Structure of a Docker Image:

1. **BootFS (Boot File System):**
   - **Description:** This is the bottom-most layer in the Docker image. It includes files and directories needed to boot up a system.
   - **Function:** It sets up the foundation for the base operating system within the container, similar to the host machine’s `/boot` folder.

2. **Base Image:**
   - **Description:** The base image is typically a minimal operating system (e.g., Ubuntu, Alpine Linux) or any other image that acts as a starting point for your container.
   - **Examples:** Ubuntu, Alpine, Debian.
   - **Function:** Provides the core OS functionalities and dependencies needed for the higher layers.

3. **Libraries:**
   - **Description:** Libraries required by the applications running in the container.
   - **Examples:** libc, libssl, or any other standard libraries needed by the applications.
   - **Function:** Provides necessary functionality for applications, ensuring they can function correctly within the container.

4. **Packages and Applications:**
   - **Description:** Specific software, tools, or libraries that your application depends on.
   - **Examples:** vim, curl, git, node.js, or custom software required by your application.
   - **Function:** These packages allow you to run applications and scripts necessary for the container's purpose.

5. **User Application (Optional):**
   - **Description:** The main application code that you intend to run within the container.
   - **Examples:** A web server like Apache, Nginx, or any microservice application.
   - **Function:** It is the purpose of the container, which could be serving web traffic, processing data, or any other specific task.

### Writable Layer (Container-Specific):

- **Description:** Once a container is created from a Docker image, a writable layer is added on top of the image layers.
- **Function:** Any changes made during the container's runtime (like creating files or modifying configurations) are stored in this writable layer.
- **Key Point:** Changes to the writable layer do not impact the underlying image layers.

---
