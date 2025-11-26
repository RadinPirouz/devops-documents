# Setting Up GitLab CE on Ubuntu

Follow the steps below to install and configure GitLab Community Edition (CE) on your Ubuntu system.

---

## Step 1: Update the System
Ensure your package lists are up-to-date:
```bash
sudo apt update
```

---

## Step 2: Install Dependencies
Install required packages for GitLab:
```bash
sudo apt install -y ca-certificates curl openssh-server postfix tzdata perl
```

- **ca-certificates**: Ensures proper SSL certificate handling.
- **curl**: For downloading files.
- **openssh-server**: For SSH-based Git operations.
- **postfix**: Mail transport agent for email notifications.
- **tzdata**: Time zone data.
- **perl**: Required by GitLab scripts.

During the installation, configure **Postfix** to match your mail setup. If unsure, select "Internet Site" and provide your domain.

---

## Step 3: Add GitLab's Repository
Download and run the repository setup script:
```bash
curl -LO https://packages.gitlab.com/install/repositories/gitlab/gitlab-ce/script.deb.sh
sudo bash script.deb.sh
```

---

## Step 4: Install GitLab CE
Install the GitLab CE package:
```bash
sudo apt install -y gitlab-ce
```

---

## Step 5: Configure GitLab
Edit the GitLab configuration file to match your environment:
```bash
sudo vim /etc/gitlab/gitlab.rb
```

- Modify the `external_url` setting to your desired domain or IP.

Save and exit the editor.

---

## Step 6: Apply the Configuration
Reconfigure GitLab to apply the changes:
```bash
sudo gitlab-ctl reconfigure
```

---

## Step 7: Retrieve the Initial Root Password
After configuration, retrieve the initial root password:
```bash
sudo cat /etc/gitlab/initial_root_password
```

---

## Notes
- The default admin username is `root`.
- Save the password securely and change it after the first login.

---

## Troubleshooting
- If you encounter issues, consult the [GitLab Documentation](https://docs.gitlab.com) or check logs in `/var/log/gitlab`.

---

Enjoy using GitLab CE!
