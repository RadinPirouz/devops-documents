# Jitsi Docker Plugins and Third-Party Software Catalog

This is a practical DevOps checklist for a self-hosted Jitsi Meet deployment running with Docker Compose. The official Docker stack is based around `web`, `prosody`, `jicofo`, and `jvb`, with optional Compose overlays for services like `jibri`, `jigasi`, `etherpad`, `whiteboard`, `transcriber`, `grafana`, `prometheus`, `rtcstats`, and log analysis. ([GitHub][1])

## 1. Core Jitsi Docker Components

| Component         | Purpose                                             | Docker Service |
| ----------------- | --------------------------------------------------- | -------------- |
| Jitsi Meet Web    | Frontend web UI, Nginx, static assets, external API | `web`          |
| Prosody           | XMPP server used for signaling, auth, room control  | `prosody`      |
| Jicofo            | Conference focus, room/session orchestration        | `jicofo`       |
| Jitsi Videobridge | SFU media bridge for audio/video routing            | `jvb`          |
| Jibri             | Recording and live streaming worker                 | `jibri`        |
| Jigasi            | SIP gateway and dial-in/dial-out support            | `jigasi`       |
| Jitsi Transcriber | Speech-to-text transcription support                | `transcriber`  |
| JaaS Components   | Hosted Jigasi-style components from 8x8/JaaS        | optional       |

## 2. Official Optional Docker Overlays

| Overlay File       | Feature                 | Use Case                                |
| ------------------ | ----------------------- | --------------------------------------- |
| `jibri.yml`        | Recording and streaming | Record meetings, stream to YouTube/RTMP |
| `jigasi.yml`       | SIP gateway             | Connect SIP PBX, PSTN, VoIP users       |
| `etherpad.yml`     | Shared documents        | Collaborative meeting notes             |
| `whiteboard.yml`   | Excalidraw whiteboard   | Collaborative drawing/whiteboard        |
| `transcriber.yml`  | Transcription           | Meeting captions/transcripts            |
| `grafana.yml`      | Grafana dashboard       | Metrics visualization                   |
| `prometheus.yml`   | Metrics scraping        | Monitoring Jitsi services               |
| `rtcstats.yml`     | WebRTC analytics        | Client-side WebRTC quality data         |
| `log-analyser.yml` | Log analysis            | Loki/OpenTelemetry/Grafana log view     |

The official Docker guide shows these overlays being started with commands like `docker compose -f docker-compose.yml -f jibri.yml up -d`, and similar combinations for Jigasi, Etherpad, whiteboard, transcriber, Grafana, and log analysis. ([Jitsi][2])

## 3. Reverse Proxy and TLS Software

| Software      | Purpose                                      | Docker-Friendly | Notes                                                           |
| ------------- | -------------------------------------------- | --------------- | --------------------------------------------------------------- |
| Nginx         | Reverse proxy, TLS termination, HTTP routing | Yes             | Common production choice                                        |
| Traefik       | Dynamic reverse proxy for Docker labels      | Yes             | Good for multi-service Docker hosts                             |

Jitsi Docker requires a real `PUBLIC_URL` for production deployments, and the official `.env` includes Let’s Encrypt-related settings such as domain, email, staging mode, and ACME server selection. ([Jitsi][2])

## 4. NAT, STUN, and TURN

| Software           | Purpose                | When to Use                                             |
| ------------------ | ---------------------- | ------------------------------------------------------- |
| coturn             | TURN/STUN relay server | Required for reliable calls behind strict NAT/firewalls |
| Google STUN        | Public STUN service    | Basic NAT discovery, not enough for all networks        |
| Custom STUN        | Your own STUN endpoint | Controlled infrastructure                               |
| TURN over TCP 443  | Firewall bypass        | Corporate networks that block UDP                       |
| TURN over TLS 5349 | Secure TURN relay      | Better for enterprise deployments                       |

Jitsi can use a TURN server for cases where direct peer-to-peer connectivity fails; the official TURN guide discusses coturn, XMPP-delivered TURN credentials, UDP 3478, TCP/TLS 5349, and using port 443 for restrictive networks. ([Jitsi][3])

