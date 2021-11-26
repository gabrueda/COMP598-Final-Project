#!/usr/bin/env python3

__authors__ = ['Nathalie Redick', 'Gabriela Rueda', 'Yusen Tang']
__emails__ = ['nathalie.redick@mail.mcgill.ca', 'gabriela.rueda@mail.mcgill.ca', 'yusen.tang@mail.mcgill.ca']
__date__ = 'November 2021'

'''
- takes in 3 input files from the 3 days of tweet collectin, samples 333 at random from each and puts them into one file 
'''

## imports 
import argparse, os, sys, json, random, itertools
import os.path as osp
from pathlib import Path

# set up parent directory path 
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)

def sample_tweets(f, num):
    with open(f, 'r') as f: 
        tweets = f.readlines()
    
    return random.sample(tweets, num)


def main():
    # arg parser 
    parser = argparse.ArgumentParser()  
    parser.add_argument('-i', nargs=3, dest='input_files', help='', required=True)
    parser.add_argument('-o', nargs=1, dest='output_path', help='<sampled.json> (optional)', default=['data/sampled.json'])
    args = parser.parse_args()
    
    input_files = args.input_files     
    output_path = args.output_path[0] # output file path 
    
    # check to make sure the output file path dirs exist & create them if they dont 
    if '/' in output_path or '\\' in output_path and not osp.isdir(output_path):
        os.makedirs(osp.dirname(output_path), exist_ok=True)
        
    print(input_files, output_path)
    
    samples = []
    for f in input_files:
        samples.append(sample_tweets(f, 333))
     
    # pick one of the files at random for the last tweet 
    f = random.sample(input_files, 1)  
    samples.append(sample_tweets(*f, 1))
    
    flattened = list(itertools.chain(*samples))
    print(len(flattened))
    
    with open(output_path, 'w+') as out: 
        out.writelines(flattened)

if __name__ == '__main__':
    main()