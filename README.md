# Three-Tier Application Demo

## Overview

A demo of a simple three-tier application (Frontend -> Backend -> Database) to demonstrate platform capabilities.

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

### Security
- Component interaction is restricted by network policies.
- Application access requires authentication via Dex.

![](./demo-app.png)

### Users
- Application user: `demo-user@flant.com`
- `demo-db` project admin: `demo-db-admin@flant.com`
- `demo-app` project admin: `demo-app-admin@flant.com`

## Repository Structure
- `/apps` - Frontend and backend source code
- `/k8s` - Kubernetes deployment manifests

## Requirements

Ensure the following d8 modules are enabled:
- `admission-policy-engine`
- `cni-cilium`
- `console`
- `multitenancy-manager`
- `service-with-healthchecks`
- `user-authn`
- `virtualization`

## Installation

1. Create a `.env` file with infrastructure settings:

```ini
STORAGE_CLASS=linstor-thin-r1
PASSWORD=password
FQDN=demo.example.com
```

Install APP

```bash
task deploy
```

Uninstall APP

```bash
task undeploy
```

## How to connect to VM

Via SSH

```bash
d8 v ssh -n demo-app cloud@frontend -i ./tmp/demo --local-ssh
```

Via console

```bash
d8 v console -n demo-app frontend
```