## 5. Authentication and SSO

| Tool                           | Integration Type                 | Notes                                             |
| ------------------------------ | -------------------------------- | ------------------------------------------------- |
| Internal Prosody Auth          | Username/password inside Prosody | Simple small deployment                           |
| JWT Auth                       | Token-based authentication       | Best for custom apps and portals                  |
| LDAP                           | Directory authentication         | Enterprise user directories                       |
| Active Directory               | LDAP/SASL integration            | Corporate auth                                    |
| OpenLDAP                       | LDAP backend                     | Self-hosted directory                             |
| Keycloak                       | OIDC/SAML identity provider      | Usually integrated through JWT adapters           |
| authentik                      | OIDC/SAML identity provider      | Good self-hosted SSO option                       |
| Authelia                       | SSO and access control           | Usually used in front of apps                     |
| Dex                            | Lightweight OIDC provider        | Kubernetes-friendly                               |
| OAuth2 Proxy                   | Auth gateway                     | Can protect Jitsi landing pages or custom portals |
| jitsi-OIDC-adapter             | OIDC to Jitsi JWT bridge         | Community integration                             |
| jitsi-OIDC-SAML-adapter        | OIDC/SAML to Jitsi JWT bridge    | Community integration                             |
| nordeck/jitsi-keycloak-adapter | Keycloak adapter                 | Dockerized Jitsi integration                      |

The official Docker `.env` supports `AUTH_TYPE=internal`, `jwt`, `ldap`, or `matrix`, and includes JWT and LDAP configuration fields. Jitsi’s JWT auth plugin verifies client connections using JWT and supports shared-secret or public-key validation. ([GitHub][4])

## 6. SIP, VoIP, and Telephony

| Software                    | Purpose                | Works With               |
| --------------------------- | ---------------------- | ------------------------ |
| Jigasi                      | Jitsi SIP gateway      | SIP providers, PBX, PSTN |
| Asterisk                    | PBX server             | Jigasi                   |
| FreePBX                     | Asterisk management UI | Jigasi                   |
| FreeSWITCH                  | PBX/media server       | Jigasi                   |
| Kamailio                    | SIP proxy              | Large SIP routing        |
| OpenSIPS                    | SIP proxy              | Large SIP routing        |
| SIP provider account        | External calling       | Jigasi                   |
| Twilio Elastic SIP Trunking | SIP trunk              | Jigasi/Asterisk          |
| Telnyx SIP                  | SIP trunk              | Jigasi/Asterisk          |
| VoIP.ms                     | SIP trunk              | Jigasi/Asterisk          |
| SignalWire                  | SIP/telephony          | Jigasi/Asterisk          |

Jitsi Docker’s `.env` includes Jigasi SIP settings such as SIP URI, SIP password, SIP server, SIP port, and SIP transport. ([GitHub][4])

## 7. Recording, Streaming, and Storage

| Software               | Purpose                      | Notes                                 |
| ---------------------- | ---------------------------- | ------------------------------------- |
| Jibri                  | Recording and streaming      | Official Jitsi recording component    |
| FFmpeg                 | Media processing             | Used in recording/streaming workflows |
| Google Chrome/Chromium | Headless capture for Jibri   | Required by Jibri                     |
| ALSA/PulseAudio        | Audio capture stack          | Used by Jibri                         |
| YouTube Live           | RTMP streaming target        | Jibri can stream to RTMP              |
| Twitch                 | RTMP streaming target        | Possible with stream key              |
| Facebook Live          | RTMP streaming target        | Possible with stream key              |
| Nginx RTMP Module      | Self-hosted RTMP endpoint    | Internal streaming pipeline           |
| Owncast                | Self-hosted live streaming   | RTMP target                           |
| Restream               | Multi-platform streaming     | RTMP target                           |
| MinIO                  | S3-compatible object storage | Store recordings                      |
| AWS S3                 | Object storage               | Store recordings                      |
| Wasabi                 | S3-compatible storage        | Store recordings                      |
| Backblaze B2           | Object storage               | Store recordings                      |
| rclone                 | Upload/sync recordings       | Post-recording automation             |

