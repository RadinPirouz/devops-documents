# Replicating Jitsi Videobridge in Docker

## 1. What JVB replication means

In Jitsi, the component that normally becomes the bottleneck is **Jitsi Videobridge**, also called **JVB**. JVB is the SFU/media router that handles RTP audio and video traffic. The official Jitsi scalable setup is based on **one Jitsi Meet core node** running web, Prosody, and Jicofo, plus **multiple JVB nodes** handling media traffic. Jitsi’s own guide says the videobridge is usually the first limiting factor and that bridges can be scaled horizontally by adding more of them. ([Jitsi][1])

Important: this is not classic load balancing with HAProxy or Nginx in front of UDP media. JVBs register into the bridge pool, and **Jicofo selects a bridge when a new conference starts**. ([Jitsi][1])

## 2. Target architecture

```text
                          Users
                            |
                      80/443 TCP
                            |
                    +----------------+
                    | Jitsi Core     |
                    | web/nginx      |
                    | prosody        |
                    | jicofo         |
                    +----------------+
                         | 5222 TCP
              private / firewall-restricted XMPP
                         |
        +----------------+----------------+
        |                |                |
+---------------+ +---------------+ +---------------+
| JVB node 1    | | JVB node 2    | | JVB node 3    |
| Docker jvb    | | Docker jvb    | | Docker jvb    |
| 10000/udp     | | 10000/udp     | | 10000/udp     |
+---------------+ +---------------+ +---------------+
        |                |                |
        +------ media RTP to clients -----+
```

Jitsi’s scalable guide shows this same pattern: one central Jitsi Meet server with nginx, Prosody, and Jicofo, plus multiple videobridges connected over XMPP. It also documents `80/tcp`, `443/tcp`, `5222/tcp`, and `10000/udp` as the key ports in this architecture. ([Jitsi][1])

## 3. What replication improves

JVB replication improves:

* Total concurrent meetings
* Total concurrent users
* Media CPU capacity
* Network bandwidth capacity
* Fault isolation between conferences
* Easier horizontal scaling by adding more bridge hosts

It does not automatically make one very large conference split across all bridges. By default, Jicofo schedules a conference onto a selected bridge. If you need one conference distributed across multiple bridges, that becomes an **Octo / cascading JVB** design and should be treated as a separate advanced architecture.

## 4. Recommended deployment model

For production, use:

```text
1 core Jitsi node:
  web
  prosody
  jicofo
  optionally one local jvb

N remote JVB nodes:
  jvb only
```

Running many JVB containers on the same host is possible for testing, but it is not the best production model because each JVB needs UDP media ports, CPU, memory, kernel UDP buffers, and public reachability. The official sizing guide also notes that videobridges carry more load than the main Jitsi Meet server and suggests larger CPU allocation for JVB hosts. ([Jitsi][1])

## 5. Required ports

### Core Jitsi node

| Port       |                      Direction | Purpose                            |
| ---------- | -----------------------------: | ---------------------------------- |
| `80/tcp`   |                 public inbound | HTTP redirect or ACME challenge    |
| `443/tcp`  |                 public inbound | Jitsi web UI and WebSocket traffic |
| `5222/tcp` | private inbound from JVB nodes | Prosody XMPP client connection     |
| `5347/tcp` |                  internal only | XMPP component connections         |
| `5280/tcp` |    internal or reverse-proxied | BOSH/WebSocket depending on setup  |

The Docker self-hosting guide lists `80/tcp`, `443/tcp`, and `10000/udp` as the main external ports, and the scalable guide says `5222/tcp` should be open only to videobridges. ([Jitsi][2])

### Each JVB node

| Port                            |              Direction | Purpose                                 |
| ------------------------------- | ---------------------: | --------------------------------------- |
| `10000/udp`                     |         public inbound | WebRTC RTP media                        |
| `8080/tcp`                      | localhost/private only | Colibri REST API                        |
| `443/tcp` or reverse proxy path |               optional | Colibri WebSocket if exposed separately |

The Docker guide defines `JVB_PORT` as the UDP media port, defaulting to `10000`, and `JVB_COLIBRI_PORT` as the local Colibri API port, defaulting to `8080`. ([Jitsi][2])

## 6. Core node Docker configuration

Start with the normal `docker-jitsi-meet` stack.

