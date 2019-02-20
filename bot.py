import configparser, tweepy, random, time

# read settings file
parser = configparser.SafeConfigParser()
parser.read('configfile')

# get hashtag, tweetlanguage and number of retweet
hashtag = parser.get("settings", "hashtags")
tweetLang = parser.get("settings", "language")
n = int(parser.get("settings","rt_number"))

# blocked users and words if necessary
blockedUsers = set()
blockedWords = set()

# credentials for Twitter API
ACCESS_TOKEN    = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
ACCESS_SECRET   = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
CONSUMER_KEY    = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
CONSUMER_SECRET = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

# create bot
auth = tweepy.OAuthHandler(CONSUMER_KEY, COMSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
bot = tweepy.API(auth)

# search for hashtag and put them into a list
searchHash = tweepy.Cursor(bot.search, q=hashtag, lang=tweetLang).items(n)
candidates = []
for status in searchHash:
    candidates.append(status)

# filter candidates if having blocked users or words
candidates = filter(lambda status: not any(word in status.text.split() for word in blockedWords), candidates)
candidates = filter(lambda status: status.author.screen_name not in blockedUsers, candidates)
candidates = list(candidates)

record = open('Log.txt', 'a')

# iterate candidates and retweet
for status in candidates:
    try:
        # retweet and add retweet information to log file
        record.write("(%(date)s) %(name)s: %(message)s\n" % \
              {"date": status.created_at,
               "name": status.author.screen_name.encode('utf-8'),
               "message": status.text.encode('utf-8')})
        record.flush()
        bot.retweet(status.id)
    except tweepy.error.TweepError as e:
        # in case error occurs
        record.write(e)
        continue
    time.sleep(random.randint(3000, 3600) * 6)   

record.close()     