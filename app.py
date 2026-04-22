import streamlit as st
import pandas as pd
import plotly.express as px

# 页面基础配置
st.set_page_config(
    page_title="ACC102 Financial Analysis Tool",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 页面标题
st.title("📊 ACC102 Listed Company Financial Analysis Tool")
st.markdown("Interactive dashboard for analyzing key financial metrics of listed companies.")

# -------------------------- 侧边栏交互区 --------------------------
st.sidebar.header("⚙️ Control Panel")

# 1. 数据上传/加载
st.sidebar.subheader("1. Data Source")
uploaded_file = st.sidebar.file_uploader("Upload your financial data (CSV)", type=["csv"])

# 2. 年份筛选
st.sidebar.subheader("2. Filter Options")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    # 加载示例数据
    df = pd.DataFrame({
        "Year": [2023, 2023, 2023, 2023, 2023],
        "Company": ["SPD Bank", "CMB", "Ping An Insurance", "Zijin Mining", "Ping An Bank"],
        "ROE": [0.112, 0.168, 0.089, 0.125, 0.097],
        "NetProfitMargin": [0.352, 0.391, 0.128, 0.156, 0.324]
    })

# 年份筛选器（互动点1：下拉选年份）
if "Year" in df.columns:
    selected_year = st.sidebar.selectbox("Select Year", sorted(df["Year"].unique(), reverse=True))
    filtered_df = df[df["Year"] == selected_year]
else:
    filtered_df = df

# 指标选择器（互动点2：多选指标）
selected_metrics = st.sidebar.multiselect(
    "Select Metrics to Display",
    ["ROE", "NetProfitMargin"],
    default=["ROE", "NetProfitMargin"]
)

# -------------------------- 主页面互动内容 --------------------------
# 1. 数据预览（随筛选动态变化）
st.subheader("📋 Data Preview (Filtered)")
st.dataframe(filtered_df[["Company"] + selected_metrics], use_container_width=True)

# 2. 动态柱状图（随筛选变化）
if "ROE" in selected_metrics:
    st.subheader("📈 Company ROE Comparison (Interactive)")
    fig = px.bar(
        filtered_df,
        x="Company",
        y="ROE",
        color="ROE",
        title=f"Return on Equity (ROE) - {selected_year}",
        text_auto=".2%"
    )
    st.plotly_chart(fig, use_container_width=True)

# 3. 动态散点图（多指标联动）
if len(selected_metrics) >= 2:
    st.subheader("🔗 Correlation Analysis (Interactive)")
    fig2 = px.scatter(
        filtered_df,
        x=selected_metrics[0],
        y=selected_metrics[1],
        hover_data=["Company"],
        title=f"{selected_metrics[0]} vs {selected_metrics[1]} Correlation"
    )
    st.plotly_chart(fig2, use_container_width=True)

# 4. 财务指标解读
st.subheader("💡 Key Financial Metrics Explanation")
st.markdown("""
- **ROE (Return on Equity)**: Measures how efficiently a company uses shareholders' equity to generate profit.
- **Net Profit Margin**: Represents how much net income a company generates per dollar of revenue.
""")

# 页脚
st.divider()
st.caption("ACC102 Course Assignment | Streamlit Interactive Dashboard")