```bash
git clone https://github.com/jitsi/docker-jitsi-meet
cd docker-jitsi-meet
cp env.example .env
./gen-passwords.sh
mkdir -p ~/.jitsi-meet-cfg/{web,transcripts,prosody/config,prosody/prosody-plugins-custom,jicofo,jvb,jigasi,jibri}
```

The Docker guide recommends copying `env.example`, generating strong internal passwords with `./gen-passwords.sh`, and creating the required config directories before starting the stack. ([Jitsi][2])

Example core `.env`:

```env
CONFIG=~/.jitsi-meet-cfg
TZ=UTC

PUBLIC_URL=https://meet.example.com

HTTP_PORT=80
HTTPS_PORT=443

ENABLE_LETSENCRYPT=1
LETSENCRYPT_DOMAIN=meet.example.com
LETSENCRYPT_EMAIL=admin@example.com
ENABLE_HTTP_REDIRECT=1

JVB_AUTH_USER=jvb
JVB_AUTH_PASSWORD=use_the_generated_password_from_core_env

JVB_BREWERY_MUC=jvbbrewery

XMPP_DOMAIN=meet.jitsi
XMPP_AUTH_DOMAIN=auth.meet.jitsi
XMPP_INTERNAL_MUC_DOMAIN=internal-muc.meet.jitsi
XMPP_MUC_DOMAIN=muc.meet.jitsi
XMPP_SERVER=xmpp.meet.jitsi
XMPP_PORT=5222
```

Expose Prosody `5222/tcp` from the core node to the JVB nodes. Do not expose it to the entire Internet.

Example `docker-compose.override.yml` on the core node:

```yaml
services:
  prosody:
    ports:
      - "10.0.0.10:5222:5222"
```

Use a private network address if possible. If your JVBs are on separate public servers, restrict this port with firewall rules.

Example firewall logic:

```bash
ufw allow 80/tcp
ufw allow 443/tcp

ufw allow from JVB1_PUBLIC_OR_PRIVATE_IP to any port 5222 proto tcp
ufw allow from JVB2_PUBLIC_OR_PRIVATE_IP to any port 5222 proto tcp

ufw deny 5222/tcp
```

Start the core stack:

```bash
docker compose up -d
```

## 7. Remote JVB node Docker Compose

On every remote JVB server, run only the `jvb` container.

Directory layout:

```bash
mkdir -p /opt/jitsi-jvb
cd /opt/jitsi-jvb
mkdir -p ~/.jitsi-meet-cfg/jvb
```

Create `.env`:

```env
CONFIG=~/.jitsi-meet-cfg
TZ=UTC

JITSI_IMAGE_VERSION=stable

PUBLIC_URL=https://meet.example.com

XMPP_SERVER=10.0.0.10
XMPP_PORT=5222
XMPP_DOMAIN=meet.jitsi
XMPP_AUTH_DOMAIN=auth.meet.jitsi
XMPP_INTERNAL_MUC_DOMAIN=internal-muc.meet.jitsi

JVB_AUTH_USER=jvb
JVB_AUTH_PASSWORD=the_same_JVB_AUTH_PASSWORD_from_core

JVB_BREWERY_MUC=jvbbrewery

JVB_PORT=10000
JVB_ADVERTISE_IPS=JVB_PUBLIC_IP

JVB_MUC_NICKNAME=jvb-node-01
JVB_INSTANCE_ID=jvb-node-01

COLIBRI_REST_ENABLED=true
SHUTDOWN_REST_ENABLED=true

VIDEOBRIDGE_MAX_MEMORY=3072m
```

`JVB_ADVERTISE_IPS` is critical. The Docker guide says it controls which IPs and ports the bridge advertises for WebRTC media, and it must be set correctly when behind NAT or on the public Internet. If it is wrong, calls can fail when more than two users join. ([Jitsi][2])

Create `docker-compose.yml`:

