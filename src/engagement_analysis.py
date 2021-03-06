#!/usr/bin/env python3

__authors__ = ['Nathalie Redick', 'Gabriela Rueda', 'Yusen Tang']
__emails__ = ['nathalie.redick@mail.mcgill.ca', 'gabriela.rueda@mail.mcgill.ca', 'yusen.tang@mail.mcgill.ca']
__date__ = 'December 2021'

'''
- analyze the relative engagement of each topic 
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


# get the count of tweets by topic
def freq_by_topic(tweets, topics_key):
    num_tweets = int(tweets.size)
    if not topics_key.empty: 
        titles = {sr.code : sr.topic.title() for _, sr in topics_key.iterrows()}
        return {titles[topic] : int((tweets.loc[tweets['topic'] == topic]).size)/num_tweets for topic in tweets.topic.unique()}
    else:
        return {topic : int((tweets.loc[tweets['topic'] == topic]).size)/num_tweets for topic in tweets.topic.unique()}
    

# get the count of tweets by topic
def retweeted_by_topic(tweets, topics_key):
    num_tweets = int(tweets.size)
    if not topics_key.empty: 
        titles = {sr.code : sr.topic.title() for _, sr in topics_key.iterrows()}
        return {titles[topic] : int((tweets.loc[((tweets['retweet'] == True) & (tweets['topic'] == topic))]).size)/int(tweets[tweets['topic'] == topic].size) for topic in tweets.topic.unique()}
    else:
        return {topic : int((tweets.loc[((tweets['retweet'] == True) & (tweets['topic'] == topic))]).size)/int(tweets[tweets['topic'] == topic].size) for topic in tweets.topic.unique()}
     

# plot the engagement 
def plot_engagement(freqs, retweets):
    plt.figure(figsize=(12, 10))
    outpath = osp.join(parentdir, 'data', 'figures')
    
    try:
        os.makedirs(outpath, exist_ok=True)
    except:
        pass
    
    ## plot freqs in a pie chart 
    x = freqs.keys()  
    y = list(freqs.values())
    
    # args 
    explode = [(1/freq)*0.005 for freq in y]
    colors = ('#FFADAD', '#FFD6A5', '#FDFFB6', '#CAFFBF', '#9BF6FF', '#A0C4FF', '#BDB2FF')
    # Creating autocpt arguments
    def func(pct, allvalues):
        absolute = int(pct/100.*np.sum(allvalues))
        return "{:.1f}%".format(pct, absolute)
    
    fig, ax = plt.subplots(figsize=(10, 7))
    wedges, texts, autotexts = ax.pie(y,
                                    autopct = lambda pct: func(pct, y),
                                    explode = explode,
                                    shadow = False,
                                    colors = colors,
                                    startangle = 90,
                                    textprops = dict(color='black'))
    
    ax.legend(wedges, x,
          title = 'Topics',
          loc = 'center left',
          bbox_to_anchor = (1, 0, 0.5, 1))

    plt.setp(autotexts, size=10, weight='bold')    
    #ax.set_title('Engagement by Topic Frequency')
    
    plt.savefig(osp.join(outpath, f'fig_engagement_freq.png'), dpi=300, format='png', bbox_inches='tight')
    plt.clf()  
    
    ## plot retweets in a histogram
    
    width = 0.75 # the width of the bars
    topics = retweets.keys()
    t = [p for p in retweets.values()]
    f = [1-p for p in retweets.values()]
        
    plt.bar(topics, t, width, color='#CAFFBF')
    plt.bar(topics, f, width, bottom=t, color='#FFADAD')

    plt.ylabel('Percentage of Retweets', fontsize=14)
    plt.xlabel('Topics', fontsize=14)
    plt.legend(['Retweets', 'Non-retweets'], loc=1, fontsize=14)
    plt.xticks(rotation=45)   
    
    plt.savefig(osp.join(outpath, f'fig_engagement_retweets.png'), dpi=300, format='png', bbox_inches='tight')
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
    
    freqs = freq_by_topic(tweets, topics_key)  
    retweets = retweeted_by_topic(tweets, topics_key)  
    plot_engagement(freqs, retweets)
    
    with open(osp.join(parentdir, 'data', 'analysis_engagement_freqs.json'), 'w+') as out:
        out.write(json.dumps(freqs, indent=4))
    with open(osp.join(parentdir, 'data', 'analysis_engagement_retweets.json'), 'w+') as out:
        out.write(json.dumps(retweets, indent=4))   


if __name__ == '__main__':
    main()