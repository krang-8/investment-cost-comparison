import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta
import streamlit as st

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_stock_data(ticker: str):
    """Fetch stock data and return current price and historical data"""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        # Try different price attributes
        current_price = (
            info.get('currentPrice') or 
            info.get('regularMarketPrice') or 
            info.get('previousClose')
        )

        if not current_price:
            st.error(f"Could not fetch price for {ticker}. Please try again.")
            return None

        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)

        # Get historical data
        hist_data = stock.history(start=start_date, end=end_date, interval='1d')
        if hist_data.empty:
            st.error(f"Could not fetch historical data for {ticker}")
            return None

        # Get currency and name with fallbacks
        currency = info.get('currency', 'USD')
        name = info.get('longName', ticker.upper())

        return {
            'price': current_price,
            'historical_data': hist_data,
            'currency': currency,
            'name': name
        }
    except Exception as e:
        st.error(f"Error fetching stock data for {ticker}: {str(e)}")
        st.info("Please verify the ticker symbol and try again.")
        return None

def create_stock_chart(historical_data, ticker: str):
    """Create a candlestick chart using plotly"""
    fig = go.Figure(data=[go.Candlestick(
        x=historical_data.index,
        open=historical_data['Open'],
        high=historical_data['High'],
        low=historical_data['Low'],
        close=historical_data['Close'],
        name=ticker.upper()
    )])

    fig.update_layout(
        title=f'{ticker.upper()} - 30 Day Price History',
        yaxis_title='Price',
        template='plotly_white',
        height=400,
        margin=dict(l=0, r=0, t=40, b=0)
    )

    return fig

def calculate_shares(amount: float, price: float, total_fees: float):
    """Calculate number of shares that can be purchased after fees"""
    available_amount = amount - total_fees
    if price <= 0:
        return 0
    return available_amount / price

def detect_investment_type(ticker: str) -> str:
    """Detect the investment type based on the ticker symbol"""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        # Check if it's an ETF
        if info.get('quoteType', '').upper() == 'ETF':
            # Check currency to determine if it's CAD or USD
            currency = info.get('currency', 'USD')
            return 'CAD ETF' if currency == 'CAD' else 'USD ETF'
        else:
            # For stocks, check the primary exchange
            exchange = info.get('exchange', '').upper()
            currency = info.get('currency', 'USD')

            if currency == 'CAD' or exchange in ['TSX', 'TSXV', 'NEO']:
                return 'CAD STOCK'
            return 'US STOCK'

    except Exception:
        # Default to US STOCK if we can't determine
        return 'US STOCK'