import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
from datetime import datetime, timedelta

# 페이지 설정
st.set_page_config(page_title="📈 글로벌 시가총액 TOP10 주식 트렌드", layout="wide")

st.title("📈 글로벌 시가총액 TOP10 주식 변화 (최근 1년)")
st.markdown("야후 파이낸스 데이터를 기반으로 Plotly 시각화")

# 1. 주식 정보 설정
company_info = {
    'Apple': 'AAPL',
    'Microsoft': 'MSFT',
    'Nvidia': 'NVDA',
    'Amazon': 'AMZN',
    'Alphabet (Google)': 'GOOGL',
    'Berkshire Hathaway': 'BRK-B',
    'Meta': 'META',
    'Eli Lilly': 'LLY',
    'TSMC': 'TSM',
    'Visa': 'V'
}

selected_companies = st.multiselect(
    "비교할 회사를 선택하세요 (2개 이상 추천)",
    list(company_info.keys()),
    default=['Apple', 'Microsoft', 'Nvidia']
)

if not selected_companies:
    st.warning("⛔ 최소 한 개 이상 선택해주세요.")
    st.stop()

# 2. 주식 데이터 수집
ticker_list = [company_info[comp] for comp in selected_companies]
end_date = datetime.today()
start_date = end_date - timedelta(days=365)

# 가져오기
df_raw = yf.download(ticker_list, start=start_date, end=end_date)['Adj Close']

# 단일 종목일 경우 처리
if isinstance(df_raw, pd.Series):
    df_raw = df_raw.to_frame()
    df_raw.columns = [selected_companies[0]]
else:
    df_raw.columns = selected_companies

# 결측치 처리
df_raw = df_raw.ffill()

# 3. 시각화
st.subheader("📊 주가 추이 비교 (Plotly)")
fig = px.line(
    df_raw,
    x=df_raw.index,
    y=df_raw.columns,
    labels={"value": "주가", "index": "날짜"},
    title="최근 1년 간 주가 변화",
    markers=True
)
fig.update_layout(hovermode="x unified")
st.plotly_chart(fig, use_container_width=True)

# 4. 수익률 변동 분석
returns = df_raw.pct_change().dropna()
cumulative_returns = (1 + returns).cumprod() - 1

st.subheader("📈 누적 수익률 비교")
fig2 = px.line(
    cumulative_returns,
    x=cumulative_returns.index,
    y=cumulative_returns.columns,
    labels={"value": "누적 수익률", "index": "날짜"},
    title="최근 1년 누적 수익률 (%)"
)
fig2.update_yaxes(tickformat=".0%")
st.plotly_chart(fig2, use_container_width=True)
