from flask import Flask, request, render_template_string
from datetime import datetime

from news_trading.financial_analyzer_1210 import analyze_financial_news

app = Flask(__name__)

# Dummy function for demonstration
# def analyze_financial_news(ticker, start_date, end_date):
#     # Replace with your actual analysis logic
#     # Example news data
#     news_data = [
#         ('https://seekingalpha.com/news/4041014', "U.S. warns ships of 'evolving threats' in critical trade route"),
#         ('https://seekingalpha.com/news/4040526', 'ZIM warns of longer transit times as travel threats force it to re-route vessels')
#     ]
#     analysis_text = "The overall effect of the news on ZIM's stock price is likely to be negative. The U.S. warning about the growing threat of attacks in the Red Sea region and the recent hijackings of ships with Israeli links create additional risks and challenges for ZIM. The temporary re-routing of vessels by ZIM and other shipping companies, including Maersk, indicates the seriousness of the situation.\n\nThe key points from the news are the warnings of attacks in the Red Sea region and the hijacking of a cargo ship owned by Israeli billionaire Rami Ungar's Ray Car Carriers. These incidents increase the risks for ZIM and other shipping companies operating in the area. The re-routing of vessels may result in longer transit times and potential disruptions to ZIM's operations.\n\nThe future prospects for ZIM and its stock price are impacted by the potential risks associated with navigating the Red Sea region."
#     return news_data, analysis_text

@app.route('/', methods=['GET', 'POST'])
def form():
    result = []
    analysis = ''
    ticker = ''
    start_date = ''
    end_date = ''
    if request.method == 'POST':
        ticker = request.form['ticker']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
        result, analysis = analyze_financial_news(ticker, start_date_obj, end_date_obj)

    return render_template_string('''
        <html>
            <body>
                <form method="post">
                    Ticker: <input type="text" name="ticker" value="{{ ticker }}"><br>
                    Start Date (yyyy-mm-dd): <input type="date" name="start_date" value="{{ start_date }}"><br>
                    End Date (yyyy-mm-dd): <input type="date" name="end_date" value="{{ end_date }}"><br>
                    <input type="submit" value="Analyze">
                </form>
                {% if result %}
                    <h3>News</h3>
                    <div style="font-size:14px; margin-top:20px;">
                        {% for url, title in result %}
                            <div><a href="{{ url }}" target="_blank">{{ title }}</a></div>
                        {% endfor %}
                    </div>
                {% endif %}
                {% if analysis %}
                    <h3>Analysis</h3>
                    <div style="font-size:14px; margin-top:20px; white-space: pre-wrap;">{{ analysis }}</div>
                {% endif %}
            </body>
        </html>
    ''', ticker=ticker, start_date=start_date, end_date=end_date, result=result, analysis=analysis)

if __name__ == '__main__':
    app.run(debug=True)
