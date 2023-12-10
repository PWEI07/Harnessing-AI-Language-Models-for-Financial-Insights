from datetime import datetime
from flask import Flask, request, render_template_string
from news_trading.financial_analyzer_1210 import analyze_financial_news

app = Flask(__name__)


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
