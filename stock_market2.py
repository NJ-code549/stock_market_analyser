import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Step 1: Get list of S&P 500 tickers from Wikipedia
def get_sp500_tickers():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'id': 'constituents'})
    
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td') [0].text.strip()
        tickers.append(ticker)
    
    return tickers

# Step 2: Get stock data and calculate indicators
def get_stock_data(ticker):
    
    stock_data = yf.download(ticker, period='1y', interval='1d')
    return stock_data

def calculate_moving_averages(stock_data):
    stock_data['SMA_50'] = stock_data['Close'].rolling(window=50).mean()
    stock_data['SMA_200'] = stock_data['Close'].rolling(window=200).mean()
    return stock_data

def check_buy_signal(stock_data):
    if stock_data['SMA_50'][-1] > stock_data['SMA_200'][-1] and stock_data['SMA_50'][-2] <= stock_data['SMA_200'][-2]:
        return True
    return False

# Step 3: Analyze multiple stocks and provide recommendations
def analyze_stocks(tickers):
    buy_signals = []
    
    for ticker in tickers:
        print(f"Analyzing {ticker}...")
        try:
            stock_data = get_stock_data(ticker)
            stock_data = calculate_moving_averages(stock_data)
            
            if check_buy_signal(stock_data):
                buy_signals.append(ticker)
        except Exception as e:
            print(f"Error analyzing {ticker}: {e}")
    
    return buy_signals

# Main function to run the analysis
def main():
    tickers = get_sp500_tickers()  # Get S&P 500 tickers
    buy_signals = analyze_stocks(tickers)  # Analyze each stock
    
    if buy_signals:
        print(f"Buy signals generated for the following stocks: {buy_signals}")
    else:
        print("No buy signals found at this time.")

# Run the script
if __name__ == "__main__":
    main()
