# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 14:06:17 2021

@author: Teo Bee Guan
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

ticker = "AAPL"
url = "https://financialmodelingprep.com/financial-summary/" + ticker
request = requests.get(url)
print(request.text)

parser = BeautifulSoup(request.text, "html.parser")
news_html = parser.find_all('a', {'class': 'article'})
print(news_html[0])

sentiments = []
for i in range(0, len(news_html)):
    sentiments.append(
            {
                'ticker': ticker,
                'date': news_html[i].find('h5', {'class': 'article__date'}).text,
                'title': news_html[i].find('h4', {'class': 'article__title-text'}).text,
                'text': news_html[i].find('p', {'class': 'article__text'}).text
            }
        )

df = pd.DataFrame(sentiments)
df = df.set_index('date')

from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')
analyser = SentimentIntensityAnalyzer()
file_path = "temp_output.txt"

# Open the file in write mode (use 'w' for writing, 'a' for appending)
with open(file_path, 'w') as file:
    # Write the string to the file
    file.write(df['text'][0])

print(df['text'][0])
print(analyser.polarity_scores(df['text'][0]))


