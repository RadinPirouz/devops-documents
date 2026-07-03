
# Setting Up and Configuring Redis Server

## 1. Install Redis Server
Update your package list and install Redis server:
```bash
apt update && apt install redis-server -y
```

## 2. Update Redis Configuration
Edit the Redis configuration file:
```bash
vim /etc/redis/redis.conf
```

### Change Supervision Service to Systemd
Locate the `supervised` directive and change its value to `systemd`:
```conf
supervised systemd
```

### Restart the Redis Service
Restart the Redis service to apply changes:
```bash
systemctl restart redis
```

## 3. Test Redis Server
Use the Redis CLI to test the server:
```bash
redis-cli
```

Run the following commands:
- Test connectivity:
  ```bash
  ping
  ```
  Expected output:
  ```
  PONG
  ```
- Test basic operations:
  ```bash
  set test "This is test"
  get test
  ```
  Expected output:
  ```
  "This is test"
  ```

## 4. Configure Binding
Edit the Redis configuration file:
```bash
vim /etc/redis/redis.conf
```

### Change Binding Address
Update the `bind` directive to allow external connections. For example:
```conf
bind 0.0.0.0
```
> **Note:** Replace `0.0.0.0` with the specific IP addresses you want to allow, if necessary.

## 5. Set a Password
Secure your Redis server by setting a password:
```bash
vim /etc/redis/redis.conf
```

Find the `requirepass` directive and set your desired password:
```conf
requirepass <password>
```

### Test Authentication
To test the password configuration:
```bash
redis-cli
auth <password>
```

Run the `ping` command again:
```bash
ping
```
Expected output:
```
PONG
```

---
Now your Redis server is installed, configured, and secured!
