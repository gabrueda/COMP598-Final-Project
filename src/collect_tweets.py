import tweepy
import re
import csv

def main():
    consumer_key='7T1PQSi4RMFdP7iqM6cZikPuV'
    consumer_secret='zRYqlDmC8aL4GYHRlrsTnLMPsk9ygCAWuX4YtX7Yas90zZZWE0'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    header = ['id', 'created_at', 'location', 'text', 'retweet', 'url']
    with open('../data/tweets.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)

    count = 0

    for tweet in tweepy.Cursor(api.search_tweets, 
                                q='covid OR vaccine OR COVID OR vaccination OR pfizer OR moderna OR astrazeneca OR janssen OR covid19', 
                                lang="en", result_type='mixed', tweet_mode='extended').items():
        location = get_location(tweet)
        if location:
            id = tweet._json['id']
            created_at = tweet._json['created_at']
            text = full_text(tweet)
            retweet = True if 'retweeted_status' in tweet._json else False
            url = 'https://twitter.com/twitter/statuses/' + str(id)
            with open('../data/tweets.csv', 'a+') as f:
                writer = csv.writer(f)
                data = [id, created_at, location, text, retweet, url]
                writer.writerow(data)

            count += 1
            print(count)
        
        if count == 1000:
            break

def full_text(tweet):
    if 'retweeted_status' in tweet._json:
        text = tweet._json['retweeted_status']['full_text']
    else:
        text = tweet.full_text
    return text

def get_location(tweet):
    # get location
    if tweet._json['place']:
        if tweet._json['place']['country'] == 'Canada':
            return tweet._json['place']['full_name'].lower()
    # check if valid
    locations = ['Canada', 'Ottawa', 'Alberta', 'Edmonton', 'British Columbia', 'BC', 'Vancouver', 'Victoria', 
                    'Manitoba', 'Winnipeg', 'New Brunswick', 'Fredericton', 'Newfoundland and Labrador', 'NL', 'St. John\'s',
                    'Nova Scotia', 'Halifax', 'Ontario', 'Toronto', 'Prince Edward Island', 'PEI', 'Charlottetown'
                    'Quebec', 'Quebec City', 'Montreal', 'Saskatchewan', 'Regina', 'Northwest Territories', 'Yellowknife'
                    'Nunavut', 'Iqaluit', 'Yukon', 'Whitehorse']

    if tweet._json['user']['location']:
        location = tweet._json['user']['location']
        for loc in locations:
            if re.search(loc, location, re.IGNORECASE):
                return loc.lower()

    return None


if __name__ == '__main__':
    main()