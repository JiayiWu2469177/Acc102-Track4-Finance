import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="ACC102 Financial Analysis Tool", layout="wide")
st.title("📊 ACC102 Listed Company Financial Analysis Tool")

# Load data
df = pd.read_csv("data.csv")

# Data preview
st.subheader("📋 Data Preview")
st.dataframe(df, use_container_width=True)

# ROE comparison chart
st.subheader("📈 Company ROE Comparison")
fig = px.bar(
    df, 
    x="Company", 
    y="ROE", 
    color="ROE", 
    title="Return on Equity (ROE) Comparison Across Companies",
    text_auto=".2%"
)
st.plotly_chart(fig, use_container_width=True)

# Financial metrics explanation
st.subheader("💡 Key Financial Metrics Explanation")
st.markdown("""
- **ROE (Return on Equity)**: Measures how efficiently a company uses shareholders' equity to generate profit. A higher value indicates stronger profitability.
- **Net Profit Margin**: Represents how much net income a company generates per dollar of revenue, reflecting profitability quality and cost control.
""")
