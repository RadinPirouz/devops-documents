---
title: "Jitsi Production Component Guide"
subtitle: "Component-by-component explanation for production DevOps design"
author: "Prepared for production planning"
date: "2026-05-29"
---

# Jitsi Production Component Guide

## 1. Purpose of this document

This document explains the main Jitsi components, what each one does, how they communicate, what ports they use, how they scale, and how to operate them in a production environment.

The focus is a production Jitsi Meet deployment that can handle more than 1000 concurrent participants across many different meetings. This is not the same as one single 1000-person interactive room. A single huge room should normally be treated as a webinar or livestream design, while many simultaneous rooms are handled by horizontal scaling of the media layer.

## 2. Core idea: signaling and media are separate

A Jitsi system has two main traffic planes:

1. Signaling plane: users and backend components exchange control messages. This includes joining a room, creating a conference, presence, mute state, chat, permissions, lobby, and room metadata. Jitsi uses XMPP for this signaling layer.
2. Media plane: audio, video, screen share, RTP/RTCP, bandwidth estimation, packet routing, and WebRTC transport. This is handled mainly by Jitsi Videobridge.

A production deployment is successful when these two planes are treated separately:

- Prosody and Jicofo are the control/signaling brain.
- Jitsi Videobridge is the high-bandwidth media router.
- Nginx serves the web app and proxies WebSocket/BOSH traffic.
- TURN helps users behind restrictive networks.
- Jibri records or livestreams conferences.
- Jigasi connects SIP/PSTN-style audio systems.

## 3. High-level architecture

```text
Browser / Mobile App
        |
        | HTTPS 443, WebSocket, BOSH
        v
Nginx / Jitsi Meet Web
        |
        | XMPP signaling
        v
Prosody XMPP Server <----> Jicofo Conference Focus
        ^                         |
        |                         | COLIBRI / bridge control
        |                         v
        |                  Jitsi Videobridge Pool
        |                         |
        |                         | WebRTC media: UDP 10000, SRTP/RTP/RTCP
        v                         v
Participants  <--------------->  JVB media routing

Optional components:
- Coturn: STUN/TURN relay for difficult NAT/firewall cases
- Jibri: recording and livestreaming worker
- Jigasi: SIP audio gateway
- Etherpad: collaborative document integration
- Monitoring: Prometheus, Grafana, logs, alerts
```

Official Jitsi documentation describes the main components as Jitsi Meet, Jitsi Videobridge, Jicofo, Jigasi, Jibri, and Prosody. It also defines Prosody as the XMPP server used for signaling, JVB as the WebRTC server that routes video streams, and Jicofo as the server-side focus component that manages media sessions and acts as a load-balancing controller between participants and videobridges. [1]

## 4. Component summary table

| Component | Main job | Traffic type | Scale method | Production note |
|---|---|---|---|---|
| Jitsi Meet Web | Browser UI and frontend application | HTTPS, WebSocket, BOSH | Horizontally with stateless web nodes or shards | Keep config consistent across nodes |
| Nginx | TLS termination, static files, reverse proxy | TCP 80/443 | Horizontal behind load balancer | Must correctly proxy WebSocket/BOSH paths |
| Prosody | XMPP signaling and authentication | XMPP, internal modules | Usually per shard; not the main media bottleneck | Protect internal XMPP ports |
| Jicofo | Conference focus, room orchestration, bridge selection | XMPP, COLIBRI control | Usually per shard; one active focus per deployment/shard | Critical control-plane component |
| Jitsi Videobridge | SFU media routing | WebRTC, UDP/RTP/SRTP | Add more JVB nodes | Main scaling point for 1000+ users |
| Coturn | STUN/TURN relay | UDP/TCP/TLS relay | Add more TURN nodes | Can consume large bandwidth |
| Jibri | Recording/livestream worker | Joins as special participant, encodes output | One worker per simultaneous recording | Heavy CPU/RAM/disk usage |
| Jigasi | SIP audio gateway | SIP/RTP/XMPP | Add instances if SIP demand grows | Audio-only SIP bridge |
| Etherpad | Shared notes/document editing | HTTP/WebSocket | Optional app scaling | Not required for video calls |
| Prometheus/Grafana/Loki | Metrics, dashboarding, logs | Metrics/log collection | Scale by observability need | Required for production operation |

