import re
from datetime import datetime, timedelta




import feedparser

# Define the RSS feed URL for historical news
rss_url = 'https://news.google.com/rss/search?q=AAPL%20stock%20news&hl=en-US&gl=US&ceid=US%3Aen'

# Fetch and parse the historical news feed
feed = feedparser.parse(rss_url)

# Print the titles and summaries of historical news articles
for entry in feed.entries:
    article_title = entry.title
    article_summary = entry.summary
    article_link = entry.link

    print("Title:", article_title)
    print("Summary:", article_summary)
    print("Link:", article_link)
    print("\n")








# ======================


from newspaper import Article
from datetime import datetime

# Define the date for which you want to fetch news
target_date = datetime(2023, 11, 30)

# Create a list to store the news articles
news_articles = []

# Define a list of news sources to search for AAPL news (you can add more sources if needed)
news_sources = [
    # 'https://www.reuters.com/',
    'https://www.bloomberg.com/',
    # Add more news sources here
]

# Iterate through the news sources and fetch articles
for source_url in news_sources:
    try:
        # Initialize a Newspaper3k Article object
        article = Article(source_url)

        # Download and parse the article
        article.download()
        article.parse()

        # Check if the article's publication date matches the target date
        article_date = article.publish_date
        if article_date and article_date.date() == target_date.date():
            # Append the article to the list if the date matches
            news_articles.append({
                'title': article.title,
                'publish_date': article_date.strftime('%Y-%m-%d %H:%M:%S'),
                'source_url': source_url,
                'article_text': article.text,
            })

    except Exception as e:
        print(f"Error fetching news from {source_url}: {str(e)}")

# Print or process the collected news articles
for article in news_articles:
    print("Title:", article['title'])
    print("Publish Date:", article['publish_date'])
    print("Source URL:", article['source_url'])
    print("Article Text:", article['article_text'])
    print("\n")


    # =======================


import feedparser
import datetime
import newspaper

# Define the RSS feed URL for historical news
rss_url = 'https://news.google.com/rss/search?q=AAPL%20stock%20news&hl=en-US&gl=US&ceid=US%3Aen'

# Fetch and parse the historical news feed
feed = feedparser.parse(rss_url)

# Define the time range for filtering news (between 9 am to 10 am today)
now = datetime.datetime.now()
start_time = now.replace(hour=9, minute=0, second=0, microsecond=0)
end_time = now.replace(hour=10, minute=0, second=0, microsecond=0)

# Create a newspaper3k Article object for article parsing
article_parser = newspaper.Article('')

# Iterate through the entries in the feed
for entry in feed.entries:
    # Parse the timestamp from the entry
    published_time = datetime.datetime.fromisoformat(entry.published)

    # Check if the news article is within the specified time range
    if start_time <= published_time <= end_time:
        article_title = entry.title
        article_summary = entry.summary
        article_link = entry.link

        # Fetch and parse the full article content
        article_parser.set_url(article_link)
        article_parser.download()
        article_parser.parse()

        # Get the article text
        article_content = article_parser.text

        # Record the timestamp when the article is processed
        processing_time = datetime.datetime.now()

        # Print or store the article title, timestamp, summary, content, and processing timestamp
        print("Title:", article_title)
        print("Published Timestamp:", published_time)
        print("Summary:", article_summary)
        print("Link:", article_link)
        print("Article Content:")
        print(article_content)
        print("Processing Timestamp:", processing_time)
        print("\n")
