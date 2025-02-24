## Info

demo app env:

- namespace: demo-db
  - DB
    - vm: db (postresql)
- namespace: demo-app
  - Frontend
    - vm: frontend (bootstrap app)
    - pod: frontend (bootstrap app)
  - Backend
    - vm: backend-a (flask - gunicorn)
    - vm: backend-b (flask - gunicorn)

![](./demo-app.png)

Users:
- User to access app: `demo-user@flant.com`
- Admin of demo-db project: `demo-db-admin@flant.com`
- Admin of demo-app project: `demo-app-admin@flant.com`

## Requirements

Following d8 modules should be enabled:
- admission-policy-engine
- cni-cilium
- console
- multitenancy-manager
- service-with-healthchecks
- user-authn
- virtualization


## Install



Before install create `.env` file with infra settings. Example:

```
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
