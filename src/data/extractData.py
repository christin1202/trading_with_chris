import numpy as np
import pandas as pd
import yahoo_fin.stock_info as si
import requests
import snscrape.modules.twitter as sntwitter


def extractHistoricalPrice(ticker_list, start_date, end_date, interval='1d', data_path):
    historical_data = {}
    for ticker in ticker_list:
        historical_data[ticker] = si.get_data(ticker, start_date=start_date, end_date=end_date, interval=interval)
        historical_data[ticker].to_csv(data_path + '{}_{}_{}_price.csv'.format(ticker, start_date[:4], end_date[:4]))

    return None

def extractTickerNews(ticker_list, start_date, end_date, n_news, eod_api_key, offset = 0, data_path):
    for ticker in ticker_list:
        url = f'https://eodhistoricaldata.com/api/news?api_token={eod_api_key}&s={ticker}&limit={n_news}&offset={offset}&from={start_date}&to={end_date}'
        news_json = requests.get(url).json()
        news = []
        for i in range(len(news_json)):
            date = news_json[-i]['date']
            title = news_json[-i]['title']
            news.append([ticker, date, title])

        news = pd.DataFrame(news, columns=['ticker', 'date', 'title'])   
        news.to_csv(data_path + '{}_{}_{}_news.csv'.format(ticker, start_date[:4], end_date[:4]))

    return None


def extractTweets(query, max_nb_tweets, data_path):
    # from advanced search, copy the query in the search bar
    # query = "(amazon OR google OR meta) min_replies:50 min_faves:100 min_retweets:200 lang:en until:2022-11-20 since:2020-01-01"
    tweets = []

    for tweet in sntwitter.TwitterSearchScraper(query).get_items():   
       if len(tweets) == max_nb_tweets:
         break
       else:
         tweets.append([tweet.date, tweet.username, tweet.content])
    df = pd.DataFrame(tweets, columns=['Date', 'User', 'Tweet'])
    df.to_csv(data_path + 'tweets.csv')

    return None