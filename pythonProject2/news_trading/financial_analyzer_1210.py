import json
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from openai import OpenAI


def generate_seeking_alpha_url(ticker, start_date, end_date):
    # Format dates in the required format
    start_date_formatted = start_date.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    end_date_formatted = end_date.strftime("%Y-%m-%dT%H:%M:%S.999Z")

    # Construct the URL
    url = f"https://seekingalpha.com/symbol/{ticker}/news?from={start_date_formatted}&to={end_date_formatted}"
    return url


def extract_news_url(ticker, start_date, end_date):
    url = generate_seeking_alpha_url(ticker, start_date, end_date)
    # url = "https://seekingalpha.com/symbol/ZIM/news?from=2023-11-26T00:00:00.000Z&to=2023-11-30T00:00:00.999Z"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Regular expression pattern to match the desired structure and capture the id, publishOn, and title
    pattern = r'"id":"(\d+?)","type":"news","attributes":{"publishOn":"(.*?)",".*?"title":"(.*?)"'

    # Find all matches using the regular expression
    matches = re.findall(pattern, str(soup))

    # Filter matches by the publishOn date and collect news titles
    filtered_matches = []
    for match in matches:
        news_id, publish_on_str, title = match
        publish_on_date = datetime.strptime(publish_on_str.split("T")[0], "%Y-%m-%d")

        if start_date <= publish_on_date <= end_date:
            filtered_matches.append((news_id, title))

    # Create a list of URLs with titles
    return [(f'https://seekingalpha.com/news/{x[0]}', x[1]) for x in filtered_matches]
# ===================================

def get_text_from_url(url):
    # Send a request to the URL
    response = requests.get(url)
    # Parse the content of the request with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract text from the BeautifulSoup object
    text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    return text


steps = """ 1) Analyze the overall effect of all the news on company stock price (positive, negative, neutral). 2) Summarize key points and assess how each news impact the company's future prospects and stock price. keep in mind the max length of your response is 200 words in total, so prioritize the news that are most important and relavent to the company's prospects. 
"""
client = OpenAI()


# Example usage
def analyze_financial_news(ticker, start_date, end_date):
    news = extract_news_url(ticker, start_date, end_date)
    news_urls = [x[0] for x in news]
    # news_titles = [x[1] for x in news]
    news_text = '\n'.join([get_text_from_url(url) for url in news_urls]).replace(
        "Have a tip? Submit confidentially to our News team. Found a factual error? Report here.", "")
    user_msg_2 = f"analyze the effect of these news for {ticker}: {news_text[:1000]} "
    response2 = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": f"You are a professional financial anlayst, you generate insights that are both practical and analytical, potentially useful for investment or trading decisions. You dont include cliche warnings like 'It is recommended to conduct further research and analysis or consult with a financial advisor before making an investment decision'. You're succinct and are able to present all your anlaysis and news summarization in no more than 200 words. To do this, you prioritize important news, skip not-that-important news, and get rid of repetitive information.Use the following step-by-step instructions to respond to user inputs (which contains ticker, and news for you to analyze). {steps}"},
            {"role": "user", "content": user_msg_2},
        ],
        max_tokens=300  # Estimated tokens for a 200-word response
    )

    return news, response2.choices[0].message.content

if __name__ == "__main__":
    ticker = "ZIM"  # Replace with your ticker
    start_date = datetime(2023, 11, 25)  # Start date in yyyy, mm, dd format
    end_date = datetime(2023, 12, 1)  # End date in yyyy, mm, dd format
    news = extract_news_url(ticker, start_date, end_date)

    analyze_financial_news(ticker, start_date, end_date)