```yaml
services:
  jvb:
    image: jitsi/jvb:${JITSI_IMAGE_VERSION:-stable}
    restart: unless-stopped

    ports:
      - "${JVB_PORT:-10000}:${JVB_PORT:-10000}/udp"
      - "127.0.0.1:8080:8080"

    volumes:
      - ${CONFIG}/jvb:/config

    environment:
      - TZ
      - PUBLIC_URL

      - XMPP_SERVER
      - XMPP_PORT
      - XMPP_DOMAIN
      - XMPP_AUTH_DOMAIN
      - XMPP_INTERNAL_MUC_DOMAIN

      - JVB_AUTH_USER
      - JVB_AUTH_PASSWORD
      - JVB_BREWERY_MUC

      - JVB_PORT
      - JVB_ADVERTISE_IPS
      - JVB_MUC_NICKNAME
      - JVB_INSTANCE_ID

      - COLIBRI_REST_ENABLED
      - SHUTDOWN_REST_ENABLED
      - VIDEOBRIDGE_MAX_MEMORY
```

Start the remote JVB:

```bash
docker compose up -d
```

Check logs:

```bash
docker compose logs -f jvb
```

On the core node:

```bash
docker compose logs -f prosody
docker compose logs -f jicofo
```

You should see the new bridge join the brewery MUC, and Jicofo should detect it. The scalable setup guide says you can verify bridge connection in Prosody and Jicofo logs, and that Jicofo picks a videobridge when a new conference starts. ([Jitsi][1])

## 8. Same-host multi-JVB setup

Use this only for testing or small deployments.

Problem: two containers cannot both bind host port `10000/udp`.

Example:

```yaml
services:
  jvb1:
    image: jitsi/jvb:${JITSI_IMAGE_VERSION:-stable}
    restart: unless-stopped
    ports:
      - "10000:10000/udp"
      - "127.0.0.1:8081:8080"
    environment:
      - JVB_PORT=10000
      - JVB_ADVERTISE_IPS=PUBLIC_IP#10000
      - JVB_MUC_NICKNAME=jvb1
      - JVB_INSTANCE_ID=jvb1
      - JVB_AUTH_USER=jvb
      - JVB_AUTH_PASSWORD=${JVB_AUTH_PASSWORD}
      - JVB_BREWERY_MUC=jvbbrewery
      - XMPP_SERVER=xmpp.meet.jitsi
      - XMPP_DOMAIN=meet.jitsi
      - XMPP_AUTH_DOMAIN=auth.meet.jitsi
      - XMPP_INTERNAL_MUC_DOMAIN=internal-muc.meet.jitsi

  jvb2:
    image: jitsi/jvb:${JITSI_IMAGE_VERSION:-stable}
    restart: unless-stopped
    ports:
      - "10001:10000/udp"
      - "127.0.0.1:8082:8080"
    environment:
      - JVB_PORT=10000
      - JVB_ADVERTISE_IPS=PUBLIC_IP#10001
      - JVB_MUC_NICKNAME=jvb2
      - JVB_INSTANCE_ID=jvb2
      - JVB_AUTH_USER=jvb
      - JVB_AUTH_PASSWORD=${JVB_AUTH_PASSWORD}
      - JVB_BREWERY_MUC=jvbbrewery
      - XMPP_SERVER=xmpp.meet.jitsi
      - XMPP_DOMAIN=meet.jitsi
      - XMPP_AUTH_DOMAIN=auth.meet.jitsi
      - XMPP_INTERNAL_MUC_DOMAIN=internal-muc.meet.jitsi
```

The `#port` syntax is used when the advertised external port differs from the internal JVB port. The Docker guide documents this pattern for `JVB_ADVERTISE_IPS`. ([Jitsi][2])

## 9. Colibri WebSocket considerations

Modern Jitsi deployments commonly use Colibri WebSockets for bridge-channel communication. Jitsi Videobridge documents that WebSocket URLs include a `server-id` path such as:

```text
/colibri-ws/server-id/conf-id/endpoint-id
```

When multiple bridges are behind one HTTP proxy, the proxy must route each `server-id` to the correct JVB. Jitsi’s Videobridge WebSocket documentation explicitly shows separate proxy routes for `jvb1` and `jvb2`. ([GitHub][3])

For a simple Docker deployment, the easiest options are:

1. Keep JVBs directly reachable by UDP and avoid custom WebSocket routing unless needed.
2. If using Colibri WebSocket through the main domain, assign unique bridge IDs and configure reverse-proxy routing.
3. If using remote JVBs with their own public hostnames, make each JVB advertise the correct public WebSocket domain.

For production behind a reverse proxy, review these variables:

