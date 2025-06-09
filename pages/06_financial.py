import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# 🏢 시가총액 상위 10대 글로벌 기업
company_dict = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Saudi Aramco": "2222.SR",
    "Alphabet (Google)": "GOOGL",
    "Amazon": "AMZN",
    "NVIDIA": "NVDA",
    "Berkshire Hathaway": "BRK-B",
    "Meta (Facebook)": "META",
    "TSMC": "TSM",
    "Tesla": "TSLA"
}

# ✅ 기업 선택
selected_companies = st.multiselect(
    "📈 기업을 선택하세요 (복수 선택 가능)",
    options=list(company_dict.keys()),
    default=["Apple", "Microsoft"]
)

if not selected_companies:
    st.warning("⚠️ 최소 하나 이상의 기업을 선택해 주세요.")
    st.stop()

# 🗓️ 1년치 데이터 불러오기
end_date = pd.Timestamp.today()
start_date = end_date - pd.DateOffset(years=1)

symbols = [company_dict[company] for company in selected_companies]

# 📦 주가 데이터 불러오기
@st.cache_data
def load_data(tickers):
    data = yf.download(tickers, start=start_date, end=end_date)["Adj Close"]
    return data

try:
    price_df = load_data(symbols)

    # ✅ 단일 선택 시 DataFrame 구조 정리
    if isinstance(price_df, pd.Series):
        price_df = price_df.to_frame(name=symbols[0])

    # 📉 선 그래프: 주가 추이
    st.subheader("📉 최근 1년 주가 추이")
    fig_price = px.line(
        price_df,
        x=price_df.index,
        y=price_df.columns,
        labels={"value": "주가 (USD)", "variable": "기업"},
        title="최근 1년간 주가 변화"
    )
    fig_price.update_layout(font=dict(family="Malgun Gothic"), xaxis_title="날짜")
    st.plotly_chart(fig_price, use_container_width=True)

    # 📈 누적 수익률 계산
    st.subheader("📊 누적 수익률 (%)")
    cum_return = (price_df / price_df.iloc[0] - 1) * 100

    fig_return = px.line(
        cum_return,
        x=cum_return.index,
        y=cum_return.columns,
        labels={"value": "누적 수익률 (%)", "variable": "기업"},
        title="최근 1년간 누적 수익률"
    )
    fig_return.update_layout(font=dict(family="Malgun Gothic"), xaxis_title="날짜")
    st.plotly_chart(fig_return, use_container_width=True)

except Exception as e:
    st.error(f"❌ 데이터를 불러오거나 시각화하는 중 오류가 발생했습니다: {e}")
