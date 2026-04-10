# 🛣️ `route` Command Documentation

The `route` command is used to view and manipulate the IP routing table in Linux systems. Below is a concise guide to listing, adding, and deleting routes using `route`.

---

## 📋 View Routing Table

```bash
route -n
```

* **Description**: Displays the kernel routing table.
* **`-n`**: Shows numerical addresses instead of resolving hostnames (faster and cleaner).

---

## ➕ Add Routes

### Add a Network Route

```bash
route add -net 10.10.10.0 netmask 255.255.255.0 gw 192.168.1.1
```

* **`-net 10.10.10.0`**: Specifies the network address.
* **`netmask 255.255.255.0`**: Defines the subnet mask for the network.
* **`gw 192.168.1.1`**: Sets the gateway through which packets will be routed.

### Add a Default Gateway

```bash
route add default gw 192.168.1.1
```

* **default**: Indicates this is the default route.
* **`gw 192.168.1.1`**: The default gateway IP address for all traffic not destined for a known network.

---

## ❌ Delete Routes

### Delete a Network Route

```bash
route del -net 10.10.10.0 netmask 255.255.255.0
```

* Removes the specified network route.

### Delete the Default Route

```bash
route del default
```

* Removes the current default gateway.

---

## 📎 Notes

* These commands typically require **superuser (root)** privileges. Use `sudo` if needed:

  ```bash
  sudo route add ...
  ```

* Consider using `ip route` instead of `route`, as `route` is deprecated on some modern distributions:

  ```bash
  ip route show
  ```

