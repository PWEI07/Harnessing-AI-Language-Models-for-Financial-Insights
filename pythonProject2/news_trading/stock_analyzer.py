# https://wire.insiderfinance.io/an-ai-based-stock-analyzer-using-llm-and-langchain-7f8a62cbcaaa
import json
import os
import re
import warnings

# openai.api_key = "sk-...XtWM"
print(os.getenv("OPENAI_API_KEY"))

from openai import OpenAI

client = OpenAI()
import yfinance as yf
from langchain.llms import OpenAI
# openai.api_key = os.getenv(“OPENAI_API_KEY”)

# os.environ["OPENAI_API_KEY"] = "sk-...XtWM"

warnings.filterwarnings("ignore")
llm = OpenAI(temperature=0,
             model_name="gpt-3.5-turbo-16k-0613")

# Define the function to interface with OpenAI
function = [
    {
        "name": "get_company_Stock_ticker",
        "description": "This will get the Indian NSE/BSE stock ticker of the company",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker_symbol": {"type": "string", "description": "The stock symbol of the company."},
                "company_name": {"type": "string", "description": "The name of the company given in the query"},
            },
            "required": ["company_name", "ticker_symbol"],
        },
    }
]


def get_stock_ticker(query):
    """Extracts the company name and ticker symbol from the user's query."""
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    temperature=0,
    messages=[{"role": "user", "content": f"What is the company name and stock ticker for: {query}?"}],
    functions=function,
    function_call={"name": "get_company_Stock_ticker"})
    message = response["choices"][0]["message"]
    arguments = json.loads(message["function_call"]["arguments"])
    return arguments["company_name"], arguments["ticker_symbol"]


def get_financial_statements(ticker):
    # time.sleep(4) #To avoid rate limit error
    if "." in ticker:
        ticker = ticker.split(".")[0]
    else:
        ticker = ticker
    ticker = ticker + ".NS"
    company = yf.Ticker(ticker)
    balance_sheet = company.balance_sheet
    if balance_sheet.shape[1] >= 3:
        balance_sheet = balance_sheet.iloc[:, :3]  # Remove 4th years data
    balance_sheet = balance_sheet.dropna(how="any")
    balance_sheet = balance_sheet.to_string()

    # cash_flow = company.cash_flow.to_string()
    # print(balance_sheet)
    # print(cash_flow)
    return balance_sheet


def google_query(search_term):
    if "news" not in search_term:
        search_term = search_term + " stock news"
    url = f"https://www.google.com/search?q={search_term}&cr=countryIN"
    url = re.sub(r"\s", "+", url)
    return url


# print(get_financial_statements("TATAPOWER.NS"))
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


def analyze_stock(query):
    """Performs a detailed analysis of a stock based on user query."""
    company_name, ticker = get_stock_ticker(query)
    print({"Query": query, "Company Name": company_name, "Ticker": ticker})

    # Fetch relevant stock data (these functions need to be defined)
    # stock_data = get_stock_price(ticker, history=10)
    stock_financials = get_financial_statements(ticker)
    stock_news = get_recent_stock_news(company_name)

    # Compile information for analysis
    available_information = f"Stock Financials: {stock_financials}\n\nStock News: {stock_news}"

    # Conduct analysis using GPT model (llm function needs to be defined)
    analysis = llm(
        f"Provide a detailed stock analysis for {company_name} based on the following information: {available_information}")
    print(analysis)

    return analysis


# Example usage
temp = analyze_stock("How is the stock of Paytm doing?")


#====================

import praw
# Read-only instance
reddit_read_only = praw.Reddit(client_id="TuHjLZK5MKx0T3SCmYv2UQ",         # your client id
                               client_secret="NoQQ9oPOHZieZ4CZbNlRydvINfLjLA",      # your client secret
                               user_agent="llm_finance")        # your user agent

subreddit = reddit_read_only.subreddit("redditdev")

# Display the name of the Subreddit
print("Display Name:", subreddit.display_name)

# Display the title of the Subreddit
print("Title:", subreddit.title)

# Display the description of the Subreddit
print("Description:", subreddit.description)
from pmaw import PushshiftAPI
api = PushshiftAPI()

import datetime as dt
before = int(dt.datetime(2021,2,1,0,0).timestamp())
after = int(dt.datetime(2020,12,1,0,0).timestamp())

subreddit="wallstreetbets"
limit=10
comments = api.search_comments(subreddit=subreddit, limit=limit, before=before, after=after)
print(f'Retrieved {len(comments)} comments from Pushshift')


start_epoch = int(dt.datetime(2023, 11, 29).timestamp())
end_epoch = int(dt.datetime(2023, 11, 30).timestamp())

submissions = list(api.search_submissions(after=start_epoch,
                                           before=end_epoch,
                                           q='AAPL',
                                           subreddit='all',
                                           filter=['url', 'author', 'title', 'subreddit'],
                                           limit=None))

comments = list(api.search_comments(after=start_epoch,
                                     before=end_epoch,
                                     q='AAPL',
                                     subreddit='all',
                                     filter=['url', 'author', 'body', 'subreddit'],
                                     limit=None))

subreddit = reddit_read_only.subreddit("Bitcoin")

for post in subreddit.hot(limit=5):
    print(post.title)
    print()
import pandas as pd
posts_dict = {"Title": [], "Post Text": [],
              "ID": [], "Score": [],
              "comments": [], "Post URL": [], "ups": [], "upvote_ratio": [], "utc": []
              }
for post in subreddit.new(limit=100):
    # Title of each post
    posts_dict["Title"].append(post.title)

    # Text inside a post
    posts_dict["Post Text"].append(post.selftext)

    # Unique ID of each post
    posts_dict["ID"].append(post.id)

    # The score of a post
    posts_dict["Score"].append(post.score)
    # Fetching comments for each post
    post.comments.replace_more(limit=None)  # Load all comments; you can set a limit if needed
    comments = [comment.body for comment in post.comments.list()]
    posts_dict["comments"].append(comments)
    # Total number of comments inside the post
    # posts_dict["Total Comments"].append(post.num_comments)

    # URL of each post
    posts_dict["Post URL"].append(post.url)
    posts_dict["ups"].append(post.ups)
    posts_dict["utc"].append(post.created_utc)
    posts_dict["upvote_ratio"].append(post.upvote_ratio)

# Saving the data in a pandas dataframe
top_posts = pd.DataFrame(posts_dict)
# top_posts
# pandas_timestamp = pd.to_datetime(post.created_utc, unit='s')
top_posts["utc"] = top_posts["utc"].apply(lambda x: pd.to_datetime(x, unit='s'))
top_posts["Post URL"].values()




# ============================
import requests
from bs4 import BeautifulSoup


def get_10k_filings(ticker, filings_count=3):
    base_url = "https://www.sec.gov/cgi-bin/browse-edgar"
    params = {'action': 'getcompany', 'CIK': ticker, 'type': '10-K', 'dateb': '', 'count': filings_count,
              'output': 'atom'}
    response = requests.get(base_url, params=params)
    soup = BeautifulSoup(response.content, 'xml')

    filings = []
    for entry in soup.find_all('entry', limit=filings_count):
        filing = {}
        filing['title'] = entry.title.text
        filing['link'] = entry.link['href']
        filing['date'] = entry.updated.text
        filings.append(filing)

    return filings


# Retrieve the 3 most recent 10-K filings for AAPL
aapl_10k_filings = get_10k_filings('AAPL')
for filing in aapl_10k_filings:
    print(f"Title: {filing['title']}, Date: {filing['date']}, URL: {filing['link']}")

# Note: You can further extract the complete 10-K document by following the URL in each filing.







