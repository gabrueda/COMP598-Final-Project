#!/usr/bin/env python3

__authors__ = ['Nathalie Redick', 'Gabriela Rueda', 'Yusen Tang']
__emails__ = ['nathalie.redick@mail.mcgill.ca', 'gabriela.rueda@mail.mcgill.ca', 'yusen.tang@mail.mcgill.ca']
__date__ = 'December 2021'

'''
- analyze overall sentiment of each topic, plot counts of each sentiment??
'''

# imports 
import argparse, string, json, sys, sklearn, math, os
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import os.path as osp
from pathlib import Path
# set up parent directory path 
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)


# function to parse input args 
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', help='<final_tweets_annotated.csv>', required=True, nargs=1)
    parser.add_argument('-k', '--keywords_file', help='<keywords.csv>', required=False, nargs=1)
    parser.add_argument('-t', '--topics_key', help='<topics_key.csv>', required=False, nargs=1)
    #parser.add_argument('-o', '--output_file', help='<output_file.json>', required=False, nargs=1, default=osp.join(parentdir, 'tfidf.json'))
    args = parser.parse_args()
    return args


# get counts for each sentiment for each topic 
def get_sentiments(tweets, topics_key):
    num_tweets = int(tweets.size)
    if not topics_key.empty: 
        titles = {sr.code : sr.topic.title() for _, sr in topics_key.iterrows()}
        return {titles[t] : tweets.loc[tweets['topic'] == t].sentiment.value_counts().to_dict() for t in tweets.topic.unique()}  
    else:
        return {t : tweets.loc[tweets['topic'] == t].sentiment.value_counts().to_dict() for t in tweets.topic.unique()}  

# (on one plot) stacked bars for pos/neg/netural for each topic 
def plot_sentiment(s):
    plt.figure(figsize=(12, 10))
    outpath = osp.join(parentdir, 'data', 'figures')
    
    try:
        os.makedirs(outpath, exist_ok=True)
    except:
        pass
    
    width = 0.75 # the width of the bars
    topics = s.keys()
    num_s = len(s.keys())

    pos = []
    neg = []
    neu = []
    for key, val in s.items():
        pos.append(val['positive'])
        neg.append(val['negative'])
        neu.append(val['neutral'])
        
    plt.bar(topics, neu, width, color='#adb5bd')
    plt.bar(topics, pos, width, bottom=neu, color='#43A43D')
    plt.bar(topics, neg, width, bottom=np.asarray(pos)+np.asarray(neu), color='#E00016')

    plt.ylabel('Sentiment by Number of Tweets', fontsize=14)
    plt.xlabel('Topics', fontsize=14)
    plt.legend(['Neutral', 'Positive', 'Negative'], loc=1, title='Sentiments', fontsize=14)

    plt.savefig(osp.join(outpath, f'fig_sentiment.png'), dpi=300, format='png', bbox_inches='tight')
    plt.clf()  
    

def main():
    args = parse_arguments()
    input_file = args.input_file[0] # get the annotated tweets from input
    #output_file = args.output_file[0] 
    
    with open(input_file, 'r+') as f: 
        tweets = pd.read_csv(f) # load tweets into a pandas df 

    try: # get the topics key if it exists
        with open(args.topics_key[0], 'r+') as f: 
            topics_key = pd.read_csv(f) # read in the topics key 
            topics_key.drop('subtopics', axis=1, inplace=True)
    except:
       topics_key = pd.DataFrame()
       
    try: # get the keywords file if it exists,
        with open(args.keywords_file[0], 'r+') as f: 
            keywords = f.read().splitlines() # read in the keywords
    except:
       keywords = False
       
    s = get_sentiments(tweets, topics_key)
    plot_sentiment(s)
    
    with open(osp.join(parentdir, 'data', 'analysis_sentiment.json'), 'w+') as out:
        out.write(json.dumps(s, indent=4))   
       

if __name__ == '__main__':
    main()