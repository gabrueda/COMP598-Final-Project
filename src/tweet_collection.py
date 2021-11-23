#!/usr/bin/env python3

__authors__ = ['Nathalie Redick', 'Gabriela Rueda', 'Yusen Tang']
__emails__ = ['nathalie.redick@mail.mcgill.ca', 'gabriela.rueda@mail.mcgill.ca', 'yusen.tang@mail.mcgill.ca']
__date__ = '22 November 2021'

'''
- COVID in Canadian social media => filter by location: filter on the English language and the timezones that cover the Americas
- collect 1,000 tweets within a 3 day window
- all 1,000 posts mention either COVID, vaccination, or a name-brand COVID vaccine AND all are in English
    - you can choose the exact words, as long as they are related to the context that we mentioned before: vaccine hesitancy
- each post in your collection should be unique
'''

#imports 
import argparse, os, sys, requests, json, datetime
import os.path as osp
import pandas as pd
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
BEARER_TOKEN = os.getenv('BEARER_TOKEN')

search_url = 'https://api.twitter.com/2/tweets/search/recent'

## helper functions for api authorization 

def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {BEARER_TOKEN}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def main():
    # argparse
    parser = argparse.ArgumentParser()  
    parser.add_argument('-k', nargs=1, dest='keyword_path', help='<keywords.csv>')
    args = parser.parse_args()
    
    # try to get the keyword path from args 
    try: 
        keyword_path = args.keyword_path[0] 
    except: 
        pass
    
    # get keywords file 
    try: 
        keywords = pd.read_csv(keyword_path, header=None)
    except: 
        print(f'Warning: Cannot find keywords file or no path given, using default keywords instead.')
        keywords = pd.DataFrame(['covid', 'covid-19', 'pfizer', 'moderna', 'astrazeneca', 'johnson & johnson', 'vaccination'])

    print(keywords, type(keywords))  
    
    query_params = {'query': 'from:twitterdev',
                    'tweet.fields': 'public_metrics,created_at,lang', 
                    'max_results': 10}
                    #todo: 'since_id'
                    #todo: figure out how to bound for tweets in the north american timezones 
    
    json_response = connect_to_endpoint(search_url, query_params)
    print(json.dumps(json_response, indent=4, sort_keys=True)) # prints tweets to output 
    
    #todo: save tweets to file 

    
if __name__ == '__main__':
    main()