## 5. Jitsi Meet Web

### What it is

Jitsi Meet Web is the user-facing web application. It is a WebRTC-compatible JavaScript application built with React and React Native concepts. In a browser deployment, users load this app from the Jitsi web server, usually through Nginx. The same product family also supports mobile applications.

### What it does

Jitsi Meet Web handles:

- Room URL and initial page load.
- User interface for camera, microphone, screen share, chat, reactions, tiles, moderator controls, lobby, settings, and device selection.
- WebRTC client logic in the browser.
- Signaling connection to Prosody through BOSH or WebSocket.
- Interaction with the Jitsi Meet External API when embedded inside another application.
- Configuration from files such as `config.js` and `interface_config.js` in package-based deployments.

### How it works in a call

1. User opens `https://meet.example.com/room-name`.
2. Nginx serves the static Jitsi Meet web application.
3. The web app reads configuration such as domain, anonymous domain, BOSH/WebSocket URLs, video constraints, prejoin behavior, lobby, and authentication settings.
4. The browser connects to Prosody for signaling.
5. The browser starts WebRTC negotiation and exchanges transport/media information through the signaling layer.
6. Actual audio/video packets go to Jitsi Videobridge, not to the web app.

### Production handling

- Keep web configuration version-controlled.
- Use the same `config.js` values across all web nodes in a shard.
- Put web nodes behind a load balancer only if the signaling paths and domain/shard routing are designed correctly.
- Do not overload the web component with recording, media routing, or TURN duties.
- For application integration, prefer JWT authentication and controlled room creation rather than public anonymous room creation.

## 6. Nginx or reverse proxy

### What it is

Nginx is normally used to serve the Jitsi Meet frontend, terminate TLS, redirect HTTP to HTTPS, and proxy special routes for signaling and bridge communication.

### What it does

Nginx handles:

- Port 80 for HTTP redirects and Let's Encrypt validation.
- Port 443 for HTTPS access.
- Static web assets.
- Reverse proxying for XMPP over WebSocket or BOSH.
- Reverse proxying for Colibri WebSocket paths used by JVB.
- Optional TLS routing or stream multiplexing when TURN over 443 is used.

### Important routes

Common important routes include:

```text
/                 Jitsi Meet web application
/http-bind        BOSH fallback for XMPP signaling
/xmpp-websocket   XMPP over WebSocket
/colibri-ws       JVB Colibri WebSocket path
```

### Production handling

- Use a trusted TLS certificate.
- Enable HTTP to HTTPS redirect.
- Forward WebSocket upgrade headers correctly.
- Do not expose internal admin or metrics endpoints through public Nginx.
- If using Cloudflare or another proxy, ensure WebRTC and WebSocket behavior is compatible with the deployment.
- Keep Nginx logs integrated with centralized logging.

## 7. Prosody

### What it is

Prosody is the XMPP server in Jitsi. It is the signaling backbone. Jitsi documentation describes Prosody as the XMPP server used for signaling. [1]

### What it does

Prosody handles:

- User XMPP sessions.
- Presence inside rooms.
- Multi-user chat rooms for conferences.
- Authentication domains.
- Guest domains.
- Lobby rooms and waiting behavior.
- JWT token verification modules.
- Internal accounts used by Jicofo, JVB, Jibri, and Jigasi.
- XMPP service discovery.
- TURN credential advertisement through XMPP when configured.

### Important virtual hosts and components

A typical deployment can include these logical domains:

```text
meet.example.com                  Main user-facing XMPP virtual host
auth.meet.example.com             Internal authenticated domain
conference.meet.example.com       MUC component for conference rooms
internal.auth.meet.example.com    Internal component/auth domain
focus.meet.example.com            Jicofo focus identity
recorder.meet.example.com         Jibri recorder domain, if recording is enabled
guest.meet.example.com            Anonymous guest domain, if guest access is enabled
```

Exact names depend on package, Docker, and authentication design.

### How Prosody works in a call

1. A browser client connects to Prosody through Nginx using XMPP over WebSocket or BOSH.
2. Prosody authenticates the user or treats the user as a guest depending on configuration.
3. The user joins a MUC room such as `room-name@conference.meet.example.com`.
4. Jicofo observes room creation and coordinates the conference.
5. JVB and Jicofo also connect through XMPP service accounts.
6. Signaling messages continue through Prosody while media flows through JVB.

