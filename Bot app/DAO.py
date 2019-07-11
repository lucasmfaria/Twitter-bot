from cassandra.cluster import Cluster


class CassandraDAO:
    
    def __init__(self, cassandra_ip):
        self.cassandra_ip = cassandra_ip
        self.cluster = Cluster([cassandra_ip], port=9042)
        self.session = self.cluster.connect()
    
    def create(self, keyspace, table1, table2):
        self.session.execute("CREATE KEYSPACE IF NOT EXISTS " + keyspace + " WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 }")
        self.session.set_keyspace(keyspace)
        self.session.execute("CREATE TABLE IF NOT EXISTS " + table1 + " (tweet_id bigint primary key, tweet_created_at text, tweet_txt text, tweet_user_name text, tweet_user_followers_count int, tweet_lang text, telegram_hashtag text, telegram_user_id bigint)")
        self.session.execute("CREATE TABLE IF NOT EXISTS " + table2 + " (request_id int primary key, popular_users text, total_portuguese int, total_grouped text)")
    
    def insert(self, tweets, hashtag, telegram_user_id):
        response_message = ""
        for tweet in tweets:
            response_message = response_message + "Usuário: " + tweet._json['user']['name'] + "\nTweet: " + tweet._json['text'] + "\n\n"
            self.session.execute("""INSERT INTO tweet (tweet_id, tweet_created_at, tweet_txt, tweet_user_name, tweet_user_followers_count, tweet_lang, telegram_hashtag, telegram_user_id) values (%s, %s, %s, %s, %s, %s, %s, %s)""", (tweet._json['id'], str(tweet._json['created_at']), tweet._json['text'], tweet._json['user']['name'], tweet._json['user']['followers_count'], tweet._json['lang'], hashtag, telegram_user_id))
        return response_message
    
    def close(self):
        self.session.shutdown()
        self.cluster.shutdown()
    