import os
import time
from bs4 import BeautifulSoup
import re
import requests
import warnings

import langchain
from langchain.llms import OpenAI
from langchain.agents import load_tools, AgentType, Tool, initialize_agent

os.environ["OPENAI_API_KEY"] = "ENter your API key here"

warnings.filterwarnings("ignore")

llm = OpenAI(temperature=0,
             model_name="gpt-3.5-turbo-16k-0613")
import yfinance as yf


# Fetch stock data from Yahoo Finance

def get_stock_price(ticker, history=5):
    # time.sleep(4) #To avoid rate limit error
    if "." in ticker:
        ticker = ticker.split(".")[0]
    ticker = ticker + ".NS"
    stock = yf.Ticker(ticker)
    df = stock.history(period="1y")
    df = df[["Close", "Volume"]]
    df.index = [str(x).split()[0] for x in list(df.index)]
    df.index.rename("Date", inplace=True)
    df = df[-history:]
    # print(df.columns)

    return df.to_string()

temp = get_stock_price("TITAN")
print(temp)
# =======================================================

# Script to scrap top5 googgle news for given company name

def google_query(ticker):
    # if "news" not in search_term:
    #     search_term = search_term + " stock news"
    # url = f"https://www.google.com/search?q={search_term}&cr=countryIN"
    # url = re.sub(r"\s", "+", url)
    start_time = '2023-11-29T15:00:00'
    end_time = '2023-11-30T17:00:00'
    query = f'{ticker} news'

    url = f'https://www.google.com/search?q={urllib.parse.quote(query)}&tbs=cdr:1,cd_min:{start_time},cd_max:{end_time}'
    print(url)
    return url

company_name='AALP'
def get_recent_stock_news(company_name):
    # time.sleep(4) #To avoid rate limit error
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

    g_query = google_query(company_name)
    res = requests.get(g_query, headers=headers).text
    soup = BeautifulSoup(res, "html.parser")
    news = []

    soup.find_all("div", "tF2Cxc")
    news = []
    for n in soup.find_all("div", "tF2Cxc"):
        try:
            title = n.find("h3").text
            link = n.find("a")["href"]

            # Fetch the article page
            article_page = requests.get(link).text
            article_soup = BeautifulSoup(article_page, 'html.parser')

            # Extract the article text
            article_text = article_soup.find('div', {'class': 'tF2Cxc'}).text.strip()

            news.append({'title': title, 'article_text': article_text})
        except Exception as e:
            pass

    for n in soup.find_all("div", "n0jPhd ynAwRc tNxQIb nDgy9d"):
        news.append(n.text)
    for n in soup.find_all("div", "IJl0Z"):
        news.append(n.text)

    if len(news) > 6:
        news = news[:4]
    else:
        news = news
    news_string = ""
    for i, n in enumerate(news):
        news_string += f"{i}. {n}\n"
    top5_news = "Recent News:\n\n" + news_string

    return top5_news

temp1 = get_recent_stock_news("Asian paints")
print(temp1)
# =========================
# Script to scrap top5 googgle news for given company name

def google_query(search_term):
    if "news" not in search_term:
        # search_term = '"'+search_term + '"' + " stock news reuters"
        search_term1 = '\"' +search_term + '\"' + " stock news"

    start_time = '2023-11-29T15:00:00'
    end_time = '2023-11-30T17:00:00'

    # Encode the search_term to ensure it's included in the query
    encoded_search_term = re.sub(r"\s", "+", search_term1)

    url = f'https://www.google.com/search?q={encoded_search_term}&tbs=cdr:1,cd_min:{start_time},cd_max:{end_time}'

    return url

company_name = "Asian paints"
company_name = "Apple"






aapl = yf.Ticker("AAPL")
news_df = aapl.news
news_df = news_df[(news_df.index >= "2023-11-29 10:00:00") & (news_df.index <= "2023-11-30 17:00:00")]
print(news_df["title"])

from newspaper import Article
url = news_df[1]['link']
article = Article(url)
article.download()
article.html
article.parse()
article.authors
article.publish_date
article.text


def get_recent_stock_news(company_name):
    # time.sleep(4) #To avoid rate limit error
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

    g_query = google_query(company_name)
    res = requests.get(g_query, headers=headers).text
    soup = BeautifulSoup(res, "html.parser")
    news = []
    for n in soup.find_all("div", "n0jPhd ynAwRc tNxQIb nDgy9d"):
        news.append(n.text)
    for n in soup.find_all("div", "IJl0Z"):
        news.append(n.text)

    if len(news) > 6:
        news = news[:4]
    else:
        news = news
    news_string = ""
    for i, n in enumerate(news):
        news_string += f"{i}. {n}\n"
    top5_news = "Recent News:\n\n" + news_string

    return top5_news


print(get_recent_stock_news("Asian paints"))
#



import requests

url = "http://api.marketstack.com/v1/tickers/aapl/news"
params = {
    "access_key": "4b14e83f17f404015ef6869934f130a4",
    "date_from": "2023-11-29T07:00:00",
    "date_to": "2023-11-30T22:00:00"
}

response = requests.get(url, params=params)
news = response.json()["data"]
titles = []
urls = []
sources = []
dates = []
texts = []

for article in news:
    titles.append(article["title"])
    urls.append(article["url"])
    sources.append(article["source"])
    dates.append(article["date"])
    texts.append(requests.get(article["url"]).text)







# =========================
import urllib.parse

start_time = '2023-11-29T15:00:00'
end_time = '2023-11-30T17:00:00'
query = 'AAPL news'

url = f'https://www.google.com/search?q={urllib.parse.quote(query)}&tbs=cdr:1,cd_min:{start_time},cd_max:{end_time}'
print(url)