### Production handling

- Do not expose Prosody's internal ports publicly.
- Restrict XMPP component/client ports to internal networks or known JVB/Jicofo/Jibri hosts.
- Use JWT authentication for app-based deployments.
- Use guest domain only when you want authenticated moderators and unauthenticated attendees.
- Monitor Prosody CPU, memory, connection count, and logs.
- Be aware that Prosody is usually not the media bottleneck, but it is a critical control-plane dependency.

## 8. Jicofo

### What it is

Jicofo means Jitsi Conference Focus. It is the conference coordinator. Official Jitsi documentation describes Jicofo as the server-side focus component used in Jitsi Meet conferences that manages media sessions and acts as a load balancer between participants and the videobridge. [1]

### What it does

Jicofo handles:

- Conference creation and lifecycle.
- Selecting a Jitsi Videobridge for a conference.
- Managing participants at the signaling level.
- Managing the relationship between conference rooms and JVBs.
- Controlling JVBs through the COLIBRI protocol.
- Coordinating Jibri sessions for recording or livestreaming.
- Moderator and feature coordination with Prosody modules.
- Bridge health and load-aware bridge selection.

### How Jicofo works in a call

1. A user joins a room through Prosody.
2. Jicofo detects or is assigned to manage the room.
3. Jicofo checks available JVBs.
4. Jicofo selects an appropriate JVB for the conference.
5. Jicofo instructs JVB to create or update the conference state.
6. Participants exchange WebRTC offers/answers and ICE data through signaling.
7. Jicofo continues coordinating participant joins/leaves, bridge state, and optional services.

### Scaling behavior

In the official scalable setup, the central Jitsi Meet instance includes Nginx, Prosody, and Jicofo, while multiple JVB nodes are attached separately. The documentation states that when a new conference starts, Jicofo picks a videobridge and schedules the conference on it. [3]

### Production handling

- Treat Jicofo as a critical control-plane service.
- Keep Jicofo logs centralized.
- Monitor bridge selection behavior and conference allocation.
- If using sharding, run separate Jicofo/Prosody stacks per shard rather than trying to make one huge control plane without design.
- Restart Jicofo carefully because existing conferences can be affected depending on deployment behavior and reconnect handling.

## 9. Jitsi Videobridge

### What it is

Jitsi Videobridge, usually called JVB, is the media router. It is a Selective Forwarding Unit, or SFU. Official Jitsi documentation describes it as a WebRTC-compatible server designed to route video streams among conference participants. [1]

### What it does

JVB handles:

- WebRTC media transport.
- ICE connectivity.
- DTLS-SRTP media security.
- RTP and RTCP packet routing.
- Audio/video forwarding.
- Screen-share forwarding.
- Simulcast and scalable video routing.
- Bandwidth estimation.
- Receiver constraints and LastN behavior.
- Packet loss recovery features such as retransmissions, depending on configuration and browser support.
- Colibri WebSocket communication.
- Media-related metrics.

### How JVB is different from an MCU

JVB normally does not mix or transcode every user's video into one combined stream. Instead, it selectively forwards streams. This is why Jitsi can scale better than a traditional MCU design, but it also means that bandwidth planning and client CPU are still important.

### How media flows

```text
User A camera/mic -> encrypted WebRTC stream -> JVB
JVB decides which participants should receive User A
JVB forwards selected encrypted media packets -> User B, User C, User D
```

JVB is not the same as TURN. TURN simply relays traffic when endpoints cannot connect normally. JVB understands the conference and makes routing decisions.

### Why JVB is the main scaling component

The official scalable setup says the first limiting factor in a single-server Jitsi installation is the Videobridge, because it handles the actual video and audio traffic, and that videobridges are easy to scale horizontally by adding as many as needed. [3]

### Production handling

- Put JVB nodes on servers with strong network capacity.
- Open UDP 10000 from the public internet to each JVB unless your deployment uses a different media design.
- Ensure the advertised public IP is correct, especially with Docker, NAT, or private cloud networks.
- Keep 25-35 percent spare capacity.
- Monitor network throughput, packet loss, CPU, memory, conferences, endpoints, and bridge stress.
- Add JVB nodes to scale concurrent meetings.
- Do not assume one JVB can safely carry a whole production deployment.

