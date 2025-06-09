# streamlit_stock_dashboard.py

import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# 페이지 설정
st.set_page_config(page_title="Global Top10 주가 분석", layout="wide")
st.title("📈 글로벌 시가총액 Top10 기업의 최근 1년 주가 변화")

# 티커 목록 정의
top10_tickers = {
    'Apple': 'AAPL',
    'Microsoft': 'MSFT',
    'Saudi Aramco': '2222.SR',
    'Alphabet': 'GOOGL',
    'Amazon': 'AMZN',
    'NVIDIA': 'NVDA',
    'Berkshire Hathaway': 'BRK-B',
    'Meta Platforms': 'META',
    'Tesla': 'TSLA',
    'TSMC': 'TSM'
}

# 선택 옵션
selected_companies = st.multiselect("🔍 비교할 기업을 선택하세요", list(top10_tickers.keys()), default=list(top10_tickers.keys()))

if selected_companies:
    # 기간 설정
    end_date = datetime.today()
    start_date = end_date - timedelta(days=365)

    # 데이터 불러오기
    ticker_list = [top10_tickers[company] for company in selected_companies]
    df = yf.download(ticker_list, start=start_date, end=end_date)['Adj Close']
    
    # 컬럼명 정리
    if isinstance(df, pd.Series):
        df = df.to_frame()
    df.columns = selected_companies
    df = df.ffill()

    # melt for plotly
    df_plot = df.reset_index().melt(id_vars='Date', var_name='기업', value_name='주가')

    # Plotly 시각화
    fig = px.line(df_plot, x="Date", y="주가", color="기업", title="Top10 기업의 최근 1년 주가 변화")
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("최소 한 개의 기업을 선택해주세요.")