# Send an HTTP GET request to the generated URL
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
res = requests.get(url, headers=headers).text

# Parse the HTML content
soup = BeautifulSoup(res, "html.parser")

# Find and parse the top 10 news articles
news = []
for n in soup.find_all("div", "tF2Cxc"):
    title = n.find("h3").text
    link = n.find("a")["href"]

    # Fetch the article page
    article_page = requests.get(link).text
    article_soup = BeautifulSoup(article_page, 'html.parser')

    # Extract the article text
    article_text = article_soup.find('div', {'class': 'tF2Cxc'}).text.strip()

    news.append({'title': title, 'article_text': article_text})

# Print or process the top 10 news articles
for i, article in enumerate(news, start=1):
    print(f"News {i}:")
    print("Title:", article['title'])
    print("Article Text:", article['article_text'])
    print()



query = google_query('aapl')


# Send a GET request to the URL
response = requests.get(query)
# response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
links = []
for link in soup.find_all("a"):
    href = link.get("href")
    if href.startswith("/url?q="):
        url = href[7:].split("&")[0]
        print(url)
        links.append(url)


# # Check if the request was successful
# if response.status_code == 200:
#     # Parse the HTML content using BeautifulSoup
#     soup = BeautifulSoup(response.text, "html.parser")
#
#     # Find all the search result links
#     result_links = soup.find_all("a", href=True)
#
#     # Extract the URLs from the links
#     urls = [re.search(r"https?://[^\s]+", link["href"]).group() for link in result_links]
#
#     # Print the top 20 URLs
#     for i, url in enumerate(urls[:20], start=1):
#         print(f"{i}. {url}")
# else:
#     print("Failed to fetch the search result page.")
#
#
# # Send an HTTP GET request to the Google search URL
# response = requests.get(query)
#
# # Parse the HTML content of the response using BeautifulSoup
# soup = BeautifulSoup(response.text, 'html.parser')
#
# # Find all the search result links in the HTML
# search_results = soup.find_all('a', href=True)
# #
# # # Filter out the relevant links (usually, Google search result links start with "/url?q=")
# filtered_links = [link['href'][7:] for link in search_results if link['href'].startswith('/url?q=')]
# len(filtered_links)
# # Extract the top 20 links
# # top_20_links = filtered_links[:20]
# top_20_links = filtered_links

dates = []
text = []


for link in links:
    try:
        article = Article(link)
        article.download()
        # article.html
        article.parse()
        # article.authors
        dates.append(article.publish_date)
        text.append(article.text)
        print(article.text)
    except Exception as e:
        pass










# Print the top 20 links
for i, link in enumerate(top_20_links, start=1):
    print(f"{i}. {link}")


from googlesearch import search

query = "Apple stock news"
tbs = "cdr:1,cd_min:2023-11-29T15:00:00,cd_max:2023-11-30T17:00:00"
num_results = 20

for i, url in enumerate(search(query, tbs=tbs, num_results=num_results)):
    print(f"{i+1}. {url}")

ticker = 'aapl'
def google_query(ticker):
    if "news" not in ticker:
        search_term = ticker + " stock news"
    else:
        search_term = ticker

    start_time = '2023-11-29T15:00:00'
    end_time = '2023-11-30T17:00:00'

    # Encode the search_term to ensure it's included in the query
    encoded_search_term = re.sub(r"\s", "+", search_term)

    url = f'https://www.google.com/search?q={encoded_search_term}&tbs=cdr:1,cd_min:{start_time},cd_max:{end_time}&oq={ticker}&start={ticker}'
    return url

    #
    # response = requests.get(url)
    # soup = BeautifulSoup(response.text, 'html.parser')
    #
    # results = soup.find_all('div', class_='BNeawe vvjwJb AP7Wnd')
    # for result in results:
    #     if ticker.lower() in result.text.lower():
    #         print(result.text)
    #         print()


# Script to scrap top5 googgle news for given company name

def google_query(search_term):
    if "news" not in search_term:
        search_term = search_term + " stock news"
    url = f"https://www.google.com/search?q={search_term}&cr=countryIN"
    url = re.sub(r"\s", "+", url)
    return url


def get_recent_stock_news(company_name):
    # time.sleep(4) #To avoid rate limit error
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

    g_query = google_query(company_name)
    res = requests.get(g_query, headers=headers).text
    soup = BeautifulSoup(res, "html.parser")
    news = []
    for n in soup.find_all("div", "n0jPhd ynAwRc tNxQIb nDgy9d"):
        news.append(n.text)
    for n in soup.find_all("div", "IJl0Z"):
        news.append(n.text)

    if len(news) > 6:
        news = news[:4]
    else:
        news = news
    news_string = ""
    for i, n in enumerate(news):
        news_string += f"{i}. {n}\n"
    top5_news = "Recent News:\n\n" + news_string

    return top5_news


print(get_recent_stock_news("Asian paints"))


# Fetch financial statements from Yahoo Finance

def get_financial_statements(ticker):
    # time.sleep(4) #To avoid rate limit error
    company = yf.Ticker(ticker)
    balance_sheet = company.balance_sheet
    # if balance_sheet.shape[1] >= 3:
    #     balance_sheet = balance_sheet.iloc[:, :3]  # Remove 4th years data
    # balance_sheet = balance_sheet.dropna(how="any")
    # balance_sheet = balance_sheet.to_string()

    return balance_sheet

temp = get_financial_statements('AAPL')
print(get_financial_statements("TATAPOWER.NS"))


from langchain.tools import DuckDuckGoSearchRun
search=DuckDuckGoSearchRun()

search("Stock news India")