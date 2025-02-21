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

Attention! When using projects, the command must be executed twice, because the namespace that creates the project is not created instantly.

```bash
task deploy
```

Uninstall

```bash
task undeploy
```

## How to debug

### frontend

```bash
d8 v console -n demo-app frontend

# cloud/cloud

curl http://backend.demo-app.svc.cluster.local:5000
# [{"id":1,"name":"Deckhouse Kubernetes Platform"},{"id":2,"name":"Deckhouse Virtualiztion Platform"},{"id":3,"name":"Deckhouse Stronghold"},{"id":4,"name":"Deckhouse Observability Platform Platform"},{"id":5,"name":"Deckhouse Commander"},{"id":6,"name":"Deckhouse Delivery Kit"}]
```

### backend

```bash
d8 v console -n demo-app backend-a

# cloud/cloud

sudo apk add postgresql

PGPASSWORD=mypassword psql -h db.demo-db.svc.cluster.local -U myuser -d mydb -c "SELECT * FROM test_table;"

#  id |                   name
# ----+-------------------------------------------
#   1 | Deckhouse Kubernetes Platform
#   2 | Deckhouse Virtualiztion Platform
#   3 | Deckhouse Stronghold
#   4 | Deckhouse Observability Platform Platform
#   5 | Deckhouse Commander
#   6 | Deckhouse Delivery Kit
# (6 rows)
```

### DB

```bash
d8 v console -n demo-db db

# cloud/cloud

PGPASSWORD=mypassword psql  -U myuser -d mydb -c "SELECT * FROM test_table;"

PGPASSWORD=healthchecker psql -U healthchecker -d mydb -c "SELECT * FROM ping_database();"

PGPASSWORD=healthchecker psql -U healthchecker -d mydb -c "SELECT 1;"
#  id |                   name
# ----+-------------------------------------------
#   1 | Deckhouse Kubernetes Platform
#   2 | Deckhouse Virtualiztion Platform
#   3 | Deckhouse Stronghold
#   4 | Deckhouse Observability Platform Platform
#   5 | Deckhouse Commander
#   6 | Deckhouse Delivery Kit
# (6 rows)
```
