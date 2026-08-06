# AWS Fundamentals

Complete reference covering AWS global infrastructure, billing, compute, containers, networking, databases, security, load balancing, and monitoring. Practical explanations of how each piece works and how they fit together.

---

## Table of contents

1. [AWS Global Infrastructure](#1-aws-global-infrastructure)
2. [Billing & Cost Management](#2-billing--cost-management)
3. [IAM — Identity and Access Management](#3-iam--identity-and-access-management)
4. [Networking — VPC and Traffic Flow](#4-networking--vpc-and-traffic-flow)
5. [IP Addressing](#5-ip-addressing)
6. [ENI — Elastic Network Interface](#6-eni--elastic-network-interface)
7. [Security Groups](#7-security-groups)
8. [EC2 — Elastic Compute Cloud](#8-ec2--elastic-compute-cloud)
9. [EC2 Hibernation](#9-ec2-hibernation)
10. [EC2 Storage — EBS and EFS](#10-ec2-storage--ebs-and-efs)
11. [EC2 Placement Groups](#11-ec2-placement-groups)
12. [Containers — ECS, ECR, EKS](#12-containers--ecs-ecr-eks)
13. [AWS Lambda](#13-aws-lambda)
14. [Load Balancing](#14-load-balancing)
15. [Databases — RDS and DynamoDB](#15-databases--rds-and-dynamodb)
16. [Messaging — SQS](#16-messaging--sqs)
17. [Monitoring — CloudWatch](#17-monitoring--cloudwatch)
18. [Quick reference](#18-quick-reference)

---

## 1. AWS Global Infrastructure

AWS runs worldwide. Knowing **where** resources live matters for latency, compliance, high availability, and cost.

### Region

A **Region** is a geographic area (for example `eu-west-1` Ireland, `us-east-1` N. Virginia). Each region is independent: you choose one when you create most resources. Pick a region close to users for lower latency, and match data-residency rules if you have them.

### Availability Zone (AZ)

An **Availability Zone** is one or more isolated data centers inside a region. AZs in the same region are linked by fast, private networking but fail independently (power, network, disaster).

**Why it matters:** put copies of critical workloads in **at least two AZs** so one AZ outage does not take everything down. Multi-AZ RDS and load-balanced EC2 across AZs are common patterns.

### Global vs regional services

| Type | Meaning | Examples |
| --- | --- | --- |
| **Global** | One logical service across regions (or managed outside a single region) | IAM, Route 53, CloudFront, AWS WAF |
| **Regional** | Created and used inside a chosen region | EC2, ECS, EKS, RDS, Lambda, VPC |

IAM users and policies are global: create a user once, use it in every region. An EC2 instance exists only in the region (and AZ) where you launched it.

---

## 2. Billing & Cost Management

### Billing console

The billing console shows current-month spend, past invoices, and cost breakdowns by service.

**IAM access to billing is special:** by default IAM users cannot see billing, even with broad admin policies. The **root account** must first enable IAM access to billing (Account settings), then you attach billing-related permissions to the target IAM user or group.

### AWS Budgets

**Budgets** let you set limits and get alerts (email/SNS) when actual or forecasted spend/usage crosses thresholds. Useful to catch runaway costs early.

| Budget type | What it does |
| --- | --- |
| **Zero spend budget** | Alerts once spending exceeds about $0.01 — good for accounts that should stay idle |
| **Monthly cost budget** | Alerts if you exceed, or are **forecasted** to exceed, a monthly dollar amount |
| **Daily Savings Plans coverage budget** | Alerts when Savings Plans coverage drops below a target % |
| **Daily reservation utilization budget** | Alerts when Reserved Instance utilization drops below a target % |

Savings Plans and reservations are discount commitments; coverage/utilization budgets help you notice when you are not using what you paid for.

---

## 3. IAM — Identity and Access Management

IAM controls **who** can do **what** in your account. It is a **global** service.

### Building blocks

| Concept | Role |
| --- | --- |
| **User** | Long-lived identity for a person or (less ideally) an application |
| **Group** | Collection of users that share the same policies |
| **Role** | Identity that can be **assumed** temporarily (by a user, service, or another account) |
| **Policy** | JSON document of allow/deny permissions on actions and resources |

Prefer **roles** for AWS services and workloads (EC2, Lambda, ECS tasks) instead of embedding access keys. Prefer groups + policies over attaching many policies to individual users.

### IAM roles for EC2

Attach a role to an EC2 instance so the AWS CLI/SDK can call APIs **without** storing access keys on the disk.

**Example: list IAM users from an instance**

1. **IAM** → **Roles** → **Create role**
2. Trusted entity: **AWS service** → **EC2**
3. Attach a policy (for example `IAMReadOnlyAccess`)
4. On the instance: **Actions** → **Security** → **Modify IAM role** → select the role
5. Connect to the instance and run:

```bash
aws iam list-users
```

The instance gets temporary credentials from the **Instance Metadata Service (IMDS)** via the role. No `aws configure` on the box is required for that role’s permissions.

### IAM reports

| Report | Purpose |
| --- | --- |
| **Credential report** | CSV of all users: passwords, access keys, MFA, last used — audit hygiene |
| **Access Advisor** | When a user/role last used each service — helps trim unused permissions |

---

## 4. Networking — VPC and Traffic Flow

### VPC (Virtual Private Cloud)

A **VPC** is your private network in AWS. You choose a CIDR block (for example `10.0.0.0/16`). Resources inside talk using private IPs from that range.

### Subnets

Subnets carve the VPC into smaller CIDR ranges, each in **one AZ**.

| Subnet type | Meaning |
| --- | --- |
| **Public** | Route table sends `0.0.0.0/0` traffic to an **Internet Gateway** — instances can have public IPs and be reached from the internet (if security groups allow) |
| **Private** | No direct route to the IGW — no inbound internet; outbound internet only via **NAT** (if you add one) |

Typical design: public subnets for load balancers / bastion hosts; private subnets for app servers and databases.

### Internet Gateway (IGW)

An **IGW** attaches to the VPC and enables internet connectivity for resources in public subnets (with a public or Elastic IP and the right route). Without an IGW (or equivalent), the VPC cannot reach the public internet that way.

### NAT Gateway

A **NAT Gateway** sits in a **public** subnet and gives **private** subnet instances **outbound-only** internet access (package updates, API calls). The internet cannot initiate connections inbound through NAT.

| Component | Inbound from internet | Outbound to internet |
| --- | --- | --- |
| IGW + public subnet | Yes (if SG allows) | Yes |
| NAT + private subnet | No | Yes |

### Route 53

**Route 53** is AWS’s managed DNS service. It can:

- Register domains
- Host DNS zones and records
- Apply routing policies (simple, weighted, latency, failover, geolocation, etc.)
- Run health checks and fail over when targets are unhealthy

DNS often points users at a load balancer (ALB/NLB) or CloudFront, not directly at a single EC2 public IP.

---

## 5. IP Addressing

| Address | Where it comes from | Behavior |
| --- | --- | --- |
| **Private IP** | VPC/subnet CIDR | Used inside the VPC; stays with the instance for its life in that subnet |
| **Public IP** (auto-assigned) | AWS public pool | Optional on public subnets; **released and usually changed** when the instance is **stopped and started** |
| **Elastic IP (EIP)** | Allocated to your account in a region | Static public IPv4 you associate with an instance or ENI; survives stop/start |

**Reboot vs stop/start:** a reboot keeps the same public IP. Stop/start releases an auto-assigned public IP. Use an **Elastic IP** when you need a stable public address (or prefer a DNS name on a load balancer instead).

Idle Elastic IPs (allocated but not associated) can incur a charge. Prefer DNS + load balancer over pinning many EIPs when you can.

---

## 6. ENI — Elastic Network Interface

An **ENI** is a virtual network card in a VPC. Every EC2 instance has a **primary ENI** (`eth0`). You can create extra ENIs and attach them for multi-homing, failover, or moving a network identity between instances.

### Attributes an ENI can hold

| Attribute | Notes |
| --- | --- |
| **Primary private IPv4** | Required; from the subnet CIDR |
| **Secondary private IPv4(s)** | Optional extra private addresses on the same ENI |
| **One Elastic IP per private IPv4** | You can map an EIP to the primary or a secondary private IP |
| **One public IPv4** | Auto-assigned public IP (when the subnet/instance settings allow) — distinct from an EIP you allocate |
| **One or more security groups** | Firewall rules are bound to the ENI, not “the instance” in the abstract |
| **MAC address** | Stable for that ENI; useful for licensing or software that keys off MAC |
| **Source/destination check** | On by default; turn off for NAT/router-style instances |

### Why ENIs matter

- **Move networking between instances:** detach an ENI (with its IPs and SGs) from one instance and attach it to another — failover without changing DNS or client configs as much
- **Multiple subnets / dual-homed hosts:** attach ENIs from different subnets (same AZ) for management vs data planes
- **Security groups attach to ENIs:** traffic is filtered per interface

ENIs are **AZ-scoped** (like the subnet they belong to). You cannot attach an ENI to an instance in a different AZ.

---

## 7. Security Groups

Security groups are **stateful virtual firewalls** attached to resources (EC2, ALB, RDS, ENIs, etc.).

### How they work

- Rules use **protocol**, **port**, and **source** (inbound) or **destination** (outbound) — CIDR or another security group
- **Inbound** (ingress): who may connect in
- **Outbound** (egress): where the resource may connect out
- Default for a new SG: allow all outbound; **no** inbound until you add rules
- **Stateful:** if you allow inbound on port 443, return traffic is allowed automatically (you do not open ephemeral ports for the reply)

### Referencing other security groups

You can allow traffic **from another security group ID**, not only from IP ranges.

Example: instance A (group `sg-app`) and instance B (group `sg-db`). If `sg-db` allows inbound TCP 5432 from `sg-app`, every instance using `sg-app` can reach the DB without listing each private IP. When instances scale or change IP, rules still work.

Security groups **allow** only (no explicit deny lists). For network ACLs (optional, subnet-level), deny rules exist — NACL is a separate, less common topic for most app designs.

---

## 8. EC2 — Elastic Compute Cloud

EC2 is **IaaS**: you rent virtual machines (**instances**). You choose OS image (AMI), size, network, storage, and you manage the guest OS (patches, agents, app install) unless you automate it.

### Creating an instance (console flow)

1. **EC2** → **Instances** → **Launch instance**
2. Name, AMI (Amazon Linux, Ubuntu, etc.)
3. Instance type (CPU/RAM profile)
4. Key pair (SSH) or other login method
5. Network: VPC, subnet, auto-assign public IP, security group
6. Storage (EBS volume size/type)
7. Optional: IAM instance profile, **User data** bootstrap script
8. Launch

### Bootstrapping (User data)

**Bootstrapping** means running a script when the instance starts, supplied as **User data**. Common uses: install packages, enable services, write config files, pull application code. On many Linux AMIs, cloud-init runs user data on first boot (behavior depends on AMI and settings).

### Instance types

| Category | Best for | Naming hint | Example |
| --- | --- | --- | --- |
| **General purpose** | Balanced CPU, memory, network (web apps, small DBs) | Often `t`, `m` | `t3`, `m5` |
| **Compute optimized** | High CPU (batch, gaming, ML inference) | Starts with `c` | `c5`, `c6i` |
| **Memory optimized** | Large in-memory data (caches, in-memory DBs) | Starts with `r`, `x` | `r5` |
| **Storage optimized** | High local disk I/O or dense storage | Starts with `i`, `d` | `i3` |

### Naming convention

Example: `m5.2xlarge`

| Part | Meaning |
| --- | --- |
| `m` | Family / class (general purpose) |
| `5` | Generation (newer usually better price/performance) |
| `2xlarge` | Size within the family (more vCPU/RAM than `large`) |

Burstable types (`t2`/`t3`/`t4g`) use CPU credits — fine for spiky low-average load; sustained full CPU may throttle or cost extra depending on mode.

---

## 9. EC2 Hibernation

**Hibernation** saves the instance’s **RAM contents to the root EBS volume**, then powers the instance down. When you start it again, memory is restored from disk and processes continue almost where they left off (faster warm start than a cold boot).

### How it differs from stop / terminate

| Action | What happens to RAM / disk | Typical use |
| --- | --- | --- |
| **Stop** | RAM cleared; EBS root kept; instance can start later (cold boot) | Save compute cost overnight |
| **Hibernate** | RAM written to EBS, then instance stops | Preserve in-memory state (long app warmup, in-memory caches) |
| **Terminate** | Instance deleted; EBS may be deleted depending on settings | End of life |

### Requirements and limits (common rules)

- Root volume must be **EBS** (not instance-store root), typically **encrypted**, with types such as gp2/gp3 or io1/io2
- Enough **free space on the root volume** to hold RAM contents (plus OS and app data already on disk)
- **RAM limits (AWS prerequisites):**
  - **Linux:** less than **150 GiB**
  - **Windows:** **16 GiB** or less
- Hibernation must be **enabled at launch** (you generally cannot enable it later on an instance that was not launched with it)
- Instance family and AMI must **support hibernation**
- Max hibernation duration is limited (AWS does not support leaving an instance hibernated more than **60 days** without starting it)
- You still pay for **EBS storage** while hibernated (not for EC2 instance hours while stopped/hibernated)

### When to use it

Long application startup, warm JVM/heaps, or demos where “resume” matters more than a full reboot. For simple cost saving with no need to keep RAM, a normal **stop** is enough.

---

## 10. EC2 Storage — EBS and EFS

### EBS (Elastic Block Store)

**EBS** is network-attached **block** storage — it looks like a disk attached to one instance (or multi-attach for specific volume types/use cases).

- Lives in a **single Availability Zone**; attach only to instances in that AZ
- Can persist after instance termination if **Delete on Termination** is off
- **Snapshots** copy volume state to S3; restore as a new volume (including in another AZ in the region)
- Volume types (gp3, io2, st1, etc.) trade off IOPS, throughput, and price

EBS is **not** a shared filesystem: two normal instances do not mount the same EBS volume like NFS.

### EFS (Elastic File System)

**EFS** is a managed **NFS-compatible** filesystem. Many instances (across AZs in the region) can mount the same file system at once. Use it for shared content, home dirs, or lift-and-shift apps that need a shared disk. Different pricing and performance model than EBS.

| | EBS | EFS |
| --- | --- | --- |
| Style | Block device (disk) | Network file system |
| Share | Usually one instance | Many instances |
| Scope | Single AZ (volume) | Regional (multi-AZ) |

---

## 11. EC2 Placement Groups

Placement groups control how instances are laid out on physical hardware — for **performance** or **failure isolation**.

| Strategy | Behavior | Typical use |
| --- | --- | --- |
| **Cluster** | Instances packed close in one AZ | Lowest latency / highest throughput (HPC, tightly coupled apps) |
| **Spread** | Instances on distinct hardware; limited number per AZ | Few critical nodes that must not share a rack failure |
| **Partition** | Instances grouped into partitions (e.g. racks); partitions fail independently | Large distributed systems (Hadoop, Cassandra, Kafka-style replicas) |

- **Cluster:** best network; if that AZ or nearby hardware fails, more of the group can be affected together
- **Spread:** maximum isolation for a small count of instances
- **Partition:** scale out while keeping replica sets in different partitions

---

## 12. Containers — ECS, ECR, EKS

### ECR (Elastic Container Registry)

Private (or public) **Docker image registry**. Build images, push to ECR, pull from ECS/EKS/EC2. Think “managed Docker Hub inside your account,” with IAM for access control.

### ECS (Elastic Container Service)

AWS-native **container orchestration**: you define tasks/services; ECS schedules containers.

| Launch type | Who manages servers |
| --- | --- |
| **EC2** | You run/capacity-manage EC2 instances in a cluster |
| **Fargate** | Serverless — you set CPU/memory; AWS runs the tasks |

Use ECS when you want AWS-integrated containers without operating Kubernetes.

### EKS (Elastic Kubernetes Service)

**Managed Kubernetes**. AWS runs the control plane; worker nodes run on EC2 or Fargate. Use EKS when you need Kubernetes APIs, portability, or existing K8s tooling.

| | ECS | EKS |
| --- | --- | --- |
| API | AWS ECS APIs | Kubernetes APIs |
| Ops model | Simpler AWS-native | More flexible, more K8s surface area |
| Images | Usually from ECR | Usually from ECR |

---

## 13. AWS Lambda

**Lambda** is **serverless compute**: upload code (or container image), configure triggers, AWS runs it on demand. You do not manage servers, patching, or idle capacity.

- **Event-driven:** API Gateway, S3 events, SQS, EventBridge, DynamoDB streams, etc.
- **Max duration:** **15 minutes** per invocation
- Billed by requests and duration (GB-seconds), plus free tier
- Common uses: APIs, glue code, file processing, scheduled jobs, automation

If a job needs hours of continuous work or a custom long-lived runtime, prefer EC2, ECS/Fargate, or Batch instead of Lambda.

---

## 14. Load Balancing

### ELB (Elastic Load Balancing)

**ELB** is the family name for AWS load balancers. They distribute traffic across targets (instances, IPs, Lambda, containers) and improve availability.

### ALB (Application Load Balancer)

**ALB** works at **Layer 7** (HTTP/HTTPS).

- Path- and host-based routing (`/api` → one target group, `app.example.com` → another)
- Native HTTP features (redirects, fixed responses, WebSockets, gRPC in supported setups)
- Targets can include: **EC2**, **ECS tasks**, **Lambda**, **IP addresses**

Typical public web pattern: Route 53 → ALB (public subnets) → app instances/tasks in private subnets.

Other ELB types (for awareness): **NLB** (Layer 4, ultra-low latency / static IPs), **GWLB** (third-party appliances). ALB is the usual choice for HTTP apps.

---

## 15. Databases — RDS and DynamoDB

### RDS (Relational Database Service)

**RDS** manages relational engines: MySQL, PostgreSQL, MariaDB, Oracle, SQL Server, and **Aurora** (AWS’s MySQL/PostgreSQL-compatible engine).

AWS handles provisioning, patching, backups, and optional Multi-AZ failover. You still design schema, queries, and scaling choices (instance size, read replicas, Aurora capacity).

**High availability:** Multi-AZ keeps a standby in another AZ; failover is handled by AWS with a stable endpoint DNS name.

### DynamoDB

**DynamoDB** is a fully managed **NoSQL** key-value and document store. Serverless scaling, single-digit millisecond latency at scale, optional global tables for multi-region. You model around partition keys and access patterns rather than SQL joins.

| | RDS | DynamoDB |
| --- | --- | --- |
| Model | Relational (SQL) | Key-value / document |
| Ops | Managed instances (or Aurora Serverless) | Fully serverless tables |
| Best when | Complex queries, transactions, existing SQL apps | Massive scale, simple key-based access |

### Database networking best practices

- Run RDS in **private subnets** — not publicly reachable from the internet
- Access paths:
  - App/EC2/ECS in the **same VPC** (security group reference)
  - **Bastion host** or SSM Session Manager for admin access
  - **VPN** or **Direct Connect** from on-premises
- Use a **NAT Gateway** if the DB subnet needs outbound internet (patches via your own tooling — RDS patching is mostly AWS-managed)
- Lock security groups: only app SG (or bastion) on the DB port

---

## 16. Messaging — SQS

**SQS (Simple Queue Service)** is a fully managed **message queue**. Producers send messages; consumers pull and process them. That **decouples** services so a spike in producers does not crush consumers, and failed processing can retry.

| Queue type | Behavior |
| --- | --- |
| **Standard** | Highest throughput; best-effort ordering; at-least-once delivery (design for idempotency) |
| **FIFO** | Exactly-once processing semantics (within limits); ordered per message group; lower throughput than standard |

Common pattern: API or Lambda writes to SQS → workers (EC2, ECS, Lambda) process asynchronously.

---

## 17. Monitoring — CloudWatch

**CloudWatch** is the core observability service for AWS.

- **Metrics:** CPU, network, custom app metrics, billing alarms, etc.
- **Logs:** collect and query log groups (EC2 agents, Lambda, containers)
- **Alarms:** threshold on a metric → SNS email, Auto Scaling, or automation
- **Dashboards:** visualize metrics in one place
- **Events / EventBridge integration:** react to schedule or AWS events

Use CloudWatch alarms with Budgets (cost) and with EC2/ASG (health and scaling) so problems surface before users do.

---

## 18. Quick reference

| Topic | Key takeaway |
| --- | --- |
| Region / AZ | Region = geography; AZ = isolated DC; use multi-AZ for HA |
| Billing for IAM | Root enables billing access; then grant IAM permissions |
| Budgets | Alert on spend, forecast, Savings Plans coverage, RI utilization |
| IAM | Users/groups/roles/policies; prefer roles over long-lived keys |
| VPC | Your private network; public vs private = route to IGW or not |
| NAT | Outbound internet for private subnets only |
| ENI | Virtual NIC: private IPs, EIP mapping, SGs, MAC; movable between instances |
| Security groups | Stateful allow-rules; attached to ENIs; reference other SGs |
| Public IP | Changes on stop/start; Elastic IP stays stable |
| EC2 | IaaS VMs; you manage the OS |
| User data | Bootstrap script at launch |
| Hibernation | RAM → EBS root, then stop; Linux RAM < 150 GiB; enable at launch |
| Instance names | `m5.2xlarge` → family, generation, size |
| EBS vs EFS | Block/AZ vs shared regional filesystem |
| Placement | Cluster = speed; Spread/Partition = isolation |
| ECS vs EKS | AWS-native containers vs managed Kubernetes |
| Lambda | Serverless, event-driven, max 15 minutes |
| ALB | Layer 7 HTTP routing to EC2/ECS/Lambda/IP |
| RDS | Managed SQL in private subnets; Multi-AZ for HA |
| DynamoDB | Managed NoSQL at scale |
| SQS | Decouple producers and consumers |
| CloudWatch | Metrics, logs, alarms, dashboards |
