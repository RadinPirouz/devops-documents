# ELK Stack Overview (DevOps Notes)

## What is ELK?

**ELK** stands for:

* **Elasticsearch**
* **Logstash**
* **Kibana**

The ELK Stack is a powerful platform used for **log management, monitoring, data analysis, and observability**. It is widely used in DevOps for **centralized logging, troubleshooting, and performance monitoring**.

---

## Core Components

### 1. Elasticsearch

* Distributed, REST-based **search and analytics engine**
* Used for **storing, indexing, and searching logs and metrics**
* Built on Apache Lucene
* Highly scalable and fast for full-text search

**Key Responsibilities:**

* Store logs and events
* Index data for fast search
* Support aggregations and analytics

---

### 2. Logstash

* **Data processing pipeline**
* Ingests data from multiple sources
* Transforms, parses, enriches, and forwards data

**Pipeline Stages:**

```
Input → Filter → Output
```

**Examples of filters:**

* grok (parse logs)
* mutate (modify fields)
* date (timestamp handling)
* geoip (location enrichment)

---

### 3. Kibana

* **Visualization and analytics UI**
* Connects directly to Elasticsearch
* Used for:

  * Dashboards
  * Log exploration
  * Metrics visualization
  * Alerts and reporting

---

## Beats (Data Shippers)

**Beats** are lightweight agents installed on servers to collect and send data to Elasticsearch or Logstash.

Common Beats:

* **Filebeat** – collects log files
* **Metricbeat** – system and service metrics (CPU, memory, disk)
* **Heartbeat** – uptime and availability monitoring
* **Packetbeat** – network traffic analysis
* **Auditbeat** – security and audit data

**Role:**

* Data collection
* Minimal resource usage
* Sends data to Logstash or directly to Elasticsearch

---

## Fluentd

* **Cloud-native log aggregator and processor**
* Alternative to Logstash
* Common in Kubernetes environments

**Responsibilities:**

* Collect logs from multiple sources
* Enrich and transform data
* Route logs to multiple destinations (Elasticsearch, S3, Kafka)

---

## Typical ELK Architecture

```
Server / Application
        ↓
     Filebeat
        ↓
     Logstash
        ↓
   Elasticsearch
        ↓
      Kibana
```

> Note: In some setups, Beats can send data **directly to Elasticsearch** (Logstash optional).

---

## Database Concepts vs Elasticsearch Concepts

| Traditional Database | Elasticsearch              |
| -------------------- | -------------------------- |
| Database             | Index                      |
| Schema               | Mapping                    |
| Table                | Index (Type is deprecated) |
| Column               | Field                      |
| Row                  | Document                   |
| Primary Key          | Document ID                |

> ⚠️ **Note:** `Type` is deprecated in modern Elasticsearch versions (7+).

---

## Elasticsearch Data Model

* **Index**: Logical namespace for documents
* **Document**: JSON object containing data
* **Field**: Key-value pair in a document
* **Mapping**: Defines field types and structure

---

## Why ELK in DevOps?

* Centralized logging
* Faster incident response
* Debugging distributed systems
* Monitoring infrastructure and applications
* Security analysis (SIEM use cases)

---

## Summary

* **Elasticsearch** → Storage & search engine
* **Logstash / Fluentd** → Data processing & enrichment
* **Beats** → Lightweight data collectors
* **Kibana** → Visualization & dashboards

The ELK Stack enables DevOps teams to **observe, analyze, and troubleshoot systems at scale**.
