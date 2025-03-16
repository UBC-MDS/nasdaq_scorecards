# 📈 Nasdaq100 Scorecard Dashboard  
Author/Developer: Jason Lee

Interactive Streamlit app that ranks and visualizes the top 10 Nasdaq 100 stocks based on fundamental metrics like income, pricing, size, liquidity, and profit, helping investors make data-driven decisions.

## Motivation  

In today's digital age, mobile trading apps have made stock trading more accessible than ever. However, this ease of access has also gamified the experience, leading many investors to focus more on short-term price movements rather than the underlying fundamentals of the companies they invest in. This dashboard was created to encourage a more long-term, fundamentals-driven approach to investing. 

The dashboard provides a structured way to evaluate companies beyond just price action.  

## App Description

### Score Cards
To quantify key aspects of a stock's fundamentals, I developed a **scoring system** based on five core financial metrics. By visualizing these metrics using **radar charts**, the dashboard allows investors to quickly compare stocks and make more informed, data-driven decisions.   

1. **Income** – Derived from the stock's **dividend yield**, representing income-generating potential.  
2. **Price** – Based on the **P/E ratio**, reflecting how expensive the stock is relative to earnings.  
3. **Size** – Measured by **market capitalization**, indicating the company's overall valuation.  
4. **Liquidity** – Assessed using **trading volume**, representing how easily the stock can be bought or sold.  
5. **Profit** – Evaluated based on the company's **trailing 12-month profit**, showing overall profitability.  

### Clustering

The **Clustering** tab provides an **unsupervised learning analysis** of Nasdaq 100 stocks using **DBSCAN (Density-Based Spatial Clustering of Applications with Noise)**. This method is used to identify natural groupings of stocks based on fundamental features such as income, pricing, size, liquidity, and profit.

### PCA 2D Projection  

To visualize the clustering, **Principal Component Analysis (PCA)** is used to reduce the dimensionality of the 5 scoring metrics to **two principal components (PC1 and PC2)**. In doing so, a **2D scatter plot** can be used for intuitive exploration.  

### DBSCAN Clustering  

We use **DBSCAN** to group stocks based on their fundamental characteristics. Unlike K-Means, DBSCAN does not require specifying the number of clusters beforehand and is effective at identifying **outliers** in the data.

- **Cluster 0 (Red):** Stocks that exhibit dominant financial characteristics, likely **mega-cap tech companies** such as Apple (AAPL), Microsoft (MSFT), and NVIDIA (NVDA).  
- **Cluster 1 (Blue):** Other stocks that exhibit varying degrees of financial performance but do not strongly match the profile of the high-performing cluster.  
- **Outliers:** DBSCAN may label some points as noise if they do not belong to any cluster, indicating unique stocks that do not fit within the dominant groups.  


## Features  

- **Filter stocks by sector** to focus on industries of interest.  
- **Choose different scoring metrics** to analyze stocks from multiple perspectives.  
- **Interactive charts** to compare top NASDAQ stocks side by side.  
- **Summary statistics** for a quick snapshot of market trends.  

This tool aims to shift the focus away from speculative trading and back toward **fundamental investing**, helping investors build a portfolio with long-term sustainability in mind. 

## Installation  

To set up and run the dashboard locally, follow these steps:  

### 1. Clone the repository  
```bash
git clone https://github.com/UBC-MDS/nasdaq_scorecards.git
cd nasdaq_scorecards
```
### 2. Create and activate a conda environment 
```bash
conda create --name nasdaq_scorecard python=3.12 -y
conda activate nasdaq_scorecard
```

### 3. Install [dependencies](https://github.com/UBC-MDS/nasdaq_scorecards/blob/main/requirements.txt)
```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit app
```bash
streamlit run app.py
```
 

