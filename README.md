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
kubectl apply -f argocd/apps-appset.yaml
kubectl apply -f argocd/projects-appset.yaml
```

2. ArgoCD will automatically create and sync applications for `demo-app` and `demo-db` namespaces.

3. To remove, delete the ApplicationSet:

```bash
kubectl delete -f argocd/apps-appset.yaml
kubectl delete -f argocd/projects-appset.yaml
```

## How to connect to VM

Via SSH

```bash
d8 v ssh -n demo-app cloud@<vmname> -i ./tmp/demo --local-ssh
```

Via console

```bash
d8 v console -n demo-app <vmname>
```
