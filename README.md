# Twitter bot
Application to deliver Twitter hashtag statistics:

- Telegram user enter a hashtag into a bot conversation
- The bot finds the last tweets that contain the hashtag and stores it within a Cassandra DB
- The application runs a MapReduce job via a Node.js REST API to generate the statistics