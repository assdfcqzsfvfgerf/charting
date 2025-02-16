import streamlit as st
import plotly.graph_objects as go
from pycoingecko import CoinGeckoAPI
import pandas as pd
from datetime import datetime, timedelta

# Initialize CoinGecko API
cg = CoinGeckoAPI()

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

# Get list of top 100 cryptocurrencies
try:
    coins_list = cg.get_coins_markets(vs_currency='usd', order='market_cap_desc', per_page=100, sparkline=False)
    coins_dict = {coin['name']: coin['id'] for coin in coins_list}
except:
    st.error("Error fetching cryptocurrency list. Please try again later.")
    st.stop()

# Cryptocurrency selection
selected_coin = st.sidebar.selectbox("Select Cryptocurrency", list(coins_dict.keys()))

# Time range selection
time_ranges = {
    '24 Hours': 1,
    '7 Days': 7,
    '30 Days': 30,
    '90 Days': 90,
    '1 Year': 365
}
selected_range = st.sidebar.selectbox("Select Time Range", list(time_ranges.keys()))

# Fetch historical data
try:
    days = time_ranges[selected_range]
    coin_data = cg.get_coin_market_chart_by_id(
        id=coins_dict[selected_coin],
        vs_currency='usd',
        days=days
    )
    
    # Convert data to DataFrame
    prices_df = pd.DataFrame(coin_data['prices'], columns=['timestamp', 'price'])
    volumes_df = pd.DataFrame(coin_data['total_volumes'], columns=['timestamp', 'volume'])
    
    # Convert timestamp to datetime
    prices_df['timestamp'] = pd.to_datetime(prices_df['timestamp'], unit='ms')
    volumes_df['timestamp'] = pd.to_datetime(volumes_df['timestamp'], unit='ms')
    
    # Create price chart
    fig_price = go.Figure()
    fig_price.add_trace(
        go.Scatter(
            x=prices_df['timestamp'],
            y=prices_df['price'],
            name='Price',
            line=dict(color='#17C37B')
        )
    )
    
    fig_price.update_layout(
        title=f"{selected_coin} Price Chart",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        template="plotly_dark",
        height=600
    )
    
    # Create volume chart
    fig_volume = go.Figure()
    fig_volume.add_trace(
        go.Bar(
            x=volumes_df['timestamp'],
            y=volumes_df['volume'],
            name='Volume',
            marker_color='#17C37B'
        )
    )
    
    fig_volume.update_layout(
        title=f"{selected_coin} Volume Chart",
        xaxis_title="Date",
        yaxis_title="Volume (USD)",
        template="plotly_dark",
        height=400
    )
    
    # Display charts
    st.plotly_chart(fig_price, use_container_width=True)
    st.plotly_chart(fig_volume, use_container_width=True)
    
    # Display current stats
    current_price = prices_df['price'].iloc[-1]
    price_change = ((current_price - prices_df['price'].iloc[0]) / prices_df['price'].iloc[0]) * 100
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current Price", f"${current_price:,.2f}")
    with col2:
        st.metric("Price Change", f"{price_change:.2f}%")
    with col3:
        st.metric("24h Volume", f"${volumes_df['volume'].iloc[-1]:,.0f}")

except Exception as e:
    st.error(f"Error fetching data: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Data provided by CoinGecko API")
