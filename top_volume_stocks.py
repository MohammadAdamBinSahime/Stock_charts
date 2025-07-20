import yfinance as yf
import pandas as pd
import requests
import os
from datetime import datetime

def get_sp500_symbols():
    """Get S&P 500 stock symbols from Wikipedia"""
    try:
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        tables = pd.read_html(url)
        sp500_table = tables[0]
        symbols = sp500_table['Symbol'].tolist()
        return symbols
    except Exception as e:
        print(f"Error fetching S&P 500 symbols: {e}")
        # Fallback to popular stocks
        return [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'BRK-B', 'UNH', 'JNJ',
            'V', 'WMT', 'PG', 'JPM', 'MA', 'HD', 'CVX', 'ABBV', 'BAC', 'PFE',
            'KO', 'AVGO', 'PEP', 'TMO', 'COST', 'MRK', 'DHR', 'VZ', 'ABT', 'ADBE',
            'NFLX', 'XOM', 'NKE', 'CRM', 'ACN', 'QCOM', 'TXN', 'LIN', 'RTX', 'HON',
            'SBUX', 'MDT', 'UPS', 'NEE', 'LOW', 'IBM', 'AMGN', 'T', 'CVS', 'ORCL'
        ]

def fetch_volume_data(symbols, batch_size=20):
    """Fetch volume data for a list of symbols in batches"""
    volume_data = []
    
    print(f"Fetching volume data for {len(symbols)} stocks...")
    
    for i in range(0, len(symbols), batch_size):
        batch = symbols[i:i+batch_size]
        print(f"Processing batch {i//batch_size + 1}/{(len(symbols)-1)//batch_size + 1}: {len(batch)} stocks")
        
        for symbol in batch:
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="1d")
                
                if not hist.empty:
                    latest_data = hist.iloc[-1]
                    volume_data.append({
                        'Symbol': symbol,
                        'Volume': latest_data['Volume'],
                        'Close': latest_data['Close'],
                        'Change_%': ((latest_data['Close'] - latest_data['Open']) / latest_data['Open'] * 100),
                        'Market_Cap_Est': latest_data['Close'] * latest_data['Volume']  # Rough estimate
                    })
                    print(f"  {symbol}: {latest_data['Volume']:,.0f} volume")
                else:
                    print(f"  {symbol}: No data available")
                    
            except Exception as e:
                print(f"  {symbol}: Error - {e}")
                continue
    
    return volume_data

def main():
    print("=" * 60)
    print("TOP 100 VOLUME STOCKS TRACKER")
    print("=" * 60)
    
    # Get stock symbols
    symbols = get_sp500_symbols()
    print(f"Found {len(symbols)} symbols to analyze")
    
    # Fetch volume data
    volume_data = fetch_volume_data(symbols)
    
    if not volume_data:
        print("No volume data collected!")
        return
    
    # Create DataFrame and sort by volume
    df = pd.DataFrame(volume_data)
    df_sorted = df.sort_values('Volume', ascending=False)
    
    # Get top 100 (or however many we have)
    top_100 = df_sorted.head(100)
    
    print("\n" + "=" * 60)
    print(f"TOP {len(top_100)} STOCKS BY VOLUME")
    print("=" * 60)
    
    # Display results
    print(f"{'Rank':<5} {'Symbol':<8} {'Volume':<15} {'Price':<10} {'Change %':<10}")
    print("-" * 60)
    
    for idx, row in top_100.iterrows():
        rank = top_100.index.get_loc(idx) + 1
        print(f"{rank:<5} {row['Symbol']:<8} {row['Volume']:>13,.0f} ${row['Close']:>7.2f} {row['Change_%']:>8.2f}%")
    
    # Save to CSV
    os.makedirs("stock_data", exist_ok=True)
    filename = f"stock_data/top_volume_stocks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    top_100.to_csv(filename, index=False)
    print(f"\nData saved to {filename}")
    
    # Summary statistics
    print("\n" + "=" * 60)
    print("SUMMARY STATISTICS")
    print("=" * 60)
    print(f"Total stocks analyzed: {len(volume_data)}")
    print(f"Average volume (top 100): {top_100['Volume'].mean():,.0f}")
    print(f"Highest volume: {top_100['Volume'].iloc[0]:,.0f} ({top_100['Symbol'].iloc[0]})")
    print(f"Median volume (top 100): {top_100['Volume'].median():,.0f}")

if __name__ == "__main__":
    main()