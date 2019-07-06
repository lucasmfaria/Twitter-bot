from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
import tweepy
import time

#Telegram authentication
bot_token = "885901023:AAGR-DoJRSL2Zy6RgLaV5E40aZ8pdCFaOWE"

#Twitter authentication
twitter_key = "VtOkcPB7emkYlD9VOYewkxHsm"
twitter_secret = "OBnSTBeqxeXLP1xp6vlp0empy55EcJtQ7BY9PmztoO4alCFq21"
twitter_token = "1147475130987270144-xFHY6gEXYxUISXWoKD3lMSZF8AP8dP"
twitter_token_secret = "rgIz4vYUsj2qc397n0lSoB3U9AYddxsl1oSmIrkfhgsUZ"

#Max number of tweets
n_tweets = 5

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
    tweets = getTweets(twitter, hashtag)
    response_message = ""
    
    #Armazenar no banco de dados
    for tweet in tweets:
        print("Usuário: " + tweet._json['user']['name'])
        print("Tweet: " + tweet._json['text'])
        response_message = response_message + "Usuário: " + tweet._json['user']['name'] + "\nTweet: " + tweet._json['text'] + "\n\n"
    
    
    bot.send_message(chat_id=update.message.chat_id, text=response_message)

def twitter_auth():
    auth = tweepy.OAuthHandler(twitter_key, twitter_secret)
    auth.set_access_token(twitter_token, twitter_token_secret)
    twitter = tweepy.API(auth)
    return twitter

def getTweets(twitter, hashtag):
    return tweepy.Cursor(twitter.search, q=hashtag).items(n_tweets)

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