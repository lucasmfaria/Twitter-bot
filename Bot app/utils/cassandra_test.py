from cassandra.cluster import Cluster

#Docker Machine IP:
cluster = Cluster(['192.168.99.100'], port=9042)

session = cluster.connect()
session.execute("CREATE KEYSPACE IF NOT EXISTS test WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 }")
session.set_keyspace('test')
session.execute("CREATE TABLE IF NOT EXISTS user (user_id int primary key, first_name text, last_name text)")
session.execute("INSERT INTO user (user_id, first_name, last_name) values (1, 'John', 'Wick')")
session.execute("INSERT INTO user (user_id, first_name, last_name) values (2, 'Mario', 'Luigi')")

rows = session.execute('SELECT * FROM user')
for user_row in rows:
    print(user_row)

cluster.shutdown()