from flask import Flask, request, render_template_string
from datetime import datetime

app = Flask(__name__)

# Dummy function for demonstration
def analyze_financial_news(ticker, start_date, end_date):
    # Replace with your actual analysis logic
    # Example news data
    news_data = [
        ('https://seekingalpha.com/news/4041014', "U.S. warns ships of 'evolving threats' in critical trade route"),
        ('https://seekingalpha.com/news/4040526', 'ZIM warns of longer transit times as travel threats force it to re-route vessels')
    ]
    return news_data

@app.route('/', methods=['GET', 'POST'])
def form():
    result = []
    ticker = ''
    start_date = ''
    end_date = ''
    if request.method == 'POST':
        ticker = request.form['ticker']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
        result = analyze_financial_news(ticker, start_date_obj, end_date_obj)

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
            </body>
        </html>
    ''', ticker=ticker, start_date=start_date, end_date=end_date, result=result)

if __name__ == '__main__':
    app.run(debug=True)