```env
ENABLE_COLIBRI_WEBSOCKET=1
COLIBRI_WEBSOCKET_REGEX=
COLIBRI_WEBSOCKET_JVB_LOOKUP_NAME=
DISABLE_COLIBRI_WEBSOCKET_JVB_LOOKUP=
JVB_WS_DOMAIN=
JVB_WS_SERVER_ID=
JVB_WS_TLS=
```

The Docker guide states that `COLIBRI_WEBSOCKET_REGEX` controls proxy matching to JVBs and recommends overriding it in production with values matching the possible JVB IP ranges. ([Jitsi][2])

## 10. Health checks

### Check JVB container

```bash
docker compose ps
docker compose logs --tail=200 jvb
```

### Check UDP listening

```bash
ss -lunp | grep 10000
```

### Check Colibri REST locally

```bash
curl -s http://127.0.0.1:8080/colibri/stats | jq
```

Useful fields:

```text
conferences
participants
endpoints
bit_rate_download
bit_rate_upload
packet_rate_download
packet_rate_upload
stress_level
version[object Object],[object Object],[object Object],[object Object],[object Object],[object Object]
```

### Check Jicofo sees bridges

On the core node:

```bash
docker compose logs jicofo | grep -i bridge
```

Expected idea:

```text
Added new videobridge
Bridge selected for conference
```

### Check Prosody connection

```bash
docker compose logs prosody | grep -i jvb
```

## 11. Monitoring

Recommended stack:

```text
Prometheus
Grafana
Loki or centralized Docker logs
Node Exporter
cAdvisor
Blackbox Exporter
```

Monitor at least:

| Metric                    | Why it matters                   |
| ------------------------- | -------------------------------- |
| CPU usage per JVB         | SFU forwarding is CPU-sensitive  |
| NIC bandwidth             | Media traffic is bandwidth-heavy |
| UDP packet drops          | Causes audio/video instability   |
| JVB stress level          | Used for bridge load decisions   |
| Conferences per JVB       | Confirms distribution            |
| Participants per JVB      | Capacity planning                |
| Jicofo bridge count       | Detects missing bridges          |
| Prosody 5222 availability | Remote JVB registration          |
| Packet loss / jitter      | User quality indicator           |

## 12. Autoscaling approach

Basic autoscaling logic:

```text
if average JVB stress_level > 0.75 for 5 minutes:
    add one JVB node

if average JVB stress_level < 0.25 for 30 minutes:
    drain one JVB node
    wait until conferences = 0
    remove node
```

Safe scale-down process:

```bash
curl -X POST http://127.0.0.1:8080/colibri/shutdown
```

Then wait until:

```bash
curl -s http://127.0.0.1:8080/colibri/stats | jq '.conferences'
```

returns:

```text
0
```

Do not kill a busy JVB unless you accept dropping active conferences.

## 13. Common failure modes

### Calls work with two users but fail with three or more

Most likely cause:

```text
JVB_ADVERTISE_IPS is wrong
UDP 10000 is blocked
NAT is not forwarding UDP correctly
```

The Docker guide specifically warns([Jitsi][2])IP advertisement can cause calls to crash when more than two users join. citeturn115407view3

### Remote JVB never appears in Jicofo

Check:

```text
JVB_AUTH_PASSWORD mismatch
Prosody 5222 blocked
Wrong XMPP_SERVER
Wrong XMPP_AUTH_DOMAIN
Wrong XMPP_INTERNAL_MUC_DOMAIN
Wrong JVB_BREWERY_MUC
Firewall allows only public interface but JVB uses private route
```

### Multiple JVBs appear, but traffic only goes to one

Possible causes:

```text
Very few conferences
Bridge stress threshold not reached
Jicofo bridge selection strategy
One bridge has better region/locality
Other bridges are unhealthy
```

Remember: distribution is usually per conference, not per packet.

### Browser console shows Colibri WebSocket errors

Check:

```text
ENABLE_COLIBRI_WEBSOCKET
COLIBRI_WEBSOCKET_REGEX
JVB_WS_SERVER_ID
JVB_WS_DOMAIN
Reverse proxy websocket Upgrade headers
Routing /colibri-ws/<server-id>/ to the correct JVB
```

Jitsi Videobridge’s WebSocket documentati([GitHub][3]) support WebSocket and route the `server-id` path to the correct bridge. citeturn206078view0

