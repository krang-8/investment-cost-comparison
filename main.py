import streamlit as st
import pandas as pd
from calculator import InvestmentCalculator
from stock_utils import get_stock_data, create_stock_chart, calculate_shares, detect_investment_type


def load_css():
    with open("styles.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def format_currency(amount):
    return f"${amount:,.2f}"


def format_percentage(value):
    return f"{value:.2f}%"


def create_cost_bar(cost, max_cost):
    percentage = (cost / max_cost) * 100 if max_cost > 0 else 0
    return f"""
    <div class="cost-bar-container">
        <div class="cost-bar" style="width: {percentage}%"></div>
    </div>
    """


def display_platform_comparison(platform_data, max_cost, amount, all_costs):
    is_best = platform_data["total_cost"] == min(p["total_cost"]
                                                 for p in all_costs)
    cost_percentage = (platform_data["total_cost"] / amount) * 100

    return f"""
    <div class="platform-comparison {'best-option' if is_best else ''}">
        <div class="platform-name">{platform_data['platform']}</div>
        <div class="platform-metrics">
            <div class="metric">
                <div class="metric-label">Total Cost</div>
                <div class="metric-value">{format_currency(platform_data['total_cost'])}</div>
            </div>
            <div class="metric">
                <div class="metric-label">Cost %</div>
                <div class="metric-value">{format_percentage(cost_percentage)}</div>
            </div>
            {create_cost_bar(platform_data['total_cost'], max_cost)}
    """


def main():
    st.set_page_config(page_title="Investment Cost Calculator",
                       page_icon="💰",
                       layout="centered")

    load_css()

    st.title("Investment Cost Calculator")
    st.markdown(
        '<p class="description">Compare investment costs across Wealthsimple and Questrade platforms.</p>',
        unsafe_allow_html=True)

    # Initialize calculator
    calculator = InvestmentCalculator()

    # Initialize session state
    if 'investment_amount' not in st.session_state:
        st.session_state.investment_amount = 1000.0
    if 'stock_price' not in st.session_state:
        st.session_state.stock_price = 0.0

    # Optional stock ticker input
    ticker = st.text_input(
        "Stock Ticker Symbol (optional)",
        help="Enter a stock symbol (e.g., AAPL for Apple Inc.)",
        key="ticker_input").upper()

    # Form inputs
    col1, col2 = st.columns([2, 1])

    with col1:
        default_type = "CAD ETF"
        if ticker:
            default_type = detect_investment_type(ticker)

        investment_type = st.selectbox(
            "Investment Type", ["CAD ETF", "USD ETF", "US STOCK", "CAD STOCK"],
            index=["CAD ETF", "USD ETF", "US STOCK",
                   "CAD STOCK"].index(default_type),
            help="Select the type of investment you want to analyze")

    with col2:
        amount = st.number_input("Investment Amount ($)",
                                 min_value=0.0,
                                 max_value=1000000.0,
                                 value=st.session_state.investment_amount,
                                 step=100.0,
                                 help="Enter the amount you want to invest",
                                 key="amount_input")

    col1, col2 = st.columns(2)
    with col1:
        calculate = st.button("Calculate", use_container_width=True)
    with col2:
        clear = st.button("Clear", use_container_width=True)

    if clear:
        st.session_state.investment_amount = 1000.0
        st.session_state.stock_price = 0.0
        st.experimental_rerun()

    if calculate and amount > 0:
        # Fetch stock data if ticker is provided
        stock_data = None
        if ticker:
            stock_data = get_stock_data(ticker)
            if stock_data:
                st.session_state.stock_price = stock_data['price']

                # Display stock info in a clean card
                with st.container():
                    st.markdown(f"""
                    <div class="stock-info">
                        <h3>{stock_data['name']} ({ticker})</h3>
                        <p class="current-price">Current Price: {format_currency(stock_data['price'])}</p>
                        <p class="currency">Currency: {stock_data['currency']}</p>
                    </div>
                    """,
                                unsafe_allow_html=True)

                # Display stock chart
                st.plotly_chart(create_stock_chart(
                    stock_data['historical_data'], ticker),
                                use_container_width=True)

        # Calculate costs
        ws_costs = calculator.calculate_wealthsimple_costs(
            amount, investment_type)
        qt_regular = calculator.calculate_questrade_regular(
            amount, investment_type)
        qt_norberts = calculator.calculate_questrade_norberts(
            amount, investment_type)

        # Find the platform with minimum cost
        all_costs = [ws_costs, qt_regular]
        if investment_type == "US STOCK":
            all_costs.append(qt_norberts)

        min_cost_platform = min(all_costs, key=lambda x: x["total_cost"])
        max_cost = max(p["total_cost"] for p in all_costs)

        # Display recommendation
        st.markdown("### Investment Summary")
        st.markdown(f"""
        <div class="recommendation-card">
            <h3>💡 Recommended Platform</h3>
            <p>For your {investment_type} investment of {format_currency(amount)}, we recommend using 
            <span class="platform-highlight">{min_cost_platform["platform"]}</span>.</p>
            <p>This option will cost you {format_currency(min_cost_platform["total_cost"])} 
            ({format_percentage(min_cost_platform["total_cost"]/amount * 100)} of your investment).</p>
        </div>
        """,
                    unsafe_allow_html=True)

        # Display platform comparisons
        st.markdown("### Platform Comparison")
        for platform_data in all_costs:
            st.markdown(display_platform_comparison(platform_data, max_cost,
                                                    amount, all_costs),
                        unsafe_allow_html=True)

        # Detailed breakdown
        st.markdown("### Cost Breakdown")
        for platform_data in all_costs:
            with st.expander(f"🔍 {platform_data['platform']} Details"):
                st.markdown(f"""
                <div class="breakdown-section">
                    <div class="breakdown-header">
                        <div class="breakdown-platform">{platform_data["platform"]}</div>
                        <div class="breakdown-total">{format_currency(platform_data["total_cost"])}</div>
                    </div>
                """,
                            unsafe_allow_html=True)

                # Display fees
                if "conversion_fee" in platform_data:
                    st.markdown(f"""
                    <div class="fee-item">
                        <span class="fee-label">Currency Conversion</span>
                        <span class="fee-value">{format_currency(platform_data['conversion_fee'])}</span>
                    </div>
                    """,
                                unsafe_allow_html=True)

                if "commission" in platform_data:
                    st.markdown(f"""
                    <div class="fee-item">
                        <span class="fee-label">Commission</span>
                        <span class="fee-value">{format_currency(platform_data['commission'])}</span>
                    </div>
                    """,
                                unsafe_allow_html=True)

                if "ecn_fees" in platform_data:
                    st.markdown(f"""
                    <div class="fee-item">
                        <span class="fee-label">ECN Fees</span>
                        <span class="fee-value">{format_currency(platform_data['ecn_fees'])}</span>
                    </div>
                    """,
                                unsafe_allow_html=True)

                if st.session_state.stock_price > 0:
                    shares = calculate_shares(amount,
                                              st.session_state.stock_price,
                                              platform_data["total_cost"])
                    st.markdown(f"""
                    <div class="fee-item">
                        <span class="fee-label">Shares You Can Buy</span>
                        <span class="fee-value">{shares:.4f}</span>
                    </div>
                    <div class="fee-item">
                        <span class="fee-label">Total Value After Fees</span>
                        <span class="fee-value">{format_currency(shares * st.session_state.stock_price)}</span>
                    </div>
                    """,
                                unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

                if "note" in platform_data:
                    st.info(platform_data["note"])


if __name__ == "__main__":
    main()
