from cassandra.cluster import Cluster
from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
import os

class PysparkJobHandler:
    
    def __init__(self, cassandra_ip):
        self.cassandra_ip = cassandra_ip
        
        #Download the connector jar (first time only)
        #Reference: https://medium.com/coinmonks/running-pyspark-with-cassandra-using-spark-cassandra-connector-in-jupyter-notebook-9f1dc45e8dc9
        os.environ['PYSPARK_SUBMIT_ARGS'] = "--packages com.datastax.spark:spark-cassandra-connector_2.11:2.3.2 --conf spark.cassandra.connection.host=" + cassandra_ip + " pyspark-shell"
        
        self.sc = SparkContext()
        self.sqlContext = SQLContext(self.sc)
    
    def get_cassandra_df(self, table, keyspace):
        return self.sqlContext.read.format("org.apache.spark.sql.cassandra").options(table=table, keyspace=keyspace).load()
    
    def write_cassandra_table(self, pyspark_df, table, keyspace):
        pyspark_df.write.format("org.apache.spark.sql.cassandra").mode('append').options(table=table, keyspace=keyspace).save()
    
    def runJobs(self, hashtag):
        cass_df = self.get_cassandra_df(table="tweet", keyspace="botdb")
        popular_users = cass_df.select('tweet_user_name').distinct().where(cass_df.telegram_hashtag == hashtag).orderBy(cass_df.tweet_created_at.desc()).orderBy(cass_df.tweet_user_followers_count.desc()).limit(5).collect()
        total_portuguese = cass_df.where(cass_df.telegram_hashtag == hashtag).where(cass_df.tweet_lang == 'pt').count()
        
        cass_df.unpersist()
        return (popular_users, total_portuguese)
    