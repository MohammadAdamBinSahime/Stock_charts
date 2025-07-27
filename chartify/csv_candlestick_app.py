import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import pandas as pd
import mplfinance as mpf
import numpy as np
import os
import glob
import shutil
from datetime import datetime

def load_csv_data(csv_file):
    """Load and ETL CSV data to match yfinance format"""
    df = pd.read_csv(csv_file)
    
    # Convert Date column to datetime and set as index
    df['Date'] = pd.to_datetime(df['Date'], utc=True)
    df.set_index('Date', inplace=True)
    
    # Ensure index is DatetimeIndex
    if not isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.DatetimeIndex(df.index)
    
    # Ensure columns are in the right order and format for mplfinance
    # mplfinance expects: Open, High, Low, Close, Volume
    required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    
    # Check if all required columns exist
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Required column '{col}' not found in CSV")
    
    # Select only the required columns
    df_clean = df[required_columns].copy()
    
    # Convert to float (in case they're strings)
    for col in required_columns:
        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
    
    # Remove any rows with NaN values
    df_clean = df_clean.dropna()
    
    return df_clean

def create_volume_colors(data):
    """Create green/red colors for volume bars based on price movement"""
    colors = []
    for i in range(len(data)):
        if i == 0:
            colors.append('green')
        else:
            if data['Close'].iloc[i] >= data['Close'].iloc[i-1]:
                colors.append('green')
            else:
                colors.append('red')
    return colors

def calculate_bollinger_band_width(data, window=7, num_std=2):
    """Calculate Bollinger Band Width"""
    rolling_mean = data['Close'].rolling(window=window).mean()
    rolling_std = data['Close'].rolling(window=window).std()
    
    upper_band = rolling_mean + (rolling_std * num_std)
    lower_band = rolling_mean - (rolling_std * num_std)
    
    bb_width = upper_band - lower_band
    
    return bb_width

def plot_candlestick_chart(data, symbol, bb_period=7):
    """Create candlestick chart with colored volume bars and Bollinger Band Width"""
    volume_colors = create_volume_colors(data)
    
    # Calculate Bollinger Band Width with custom period
    bb_width = calculate_bollinger_band_width(data, window=bb_period)
    
    # Create additional plot for Bollinger Band Width
    apds = [
        mpf.make_addplot(bb_width, panel=2, color='purple', ylabel='BB Width')
    ]
    
    style = mpf.make_mpf_style(
        base_mpf_style='charles',
        rc={'font.size': 8},
        marketcolors=mpf.make_marketcolors(
            up='g', down='r',
            volume={'up': 'green', 'down': 'red'}
        )
    )
    
    mpf.plot(
        data,
        type='candle',
        volume=True,
        style=style,
        addplot=apds,
        title=f'{symbol} - Candlestick Chart with Volume and {bb_period}-Period BB Width',
        ylabel='Price ($)',
        ylabel_lower='Volume',
        volume_panel=1,
        panel_ratios=(3, 1, 1),
        figsize=(12, 10),
        tight_layout=True,
        volume_alpha=0.7,
        show_nontrading=False,
        savefig=f'stock_png/{symbol}.png'
    )

def main():
    """Main function to run the candlestick chart application"""
    # Get settings from days.txt
    try:
        with open("days.txt", "r") as f:
            lines = f.read().strip().split('\n')
            days = int(lines[0])
            bb_period = int(lines[1]) if len(lines) > 1 else 7
        print(f"Reading {days} days and {bb_period} BB period from days.txt")
    except (FileNotFoundError, ValueError, IndexError):
        days = 90
        bb_period = 7
        print(f"Could not read days.txt, using defaults: {days} days, {bb_period} BB period")
    
    # Create directories if they don't exist
    os.makedirs("stock_png", exist_ok=True)
    
    # Find all CSV files in stock_data directory (excluding archive)
    csv_files = [f for f in glob.glob("stock_data/*.csv") if not f.startswith("stock_data/archive")]
    
    if not csv_files:
        print("No CSV files found in stock_data/ directory")
        return
    
    print(f"Found {len(csv_files)} CSV files to process")
    
    for csv_file in csv_files:
        try:
            # Extract filename without extension for chart naming
            chart_name = os.path.basename(csv_file).rsplit('.', 1)[0]
            
            print(f"\nProcessing {csv_file}...")
            data = load_csv_data(csv_file)
            
            # Filter to last N days if specified
            if days and days < len(data):
                data = data.tail(days)
            
            if data.empty:
                print(f"No data found in {csv_file}")
                continue
            
            print(f"Data loaded successfully. {len(data)} days of data. Creating chart...")
            plot_candlestick_chart(data, chart_name, bb_period)
            print(f"Chart saved as stock_png/{chart_name}.png")
            
        except Exception as e:
            print(f"Error processing {csv_file}: {e}")
            continue
    
    print(f"\nCompleted processing all CSV files.")

if __name__ == "__main__":
    main()