# OpenSSL Command Reference for Self-Signed Certificate Generation

This document explains the OpenSSL command-line tool and provides a structured, DevOps-friendly guide for generating self-signed SSL/TLS certificates. These certificates are commonly used for internal services, development environments, testing, or private infrastructure components such as Gitea, Jenkins, internal APIs, or Kubernetes ingress controllers.

---

## 1. What is OpenSSL?

**OpenSSL** is a widely used, open-source cryptographic toolkit that implements the SSL and TLS protocols. It provides utilities for:

* Generating private and public key pairs
* Creating Certificate Signing Requests (CSRs)
* Issuing and managing X.509 certificates
* Encrypting and decrypting data
* Inspecting and troubleshooting TLS connections

OpenSSL is available on most Linux distributions by default and is commonly used in DevOps and SRE workflows.

Check installed version:

```bash
openssl version
```

---

## 2. When to Use Self-Signed Certificates

Self-signed certificates are suitable for:

* Internal services
* Development and staging environments
* Private networks
* Lab and proof-of-concept setups

They are **not recommended for public-facing production systems**, because they are not trusted by browsers or external clients without manual trust configuration.

---

## 3. Generating a Self-Signed Certificate (Example: Gitea)

This process consists of three logical steps:

1. Generate a private key
2. Create a Certificate Signing Request (CSR)
3. Sign the CSR using the same key to produce a self-signed certificate

---

## 4. Step 1: Generate a Private Key

Generate a 2048-bit RSA private key:

```bash
openssl genrsa -out gitea.key 2048
```

### Explanation

| Component        | Description                                        |
| ---------------- | -------------------------------------------------- |
| `genrsa`         | Generates an RSA private key                       |
| `-out gitea.key` | Output file for the private key                    |
| `2048`           | Key size in bits (2048 is the recommended minimum) |

Security note:

* The private key must be kept secret
* Restrict file permissions:

```bash
chmod 600 gitea.key
```

---

## 5. Step 2: Create a Certificate Signing Request (CSR)

Generate a CSR using the private key:

```bash
openssl req -new -key gitea.key -out gitea.csr
```

### Explanation

| Component        | Description                              |
| ---------------- | ---------------------------------------- |
| `req`            | Certificate request management command   |
| `-new`           | Creates a new CSR                        |
| `-key gitea.key` | Private key used to generate the request |
| `-out gitea.csr` | Output file for the CSR                  |

### Interactive Fields

During execution, OpenSSL prompts for certificate metadata:

* Country Name (C)
* State or Province (ST)
* Locality (L)
* Organization (O)
* Organizational Unit (OU)
* **Common Name (CN)**

Important:

* The **Common Name (CN)** should match the service hostname or domain name
  Example:

  ```
  gitea.example.com
  ```

For automation or CI/CD pipelines, this step can be made non-interactive (see section 8).

---

## 6. Step 3: Create the Self-Signed Certificate

Sign the CSR using the same private key:

```bash
openssl x509 -req -in gitea.csr -signkey gitea.key -out gitea.crt
```

### Explanation

| Component            | Description                                |
| -------------------- | ------------------------------------------ |
| `x509`               | X.509 certificate management               |
| `-req`               | Indicates the input is a CSR               |
| `-in gitea.csr`      | Input CSR file                             |
| `-signkey gitea.key` | Signs the certificate with the private key |
| `-out gitea.crt`     | Output certificate file                    |

Default behavior:

* Certificate is valid immediately
* Validity is typically 30 days unless specified

To set validity explicitly (example: 365 days):

```bash
openssl x509 -req -days 365 -in gitea.csr -signkey gitea.key -out gitea.crt
```

---

## 7. Verify the Certificate

Inspect certificate details:

```bash
openssl x509 -in gitea.crt -text -noout
```

Verify key and certificate match:

```bash
openssl rsa -noout -modulus -in gitea.key | openssl md5
openssl x509 -noout -modulus -in gitea.crt | openssl md5
```

Matching hashes confirm correctness.

---

## 8. Non-Interactive Certificate Generation (Recommended for Automation)

Generate key and certificate in one command:

```bash
openssl req -x509 -newkey rsa:2048 \
-keyout gitea.key \
-out gitea.crt \
-days 365 \
-nodes \
-subj "/C=US/ST=State/L=City/O=Company/OU=DevOps/CN=gitea.example.com"
```

Options explained:

* `-x509`: Generate a self-signed certificate
* `-newkey`: Create a new private key
* `-nodes`: Do not encrypt the private key (required for services)
* `-subj`: Certificate subject (non-interactive)

This approach is ideal for:

* CI/CD pipelines
* Docker images
* Infrastructure as Code workflows

---

## 9. Subject Alternative Name (SAN) Consideration

Modern TLS clients require **SAN** instead of CN.

Example OpenSSL config snippet:

```
subjectAltName = DNS:gitea.example.com,DNS:gitea.internal
```

Without SAN:

* Browsers may reject the certificate
* TLS warnings may appear even if CN matches

---

## 10. Summary of Generated Files

| File        | Description                                          |
| ----------- | ---------------------------------------------------- |
| `gitea.key` | Private key (keep secure, server-side only)          |
| `gitea.csr` | Certificate Signing Request (optional after signing) |
| `gitea.crt` | Self-signed certificate presented to clients         |

---

## 11. Best Practices

* Never commit private keys to Git
* Store secrets securely (Vault, SSM, Kubernetes secrets)
* Rotate certificates regularly
* Use Let’s Encrypt or internal CA for production
* Prefer SAN over CN
* Automate certificate generation where possible

---

If you want, I can:

* Add an OpenSSL SAN configuration example
* Provide Kubernetes, Nginx, or Gitea-specific TLS configs
* Convert this into a reusable internal PKI guide
* Add troubleshooting and common TLS errors
