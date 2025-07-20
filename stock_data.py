import yfinance as yf
import pandas as pd
from datetime import datetime

def get_stock_data(symbol, period="2y"):
    """Fetch stock data for a given symbol"""
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period=period)
        return data
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

def main():
    symbols = ["AAPL", "GOOGL", "MSFT"]
    
    print("Downloading 2 years of stock price history...")
    
    for symbol in symbols:
        print(f"\n--- {symbol} ---")
        data = get_stock_data(symbol)
        
        if data is not None and not data.empty:
            print(f"Downloaded {len(data)} days of data")
            print(f"Date range: {data.index[0].strftime('%Y-%m-%d')} to {data.index[-1].strftime('%Y-%m-%d')}")
            
            latest = data.iloc[-1]
            first = data.iloc[0]
            
            print(f"Starting Price: ${first['Close']:.2f}")
            print(f"Latest Price: ${latest['Close']:.2f}")
            print(f"2-Year Return: {((latest['Close'] - first['Close']) / first['Close'] * 100):.2f}%")
            print(f"Max Price: ${data['High'].max():.2f}")
            print(f"Min Price: ${data['Low'].min():.2f}")
            
            # Save to CSV with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{symbol}_2year_history_{timestamp}.csv"
            data.to_csv(filename)
            print(f"Data saved to {filename}")
        else:
            print(f"No data available for {symbol}")

if __name__ == "__main__":
    main()