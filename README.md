# Twitter bot
Application using Big Data tools to deliver Twitter hashtag statistics:

- A Telegram user enters a hashtag into a bot conversation
- The bot finds the last tweets that contain the hashtag and stores them within a Cassandra DB
- The application runs a MapReduce job via a Node.js REST API to generate the statistics

I used the official Docker image to run a container with Cassandra DB. Docker Hub page: https://hub.docker.com/_/cassandra.

Command to run the container:
docker run --name cassandra-node-01 -d -p 9042:9042 -p 9160:9160 --rm cassandra:latest

Main Python packages:
tweepy
python-telegram-bot
cassandra-driver