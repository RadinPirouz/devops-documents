# AWS Core Services Overview

## Compute & Container Services

**EC2 (Elastic Compute Cloud)**

* Infrastructure as a Service (IaaS)
* Provides virtual machines (instances)
* Storage options:

  * **EBS** (Elastic Block Store): High-performance block storage attached to a single instance
  * **EFS** (Elastic File System): Network file system that can be mounted by multiple instances
* Requires user management of OS, patching, and scaling

**ECS (Elastic Container Service)**

* AWS-managed container orchestration service
* Supports Docker containers
* Deployment options:

  1. **EC2 Launch Type** – you manage EC2 instances
  2. **Fargate Launch Type** – serverless, AWS manages infrastructure

**ECR (Elastic Container Registry)**

* Fully managed Docker container image registry
* Used to store, manage, and deploy container images for ECS and EKS

**EKS (Elastic Kubernetes Service)**

* Managed Kubernetes service
* AWS manages the Kubernetes control plane
* Worker nodes can run on EC2 or Fargate

**AWS Lambda**

* Serverless compute service
* Event-driven execution
* Maximum execution time: **15 minutes**
* No server management required
* Common use cases: APIs, background jobs, automation

---

## Messaging & Integration

**SQS (Simple Queue Service)**

* Fully managed message queue service
* Used for decoupling and scaling distributed systems
* Supports Standard and FIFO queues

---

## Databases

**RDS (Relational Database Service)**

* Managed relational databases (MySQL, PostgreSQL, Oracle, SQL Server, MariaDB, Aurora)
* Typically deployed in **private subnets**
* High availability using Multi-AZ
* Automated backups, patching, and scaling

**DynamoDB**

* Fully managed NoSQL key-value and document database
* Serverless, auto-scaling, and highly available
* Low latency and global replication support

---

## Networking & Traffic Management

**VPC (Virtual Private Cloud)**

* Isolated virtual network in AWS
* Uses CIDR ranges for IP addressing

**Subnets**

* **Public Subnet**: Has a route to the Internet Gateway
* **Private Subnet**: No direct internet access

**Internet Gateway (IGW)**

* Enables inbound and outbound internet access for public subnets

**NAT Gateway**

* Placed in a public subnet
* Allows **outbound-only** internet access for private subnet resources
* Cannot receive inbound connections

**Route 53**

* Managed DNS service
* Supports domain registration, routing policies, and health checks

---

## Load Balancing

**ELB (Elastic Load Balancing)**

* Distributes traffic across multiple targets

**ALB (Application Load Balancer)**

* Layer 7 (Application layer)
* Supports HTTP/HTTPS routing rules
* Can route traffic to:

  * EC2
  * ECS
  * Lambda
  * IP addresses

---

## Security & Identity

**IAM (Identity and Access Management)**

* Manages users, groups, roles, and permissions
* Global AWS service

**IAM Roles**

* Used by AWS services to access other AWS resources securely

**IAM Reports**

* **Credential Report**: Shows credential status for all users
* **Access Advisor**: Shows last-used service permissions

**Security Groups**

* Stateful virtual firewalls for AWS resources
* Control inbound and outbound traffic
* Attached to EC2, ALB, RDS, ECS, etc.

---

## Monitoring & Logging

**CloudWatch**

* Monitoring and observability service
* Collects metrics, logs, and events
* Used for alarms, dashboards, and automation

---

## AWS Global Infrastructure

**Region**

* Geographic area containing multiple Availability Zones

**Availability Zone (AZ)**

* One or more isolated data centers within a region

**Global Services**

* IAM
* Route 53
* CloudFront
* AWS WAF

**Regional Services**

* EC2
* ECS
* EKS
* RDS
* Lambda

---

## IP Addressing

**Private IP**

* Assigned from VPC CIDR range
* Used for internal communication

**Public IP**

* Assigned automatically to EC2 instances in public subnets
* Released when instance is stopped

**Elastic IP (EIP)**

* Static public IPv4 address
* Remains allocated even if the instance stops
* Used for failover and stable endpoints

---

## Database Networking Best Practices

* RDS instances should run in **private subnets**
* Access options:

  * EC2 in the same VPC
  * Bastion host
  * VPN or Direct Connect
* NAT Gateway can be used for outbound access (updates, patches)
