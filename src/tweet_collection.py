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


## helper functions 

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


def main():
    # argparse
    parser = argparse.ArgumentParser()  
    parser.add_argument('-k', nargs=1, dest='keyword_path', help='<keywords.csv> (optional)')
    parser.add_argument('-o', nargs=1, dest='output_path', help='<output.json> (optional)', default=['data/output.json'])
    args = parser.parse_args()
    
    # try to get the keyword path from args 
    try: 
        keyword_path = args.keyword_path[0] 
    except: 
        pass
    
    output_path = args.output_path[0] # output file path 
    
    # check to make sure the output file path dirs exist & create them if they dont 
    if '/' in output_path or '\\' in output_path and not osp.isdir(output_path):
        os.makedirs(osp.dirname(output_path), exist_ok=True)
    
    # get keywords file or use default keywords 
    try: 
        with open(keyword_path, 'r') as f:
            keywords = [word.rstrip('\n') for word in f.readlines()]
    except: 
        print(f'Warning: Cannot find keywords file or no filepath given, using default keywords instead.')
        keywords = ['covid', 'covid-19', 'pfizer', 'moderna', 'astrazeneca', 'johnson & johnson', 
                    'vaccination', 'vaccine', 'coronavirus', 'sars-cov-2']

    # authenticate 
    auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    
    i = 0 # count the number of valid tweets 
    used_tweets = {} # used to check if a tweet is unique 
    with open(output_path, 'w+') as out: 
        while i < 1000: 
            keys, query = build_query(keywords)
            print(f'Searching with keywords : {keys}')
            
            # only get 250 tweets at a time, prevents us from hitting the rate limit too quickly 
            tweets = tweepy.Cursor(api.search_tweets, q=query, 
                                    lang='en', result_type='recent', 
                                    tweet_mode='extended', count=250).items() 

            for j, tweet in enumerate(tweets):
                #location = get_location(tweet)
                #if location: # only grab tweets that have a valid location aka are in canada 
                
                t = {} # dict to hold tweet info 
                
                id = tweet._json['id']
                text = full_text(tweet).replace('\n', '\t') # replace newlines with tabs 
                hashed_text = hash(text) # hash the tweet txt
                created_at = tweet._json['created_at'] 
                                        
                if hashed_text not in used_tweets.keys() and 'Nov 26' in created_at: # get only unique tweets - ids do not uniquely id the text 
                    used_tweets[hashed_text] = 1 # add current tweet to used 
                    
                    # add standard tweet info 
                    t['id'] = id
                    t['created_at'] = created_at
                    
                    # add places for topic and sentiment to be added later during manual annotation
                    t['topic'] = '<TOPIC>'
                    t['sentiment'] = '<SENTIMENT>'
                    
                    # add the tweet text 
                    t['text'] = text

                    # check for a retweet, include its url if it exists else leave empty 
                    retweet = True if 'retweeted_status' in tweet._json else False
                    url = 'https://twitter.com/twitter/statuses/' + str(id)
                    if retweet:
                        t['retweet'] = url
                    else:
                        t['retweet'] = ''
                    
                    if i > 1000: 
                        break 
                    
                    out.write(json.dumps(t)+'\n') # write a tweet to the out file 
                    i += 1 # counts only the unique tweets w relevant locations 
                
                    if j >= 250: # max of 250 tweets for each 10 randomly selected keywords 
                        break # out of for loop, not while
                    
    out.close()
    
        
if __name__ == '__main__':
    main()

