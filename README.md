# Three-Tier Application Demo

## Overview

A demo application with a three-tier architecture (**Frontend → Backend → Database**) designed to:

1. Show the capabilities of the cloud platform
2. Demonstrate how Network Policies work
3. Example of integration with Dex authentication system
4. Testing the interaction of components in a virtualized environment

![](./demo-app.png)

### Application Structure

- **Project: demo-db**
  - **Database**
    - VM: `db` (PostgreSQL)
- **Project: demo-app**
  - **Frontend**
    - VM: `frontend` (Bootstrap app)
    - Pod: `frontend` (Bootstrap app)
  - **Backend**
    - VM: `backend-a` (Flask + Gunicorn)
    - VM: `backend-b` (Flask + Gunicorn)

Component interaction is restricted by network policies. Application access requires authentication via Dex.

## Access System

| User                       | Role                             | Access Rights                            |
| -------------------------- | -------------------------------- | ---------------------------------------- |
| `demo-user@flant.com`      | Application User                 | Access via web interface                 |
| `demo-db-admin@flant.com`  | Project Administrator `demo-db`  | Full VM access with PostgreSQL           |
| `demo-app-admin@flant.com` | Project Administrator `demo-app` | Management of all application components |

Translated with DeepL.com (free version)

## Repository Structure

- `/apps` - Frontend and backend source code
- `/k8s` - Kubernetes deployment manifests
- `/ansible` - Ansible playbooks for VM management

## Requirements

### Required d8 Modules

Ensure the following d8 modules are enabled and configured:

- `admission-policy-engine`
- `cni-cilium`
- `console`
- `multitenancy-manager`
- `service-with-healthchecks`
- `user-authn`
- `virtualization`
- `operator-argo` (required for ArgoCD installation)

### Installation-Specific Requirements

**For Option 1 (Manual Installation via Task):**
- [task](https://taskfile.dev)
- [yq](https://github.com/mikefarah/yq)
- [ansible](https://docs.ansible.com/ansible/latest/index.html)
- [d8](https://github.com/deckhouse/deckhouse-cli) (v0.27.0+ for ansible-inventory support)

## Installation

### Option 1: Manual Installation via Task

1. Create a `.env` file with infrastructure settings:

```ini
PASSWORD=password
FQDN=demo.example.com
```

2. Generate SSH keys for VM access:

```bash
task ssh-gen
```

3. Deploy the application:

```bash
task deploy
```

4. Uninstall the application:

```bash
task undeploy
```

### Option 2: ArgoCD Installation

1. Apply the ApplicationSet:

```bash
task argocd:apply
```

2. ArgoCD will automatically create and sync applications for `demo-app` and `demo-db` namespaces.

3. To remove, delete the ApplicationSet:

```bash
task argocd:delete
```

## How to connect to VM

### Via Task (SSH)

```bash
task ssh:frontend    # Connect to frontend VM
task ssh:backend-a   # Connect to backend-a VM
task ssh:backend-b   # Connect to backend-b VM
task ssh:db          # Connect to database VM
```

### Via d8 CLI

**SSH:**
```bash
d8 v ssh -n demo-app cloud@<vmname> -i ./tmp/demo --local-ssh
```

**Console:**
```bash
d8 v console -n demo-app <vmname>
```

## Ansible Management

The project includes Ansible playbooks for automated VM management. Uses `d8 v ansible-inventory` for dynamic inventory discovery.

**Check VM uptime:**
```bash
task ansible:uptime
```

**Update packages on all VMs:**
```bash
task ansible:update
```

**Run security checks:**
```bash
task ansible:security-check
```

