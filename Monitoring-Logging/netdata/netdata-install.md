# NetData

NetData is an open-source, real-time system and performance monitoring tool designed for Linux systems. It provides detailed insights into various aspects of system performance, including CPU usage, memory utilization, disk activity, network traffic, and more. NetData offers an interactive, web-based dashboard that allows users to monitor and analyze their system's health in real-time.

## Key Features

- **Real-time Monitoring:** NetData provides continuous, minute-by-minute updates on system performance, giving users immediate visibility into any issues or anomalies.

- **Comprehensive Metrics:** It offers a wide range of metrics, covering CPU, memory, disks, network interfaces, processes, and more, enabling users to identify and address performance bottlenecks.

- **Interactive Web Interface:** The web-based dashboard is intuitive and user-friendly, allowing users to navigate through different metrics and customize their monitoring experience.

- **Alerting and Notifications:** NetData supports customizable alarms that can be set to trigger notifications for specific performance thresholds. This enables proactive monitoring and issue resolution.

- **Easy Installation:** NetData can be easily installed on Linux systems, and it requires minimal configuration to start monitoring.

## Supported Platforms

NetData is primarily designed for Linux-based systems, including popular distributions like Ubuntu, CentOS, Debian, and others. It can also be used on FreeBSD systems.

## Installation

**Important : Run Command Az Sudoer User**

To install NetData, follow these steps:

- Download Installer Script
```bash
wget https://my-netdata.io/kickstart.sh
```

- Move To Temp Dir

```bash
mv kickstart.sh /tmp/kickstart.sh
```

- Run Installer 

```bash
sh /tmp/netdata-kickstart.sh
```