## 10. Coturn, STUN, and TURN

### What it is

Coturn is a TURN/STUN server commonly used with Jitsi. STUN helps clients discover how they are seen from the public internet. TURN relays media when direct UDP connectivity is blocked or impossible.

### What it does

TURN helps users behind:

- Symmetric NAT.
- Corporate firewalls.
- UDP-blocking networks.
- Mobile carrier restrictions.
- Networks that only allow TCP 443.

### How TURN works with Jitsi

In a simple case, users connect to JVB over UDP 10000. In a restrictive network, the browser may be unable to send media directly to the JVB. TURN then relays the traffic through an allowed port such as TCP/TLS 443 or TCP 5349.

Official Jitsi TURN documentation says peer-to-peer calls should avoid going through JVB when possible, but direct connection is not always possible, and in those cases a TURN server can relay traffic. It also notes that default TURN ports include UDP 3478 and TCP/TLS 5349, and that TCP 443 can be useful for corporate networks that allow only HTTPS-like traffic. [7]

### Production handling

- Run at least two TURN servers for production.
- Treat TURN as a bandwidth-heavy media service.
- Avoid static TURN credentials exposed to browsers for long periods; prefer ephemeral credentials when possible.
- Monitor TURN bandwidth separately from JVB bandwidth.
- Do not put TURN on the same overloaded machine as Jitsi unless traffic is tiny.
- Use valid TLS certificates for TLS TURN services.

## 11. Jibri

### What it is

Jibri means Jitsi Broadcasting Infrastructure. It is the component used for server-side recording and livestreaming.

Official Jitsi architecture documentation describes Jibri as tools for recording and/or streaming a conference by launching a Chrome instance in a virtual framebuffer and capturing/encoding the output with ffmpeg. [1]

### What it does

Jibri handles:

- Joining a Jitsi room as a special recorder participant.
- Rendering the conference in Chrome.
- Capturing the rendered output.
- Encoding with ffmpeg.
- Saving a recording file or streaming to a service such as YouTube/RTMP.
- Reporting recording state back through XMPP.

### How Jibri works in a call

```text
Moderator clicks Record or Livestream
        |
        v
Jicofo requests an available Jibri
        |
        v
Jibri joins the room as a hidden/special participant
        |
        v
Chrome renders the conference layout
        |
        v
ffmpeg captures and encodes the output
        |
        v
Recording file or livestream output is created
```

### Capacity rule

Jibri does not scale like JVB. One Jibri instance supports one recording or livestream session at a time. Jitsi requirements documentation states that Jibri needs one system per recording: one Jibri instance equals one meeting, and five simultaneous recordings require five Jibri instances. [5]

The Jibri repository also states that only one recording at a time is supported on a single Jibri. [6]

### Production handling

- Do not run Jibri on the main Jitsi controller node for serious production.
- Do not run Jibri on JVB nodes.
- Use a separate Jibri pool.
- Size one worker per simultaneous recording or livestream.
- Monitor CPU, memory, disk throughput, disk usage, Chrome/Chromedriver health, and ffmpeg errors.
- Store recordings on durable storage, object storage, or a post-processing pipeline.

## 12. Jigasi

### What it is

Jigasi means Jitsi Gateway to SIP. It allows regular SIP clients to join Jitsi Meet conferences. Official Jitsi architecture documentation describes Jigasi as a server-side application that allows regular SIP clients to join Jitsi Meet conferences. [1]

### What it does

Jigasi handles:

- SIP call-in or call-out integration.
- Audio bridge between SIP endpoints and a Jitsi room.
- Connection to Prosody/XMPP as a component or service account.
- SIP registration to a SIP provider or PBX.
- Optional transcription-related workflows in some deployments.

### How Jigasi works

```text
SIP phone / PBX / provider
        |
        | SIP/RTP
        v
Jigasi
        |
        | XMPP signaling + media bridge behavior
        v
Jitsi room
```

### Production handling

- Deploy only if you need SIP/PSTN integration.
- Isolate SIP credentials and PBX connectivity.
- Plan port ranges for SIP media if enabled.
- Monitor call setup failures, SIP registration state, audio quality, and provider errors.
- Keep SIP access restricted to expected providers or internal PBX networks.

## 13. Etherpad

### What it is

