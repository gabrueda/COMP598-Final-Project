import json
import pandas
import argparse

def main():
    args = parse_arguments()
    data = load_json(args.input_file)
    write_to_csv(data, args.output_file)

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file')
    parser.add_argument('-o', '--output_file')
    args = parser.parse_args()
    return args

def load_json(input_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    data = []
    for line in lines:
        record = json.loads(line)
        record['link'] = 'https://twitter.com/twitter/statuses/' + str(record['id'])
        record['topic'] = ''
        record['sentiment'] = ''
        data.append(record)

    return pandas.DataFrame(data)

def write_to_csv(data, output_file):
    columns_names = ['id', 'link', 'text', 'topic', 'sentiment', 'created_at', 'retweet']
    data = data.reindex(columns=columns_names)
    data.to_csv(output_file, index=False)
    
if __name__ == '__main__':
    main()