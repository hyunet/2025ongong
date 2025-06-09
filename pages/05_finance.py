import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# 1. 페이지 기본 설정
st.set_page_config(page_title="📈 글로벌 Top10 주가 분석", layout="wide")
st.title("🌍 글로벌 시가총액 Top10 기업 주가 분석")

# 2. 종목 리스트 설정 (티커: yfinance 기준)
company_dict = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Alphabet (Google)": "GOOGL",
    "Amazon": "AMZN",
    "NVIDIA": "NVDA",
    "Meta (Facebook)": "META",
    "Berkshire Hathaway": "BRK-B",
    "TSMC": "TSM",
    "Eli Lilly": "LLY",
    "Tesla": "TSLA"
}
company_names = list(company_dict.keys())
tickers = list(company_dict.values())

# 3. 사용자 선택 위젯
selected_names = st.multiselect("✅ 기업 선택", company_names, default=company_names[:5])
selected_tickers = [company_dict[name] for name in selected_names]

# 4. 날짜 설정
today = datetime.today()
one_year_ago = today - timedelta(days=365)

# 5. 데이터 다운로드
with st.spinner("📥 데이터를 불러오는 중입니다..."):
    data = yf.download(selected_tickers, start=one_year_ago, end=today)

# 6. 데이터 정리
# 단일 선택 시: Series -> DataFrame 변환
if isinstance(data.columns, pd.MultiIndex):
    if 'Adj Close' in data.columns.levels[0]:
        df = data['Adj Close'].copy()
    else:
        st.error("❌ 'Adj Close' 데이터가 존재하지 않습니다.")
        st.stop()
else:
    df = data.copy()
    df.columns = [selected_names[0]]  # 단일 선택일 경우 이름 지정

df = df.ffill()  # 결측값 보간

# 7. 시각화: 선 그래프
st.subheader("📊 주가 변화 추이 (1년간)")
fig1 = px.line(df, x=df.index, y=df.columns, labels={"value": "주가 ($)", "variable": "기업"}, height=500)
fig1.update_layout(legend_title_text="기업명")
st.plotly_chart(fig1, use_container_width=True)

# 8. 누적 수익률 계산
returns = (df / df.iloc[0] - 1) * 100
st.subheader("📈 누적 수익률 변화 (%)")
fig2 = px.line(returns, x=returns.index, y=returns.columns, labels={"value": "누적 수익률 (%)", "variable": "기업"}, height=500)
fig2.update_layout(legend_title_text="기업명")
st.plotly_chart(fig2, use_container_width=True)

# 9. 최근 수익률 표
st.subheader("📋 최근 누적 수익률 비교")
latest_returns = returns.iloc[-1].sort_values(ascending=False).round(2)
st.dataframe(latest_returns.to_frame(name="수익률 (%)"))

# 10. 피드백
st.success("✅ 분석 완료! 기업 선택을 변경해보며 비교해보세요.")
