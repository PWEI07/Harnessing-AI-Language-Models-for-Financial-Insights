# https://wire.insiderfinance.io/an-ai-based-stock-analyzer-using-llm-and-langchain-7f8a62cbcaaa
import json
import os
import re
import warnings
from openai import OpenAI

client = OpenAI()
# openai.api_key = "sk-...XtWM"
print(os.getenv("OPENAI_API_KEY"))

from openai import OpenAI

client = OpenAI()
import requests
import yfinance as yf
from bs4 import BeautifulSoup
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
                                              messages=[{"role": "user",
                                                         "content": f"What is the company name and stock ticker for: {query}?"}],
                                              functions=function,
                                              function_call={"name": "get_company_Stock_ticker"})
    response.choices[0].message.content

    # Parse the response
    choices = response["choices"]
    if choices and len(choices) > 0:
        message = choices[0]["message"]
        arguments = json.loads(message["function_call"]["arguments"])
        return arguments["company_name"], arguments["ticker_symbol"]
    else:
        # Handle the case where there is no valid response
        return None, None

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

response = client.completions.create(model="gpt-3.5-turbo",
                                     prompt=f"Analyzing the prospect of ZIM company based on the recent news",
                                     max_tokens=50,
                                     n=1,
                                     stop=None,
                                     temperature=0.7)

stream = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Say this is a test"}],
    stream=True,
)
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")

impact_analysis.append(response.choices[0].text.strip())





from openai import OpenAI
from datetime import datetime

def generate_seeking_alpha_url(ticker, start_date, end_date):
    # Format dates in the required format
    start_date_formatted = start_date.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    end_date_formatted = end_date.strftime("%Y-%m-%dT%H:%M:%S.999Z")

    # Construct the URL
    url = f"https://seekingalpha.com/symbol/{ticker}/news?from={start_date_formatted}&to={end_date_formatted}"
    return url

# Example usage
ticker = "ZIM"  # Replace with your ticker
start_date = datetime(2023, 11, 15)  # Start date in yyyy, mm, dd format
end_date = datetime(2023, 12, 1)  # End date in yyyy, mm, dd format

url = generate_seeking_alpha_url(ticker, start_date, end_date)

def extract_news_urls(url):
    # Send a request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve the webpage: Status code {response.status_code}")
        return []

    # Parse the content of the page
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all anchor tags in the news section
    # Note: The exact class or identifier will depend on the webpage's structure
    news_links = soup.find_all('a', href=True, class_='article')
    links = soup.find_all('a', href=True)
    hrefs = [a['href'] for a in soup.find_all('a', {'class': 'text-share-text'})]

    # Extract the URLs
    urls = [link['href'] for link in news_links]
    return urls

news_section = soup.find("section", {"id": "news"})
news_url = soup.find("a")["href"]


link_tag = soup.find('a', class_="text-share-text")
href = link_tag['href'] if link_tag else 'No link found'

div_tag = soup.find('div', class_="vR_Oe w_aE")

import json

# Your parsed result (assuming it's a string)


# Parse the JSON content
try:
    data = json.loads(soup)

    # Navigate through the JSON to find the news data
    news_items = data.get("news", {}).get("response", {}).get("data", [])

    # Extract news IDs
    news_ids = [item.get("id") for item in news_items]

    print(news_ids)
except json.JSONDecodeError as e:
    print("Error parsing JSON:", e)

<h3 class="text-share-text visited:text-share-text hover:text-share-text focus:text-share-text m-0 grow no-underline  text-x-large-r lg:text-large-r mb-4"><a data-test-id="post-list-item-title" class="text-share-text visited:text-share-text hover:text-share-text focus:text-share-text" href="/news/4040526-zim-warns-of-longer-transit-times-as-travel-threats-force-it-to-re-route-vessels?source=content_type%3Areact%7Csection%3Asummary%7Csection_asset%3Anews_news%7Cfirst_level_url%3Asymbol%7Cbutton%3ATitle%7Clock_status%3ANo%7Cline%3A2">ZIM warns of longer transit times as travel threats force it to re-route vessels</a></h3>





