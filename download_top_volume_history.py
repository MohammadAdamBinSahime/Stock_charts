import yfinance as yf
import pandas as pd
from datetime import datetime
import os
import time

def get_stock_data(symbol, period="2y"):
    """Fetch stock data for a given symbol"""
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period=period)
        return data
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

def read_top_volume_csv():
    """Read the latest top volume stocks CSV file"""
    csv_files = [f for f in os.listdir('stock_data') if f.startswith('top_volume_stocks_') and f.endswith('.csv')]
    if not csv_files:
        print("No top volume stocks CSV file found!")
        return None
    
    # Get the most recent file
    latest_file = sorted(csv_files)[-1]
    print(f"Reading ticker symbols from: {latest_file}")
    
    try:
        df = pd.read_csv(f"stock_data/{latest_file}")
        return df['Symbol'].tolist()
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None

def download_historical_data_for_tickers(tickers, period="2y", batch_size=10):
    """Download historical data for a list of tickers"""
    if not tickers:
        print("No tickers provided!")
        return
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    success_count = 0
    error_count = 0
    
    print(f"Starting download of {period} historical data for {len(tickers)} tickers...")
    print(f"Timestamp: {timestamp}")
    print("=" * 60)
    
    for i, symbol in enumerate(tickers, 1):
        print(f"[{i}/{len(tickers)}] Processing {symbol}...", end=" ")
        
        try:
            data = get_stock_data(symbol, period)
            
            if data is not None and not data.empty:
                # Save to CSV with timestamp
                os.makedirs("stock_data", exist_ok=True)
                filename = f"stock_data/{symbol}_2year_history_{timestamp}.csv"
                data.to_csv(filename)
                
                # Calculate stats
                latest = data.iloc[-1]
                first = data.iloc[0]
                return_pct = ((latest['Close'] - first['Close']) / first['Close'] * 100)
                
                print(f"OK {len(data)} days | Return: {return_pct:.2f}% | Saved to {filename}")
                success_count += 1
            else:
                print(f"FAIL No data available")
                error_count += 1
                
        except Exception as e:
            print(f"ERROR: {e}")
            error_count += 1
        
        # Add small delay to avoid overwhelming the API
        if i % batch_size == 0:
            time.sleep(1)
    
    print("\n" + "=" * 60)
    print("DOWNLOAD SUMMARY")
    print("=" * 60)
    print(f"Total tickers processed: {len(tickers)}")
    print(f"Successful downloads: {success_count}")
    print(f"Failed downloads: {error_count}")
    print(f"Success rate: {(success_count/len(tickers)*100):.1f}%")
    print(f"Files saved with timestamp: {timestamp}")

def main():
    print("TOP VOLUME STOCKS HISTORICAL DATA DOWNLOADER")
    print("=" * 60)
    
    # Read ticker symbols from the top volume CSV
    tickers = read_top_volume_csv()
    
    if not tickers:
        print("Could not load ticker symbols. Exiting.")
        return
    
    print(f"Found {len(tickers)} ticker symbols")
    print(f"\nStarting download of 2-year historical data for all {len(tickers)} tickers...")
    
    # Download historical data for all tickers
    download_historical_data_for_tickers(tickers)

if __name__ == "__main__":
    main()