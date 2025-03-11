import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler

st.set_page_config(layout="wide")

st.markdown("""
    <style>
        .block-container {
            padding-top: 0px !important;
            padding-bottom: 0px !important;
        }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    data = pd.read_csv("data/QQQM_Data.csv")
    return data

def process_data(data): 
    """
    Process the data to normalize the scores between 0 and 1
    """

    # Drop columns that are not needed
    drop_columns = ["IntradayReturn", "Amount", "IntradayContribution", "YTDContribution", "SharesOutstanding", "Dividend"]

    # Define the scores to normalize
    scoring_columns = ["DividendYield", "PE", "MarketCap", "Volume", "Profit_TTM"]

    # Save a copy of the original data
    df_original = data[["DividendYield", "PE", "MarketCap", "Volume", "Profit_TTM"]]

    scaler = MinMaxScaler()

    # Normalize all scores between 0 and 1
    df_scaled = data.copy()
    df_scaled = df_scaled.drop(drop_columns, axis=1)
    df_scaled[scoring_columns] = scaler.fit_transform(data[scoring_columns])
    df_scaled["PE"] = 1 - df_scaled["PE"]
    df_scaled.rename(columns={"DividendYield": "Income", 
                            "PE": "Pricing", 
                            "MarketCap": "Size", 
                            "Volume": "Liquidity", 
                            "Profit_TTM": "Profit"}, inplace=True)

    processed_data = pd.concat([df_original, df_scaled], axis=1)

    # Change column order
    processed_data = processed_data[["Ticker", "Name", "Sector", "Weight", "Price",
                                     "DividendYield", "PE", "MarketCap", "Volume", "Profit_TTM",
                                     "Income", "Pricing", "Size", "Liquidity", "Profit"]]

    return processed_data

def top_stock_tickers(data, metric="Weight", n=5):
    """
    Get the top n stock tickers based on the metric
    """
    top_n = data.nlargest(n, metric)
    top_n_tickers = top_n["Ticker"].tolist()
    return top_n_tickers

def create_radar_chart(ticker, data, fill_color='rgba(0, 128, 255, 0.4)', line_color='#007BFF'):

    def metric_data(ticker, data):
        """
        Pivot the data to show the scores by ticker
        """
        stock_data = data[data["Ticker"] == ticker]

        # Convert DataFrame to Long Format for Plotly Express
        scoring_columns = ["Income", "Pricing", "Size", "Liquidity", "Profit"]
        
        actual_columns = ["DividendYield", "PE", "MarketCap", "Volume", "Profit_TTM"]

        long_df = pd.DataFrame({
            "Metric": scoring_columns * 1,  # Repeat for each stock if needed
            "Score": stock_data[scoring_columns].values.flatten(),
            "Actual": stock_data[actual_columns].values.flatten(),
        })
        return long_df

    # Create Radar Chart using Plotly Express
    fig = px.line_polar(
        metric_data(ticker, data), 
        r="Score", 
        theta="Metric",
        line_close=True,  # Ensures shape closure
        title=f"{ticker}"
    )

    fig.update_layout(
    autosize=False,
    width = 200,
    height = 200,
    template="plotly_dark"
    )

    fig.update_layout(
        margin=dict(l=40, r=40, t=30, b=40),
        polar=dict(radialaxis=dict(visible=True, tickfont=dict(size=8))),
        font=dict(size=12),
        title = dict(y=0.95)
    )  

    fig.update_traces(
        fill='toself',
        fillcolor=fill_color,
        line=dict(color=line_color, width=2)
    )
    return fig

def create_charts(processed_data, scoring_metric="Weight", n=5):

    tickers = top_stock_tickers(processed_data, scoring_metric, n)
    chart_list = []

    # List of colors
    fill_colors = ["rgba(0, 128, 255, 0.4)", # Cool Blue
                   "rgba(0, 200, 100, 0.4)", # Vibrant Green
                   "rgba(255, 69, 0, 0.4)", # Fiery Red
                   "rgba(255, 140, 0, 0.4)", # Sunset Orange
                   "rgba(138, 43, 226, 0.4)", # Royal Purple
                   "rgba(255, 215, 0, 0.4)", # Golden Yellow
                   "rgba(255, 0, 255, 0.4)", # Magenta Burst
                   "rgba(0, 206, 209, 0.4)", # Teal Ocean
                   "rgba(165, 42, 42, 0.4)", # Autumn Brown
                   "rgba(0, 139, 139, 0.4)"] # Dark Cyan

    # Line colors
    line_colors = ['#007BFF', 
                   '#00C864', 
                   '#FF4500', 
                   '#FF8C00', 
                   '#8A2BE2', 
                   '#FFD700', 
                   '#FF00FF', 
                   '#00CED1', 
                   '#A52A2A', 
                   '#008B8B']

    for i in range(n):
        radar_chart = create_radar_chart(tickers[i], processed_data, fill_color=fill_colors[i], line_color=line_colors[i])
        chart_list.append(radar_chart)
    return chart_list

data_load_state = st.text('Loading data...')
data_load_state.text("Done! (using st.cache_data)")

data = load_data()
processed_data = process_data(data)

# Layout the dashboard

# Sidebar
with st.sidebar:
    st.title('Stock Score Charts')

    # Sector Selection
    sectors = ["All"] + list(processed_data["Sector"].unique())
    sector = st.selectbox('Sector', sectors)
    if sector != 'All':
        processed_data = processed_data[processed_data['Sector'] == sector]
    
    scoring_metrics = ["Weight", "Income", "Pricing", "Size", "Liquidity", "Profit"]
    scoring_metric = st.selectbox('Scoring Metric', scoring_metrics)
    if scoring_metric != 'Weight':
        processed_data = processed_data.sort_values(by=scoring_metric, ascending=False)

# Components
n = min(10, processed_data['Ticker'].count())

charts = create_charts(processed_data, scoring_metric, n=n)

# Radar Charts

col1, col2, col3, col4, col5 = st.columns(5)

avg_dividend_yield = processed_data["DividendYield"].mean()
avg_pe = processed_data["PE"].mean()
avg_market_cap = processed_data["MarketCap"].mean()
avg_volume = processed_data["Volume"].mean()
avg_profit = processed_data["Profit_TTM"].mean()

col1.metric("Avg Dividend Yield", value=f"{avg_dividend_yield * 100:.2f}%")
col2.metric("Avg PE", value=f"{avg_pe:.2f}")
col3.metric("Avg Market Cap", value=f"{avg_market_cap / 1e9:,.2f}B") #in billions
col4.metric("Avg Volume", value=f"{avg_volume / 1e6:,.2f}M") #in millions
col5.metric("Avg Profit", value=f"{avg_profit / 1e9:,.2f}B") #in billions

tab1, tab2 = st.tabs(["Score Cards", "Data"])

with tab1:

    with st.container():
        # Loop through the charts and display in rows of 4
        for i in range(0, len(charts), 4):
            cols = st.columns(4, gap="small")  # Create 4 columns
            for j in range(4):
                if i + j < len(charts):  # Ensure index is within range
                    with cols[j]:  # Assign charts to each column
                        st.plotly_chart(charts[i + j], use_container_width=True)

with tab2:
    st.write(processed_data)