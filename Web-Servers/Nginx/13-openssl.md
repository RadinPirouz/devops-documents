## OpenSSL Command Reference for Self-Signed Certificate Generation

This document provides an overview of the `openssl` command-line tool and details the steps for generating a self-signed SSL/TLS certificate using specific commands.

---

### What is OpenSSL?

**OpenSSL** is a powerful, open-source command-line toolkit implementing the Secure Sockets Layer (SSL) and Transport Layer Security (TLS) protocols. It is widely used for generating private keys, creating Certificate Signing Requests (CSRs), managing certificates, and performing cryptographic operations.

---

### Generating a Self-Signed Certificate (Example: For Gitea)

The following sequence generates a private key, creates a CSR, and then uses the key and CSR to sign and create a self-signed certificate.

#### Step 1: Generate a Private Key

This command creates an RSA private key of 2048 bits and saves it to a file named `gitea.key`.

```bash
openssl genrsa -out gitea.key 2048
```

| Component | Description |
| :--- | :--- |
| `genrsa` | Subcommand to generate an RSA private key. |
| `-out gitea.key` | Specifies the output file for the private key. |
| `2048` | Defines the key length in bits (2048 is a common standard). |

#### Step 2: Create a Certificate Signing Request (CSR)

This command uses the generated private key (`gitea.key`) to create a Certificate Signing Request (`gitea.csr`). The CSR contains your public key and identity information (like Common Name, Organization) that a Certificate Authority (CA) would normally use to issue a trusted certificate.

```bash
openssl req -new -key gitea.key -out gitea.csr
```

| Component | Description |
| :--- | :--- |
| `req` | Subcommand used for CSR management and certificate requests. |
| `-new` | Indicates that a new CSR is being created. |
| `-key gitea.key` | Specifies the private key to be associated with this request. |
| `-out gitea.csr` | Specifies the output file for the CSR. |
| *Interactive Prompt* | OpenSSL will prompt you to enter certificate details (Country Name, Common Name, etc.). **The Common Name (CN) should usually match the domain name** where the service (e.g., Gitea) will be hosted. |

#### Step 3: Create the Self-Signed Certificate

This command takes the CSR and the private key and signs the request with the key itself, creating a certificate (`gitea.crt`) that is valid immediately but *not* trusted by default by web browsers or clients (since it's not signed by a recognized CA).

```bash
openssl x509 -req -in gitea.csr -signkey gitea.key -out gitea.crt
```

| Component | Description |
| :--- | :--- |
| `x509` | Subcommand used for X.509 certificate management (like viewing, signing, testing). |
| `-req` | Specifies that the input file is a CSR. |
| `-in gitea.csr` | Specifies the input CSR file. |
| `-signkey gitea.key` | Uses the private key to sign the certificate request, making it self-signed. |
| `-out gitea.crt` | Specifies the output file for the final certificate. |

---

### Summary of Generated Files

1.  **`gitea.key`**: The **Private Key**. Must be kept secret and secure. Used by the server (e.g., Gitea) to decrypt incoming traffic.
2.  **`gitea.csr`**: The **Certificate Signing Request**. Contains identifying information and the public key. (Not strictly needed after Step 3).
3.  **`gitea.crt`**: The **Self-Signed Certificate**. Contains the public key and identity details, signed by your private key. This is what the server presents to clients.