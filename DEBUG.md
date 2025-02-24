## How to debug

### frontend

```bash
d8 v ssh -n demo-app cloud@frontend -i ./tmp/demo --local-ssh

# or

d8 v console -n demo-app frontend

# cloud/cloud

curl http://backend.demo-app.svc.cluster.local:5000
# [{"id":1,"name":"Deckhouse Kubernetes Platform"},{"id":2,"name":"Deckhouse Virtualiztion Platform"},{"id":3,"name":"Deckhouse Stronghold"},{"id":4,"name":"Deckhouse Observability Platform Platform"},{"id":5,"name":"Deckhouse Commander"},{"id":6,"name":"Deckhouse Delivery Kit"}]
```

### backend

```bash
d8 v ssh -n demo-app cloud@backend-a -i ./tmp/demo --local-ssh

# or

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

PGPASSWORD=healthchecker psql -h db.demo-db.svc.cluster.local -U healthchecker -d mydb -c "SELECT 1;"

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