Etherpad is an optional collaborative text editing service that can be integrated with Jitsi Meet for shared notes.

### What it does

Etherpad handles:

- Shared collaborative documents.
- Meeting notes.
- Text collaboration beside the video call.

### Production handling

- Do not deploy Etherpad unless users need shared notes.
- Put it behind authentication or controlled access if documents contain sensitive content.
- Back up its database if meeting notes matter.
- Monitor it separately from Jitsi media services.

## 14. Authentication components

### Available authentication models

Common production authentication models include:

- Internal Prosody users.
- JWT/token authentication.
- LDAP authentication.
- Guest domain with authenticated moderators.
- Application-controlled room creation.

Official token authentication documentation states that Jitsi can allow only users with a valid token to create new conference rooms, while others can join from an anonymous domain after the room exists. [8]

### Recommended production model

For a custom application or platform:

```text
Use JWT auth.
Only your backend creates valid meeting tokens.
Moderators receive tokens with room permissions.
Guests join through controlled room links or guest domain.
Lobby is enabled for sensitive rooms.
Anonymous public room creation is disabled.
```

### Why JWT is usually best for production

JWT makes Jitsi part of your application security model:

- Your app decides who can create rooms.
- Your app decides who is moderator.
- Your app can restrict access by room name.
- Your app can expire tokens.
- Your app can map users, avatars, display names, and roles.

### Production handling

- Store JWT secrets safely.
- Rotate secrets carefully.
- Use short token lifetimes where possible.
- Do not expose app secrets in frontend code.
- Disable anonymous room creation.
- Enable lobby and moderator controls.

## 15. Web clients and mobile clients

### What they are

Clients are the browsers and mobile apps used by participants.

### What they do

Clients handle:

- Camera and microphone capture.
- WebRTC encryption and transport.
- Encoding local media.
- Decoding remote media.
- UI interactions.
- Sending receiver constraints to request fewer or lower-quality remote streams.

### Production handling

Client performance is part of your infrastructure capacity. Even if JVB has enough bandwidth, weak phones or old laptops may fail in large rooms.

Use:

- Start with audio muted for large rooms.
- Start with video muted for large rooms.
- Limit default resolution.
- Limit visible remote videos with LastN/receiver constraints.
- Recommend Chrome/Chromium-based browsers or tested clients.
- Monitor client-side error reports if you control the application.

## 16. Monitoring and logging components

### What they are

Production Jitsi needs observability. Without monitoring, you cannot know whether the problem is JVB bandwidth, TURN fallback, Prosody signaling, client CPU, or bad network conditions.

### Recommended stack

```text
Prometheus       Metrics collection
Grafana          Dashboards
Loki or ELK      Logs
Node exporter    Server metrics
Blackbox exporter External health checks
Alertmanager     Alerts
```

### Metrics to watch

| Area | Important metrics |
|---|---|
| JVB | endpoints, conferences, packet loss, bitrate, CPU, memory, network in/out |
| Prosody | connections, auth failures, MUC behavior, module errors |
| Jicofo | bridge selection, conference allocation, errors |
| Nginx | 4xx/5xx, WebSocket upgrade failures, TLS expiry |
| TURN | relay bandwidth, allocation count, failed allocations |
| Jibri | active sessions, failed recordings, CPU, memory, disk, ffmpeg errors |
| System | CPU steal, disk usage, disk IO, network saturation, process restarts |

### Production handling

- Alert before saturation, not after users complain.
- Keep dashboards per shard and per JVB.
- Log conference IDs and bridge allocation events where possible.
- Track TURN usage percentage. A sudden increase means users cannot reach UDP directly.
- Track certificate expiry.

## 17. Ports and network paths

### Standard ports

| Port | Protocol | Component | Purpose |
|---|---|---|---|
| 80 | TCP | Nginx/Web | HTTP redirect and Let's Encrypt validation |
| 443 | TCP | Nginx/Web | HTTPS web app and WebSocket/BOSH proxy |
| 10000 | UDP | JVB | Main WebRTC media path |
| 5222 | TCP | Prosody | XMPP client/component communication, usually internal/restricted |
| 3478 | UDP | Coturn | STUN/TURN |
| 5349 | TCP/TLS | Coturn | TURN over TLS fallback |
| 20000-20050 | UDP | Jigasi | Optional SIP media range depending on deployment |

