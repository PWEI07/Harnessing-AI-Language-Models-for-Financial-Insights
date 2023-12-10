from flask import Flask, render_template, request
import yfinance as yf

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def analyze_stock():
    if request.method == 'POST':
        ticker = request.form['ticker']
        try:
            company = yf.Ticker(ticker)
            if company.info:
                stock_info = company.info
                return render_template('result.html', stock_info=stock_info)
            else:
                error_message = "Invalid stock ticker."
                return render_template('index.html', error_message=error_message)
        except Exception as e:
            error_message = "An error occurred. Please try again."
            return render_template('index.html', error_message=error_message)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
