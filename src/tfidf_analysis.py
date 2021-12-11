#!/usr/bin/env python3

__authors__ = ['Nathalie Redick', 'Gabriela Rueda', 'Yusen Tang']
__emails__ = ['nathalie.redick@mail.mcgill.ca', 'gabriela.rueda@mail.mcgill.ca', 'yusen.tang@mail.mcgill.ca']
__date__ = 'December 2021'

'''
- characterize topics -- get the count of the top ten words for every topic 
'''

# imports 
import argparse, string, json, sys, sklearn, math, os
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import os.path as osp
from pathlib import Path
from sklearn.feature_extraction import text
#from sklearn.feature_extraction.text import TfidfVectorizer 
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


# for a given topic, get the count of all of the words (accounts for stopwords and punctuation)
def topic_word_counts(topic, df, stopwords):
    # change everything to lowercase
    for col in df.columns:
        try: 
            df[col] = df[col].str.lower()
        except: 
            pass
        
    df = df.loc[df['topic'] == topic] # get all tweets that have this topic
    counts = {} # init a dict for word counts
    
    # remove punctuation from the dialog
    tweet = df['text'].str.translate(str.maketrans('', '', string.punctuation))
    
    # get the word freqs from this topic 
    word_freq = tweet.apply(lambda x: pd.value_counts(x.split(' '))).sum(axis=0)
   
    try:  
        for word, count in word_freq.items():
            count = int(count)
            # word is alphanumeric and not a stopword
            if word.isalpha() and word not in stopwords: 
                counts[word] = count
    except:
        counts = {}
    
    return counts

# union standard stopwords w list of keywords, since the words w highest tfidf always end up 
# being covid, vaccine, etc and dont tell us much other info 
def get_stopwords(keywords):
    if keywords:
        return text.ENGLISH_STOP_WORDS.union([*keywords, 'amp'])
    else:
        return text.ENGLISH_STOP_WORDS.union(['amp'])


def tf(w, topic, counts):
    try: 
        return counts[topic][w]
    except:
        return 0


def idf(w, counts): 
    num_docs = 1000
    # check to see which topics used word w
    usages = 0
    for topic, freq_dict in counts.items():
        if w in freq_dict.keys():
            usages += 1
    
    return math.log(num_docs/usages)


def tf_idf(w, topic, counts):
    return tf(w, topic, counts) * idf(w, counts)


def tfidf_per_word(topic, counts, num_words):
    freq = counts[topic] # get the given topic from the counts dict
    tfidf = {word: tf_idf(word, topic, counts) for word, count in freq.items()} # compute the tf_idf for each word they used
    sorted_words = sorted(tfidf, key=tfidf.get) # sort the keys by their tf_idf values 
    # get the last num_words from the end of the list which have the highest idf in order bc sorted 
    x = list(reversed(sorted_words))[:min(len(sorted_words), num_words)] 
    y = [tfidf[w] for w in x]
    return x, y


def create_tfidf_plots(counts, num_words, topics_key):
    if not topics_key.empty: 
        titles = {sr.code : sr.topic.title() for _, sr in topics_key.iterrows()}
    
    plt.figure(figsize=(6, 5))
    outpath = osp.join(parentdir, 'data', 'figures')
    
    try:
        os.makedirs(outpath, exist_ok=True)
    except:
        pass
    
    for topic, count in counts.items():
        x, y = tfidf_per_word(topic, counts, num_words)
        
        if topics_key.empty:  
            title = topic
        else: 
            title = titles[topic]
            
        plt.plot(x, y, 'go')
        plt.ylabel(f'TF-IDF')
        plt.title(f'Top {num_words} Words by TF-IDF in {title}')
        plt.grid(visible=True, axis='both')
        plt.xticks(rotation=45)        
        plt.savefig(osp.join(outpath, f'tfidf_{topic}.png'), dpi=300, format='png', bbox_inches='tight')
        plt.clf()        
        
        
def plot_word_freq(counts, num_words, topics_key):
    if not topics_key.empty: 
        titles = {sr.code : sr.topic.title() for _, sr in topics_key.iterrows()}
    
    
    plt.figure(figsize=(6, 5))
    outpath = osp.join(parentdir, 'data', 'figures')
    
    try:
        os.makedirs(outpath, exist_ok=True)
    except:
        pass
    
    
    for topic, count in counts.items():
        sorted_count = sorted(count, key=count.get) # sort the keys by their num occurences
        x = list(reversed(sorted_count))[:min(len(sorted_count), num_words)] # get top num words occurrences 
        y = [count[w] for w in x]   
              
        if topics_key.empty:  
            title = topic
        else: 
            title = titles[topic]
            
        plt.plot(x, y, 'go')
        plt.ylabel(f'Number of Word Occurences')
        plt.title(f'Word Frequency in {title} for the Top {num_words} Occurences')
        plt.grid(visible=True, axis='both')
        plt.xticks(rotation=45)        
        plt.savefig(osp.join(outpath, f'freq_{topic}.png'), dpi=300, format='png', bbox_inches='tight')
        plt.clf() 


def main():
    args = parse_arguments()
    input_file = args.input_file[0] # get the annotated tweets from input
    #output_file = args.output_file[0] 
    
    with open(input_file, 'r+') as f: 
        df = pd.read_csv(f) # load tweets into a pandas df 

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
    

    counts = {topic: topic_word_counts(topic, df, stopwords=get_stopwords(keywords)) for topic in df.topic.unique()}
    
    tfidf = {}
    for topic in df.topic.unique():
        x, y = tfidf_per_word(topic, counts, num_words=10) 
        z = dict(zip(x, y))
        tfidf[topic] = z
        
    # write top ten words/topic and their tfidf scores to a json file 
    with open(osp.join(parentdir, 'data', 'analysis_tfidf.json'), 'w+') as out:
        out.write(json.dumps(tfidf, indent=4))   
    
    create_tfidf_plots(counts, 10, topics_key)
    plot_word_freq(counts, 10, topics_key)

if __name__ == '__main__':
    main()