import tweepy, praw, time

with open('config.ini','r') as config:
  tokens = config.readlines()
  TW_CONSUMER_KEY = tokens[0].rstrip()
  TW_CONSUMER_SECRET = tokens[1].rstrip()
  TW_ACCESS_KEY = tokens[2].rstrip()
  TW_ACCESS_SECRET = tokens[3].rstrip()
  REDDIT_APP = tokens[4].rstrip()
  REDDIT_USER = tokens[5].rstrip()

def authenticate_twitter():
  print('Authenticating twitter...')
  auth = tweepy.OAuthHandler(TW_CONSUMER_KEY, TW_CONSUMER_SECRET)
  auth.set_access_token(TW_ACCESS_KEY, TW_ACCESS_SECRET)
  twitter = tweepy.API(auth)
  print('Twitter authenticated.\n')
  return twitter

def authenticate_reddit():
    print('Authenticating reddit...\n')
    reddit = praw.Reddit(REDDIT_APP, user_agent=REDDIT_USER)
    print('Reddit authenticated.\n')
    return reddit

def get_reddit_posts(reddit):
  print("Fetching new posts...")
  time.sleep(1)
  posts = []
  for post in reddit.subreddit('mariners').hot(limit=12):
    posts.append(post)
  print("Returning " + str(len(posts)) + " reddit posts")
  return posts
    
def record_already_tweeted(submission_id):
  print("Logging tweet...")
  writeable = open("tweeted.txt", 'a+')
  writeable.write(submission_id + '\n')
  writeable.close()
  time.sleep(2)
  
def is_tweeted(submission_id):
  print("Checking to see if this has already been tweeted...")
  time.sleep(1)
  readable = open("tweeted.txt", "r")
  if submission_id in readable.read().splitlines():
    print("It has been tweeted.\n")
    time.sleep(1)
    return True
  else:
    print("It has not been tweeted.\n")
    time.sleep(1)
    return False

def tweet(twitter, submission):
  print("Tweeting...")
  try:
    twitter.update_status(submission.title + " http://reddit.com" + submission.permalink)
    record_already_tweeted(submission.id)
    print("Tweeted about the Mariners!\n")
  except:
    print("I was not able to TWEET!")
    record_already_tweeted(submission.id + "FAILURE")
  time.sleep(2)
  
def get_mariners_tweets(twitter, x):
  new_tweets = twitter.search(q="mariners", count=x, lang="en")
  print("Returning " + str(x) + " Mariners tweets")
  return new_tweets

def get_user_ids(list_of_tweets):
  user_ids = []
  for tweet in list_of_tweets:
    user_ids.append(tweet.user.id)
  print("Returning user IDs")
  return user_ids

def follow_users(list_of_ids, twitter):
  count = 0
  print("Following new accounts")
  for user_id in list_of_ids:
    try:
      twitter.create_friendship(user_id)
      count = count + 1
    except:
      print("Couldn't follow this user.")
  print("Followed " + str(count) + " new accounts")
  return count

def unfollow_old(twitter, x):
  print("Unfollowing " + str(x) + " oldest follows")
  follows_ids = twitter.friends_ids(twitter.me().id)
  follows_ids.reverse()
  for i in range(0,x-1):
    twitter.destroy_friendship(follows_ids[i])
    print(i+1)
    time.sleep(10)

def main():
  reddit = authenticate_reddit()
  twitter = authenticate_twitter()
  while True:
    for post in get_reddit_posts(reddit):
      if not is_tweeted(post.id):
        tweet(twitter, post)
        # new_followed = follow_users(get_user_ids(get_mariners_tweets(twitter, 200)), twitter)
        # unfollow_old(twitter, new_followed-10)
        print("Sleeping 5 hours...\n\n")
        time.sleep(18000)
        break

if __name__ == '__main__':
  main()
