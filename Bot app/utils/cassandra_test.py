from cassandra.cluster import Cluster

#Docker Machine IP:
cluster = Cluster(['192.168.99.100'], port=9042)

#Need a keyspace 'test' and a table 'user' created within Cassandra
session = cluster.connect('test')
rows = session.execute('SELECT * FROM user')
for user_row in rows:
    print(user_row)