## 8. Collaboration Add-ons

| Software               | Purpose                      | Integration Style              |
| ---------------------- | ---------------------------- | ------------------------------ |
| Etherpad               | Shared document editing      | Official Docker overlay        |
| Excalidraw             | Whiteboard                   | Official whiteboard overlay    |
| Nextcloud              | Files, calendar, office docs | External integration           |
| OnlyOffice             | Document editing             | With Nextcloud or standalone   |
| Collabora Online       | Document editing             | With Nextcloud                 |

The official Docker setup has direct support for Etherpad document sharing and an Excalidraw-based virtual collaborative whiteboard. ([Jitsi][2])

## 9. Chat and Team Platform Integrations

| Platform                   | Integration Method                        | Notes                               |
| -------------------------- | ----------------------------------------- | ----------------------------------- |
| Matrix / Element           | Matrix auth or meeting integration        | Jitsi can be used from Matrix rooms |
| Mattermost                 | Jitsi plugin/integration                  | Team chat video calls               |
| Rocket.Chat                | Jitsi integration                         | Team chat video calls               |
| Nextcloud Talk / Nextcloud | External meeting links or app integration | Good self-hosted suite              |
| Moodle                     | Jitsi plugin                              | Education/LMS                       |

## 10. Web and App Embedding

| Tool              | Purpose                         | Notes                          |
| ----------------- | ------------------------------- | ------------------------------ |
| Jitsi IFrame API  | Embed meetings in websites/apps | Official supported method      |
| External API JS   | Browser-side meeting control    | Loaded from `/external_api.js` |
| lib-jitsi-meet    | Low-level JS library            | Build custom video apps        |


The official IFrame API lets you embed Jitsi Meet into your own application, and the event API allows listening to meeting events through `JitsiMeetExternalAPI`. ([Jitsi][5])

## 11. Prosody Plugins and XMPP Modules

| Plugin / Module Type         | Purpose                         |
| ---------------------------- | ------------------------------- |
| Custom Prosody modules       | Add custom XMPP behavior        |
| JWT auth module              | Token authentication            |
| LDAP/SASL auth module        | Enterprise directory auth       |
| MUC modules                  | Room behavior customization     |
| Lobby modules                | Guest waiting room behavior     |
| MUC size module              | Room participant metrics        |
| MUC domain mapper            | Multi-domain setups             |
| Token moderation             | Moderator control from JWT      |
| Room metadata modules        | Store extra room info           |
| Reservation modules          | Room booking or room validation |
| External services module     | TURN credential delivery        |
| Rate limiting modules        | Abuse protection                |
| Anti-spam modules            | Public server protection        |
| Webhook-style custom module  | Send events to external backend |
| Custom access control module | Per-room or per-user policy     |

For Docker deployments, custom Prosody plugins are usually mounted into the Prosody config/plugin path and enabled through Prosody/Jitsi configuration. The official Docker guide creates a `prosody/prosody-plugins-custom` directory for custom plugin use. ([Jitsi][2])

## 12. Monitoring and Observability

| Software            | Purpose                         | Notes                                  |
| ------------------- | ------------------------------- | -------------------------------------- |
| Prometheus          | Metrics collection              | Official Docker overlay exists         |
| Grafana             | Dashboards                      | Official Docker overlay exists         |
| Jitsi Meet Exporter | Prometheus exporter             | Exposes Jitsi metrics                  |
| Loki                | Log aggregation                 | Used in log analyzer stack             |
| OpenTelemetry       | Telemetry/log pipeline          | Used in log analyzer stack             |

The Jitsi Docker repository includes `prometheus.yml`, `grafana.yml`, `rtcstats.yml`, and `log-analyser.yml`; the log analyser uses Grafana Loki and OpenTelemetry for log management and analysis. ([GitHub][1])