The official Docker deployment documentation lists external ports 80/tcp, 443/tcp, and 10000/udp, and also notes 20000-20050/udp for Jigasi SIP access if that component is deployed. [2]

The official Debian/Ubuntu self-hosting guide lists 80 TCP, 443 TCP, 10000 UDP, SSH, 3478 UDP, and 5349 TCP as relevant firewall ports for a typical server with coturn support. [4]

### Production rule

Open only what must be public. Keep the rest private.

```text
Public:
- 80/tcp
- 443/tcp
- 10000/udp on JVB nodes
- 3478/udp and 5349/tcp on TURN nodes, if used

Private/restricted:
- 5222/tcp Prosody
- metrics ports
- admin ports
- SSH
- Docker/Kubernetes APIs
```

## 18. How a participant joins a meeting

```text
1. User opens room URL.
2. Browser downloads Jitsi Meet Web from Nginx.
3. Browser opens XMPP signaling over WebSocket or BOSH.
4. Prosody authenticates or accepts guest access.
5. Browser joins the MUC room.
6. Jicofo coordinates the conference.
7. Jicofo selects a JVB.
8. Browser and JVB exchange WebRTC transport information through signaling.
9. Browser sends encrypted media to JVB.
10. JVB forwards selected media streams to other participants.
11. Prosody/Jicofo continue managing room state while JVB handles media.
```

## 19. Production topologies

### Single-server deployment

```text
One server:
- Nginx
- Jitsi Meet Web
- Prosody
- Jicofo
- JVB
- optional coturn
```

Good for testing, small internal teams, and proof of concept.

Not recommended for 1000+ production users.

### Split JVB deployment

```text
Controller node:
- Nginx
- Jitsi Meet Web
- Prosody
- Jicofo

Media nodes:
- JVB 1
- JVB 2
- JVB 3
- JVB N
```

This is the first serious production architecture. Jitsi's scalable setup recommends splitting the central Jitsi Meet instance from videobridges as the first scaling step. [3]

### Sharded deployment

```text
Shard A:
- Web
- Prosody
- Jicofo
- JVB pool

Shard B:
- Web
- Prosody
- Jicofo
- JVB pool

Application router:
- routes rooms/users to a shard
```

Good for high availability and large scale.

### Regional deployment

```text
EU region:
- EU web/control shard
- EU JVBs

US region:
- US web/control shard
- US JVBs

Asia region:
- Asia web/control shard
- Asia JVBs
```

Good when users are globally distributed and latency matters.

## 20. Scaling guide by component

| Component | Bottleneck | How to scale |
|---|---|---|
| Web/Nginx | TLS, static traffic, WebSocket proxying | Add web nodes or shards |
| Prosody | XMPP connections, modules, room state | Usually scale by shard, not by simply adding random replicas |
| Jicofo | Conference orchestration, bridge control | Usually scale by shard; design active focus carefully |
| JVB | Bandwidth, packet forwarding, CPU | Add more JVB nodes |
| TURN | Relay bandwidth | Add more TURN nodes, use geo-distribution |
| Jibri | Encoding CPU/RAM/disk | One Jibri per simultaneous recording |
| Jigasi | SIP calls and audio bridge load | Add more Jigasi instances if SIP use grows |
| Monitoring | Metrics/log volume | Scale storage and retention separately |

## 21. Production best practices

### Infrastructure

- Use separate controller and JVB nodes.
- Use separate TURN nodes for serious production.
- Use separate Jibri nodes for recording.
- Use configuration management such as Ansible, Terraform, or GitOps.
- Use pinned versions, not random latest images in production.
- Keep staging and production separate.

### Security

- Use trusted TLS certificates.
- Disable anonymous room creation.
- Prefer JWT for application integration.
- Enable lobby for guest access.
- Restrict Prosody, metrics, SSH, and admin ports.
- Rotate secrets.
- Do not expose Docker socket or internal service ports.

### Performance

- Keep UDP 10000 working for JVB nodes.
- Use TURN only as fallback, not as the normal path for everyone.
- Limit default video quality.
- Limit LastN/visible remote video count in large rooms.
- Start audio/video muted for large public rooms.
- Keep enough JVB spare capacity.

### Operations

