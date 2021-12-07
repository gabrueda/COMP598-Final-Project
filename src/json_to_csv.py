#!/usr/bin/env python3

__authors__ = ['Nathalie Redick', 'Gabriela Rueda', 'Yusen Tang']
__emails__ = ['nathalie.redick@mail.mcgill.ca', 'gabriela.rueda@mail.mcgill.ca', 'yusen.tang@mail.mcgill.ca']
__date__ = 'November 2021'

# imports 
import json
import pandas
import argparse

def main():
    args = parse_arguments()
    data = load_json(args.input_file)
    write_to_csv(data, args.output_file)


# function to parse input args 
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file')
    parser.add_argument('-o', '--output_file')
    args = parser.parse_args()
    return args


# load json, readlines all lines an return a pandas df 
def load_json(input_file):
    '''
    with open(input_file, 'r') as file:
        lines = file.readlines()

    data = []
    for line in lines:
        record = json.loads(line)
        data.append(record)
    '''
    return pd.read_csv(input_file)


# transform json data (in the df) to csv 
def write_to_csv(data, output_file):
    columns_names = ['id', 'url', 'text', 'topic', 'sentiment', 'location', 'created_at', 'retweet']
    data = data.reindex(columns=columns_names)
    data.to_csv(output_file, index=False)
   
    
if __name__ == '__main__':
    main()