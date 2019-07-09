from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
import tweepy
from config import *
from cassandra.cluster import Cluster
from twitter import *

#Authentication variables from config.py:
#bot_token
#twitter_key
#twitter_secret
#twitter_token
#twitter_token_secret

#Max number of tweets
n_tweets = 5

#Docker Machine IP:
cassandra_ip = '192.168.99.100'

def start(bot, update):
    response_message = "Digite a Hashtag a ser pesquisada"
    bot.send_message(chat_id=update.message.chat_id, text=response_message)

def unknown(bot, update):
    response_message = "Função Unknown"
    bot.send_message(chat_id=update.message.chat_id, text=response_message)

def hashtag_search(bot, update):
    #hashtag = '#machinelearning'
    hashtag = update.message.text
    twitter = twitter_auth()
    tweets = getTweets(twitter, hashtag, n_tweets)
    response_message = ""
    cluster = Cluster([cassandra_ip], port=9042)
    session = cluster.connect()
    session.execute("CREATE KEYSPACE IF NOT EXISTS botdb WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 }")
    session.set_keyspace('botdb')
    #session.execute("CREATE TABLE IF NOT EXISTS tweet (id int primary key, created_at timestamp, txt text, user_name text, user_followers_count int, lang text)")
    
    #Todos campos com texto----alterar
    session.execute("CREATE TABLE IF NOT EXISTS tweet (id text primary key, created_at text, txt text, user_name text, user_followers_count text, lang text)")
    
    for tweet in tweets:
        response_message = response_message + "Usuário: " + tweet._json['user']['name'] + "\nTweet: " + tweet._json['text'] + "\n\n"
        session.execute("""INSERT INTO tweet (id, created_at, txt, user_name, user_followers_count, lang) values (%s, %s, %s, %s, %s, %s)""", (tweet._json['id_str'], str(tweet._json['created_at']), tweet._json['text'], tweet._json['user']['name'], str(tweet._json['user']['followers_count']), tweet._json['lang']))
    
    bot.send_message(chat_id=update.message.chat_id, text=response_message)

def main():
    updater = Updater(token=bot_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.entity("hashtag"), hashtag_search))
    
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    print("press CTRL + C to cancel.")
    main()