# Example usage
generated_url = "YOUR_GENERATED_URL"  # Replace with your generated URL
news_urls = extract_news_urls(generated_url)

for url in news_urls:
    print(url)
client = OpenAI()

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "analyze the impact for ZIM based on this link https://seekingalpha.com/news/4041014-us-warning-evolving-threats-ships-red-sea-trade-route"},
  ]
)

user_msg_1 = "summarize most important news about zim between 11/15 to 11/30 on seeking alpha com and analyze the most prominent impact of them on zim, you can ignore irrelavent or netural news, your response should be less than 200 words"


user_msg_2 = "Please analyze this news's impact on zim, the link is enclosed in single quote 'https://seekingalpha.com/news/3946757-zim-integrated-shipping-services-declares-640-dividend'"
response1 = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful financial anlayst, you know what news are important and what others to ignore in order to save investor's time and provide them with"
                                  "useful opinion. and you care more about more recent news and use them to update the info you get from previous news. you stick to the resources i provided you with and you only form your analysis based on the daterange info contained in the resource link i provide you with, meaning you only use info within or prior to that daterange, no look-ahead bias"},
    {"role": "user", "content": user_msg_2},
  ], max_tokens=100  # Estimated tokens for a 200-word response

)


response1.choices[0].message

url = "https://seekingalpha.com/news/4041014-us-warning-evolving-threats-ships-red-sea-trade-route"


<a data-test-id="post-list-item-title" class="text-share-text visited:text-share-text hover:text-share-text focus:text-share-text" href="/news/4040526-zim-warns-of-longer-transit-times-as-travel-threats-force-it-to-re-route-vessels?source=content_type%3Areact%7Csection%3Asummary%7Csection_asset%3Anews_news%7Cfirst_level_url%3Asymbol%7Cbutton%3ATitle%7Clock_status%3ANo%7Cline%3A2">ZIM warns of longer transit times as travel threats force it to re-route vessels</a>

url = "https://seekingalpha.com/symbol/ZIM/news?from=2023-11-15T00:00:00.000Z&to=2023-11-30T00:00:00.999Z"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
news_links = [a["href"] for a in soup.find_all("a", {"data-test-id": "post-list-item-title"})]
print(news_links)
import requests
from bs4 import BeautifulSoup

url = "https://seekingalpha.com/symbol/ZIM/news?from=2023-11-26T00:00:00.000Z&to=2023-11-30T00:00:00.999Z"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
news_links = [a["href"] for a in soup.find_all("a", {"class": "symbol_article"})]
print(news_links)


url = "https://seekingalpha.com/symbol/ZIM/news?from=2023-11-17T05%3A00%3A00.000Z&to=2023-12-01T04%3A59%3A59.999Z"
html_content = str(soup)

# Find the start and end of the JSON structure
start_index = html_content.find('"news":{')
end_index = html_content.find('}', start_index) + 1  # Adjust this as needed to capture the full JSON structure

# Extract the JSON string
json_str = html_content[start_index:end_index]
news_details = []
data = json.loads(json_str)
import json
import re
from datetime import datetime


# Regular expression pattern to match the desired structure and capture the id and publishOn
pattern = r'"id":"(\d+?)","type":"news","attributes":{"publishOn":"(.*?)"'

# Find all matches using the regular expression
matches = re.findall(pattern, str(soup))

# Define the date range
start_date = datetime.strptime("2023-11-25", "%Y-%m-%d")
end_date = datetime.strptime("2023-11-30", "%Y-%m-%d")

# Filter matches by the publishOn date
filtered_matches = []
for match in matches:
    news_id, publish_on_str = match
    publish_on_date = datetime.strptime(publish_on_str.split("T")[0], "%Y-%m-%d")

    if start_date <= publish_on_date <= end_date:
        filtered_matches.append(news_id)

def get_text_from_url(url):
    # Send a request to the URL
    response = requests.get(url)
    # Parse the content of the request with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract text from the BeautifulSoup object
    text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    return text

text = get_text_from_url(url)



response




