from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
import tweepy
from config import *
from twitter import *
from DAO import CassandraDAO
from PysparkHandler import PysparkJobHandler

#Docker Machine IP:
cassandra_ip = '192.168.99.100'

#Authentication variables from config.py:
#bot_token
#twitter_key
#twitter_secret
#twitter_token
#twitter_token_secret

#Max number of tweets
n_tweets = 100

pysparkHandler = PysparkJobHandler(cassandra_ip)

def start(bot, update):
    response_message = "Digite a Hashtag a ser pesquisada"
    bot.send_message(chat_id=update.message.chat_id, text=response_message)

def unknown(bot, update):
    response_message = "Favor digitar no seguinte formato: #palavra_a_ser_procurada"
    bot.send_message(chat_id=update.message.chat_id, text=response_message)

def hashtag_search(bot, update):
    hashtag = update.message.text
    twitter = twitter_auth()
    tweets = getTweets(twitter, hashtag, n_tweets)
    cass_dao = CassandraDAO(cassandra_ip)
    cass_dao.create(keyspace = 'botdb', table1 = 'tweet', table2 = 'output')
    response_message = cass_dao.insert(tweets, hashtag, update.message.from_user['id'])
    response_message = response_message + "\n\n\n\nUsuários com mais seguidores:\n"
    cass_dao.close()
    
    popular_users, total_portuguese = pysparkHandler.runJobs(hashtag)
    pop_users_text = ""
    for user in popular_users:
        response_message = response_message + user.asDict()['tweet_user_name'] + "\n"
        pop_users_text = pop_users_text + user.asDict()['tweet_user_name'] + ", "
    pop_users_text = pop_users_text.rstrip(", ")
    
    response_seguidores = "Usuários com mais seguidores: " + pop_users_text
    response_total_pt = "Total de tweets em português: " + str(total_portuguese)
    
    print(response_seguidores + response_total_pt + "\n\n")
    
    #TODO - Record pop_users_text on cassandra output table
    
    #Returns the messages for the bot. Just for debugging for now.
    bot.send_message(chat_id=update.message.chat_id, text=(response_seguidores+response_total_pt))
    
    cass_dao.close()

def main():
    updater = Updater(token=bot_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.entity("hashtag"), hashtag_search))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    print("press CTRL + C to cancel.")
    main()