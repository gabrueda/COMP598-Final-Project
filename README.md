# Understanding Discussions Around COVID-19 and Vaccination Hesitancy in Canada
Final Project for COMP 598 - Fall 2021 at McGill University

Project made by [Nathalie Redick](https://github.com/nredick), [Gabriela Rueda](https://github.com/gabrueda), and [Yusen Tang](https://github.com/TeachFakerPlayingMid).

## Project Description

This project uses the [Twitter API](https://developer.twitter.com/en/docs/twitter-api) via [`tweepy`](https://www.tweepy.org) to gather recent Tweets based on keywords related to COVID-19 and COVID-19 vaccine hesitancy. The tweets are filtered geographically to select for those posted in Canada. For 3 days, 1000 tweets were collected each day based on a random selection of 10 keywords. 333 tweets were sampled from each day and used in a final dataset of 1000 tweets, which were manually annotated for sentiment and topic. 

Tweet data collected by `tweet_collection.py` is stored in a json file, and each tweet has the following associated data: _id, created_at, location, text,_ and _retweet_. 

## Usage 

**Clone this repository.**

* Recommended to use a virtual environment, which can be set up as follows: 

```
python3 -m venv <name of virtual environment>
source <name of virtual environment>/bin/activate
```

**Install requirements:** 

```
pip install -r requirements.txt
```

**Environment Variable Set-Up:** 
Environment variables are handled by [`python-dotenv`](https://pypi.org/project/python-dotenv/)

## Scripts

### tweet_collection.py
A Twitter Developer Account with Elevated access is necessary to run the code. The API key and API key secret should be stored in a `.env` file (see `.env_template`).

```
usage: tweet_collection.py [-h] [-k KEYWORD_PATH] [-o OUTPUT_PATH]

options:
  -h, --help       show this help message and exit
  -k KEYWORD_PATH  <keywords.csv> (optional)
  -o OUTPUT_PATH   <output.json> (optional)
  -d DATE DATE     <2021-11-25> <'Nov 24'>
```

**Example Usage:** (from root)

```
python3 src/tweet_collection.py -k data/keywords.csv -o data/tweets.json -d 2021-11-25 'Nov 24'
```

The file `tweet_collection.py` collects 1000 unique tweets, which can take a while due to the Twitter API's rate limit. It will sleep automatically and continue collecting tweets until it reaches 1000 tweets. The first date in format(YYYY-MM-DD) represents until which day you want to collect tweets. Twitter API only allows to query 7 days prior so the range is (7 days prior - specified date) and the second date in format (MMM DD) represents for which exact date you want to collect.

### json_to_csv.py

This script will convert a json file (with a json object in each line) into a csv file.
This script assumes the fields `['id', 'text', 'topic', 'sentiment', 'created_at', 'retweet']` are present for each record.
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

### sample_tweets.py

This script randomly samples 333 tweets from each of three input files and 1 extra from one randomly selected file for a total of 1000 tweets over three days. It takes as input three json files and returns a single json file.

```
usage: sample_tweets.py [-h] -i INPUT_FILE1 INPUT_FILE2 INPUT_FILE3
                        [-o OUTPUT_PATH]

options:
  -h, --help            show this help message and exit
  -i INPUT_FILE1 INPUT_FILE2 INPUT_FILE3
  -o OUTPUT_PATH        <sampled.json> (optional)
```

**Example Usage:** (from root)

```
python3 src/sample_tweets.py -i data/tweets_2021-11-22-location.json data/tweets_2021-11-24-location.json data/tweets_2021-11-26-location.json -o final_tweets.json
```

## Repository Structure

```
.
├── COMP 598 Final Project - Data Science Project.pdf
├── README.md
├── data
│   ├── final_tweets.csv
│   ├── final_tweets.json
│   ├── keywords-quoted.csv
│   ├── keywords.csv
│   ├── sampled.csv
│   ├── sampled.json
│   ├── topics_key.csv
│   ├── tweets-2021-11-22-location.json
│   ├── tweets-2021-11-24-location.json
│   └── tweets-2021-11-26-location.json
├── requirements.txt
└── src
    ├── json_to_csv.py
    ├── sample_tweets.py
    └── tweet_collection.py
```
