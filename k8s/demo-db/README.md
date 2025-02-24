psql -h 10.66.10.9 -U myuser -d mydb -c "SELECT * FROM test_table;"
PGPASSWORD=mypassword psql -h 10.66.10.9 -U myuser -d mydb -c "SELECT * FROM test_table;"

PGPASSWORD=mypassword psql -h db.demo-db.svc.cluster.local -U myuser -d mydb -c "SELECT * FROM test_table;"

psql -U myuser -d mydb -c "SELECT * FROM test_table;"
