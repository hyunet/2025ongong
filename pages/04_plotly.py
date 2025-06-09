import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="인구 피라미드", layout="wide")
st.title("👥 연령별 인구 피라미드 (Plotly)")

# ✅ 경로를 절대 기준으로 쓰지 않고, pages 폴더 아래에서 직접 불러옴
try:
    df = pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding='cp949')
except FileNotFoundError:
    st.error("❌ 파일이 없습니다. `pages/` 폴더 안에 CSV 파일이 있는지 확인하세요.")
    st.stop()

# 지역 선택
region_list = df['행정구역'].unique() 
selected_region = st.selectbox("🔍 행정구역을 선택하세요", region_list)

# 연령 데이터 추출
age_columns = [col for col in df.columns if '세' in col]
region_row = df[df['행정구역'] == selected_region].iloc[0]
age_data = region_row[age_columns].str.replace(",", "").astype(int)

age_labels = [col.split('_')[-1].replace('세', '').replace('이상', '100+') for col in age_columns]
age_numbers = [int(a.replace('+','')) if '+' not in a else 100 for a in age_labels]

# 슬라이더로 연령 필터
min_age, max_age = st.slider("🎚️ 연령 범위 선택", 0, 100, (0, 100))
filtered = [(a, p) for a, p in zip(age_numbers, age_data) if min_age <= a <= max_age]
ages_filtered, pops_filtered = zip(*filtered)
age_labels_filtered = [f"{a}세" if a != 100 else "100세 이상" for a in ages_filtered]

# Plotly 그래프
fig = px.bar(
    x=pops_filtered,
    y=age_labels_filtered,
    orientation='h',
    title=f"{selected_region} 연령별 인구 분포",
    labels={'x': '인구 수', 'y': '연령대'},
    color=pops_filtered,
    height=700
)
fig.update_layout(yaxis=dict(categoryorder='category ascending'))
st.plotly_chart(fig, use_container_width=True)
