import numpy as np
import pandas as pd
import yahoo_fin.stock_info as si
import requests
import snscrape.modules.twitter as sntwitter

def extractHistoricalPrice(data_path, ticker_list, start_date, end_date, interval='1d'):
    historical_data = {}
    for ticker in ticker_list:
        historical_data[ticker] = si.get_data(ticker, start_date=start_date, end_date=end_date, interval=interval)
        historical_data[ticker].to_csv(data_path + '{}_{}_{}_price.csv'.format(ticker, start_date[:4], end_date[:4]))

    return None

def extractTickerNews(data_path, ticker_list, start_date, end_date, n_news, eod_api_key, offset = 0):
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

def extractTweets(data_path, query, max_nb_tweets):
    # from advanced search, copy the query in the search bar
    # query = "(amazon OR google OR meta) min_replies:50 min_faves:100 min_retweets:200 lang:en until:2022-11-20 since:2020-01-01"
    tweets = []

    for tweet in sntwitter.TwitterSearchScraper(query).get_items():   
       if len(tweets) == max_nb_tweets:
         break
       else:
         tweets.append([tweet.date, tweet.user.username, tweet.content])
    df = pd.DataFrame(tweets, columns=['Date', 'User', 'Tweet'])
    df.to_csv(data_path + 'tweets.csv')

    return None


if __name__ == '__main__':

    data_path = '/Users/chiuchristine/Documents/dev_projects/data/'
    ticker_list = [
                    'AAPL','MSFT','AMZN','GOOGL','TSLA','UNH','JNJ','XOM','ELV','AMD',
                    'NVDA','JPM','PG','V','HD','CVX','MA','LLY','PFE','ABBV',
                    'MRK','META','PEP','BAC','KO','COST','AVGO','TMO','WMT','CSCO',
                    'MCD','ACN','ABT','DIS','DHR','WFC','BMY','LIN','NEE','TXN',
                    'ADBE','VZ','CMCSA','PM','COP','AMGN','RTX','HON','CRM','QCOM',
                    'NFLX','NKE','UPS','LOW','T','UNP','IBM','CVS','GS','ORCL'
                    ]
    start_date = '2012-01-01'
    end_date = '2022-11-30'

    # extractHistoricalPrice(data_path = data_path, ticker_list = ticker_list, 
    #                        start_date = start_date, end_date = end_date, interval='1d')

    # Apple OR Microsoft OR Amazon OR Google OR Berkshire OR Tesla OR Johnson OR Exxon OR NVIDIA OR JPMorgan OR Procter Gamble OR Home Depot OR Chevron OR Mastercard OR Eli OR Lilly OR Pfizer OR AbbVieMerck OR & OR Co OR Meta OR Pepsi OR Bank OR of OR America OR Coca-Cola OR Costco OR Broadcom OR Thermo OR Fisher OR Scientific OR Walmart OR Cisco OR McDonald's OR Accenture OR Abbott OR Laboratories OR Walt OR Disney OR Danaher OR Wells OR Fargo OR Bristol-Myers OR Squibb OR Linde OR plc OR NextEra OR Energy OR Texas OR Instruments OR Adobe OR Verizon OR Communications OR Comcast OR Philip OR Raytheon OR Honeywell OR Salesforce OR QUALCOMM OR Netflix) min_replies:280 min_faves:280 min_retweets:280 lang:en until:2022-11-30 since:2022-11-01, max_nb_tweets) (Apple OR Microsoft OR Amazon OR Google OR Berkshire OR Tesla OR Johnson OR & OR Johnson OR Exxon OR NVIDIA OR JPMorganProcter OR & OR Gamble OR Home OR Depot OR Chevron OR Mastercard OR Eli OR Lilly OR Pfizer OR AbbVieMerck OR & OR Co OR Meta OR Pepsi OR Bank OR of OR America OR Coca-Cola OR Costco OR Broadcom OR Thermo OR Fisher OR Scientific OR Walmart OR Cisco OR McDonald's OR Accenture OR Abbott OR Laboratories OR Walt OR Disney OR Danaher OR Wells OR Fargo OR Bristol-Myers OR Squibb OR Linde OR plc OR NextEra OR Energy OR Texas OR Instruments OR Adobe OR Verizon OR Communications OR Comcast OR Philip OR Raytheon OR Honeywell OR Salesforce OR QUALCOMM OR Netflix