- Monitor before production launch.
- Load test with realistic room patterns.
- Keep rollback packages or images ready.
- Upgrade JVB nodes one by one.
- Drain traffic before restarting busy components when possible.
- Keep clear incident runbooks.

## 22. Failure modes and where to look

| Symptom | Likely component | What to check |
|---|---|---|
| Page does not load | Nginx, DNS, TLS | DNS, certificate, Nginx logs, firewall 443 |
| Users can join but no audio/video | JVB, firewall, NAT | UDP 10000, JVB advertised IP, browser ICE candidates |
| Two users work but three or more fail | JVB path | JVB public IP, UDP 10000, NAT, Docker advertise IP |
| Users behind corporate networks fail | TURN | coturn health, 443/5349, credentials, certificates |
| Rooms are not created | Prosody/Jicofo | XMPP logs, auth config, Jicofo service account |
| JWT users cannot join | Prosody auth | app_id, app_secret, token claims, room claim, time skew |
| Recording fails | Jibri | Chrome, Chromedriver, ffmpeg, ALSA loopback, disk, Jibri account |
| SIP call-in fails | Jigasi | SIP credentials, PBX routing, firewall, media range |
| High packet loss | JVB/network | NIC saturation, cloud network, UDP drops, region distance |
| Random disconnects | Client/network/JVB | WebSocket stability, JVB stress, browser logs |

## 23. Recommended architecture for 1000+ concurrent users

For more than 1000 concurrent participants across many calls, a practical starting design is:

```text
2 Jitsi control shards
8-10 JVB nodes total
2 TURN nodes
1 monitoring/logging stack
Jibri pool only if recording/livestreaming is required
```

Each shard:

```text
1 controller node:
- Nginx
- Jitsi Meet Web
- Prosody
- Jicofo

4-5 JVB nodes:
- Jitsi Videobridge only
```

Shared or per-region:

```text
2 TURN nodes
Monitoring/logging
Optional Jibri worker pool
Optional Jigasi worker pool
```

This design allows:

- Horizontal media scaling by adding JVBs.
- Failure isolation by shard.
- Easier upgrades.
- Better observability.
- Controlled authentication and room routing.

## 24. Component responsibility map

```text
User interface problem        -> Jitsi Meet Web / browser
TLS or static file problem    -> Nginx / reverse proxy
Login or room auth problem    -> Prosody / JWT / LDAP
Room orchestration problem    -> Jicofo
Audio/video routing problem   -> JVB
Strict firewall problem       -> TURN
Recording/livestream problem  -> Jibri
SIP/PSTN problem              -> Jigasi
Scale problem                 -> Usually JVB, then sharding
```

## 25. Final production checklist

Before launch:

- Domain and DNS are correct.
- TLS certificate is trusted and auto-renewing.
- UDP 10000 reaches every JVB.
- JVB advertised IPs are correct.
- Prosody internal ports are not publicly exposed.
- JWT or chosen authentication is working.
- Guests cannot create rooms unless intentionally allowed.
- TURN works for restricted networks.
- Monitoring and alerts are active.
- Load test has been run with realistic room distribution.
- Jibri is deployed only if recording/livestreaming is needed.
- Backups exist for configuration and secrets.
- Upgrade and rollback procedure exists.

## References

[1] Jitsi Meet Handbook, Architecture: https://jitsi.github.io/handbook/docs/architecture/

[2] Jitsi Meet Handbook, Self-Hosting Guide - Docker: https://jitsi.github.io/handbook/docs/devops-guide/devops-guide-docker/

[3] Jitsi Meet Handbook, DevOps Guide - Scalable setup: https://jitsi.github.io/handbook/docs/devops-guide/devops-guide-scalable/

[4] Jitsi Meet Handbook, Self-Hosting Guide - Debian/Ubuntu server: https://jitsi.github.io/handbook/docs/devops-guide/devops-guide-quickstart/

[5] Jitsi Meet Handbook, Requirements - Recording/Jibri: https://jitsi.github.io/handbook/docs/devops-guide/devops-guide-requirements/

[6] Jitsi Jibri GitHub repository: https://github.com/jitsi/jibri

[7] Jitsi Meet Handbook, Setting up TURN: https://jitsi.github.io/handbook/docs/devops-guide/turn/

[8] Jitsi Meet Handbook, Token Authentication: https://jitsi.github.io/handbook/docs/devops-guide/token-authentication/