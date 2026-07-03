# Ansible Roles and Directory Structure

Ansible roles help organize automation tasks, variables, files, and other resources into a structured format. This organization promotes reusability, simplifies management, and results in cleaner, more maintainable code.

## Creating a Role Directory Structure

To create a new Ansible role, use the following command:

```bash
ansible-galaxy init <role_name>
```

This command generates the standard directory structure for an Ansible role, which includes the following directories:

### Ansible Role Directory Breakdown

1. **`roles/`**: The top-level directory where all roles are stored. Each role has its own directory within this folder.
   
2. **`<role_name>/`**: Each role directory, named after the role (e.g., `webserver`), contains the following subdirectories:

   - **`tasks/`**: Defines the list of tasks to be executed by the role, usually in a `main.yml` file.
   - **`handlers/`**: Contains handlers that are triggered by tasks, defined in a `main.yml` file.
   - **`defaults/`**: Holds default variables for the role in `defaults/main.yml`.
   - **`vars/`**: Contains variables with higher precedence than `defaults`, stored in `vars/main.yml`.
   - **`files/`**: Stores static files to be deployed to managed nodes.
   - **`templates/`**: Holds Jinja2 templates for dynamic file generation.
   - **`meta/`**: Contains metadata about the role, including dependencies.
   - **`library/`** (Optional): Stores custom modules.
   - **`module_utils/`** (Optional): Contains utilities for custom modules.
   - **`lookup_plugins/`** (Optional): Holds custom lookup plugins.
   - **`filter_plugins/`** (Optional): Stores custom filter plugins.

This structure ensures roles are well-organized, making them easier to share and reuse.

## Host-Specific Variables (`host_vars`)

`host_vars` define variables specific to individual hosts (managed nodes), allowing customization of configurations and behavior at the host level.

### Key Points:

- **Location**: `host_vars` is typically located at the same level as your inventory file or playbook.
- **Structure**: Inside `host_vars`, create files named after each host (e.g., `webserver1.example.com.yml`).
- **Precedence**: Variables in `host_vars` override group variables and defaults.

### Example:

```yaml
# host_vars/webserver1.example.com.yml
http_port: 8080
max_clients: 200
```

## Group-Specific Variables (`group_vars`)

`group_vars` define variables for groups of hosts, reducing repetition and enhancing organization when configuring multiple hosts with common settings.

### Key Points:

- **Location**: `group_vars` is typically located at the same level as your inventory file or playbook.
- **Structure**: Inside `group_vars`, create files named after each group (e.g., `webservers.yml`).
- **Precedence**: Variables in `group_vars` have a lower precedence than `host_vars` but higher than global variables.

### Example:

```yaml
# group_vars/dbservers.yml
db_port: 5432
db_user: "dbadmin"
```

## The `files` Directory in Ansible Roles

The `files` directory in an Ansible role stores static files that are copied to managed nodes.

### Usage:

- **Static Files**: Files that do not require modification before being transferred.
- **Task Example**:

```yaml
# roles/my_role/tasks/main.yml
- name: Copy a script to the target host
  ansible.builtin.copy:
    src: example_script.sh
    dest: /usr/local/bin/example_script.sh
    mode: '0755'
```

## The `templates` Directory in Ansible Roles

The `templates` directory stores Jinja2 templates, which are dynamically processed to create files on managed nodes.

### Example:

```yaml
# roles/my_role/tasks/main.yml
- name: Configure application
  ansible.builtin.template:
    src: my_config_file.conf.j2
    dest: /etc/myapp/my_config_file.conf
```

### Sample Template:

```jinja
# my_config_file.conf.j2
server_name: {{ server_name_variable }}

{% if enable_feature %}
enable_feature: true
{% else %}
enable_feature: false
{% endif %}

{% for item in item_list %}
item_name: {{ item.name }}
item_value: {{ item.value }}
{% endfor %}

database_host: {{ database_host_variable | default('localhost') }}
```

## Handlers in Ansible Roles

Handlers are tasks triggered by other tasks, typically used to perform actions like restarting a service when a configuration change occurs.

### Example:

```yaml
# roles/my_role/tasks/main.yml
- name: Install apache2
  ansible.builtin.apt:
    name: apache2
    state: present
  notify: restart apache2

handlers:
  - name: restart apache2
    ansible.builtin.service:
      name: apache2
      state: restarted
```

## Default Variables in Ansible Roles (`defaults` Directory)

The `defaults` directory contains role-specific default variables with the lowest precedence, allowing them to be easily overridden.

### Example:

```yaml
# roles/my_role/defaults/main.yml
web_server_port: 80
max_clients: 100
```

## The `tasks` Directory in Ansible Roles

The `tasks` directory is where the main actions of a role are defined. It typically contains a `main.yml` file, which outlines the tasks Ansible should perform.

### Example:

```yaml
# roles/my_role/tasks/main.yml
- name: Include setup tasks
  import_tasks: setup.yml

- name: Install required packages
  import_tasks: install.yml

- name: Configure application
  import_tasks: configure.yml
```

## Importing Roles in a Playbook

You can import multiple roles within a playbook as shown below:

```yaml
- hosts: all
  roles:
    - role: role1
    - role: role2
    - role: role3
  gather_facts: yes
```

## Importing Other Tasks

In addition to roles, you can also include specific task files within a playbook:

```yaml
- name: Basic Setup
  include_tasks: task_file.yaml
```

## Working with Tags

Tags allow you to run specific parts of your playbook or roles. They are useful when you want to execute only a subset of tasks.

### Example:

```yaml
- hosts: all
  roles:
    - role: role1
  gather_facts: yes
  tags: [install]
```

### Running Playbooks with Tags

```bash
ansible-playbook -i inventory.ini main.yml -t install
```

### Listing Tasks with Tags

To see which tasks will run under a specific tag, use:

```bash
ansible-playbook -i inventory.ini main.yml -t install --list-tasks
```

## Copying `resolv.conf` with a Jinja Template

Use a Jinja template to dynamically generate the `resolv.conf` file.

### Playbook:

```yaml
- name: Copy resolv.conf
  ansible.builtin.template:
    src: resolv.conf.j2
    dest: /etc/resolv.conf
    mode: 0644
```

### Jinja Template (`resolv.conf.j2`):

```jinja
nameserver {{ DNS1 }}
nameserver {{ DNS2 }}
```

### Group Variables (`group_vars`):

```yaml
# group_vars/all.yml
DNS1: 8.8.8.8
DNS2: 4.2.2.4
```
