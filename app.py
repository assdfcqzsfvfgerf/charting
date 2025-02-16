import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import requests
import hmac
import hashlib
import time
from datetime import datetime, timedelta
from config import API_KEY, API_SECRET, API_BASE_URL

def generate_signature(request_path, params=None):
    """Generate signature for Crypto.com API authentication"""
    timestamp = str(int(time.time() * 1000))
    params_str = ''.join([f"{key}{params[key]}" for key in sorted(params.keys())]) if params else ''
    payload = f"{timestamp}{request_path}{params_str}"
    signature = hmac.new(
        bytes(API_SECRET, 'utf-8'),
        msg=bytes(payload, 'utf-8'),
        digestmod=hashlib.sha256
    ).hexdigest()
    return timestamp, signature

def api_request(endpoint, params=None):
    """Make authenticated request to Crypto.com API"""
    request_path = f"/v2/{endpoint}"
    timestamp, signature = generate_signature(request_path, params)
    
    headers = {
        'api-key': API_KEY,
        'api-timestamp': timestamp,
        'api-signature': signature,
    }
    
    response = requests.get(
        f"{API_BASE_URL}/{endpoint}",
        params=params,
        headers=headers
    )
    
    if response.status_code == 200:
        return response.json()['result']
    else:
        raise Exception(f"API request failed: {response.text}")

# Set page config
st.set_page_config(
    page_title="Crypto Charts",
    page_icon="📈",
    layout="wide"
)

# Title
st.title("📈 Cryptocurrency Charts")

# Sidebar
st.sidebar.header("Settings")

try:
    # Get list of available instruments
    instruments = api_request('public/get-instruments')
    trading_pairs = [inst['instrument_name'] for inst in instruments['instruments'] 
                    if inst['quote_currency'] == 'USDT']  # Filter for USDT pairs
    
    # Cryptocurrency selection
    selected_pair = st.sidebar.selectbox("Select Trading Pair", trading_pairs)
    
    # Time range selection
    time_ranges = {
        '24 Hours': {'interval': '5m', 'days': 1},
        '7 Days': {'interval': '30m', 'days': 7},
        '30 Days': {'interval': '4h', 'days': 30},
        '90 Days': {'interval': '1D', 'days': 90}
    }
    selected_range = st.sidebar.selectbox("Select Time Range", list(time_ranges.keys()))
    
    # Calculate time parameters
    end_time = int(time.time() * 1000)
    start_time = end_time - (time_ranges[selected_range]['days'] * 24 * 60 * 60 * 1000)
    
    # Fetch candlestick data
    params = {
        'instrument_name': selected_pair,
        'timeframe': time_ranges[selected_range]['interval'],
        'start_ts': start_time,
        'end_ts': end_time
    }
    
    candlestick_data = api_request('public/get-candlestick', params)
    
    if candlestick_data['data']:
        # Convert data to DataFrame
        df = pd.DataFrame(candlestick_data['data'], columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume', 'amount'
        ])
        
        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        
        # Create candlestick chart
        fig_price = go.Figure(data=[go.Candlestick(
            x=df['timestamp'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='Price'
        )])
        
        fig_price.update_layout(
            title=f"{selected_pair} Price Chart",
            xaxis_title="Date",
            yaxis_title="Price (USDT)",
            template="plotly_dark",
            height=600
        )
        
        # Create volume chart
        fig_volume = go.Figure()
        fig_volume.add_trace(
            go.Bar(
                x=df['timestamp'],
                y=df['volume'],
                name='Volume',
                marker_color='#17C37B'
            )
        )
        
        fig_volume.update_layout(
            title=f"{selected_pair} Volume Chart",
            xaxis_title="Date",
            yaxis_title="Volume",
            template="plotly_dark",
            height=400
        )
        
        # Display charts
        st.plotly_chart(fig_price, use_container_width=True)
        st.plotly_chart(fig_volume, use_container_width=True)
        
        # Display current stats
        current_price = float(df['close'].iloc[-1])
        price_change = ((current_price - float(df['open'].iloc[0])) / float(df['open'].iloc[0])) * 100
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Current Price", f"${current_price:,.2f}")
        with col2:
            st.metric("Price Change", f"{price_change:.2f}%")
        with col3:
            st.metric("24h Volume", f"{float(df['volume'].sum()):,.0f}")
    
    else:
        st.warning("No data available for the selected time range")

except Exception as e:
    st.error(f"Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Data provided by Crypto.com API")
