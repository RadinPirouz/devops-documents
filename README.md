# DevOps Knowledge Base

A personal, practical reference for Linux administration, infrastructure, and DevOps workflows. Step-by-step guides, real-world configs, and ready-to-use scripts — organized by topic so you can jump straight to what you need.

**Philosophy:** minimal theory, maximum application. Copy-paste friendly, tested in real environments.

---

## Quick Start

```bash
git clone https://github.com/RadinPirouz/devops-documents.git
cd devops-documents
```

1. Browse the categories below and open the relevant folder.
2. Read the `.md` guides or inspect configs/scripts before running anything.
3. Adjust variables (hostnames, paths, credentials) to match your environment.

> Most guides are tested on **Debian/Ubuntu** and **CentOS/RHEL**. Always review configs and test in staging before production.

---

## Contents

### Linux

| Topic | Path |
| --- | --- |
| Basic Administration | [Linux/Basic-Administration](./Linux/Basic-Administration/) |
| Advanced Administration | [Linux/Advanced-Administration](./Linux/Advanced-Administration/) |
| Bash Scripting | [Linux/Bash-Script](./Linux/Bash-Script/) |
| File Sync (rsync) | [Linux/File-Synchronization](./Linux/File-Synchronization/) |
| Terminal Multiplexers | [Linux/Terminal-Multiplexers](./Linux/Terminal-Multiplexers/) |

### Containers & Orchestration

| Topic | Path |
| --- | --- |
| Docker | [Containerization-Orchestration/Docker](./Containerization-Orchestration/Docker/) |
| Kubernetes | [Containerization-Orchestration/Kubernetes](./Containerization-Orchestration/Kubernetes/) |
| Dozzle | [Containerization-Orchestration/Tools/Dozzle](./Containerization-Orchestration/Tools/Dozzle/) |

### Configuration & Automation

| Topic | Path |
| --- | --- |
| Ansible | [Configuration-Management-Automation/Ansible](./Configuration-Management-Automation/Ansible/) |
| Cron Jobs | [Security-Networking/CronJob](./Security-Networking/CronJob/) |

### Cloud

| Topic | Path |
| --- | --- |
| AWS | [AWS](./AWS/) |

### Databases & Caching

| Topic | Path |
| --- | --- |
| PostgreSQL | [Databases/Postgresql](./Databases/Postgresql/) |
| MariaDB | [Databases/Mariadb](./Databases/Mariadb/) |
| Redis | [Caching/redis](./Caching/redis/) |

### Web Servers

| Topic | Path |
| --- | --- |
| Nginx | [Web-Servers/Nginx](./Web-Servers/Nginx/) |
| Certbot | [Web-Servers/CertBot](./Web-Servers/CertBot/) |
| Nextcloud | [Web-Servers/NextCloud](./Web-Servers/NextCloud/) |

### Monitoring & Logging

| Topic | Path |
| --- | --- |
| Zabbix | [Monitoring-Logging/Zabbix](./Monitoring-Logging/Zabbix/) |
| Netdata | [Monitoring-Logging/netdata](./Monitoring-Logging/netdata/) |
| LibreNMS | [Monitoring-Logging/Librenms](./Monitoring-Logging/Librenms/) |
| ELK Stack | [Monitoring-Logging/ELK](./Monitoring-Logging/ELK/) |
| Tools (stress-ng, etc.) | [Monitoring-Logging/Tools](./Monitoring-Logging/Tools/) |

### Security & Networking

| Topic | Path |
| --- | --- |
| iptables | [Security-Networking/Iptables](./Security-Networking/Iptables/) |
| Nmap | [Security-Networking/nmap](./Security-Networking/nmap/) |
| tcpdump | [Security-Networking/tcpdump](./Security-Networking/tcpdump/) |
| hping3 | [Security-Networking/hping3](./Security-Networking/hping3/) |
| BIND9 DNS | [Security-Networking/BIND9-DNS](./Security-Networking/BIND9-DNS/) |
| File Sharing (SMB) | [Security-Networking/FileSharing](./Security-Networking/FileSharing/) |

### Storage

| Topic | Path |
| --- | --- |
| NFS | [Storage/NFS](./Storage/NFS/) |
| MinIO | [Storage/Minio](./Storage/Minio/) |
| S5CMD | [Storage/S5CMD](./Storage/S5CMD/) |

### High Availability

| Topic | Path |
| --- | --- |
| HAProxy | [High-Availability/Ha-Proxy](./High-Availability/Ha-Proxy/) |

### Code Management

| Topic | Path |
| --- | --- |
| Git | [Code-Management/Git](./Code-Management/Git/) |
| GitLab (CI/CD, install, cache) | [Code-Management/Gitlab](./Code-Management/Gitlab/) |

### Other

| Topic | Path |
| --- | --- |
| Vaultwarden | [Password-Manager/Vaultwarden](./Password-Manager/Vaultwarden/) |
| Kernel Management | [System-Kernel-Management/Kernel](./System-Kernel-Management/Kernel/) |
| Vagrant | [Vagrant](./Vagrant/) |

---

## What's Inside Each Section

Every topic folder typically includes:

- Step-by-step setup and operation guides
- Configuration examples you can adapt
- Scripts and manifests for real deployments

Sections are self-contained — start anywhere based on what you're working on.

---

## Contributing

Contributions are welcome. If you have a useful script, a better config, or a new guide:

```bash
git checkout -b feature/your-feature
# make your changes
git commit -m "Add: your feature"
git push origin feature/your-feature
```

Then open a Pull Request on [GitHub](https://github.com/RadinPirouz/devops-documents).

---

## Contact

- **GitHub:** [RadinPirouz](https://github.com/RadinPirouz)
- **Telegram:** [@RadinPirouz](https://t.me/RadinPirouz)
- **Issues:** [devops-documents/issues](https://github.com/RadinPirouz/devops-documents/issues)

If this repo helped you, consider starring it and sharing it with others.
