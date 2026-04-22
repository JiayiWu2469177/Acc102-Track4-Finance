import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 页面基础配置
st.set_page_config(
    page_title="ACC102 Financial Analysis Tool",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 页面标题
st.title("📊 ACC102 Listed Company Financial Analysis Tool")
st.markdown("Interactive dashboard for analyzing financial performance trends over time.")

# -------------------------- 侧边栏交互区 --------------------------
st.sidebar.header("⚙️ Control Panel")

# 1. 数据上传/加载
st.sidebar.subheader("1. Data Source")
uploaded_file = st.sidebar.file_uploader("Upload your financial data (CSV)", type=["csv"])

# 加载数据逻辑
if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    # 加载示例数据（已经写死了 2021-2023 三年数据）
    df = pd.DataFrame({
        "Year": [2021, 2021, 2021, 2021, 2021, 2022, 2022, 2022, 2022, 2022, 2023, 2023, 2023, 2023, 2023],
        "Company": ["SPD Bank", "CMB", "Ping An Insurance", "Zijin Mining", "Ping An Bank"] * 3,
        "ROE": [0.105, 0.152, 0.081, 0.118, 0.091, 0.108, 0.161, 0.085, 0.121, 0.094, 0.112, 0.168, 0.089, 0.125, 0.097],
        "NetProfitMargin": [0.345, 0.382, 0.119, 0.149, 0.318, 0.348, 0.387, 0.123, 0.152, 0.321, 0.352, 0.391, 0.128, 0.156, 0.324]
    })

# 2. 年份筛选
st.sidebar.subheader("2. Filter Options")
if "Year" in df.columns:
    selected_year = st.sidebar.selectbox("Select Year", sorted(df["Year"].unique(), reverse=True))
    filtered_df = df[df["Year"] == selected_year]
else:
    filtered_df = df

# 3. 指标选择
selected_metrics = st.sidebar.multiselect(
    "Select Metrics to Display",
    ["ROE", "NetProfitMargin"],
    default=["ROE"]
)

# -------------------------- 主页面内容 --------------------------

# 1. 数据预览
st.subheader(f"📋 Data Preview for {selected_year}")
st.dataframe(filtered_df[["Company"] + selected_metrics], use_container_width=True)

# 2. 年度横向对比图表（动态）
if "ROE" in selected_metrics:
    st.subheader(f"📈 ROE Comparison in {selected_year}")
    fig_roe = px.bar(
        filtered_df,
        x="Company",
        y="ROE",
        color="ROE",
        title=f"Return on Equity (ROE) - {selected_year}",
        text_auto=".2%"
    )
    st.plotly_chart(fig_roe, use_container_width=True)

# 3. 🌟 新增：年份趋势图（加分项！）
st.subheader("📉 Historical Trend Analysis (2021-2023)")
st.markdown("See how ROE has changed over the past 3 years for each company:")

# 创建多子图趋势图
fig_trend = px.line(
    df,
    x="Year",
    y="ROE",
    color="Company",
    markers=True,
    title="ROE Trend Over Time",
    labels={"ROE": "Return on Equity"}
)
# 添加样式
fig_trend.update_layout(
    xaxis=dict(tickmode='array', tickvals=[2021, 2022, 2023]),
    yaxis=dict(tickformat=".0%"),
    hovermode="x unified"
)
st.plotly_chart(fig_trend, use_container_width=True)

# 4. 指标解读
st.subheader("💡 Key Financial Metrics")
st.markdown("""
- **ROE (Return on Equity)**: Measures how efficiently a company uses shareholders' equity to generate profit.
- **Net Profit Margin**: Represents how much net income a company generates per dollar of revenue.
""")
