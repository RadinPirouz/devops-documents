# DevOps Knowledge Base

A personal, practical reference for Linux administration, infrastructure, and DevOps workflows. Step-by-step guides, real-world configs, and ready-to-use scripts — organized by topic so you can jump straight to what you need.

**Philosophy:** minimal theory, maximum application. Copy-paste friendly, tested in real environments.

---

## Table of Contents

- [Quick Start](#quick-start)
- [Repository Structure](#repository-structure)
- [Categories](#categories)
- [What's Inside Each Section](#whats-inside-each-section)
- [Contributing](#contributing)
- [Contact](#contact)

---

## Quick Start

```bash
git clone https://github.com/RadinPirouz/devops-documents.git
cd devops-documents
```

1. Pick a category below (or open its `README.md` for a detailed index).
2. Read the `.md` guides or inspect configs/scripts before running anything.
3. Adjust variables (hostnames, paths, credentials) to match your environment.

> Most guides are tested on **Debian/Ubuntu** and **CentOS/RHEL**. Always review configs and test in staging before production.

---

## Repository Structure

```
devops-documents/
├── Linux/              # OS admin, bash, cron, rsync
├── Code/               # Git, GitLab CI/CD
├── Networking/         # DNS, firewall, scanning, SMB
├── Web/                # Nginx, HAProxy, Certbot, Nextcloud
├── Containers/         # Docker, Kubernetes, Dozzle
├── Automation/         # Ansible
├── Databases/          # MySQL, MariaDB, PostgreSQL, Redis
├── Storage/            # MinIO, NFS, S5CMD
├── Monitoring/         # ELK, Zabbix, Netdata, LibreNMS
├── Cloud/              # AWS, Vagrant
├── Applications/       # Jitsi, Vaultwarden
└── System/             # Kernel compile
```

Each top-level folder has its own **README.md** with sub-topics, learning paths, and direct links to every guide.

---

## Categories

Sections follow a typical workflow: **foundation → networking → platform → data → delivery → operations**.

| # | Category | What's inside | Index |
| --- | --- | --- | --- |
| 1 | **Linux** | Administration, bash, cron, rsync, screen | [Linux/README.md](./Linux/README.md) |
| 2 | **Code** | Git, GitLab install & CI/CD | [Code/README.md](./Code/README.md) |
| 3 | **Networking** | BIND9, iptables, nmap, tcpdump, SMB | [Networking/README.md](./Networking/README.md) |
| 4 | **Web** | Nginx, HAProxy, Certbot, Nextcloud | [Web/README.md](./Web/README.md) |
| 5 | **Containers** | Docker, Kubernetes, Dozzle | [Containers/README.md](./Containers/README.md) |
| 6 | **Automation** | Ansible playbooks & roles | [Automation/README.md](./Automation/README.md) |
| 7 | **Databases** | MySQL, MariaDB, PostgreSQL, Redis | [Databases/README.md](./Databases/README.md) |
| 8 | **Storage** | MinIO, NFS, S5CMD | [Storage/README.md](./Storage/README.md) |
| 9 | **Monitoring** | ELK, Zabbix, Netdata, LibreNMS | [Monitoring/README.md](./Monitoring/README.md) |
| 10 | **Cloud** | AWS, Vagrant | [Cloud/README.md](./Cloud/README.md) |
| 11 | **Applications** | Jitsi, Vaultwarden | [Applications/README.md](./Applications/README.md) |
| 12 | **System** | Kernel management | [System/README.md](./System/README.md) |

### Quick reference — where does each topic live?

| Topic | Path |
| --- | --- |
| Linux basics | [Linux/administration/](./Linux/administration/) |
| Bash scripting | [Linux/bash/](./Linux/bash/) |
| Cron jobs | [Linux/cron/](./Linux/cron/) |
| Git | [Code/git/](./Code/git/) |
| GitLab CI/CD | [Code/gitlab/ci/](./Code/gitlab/ci/) |
| DNS (BIND9) | [Networking/bind9/](./Networking/bind9/) |
| Firewall (iptables) | [Networking/iptables/](./Networking/iptables/) |
| Nginx | [Web/nginx/](./Web/nginx/) |
| HAProxy | [Web/haproxy/](./Web/haproxy/) |
| Docker | [Containers/docker/](./Containers/docker/) |
| Kubernetes workloads | [Containers/kubernetes/workloads/](./Containers/kubernetes/workloads/) |
| Kubernetes setup | [Containers/kubernetes/setup/](./Containers/kubernetes/setup/) |
| Ansible | [Automation/ansible/](./Automation/ansible/) |
| MySQL / MariaDB / PostgreSQL | [Databases/](./Databases/) |
| Redis | [Databases/redis/](./Databases/redis/) |
| MinIO | [Storage/minio/](./Storage/minio/) |
| ELK / Zabbix | [Monitoring/elk/](./Monitoring/elk/), [Monitoring/zabbix/](./Monitoring/zabbix/) |
| AWS | [Cloud/aws/](./Cloud/aws/) |
| Vagrant | [Cloud/vagrant/](./Cloud/vagrant/) |
| Jitsi | [Applications/jitsi/](./Applications/jitsi/) |
| Vaultwarden | [Applications/vaultwarden/](./Applications/vaultwarden/) |
| Kernel compile | [System/kernel/](./System/kernel/) |

---

## What's Inside Each Section

Every topic folder typically includes:

- Step-by-step setup and operation guides
- Configuration examples you can adapt
- Scripts and manifests for real deployments

Sections are self-contained — start anywhere based on what you're working on.

**Suggested entry points:**

| If you need to… | Start here |
| --- | --- |
| Learn Linux basics | [Linux/administration/](./Linux/administration/) |
| Set up a web server | [Web/nginx/](./Web/nginx/) |
| Run containers | [Containers/docker/](./Containers/docker/) |
| Deploy to Kubernetes | [Containers/kubernetes/](./Containers/kubernetes/) |
| Automate with Ansible | [Automation/ansible/](./Automation/ansible/) |

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

**Naming conventions for new docs:**

- Top-level categories use `PascalCase` (e.g. `Linux/`, `Containers/`)
- Sub-folders use `lowercase-kebab` (e.g. `nginx/`, `file-sharing/`)
- Sequential guides use numbered prefixes (`01-`, `02-`, …)

---

## Contact

- **GitHub:** [RadinPirouz](https://github.com/RadinPirouz)
- **Telegram:** [@RadinPirouz](https://t.me/RadinPirouz)
- **Issues:** [devops-documents/issues](https://github.com/RadinPirouz/devops-documents/issues)

If this repo helped you, consider starring it and sharing it with others.
