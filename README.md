# Understanding Discussions Around COVID-19 and Vaccination Hesitancy in Canada
Final Project for COMP 598 - Fall 2021 at McGill University

Project made by [Nathalie Redick](https://github.com/nredick), [Gabriela Rueda](https://github.com/gabrueda), and [Yusen Tang](https://github.com/).

## Project Description

This project uses the [Twitter API](https://developer.twitter.com/en/docs/twitter-api) via [tweepy](https://www.tweepy.org) to gather recent Tweets based on keywords related to COVID-19 and COVID-19 vaccine hesitancy. The tweets are filtered geographically to select for those posted in Canada. For 3 days, 1000 tweets were collected each day based on a random selection of 10 keywords. 333 tweets were sampled from each day and used in a final dataset of 1000 tweets, which were manually annotated for sentiment and topic. 

Tweet data collected by _tweet_collection.py_ is stored in a json file, and each tweet has the following associated data: _id, created_at, location, text,_ and _retweet_. 

## Usage 

**Clone this repository.**

**Install requirements:** 

```
pip install -r requirements.txt
```

**Environment Variable Set-Up:** 
Environment variables are handled by _[python-dotenv](https://pypi.org/project/python-dotenv/)_

## Scripts

### tweet_collection.py
A Twitter Developer Account with Elevated access is necessary to run the code. The API key and API key secret should be stored in a _.env_ file (see _.env_template_).

```
usage: tweet_collection.py [-h] [-k KEYWORD_PATH] [-o OUTPUT_PATH]

options:
  -h, --help       show this help message and exit
  -k KEYWORD_PATH  <keywords.csv> (optional)
  -o OUTPUT_PATH   <output.json> (optional)
```

**Example Usage:** (from root)

```
python3 src/tweet_collection.py -k data/keywords.csv -o data/tweets.json
```

The file _tweet_collection.py_ collects 1000 unique tweets, which can take a while due to the Twitter API's rate limit. It will sleep automatically and continue collecting tweets until it reaches 1000 tweets.

### json_to_csv.py

This script will convert a json file (with a json object in each line) into a csv file.
This script assumes there is an 'id', 'topic' and 'sentiment' field for each record.
```
usage: json_to_csv.py -i INPUT_PATH -o OUTPUT_PATH

options:
  -I INPUT_PATH  <data.json>
  -o OUTPUT_PATH   <data.csv>
```

**Example Usage:** (from root)

```
python3 src/json_to_csv.py -i data/sampled.json -o data/sampled.csv
```

## Repository Structure

```
.
├── COMP 598 Final Project - Data Science Project.pdf
├── README.md
├── data
│   ├── keywords-quoted.csv
│   ├── keywords.csv
│   ├── tweets-1.json
│   └── tweets-2.json
├── requirements.txt
└── src
    └── tweet_collection.py
```