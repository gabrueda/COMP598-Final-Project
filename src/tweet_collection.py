#!/usr/bin/env python3

__authors__ = ['Nathalie Redick', 'Gabriela Rueda', 'Yusen Tang']
__emails__ = ['nathalie.redick@mail.mcgill.ca', 'gabriela.rueda@mail.mcgill.ca', 'yusen.tang@mail.mcgill.ca']
__date__ = 'November 2021'

'''
- COVID in Canadian social media => filter by location: filter on the English language and the timezones that cover the Americas
- collect 1,000 tweets within a 3 day window
- all 1,000 posts mention either COVID, vaccination, or a name-brand COVID vaccine AND all are in English
    - you can choose the exact words, as long as they are related to the context that we mentioned before: vaccine hesitancy
- each post in your collection should be unique
'''

## imports 
import argparse, os, sys, json, re, tweepy, random, csv, time
import os.path as osp
from dotenv import load_dotenv
from pathlib import Path
# set up parent directory path 
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)

## global variables 
# set up env variables using dotenv 
load_dotenv()
env_path = osp.join(parentdir, '.env')
load_dotenv(dotenv_path=env_path)

# retrieving keys and adding them to the project from the .env file through their key names
API_KEY = os.getenv('API_KEY')
API_KEY_SECRET = os.getenv('API_KEY_SECRET')

def main():
    # parse arguments
    args = parse_arguments()
    keyword_path = args.keywords_path
    output_path = args.output_file_path
    date = args.date
    
    # get keywords for search
    keywords = get_keywords(keyword_path)

    # collect tweets
    collect_tweets(keywords, output_path, date)

## helper functions 

# parse arguments
def parse_arguments():
    parser = argparse.ArgumentParser()  
    parser.add_argument('-k', '--keywords_path', help='<keywords.csv> (optional)', default=None)
    parser.add_argument('-o', '--output_file_path', help='<output.json> (optional)', default=['data/output.json'])
    parser.add_argument('-d', '--date', nargs=2, help='2021-11-25 Nov 25', default=['2021-11-25', 'Nov 25'])
    return parser.parse_args()

# get keywords file or use default keywords 
def get_keywords(keyword_path):
    try:
        with open(keyword_path, 'r') as f:
            return [word.rstrip('\n') for word in f.readlines()]
    except: 
        print(f'Warning: Cannot find keywords file or no filepath given, using default keywords instead.')
        return ['covid', 'covid-19', 'pfizer', 'moderna', 'astrazeneca', 'janssen', 'johnson & johnson', 
                    'vaccination', 'vaccine', 'coronavirus', 'sars-cov-2']

def collect_tweets(keywords, output_path, date):
    # authenticate 
    auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    i = 0                   # count the number of valid tweets 
    used_tweets = []        # used to check if a tweet is unique
    
    while i < 1000:
        keys, query = build_query(keywords)
        print(f'Searching with keywords : {keys}')

        for tweet in tweepy.Cursor(api.search_tweets, q=query, lang='en', 
                                    result_type='recent', tweet_mode='extended',
                                    until=date[0]).items():
            # check if tweet has valid location
            location = get_location(tweet)
            date_tweet = tweet._json['created_at']
            if location and date[1] in date_tweet:
                text = full_text(tweet).replace('\n', '\t')
                if hash(text) not in used_tweets:
                    t = {}                                                                  # dict to hold tweet info 
                    t['id'] = tweet._json['id']
                    t['text'] = text                                
                    t['created_at'] = date_tweet
                    t['topic'] = '<TOPIC>'
                    t['sentiment'] = '<SENTIMENT>'
                    t['retweet'] = True if 'retweeted_status' in tweet._json else False
                    t['url'] = 'https://twitter.com/twitter/statuses/' + str(t['id'])
                    t['location'] = location

                    with open(output_path, 'a+') as out:
                        out.write(json.dumps(t)+'\n')                                       # write a tweet to output file 
                        
                    used_tweets.append(hash(text))
                    i += 1

            # get different keywords for each 250 tweets collected
            if i % 250 == 0 and i != 0:
                break
            
            if i == 1000:
                break 
        
# builds a query string (word OR word OR...) by randomly selecting 10 keywords from the keywords file
def build_query(keywords):
    words = random.sample(keywords, 10) # api docs recommend using 10 keywords 
    return words, ' OR '.join(words) 

# get the tweet text 
def full_text(tweet):
    if 'retweeted_status' in tweet._json:
        text = tweet._json['retweeted_status']['full_text']
    else:
        text = tweet.full_text
    return text

# get tweet with valid location
def get_location(tweet):
    # get location
    if tweet._json['place']:
        if tweet._json['place']['country'] == 'Canada':
            return tweet._json['place']['full_name'].lower()
   
    locations = ['Canada', 'Ottawa', 'Alberta', 'Edmonton', 'British Columbia', 'Vancouver', 'Manitoba', 'New Brunswick', 
                'Fredericton', 'Newfoundland and Labrador', 'Nova Scotia', 'Ontario', 'Prince Edward Island', 'Quebec', 
                'Saskatchewan', 'Regina', 'Northwest Territories','Nunavut', 'Iqaluit', 'Yukon']

    if tweet._json['user']['location']:
        location = tweet._json['user']['location']
        for loc in locations:
            if re.search(loc, location, re.IGNORECASE):
                return loc.lower()

    return None
        
if __name__ == '__main__':
    main()
