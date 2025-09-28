### 📄 **NGINX File Server Configuration**

This configuration sets up an NGINX server to serve files from two different directories:

* `/srv/files` for general file browsing at the root path (`/`)
* `/srv/images` for image browsing at `/image`

```nginx
server {
    # Define the domain name for this server block
    server_name domain;

    # Default root directory for the server
    root /srv/files;

    # Serve files and list directory contents at the root URL (e.g., http://domain/)
    location / {
        autoindex on;  # Enables directory listing
    }

    # Serve images and list contents at /image (e.g., http://domain/image/)
    location /image {
        autoindex on;            # Enables directory listing
        root /srv/images;        # Note: this overrides the global root
                                 # Final path served will be /srv/images/image/ due to how root works
    }
}
```

---

### ⚠️ **Important Notes**

1. **Path Behavior**:

   * In the `/image` block, using `root` adds the location path (`/image`) to the end. So `http://domain/image/` will map to `/srv/images/image/`.
   * If you want `/image/` to map directly to `/srv/images/`, use `alias` instead:

     ```nginx
     location /image/ {
         autoindex on;
         alias /srv/images/;
     }
     ```

2. **Security**:

   * Be cautious when enabling `autoindex`; it exposes directory contents to the public.
   * Consider restricting access or adding authentication for sensitive directories.

3. **Permissions**:

   * Ensure the NGINX user (usually `www-data`) has read access to the directories.

