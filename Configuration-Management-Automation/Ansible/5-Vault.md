## Ansible Vault Guide

### 1. Creating an Encrypted File with Ansible Vault

To create a new encrypted file using Ansible Vault, use the following command:

```bash
ansible-vault create secret.yaml
```

You will be prompted to enter a password to encrypt the file. After that, you can add your variables, like in the example below:

```yaml
password: 123
```

Once you save and exit, the file will be encrypted. The content of the `secret.yaml` file will look like this:

```yaml
$ANSIBLE_VAULT;1.1;AES256
33653733613264663235353662336132376134313266666561363932373236653130393135373562
3838613763626464343334306661643634323537376537630a333833356462616666303833613066
35653039343366336233613164313365373466643262303761623363383530396336613438326263
3536633236376635320a396430353564356331623133653866663138373265363466353663353034
3830
```

### 2. Using Encrypted Variables in a Playbook

To use the encrypted variables stored in `secret.yaml`, include the file in your playbook using `vars_files`.

#### Example Playbook

```yaml
- hosts: all
  become: yes
  vars_files:
    - secret.yaml
  tasks:
    - name: Print Secret Password
      debug:
        msg: "Password is {{ password }}"
```

This playbook reads the encrypted `password` variable from `secret.yaml` and prints it.

### 3. Running the Playbook with Vault

To run a playbook that uses an encrypted file, use the following command:

```bash
ansible-playbook main.yaml -i servers.ini --ask-vault-pass --become
```

- **`--ask-vault-pass`**: Prompts for the Vault password before executing the playbook.
- **`--become`**: Ensures that the tasks are executed with elevated privileges (e.g., root).

When you run the command, you will be prompted to enter the Vault password to decrypt `secret.yaml` and access the `password` variable.

### 4. Additional Vault Commands

- **Edit an existing encrypted file**:

  ```bash
  ansible-vault edit secret.yaml
  ```

- **Rekey (change the Vault password)**:

  ```bash
  ansible-vault rekey secret.yaml
  ```

- **View the contents of an encrypted file (without decrypting it)**:

  ```bash
  ansible-vault view secret.yaml
  ```

- **Decrypt a Vault file permanently**:

  ```bash
  ansible-vault decrypt secret.yaml
  ```

- **Encrypt a previously unencrypted file**:

  ```bash
  ansible-vault encrypt secret.yaml
  ```


Ansible Vault provides a powerful way to securely manage sensitive data in your automation processes.