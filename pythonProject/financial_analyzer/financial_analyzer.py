import re
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import yfinance as yf


def generate_seeking_alpha_url(ticker, start_date, end_date):
    start_date_formatted = start_date.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    # Adjust end_date to the end of the next day and format
    end_date_adjusted = end_date + timedelta(days=1)
    end_date_formatted = end_date_adjusted.strftime("%Y-%m-%dT23:59:59.999Z")

    # Construct the URL
    url = f"https://seekingalpha.com/symbol/{ticker}/news?from={start_date_formatted}&to={end_date_formatted}"
    return url


def extract_news_url(ticker, start_date, end_date):
    url = generate_seeking_alpha_url(ticker, start_date, end_date)
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
    return [(f"https://seekingalpha.com/news/{x[0]}", x[1]) for x in filtered_matches]


def get_text_from_url(url):
    # Send a request to the URL
    response = requests.get(url)
    # Parse the content of the request with BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract text from the BeautifulSoup object
    text = " ".join(map(lambda p: p.text, soup.find_all("p")))
    return text


steps = """1) Analyze the overall effect of all the news on company stock price (positive, negative, neutral). 2) 
Summarize key points and assess how each news impact the company's future prospects and stock price. keep in mind the 
max length of your response is 200 words in total, so prioritize the news that are most important and relavent to the 
company's prospects."""
client = OpenAI()


def analyze_financial_news(ticker, start_date, end_date):
    try:
        # Validate Ticker
        if not is_valid_ticker(ticker):
            # Use OpenAI API to correct the ticker
            ticker = get_corrected_ticker(ticker)

        news = extract_news_url(ticker, start_date, end_date)
        news_urls = [x[0] for x in news]
        news_text = "\n".join([get_text_from_url(url) for url in news_urls]).replace(
            "Have a tip? Submit confidentially to our News team. Found a factual error? Report here.",
            "",
        )
        if news_text == '':
            raise Exception("No news found")
        user_msg = f"analyze the effect of these news for {ticker}: {' '.join(news_text.split()[:1500])} "
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a professional financial analyst, you generate insights that are both "
                               f"practical "
                               f"and analytical, potentially useful for investment or trading decisions. You dont "
                               f"include "
                               f"cliche warnings like 'It is recommended to conduct further research and analysis or "
                               f"consult with a financial advisor before making an investment decision'. You're "
                               f"succinct "
                               f"and are able to present all your anlaysis and news summarization in no more than 200 "
                               f"words. To do this, you prioritize important news, skip not-that-important news, "
                               f"and get rid of repetitive information.Use the following step-by-step instructions to "
                               f"respond to user inputs (which contains ticker, and news for you to analyze). {steps}",
                },
                {"role": "user", "content": user_msg},
            ],
            max_tokens=300,  # Estimated tokens for a 200-word response
        )

        return news, response.choices[0].message.content
    except:
        news = [(None, None)]
        msg = ("Could not find any news to analyze based on the ticker and date range you provided. Please enter a more accurate ticker or description for the stock you are interested in or change the date range.")
        return news, msg


def is_valid_ticker(ticker):
    try:
        info = yf.Ticker(ticker).info
        return 'symbol' in info and info['symbol'] is not None
    except Exception as e:
        print(f"Error checking ticker: {e}")
        return False


def get_corrected_ticker(input_ticker):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an AI trained to figure out stock market ticker and return it."
            },
            {
                "role": "user",
                "content": f"Return only the stock ticker symbol for the company commonly referred to as apple."
            },
            {
                "role": "assistant",
                "content": f"AAPL"
            },
            {
                "role": "user",
                "content": f"Return only the stock ticker symbol for the company commonly referred"
                           f" to as {input_ticker}."
            }
        ],
    )

    corrected_ticker = response.choices[0].message.content
    return corrected_ticker


if __name__ == "__main__":
    ticker = "ZIM"  # Replace with your ticker
    start_date = datetime(2023, 11, 25)  # Start date in yyyy, mm, dd format
    end_date = datetime(2023, 12, 1)  # End date in yyyy, mm, dd format
    news = extract_news_url(ticker, start_date, end_date)

    analyze_financial_news(ticker, start_date, end_date)
