import streamlit as st
import pandas as pd
import plotly.express as px
import re

# 📁 CSV 파일 불러오기 (CP949 인코딩)
df_gender = pd.read_csv('people_gender.csv', encoding='cp949')
df_sum = pd.read_csv('people_sum.csv', encoding='cp949')

# 📍 지역 선택
region = st.selectbox("📍 지역을 선택하세요", df_gender['행정구역'].unique())

# 👨‍👩‍👧‍👦 연령 관련 컬럼 추출
male_cols = [col for col in df_gender.columns if '_남_' in col and '세' in col]
female_cols = [col for col in df_gender.columns if '_여_' in col and '세' in col]

# 🔢 연령 숫자 추출 후 중복 제거 + 정렬
ages_raw = []
for col in male_cols:
    match = re.search(r'\d+', col)
    if match:
        ages_raw.append(int(match.group()))
ages = sorted(set(ages_raw))

# 🚫 연령 데이터가 충분하지 않으면 중단
if len(ages) < 2:
    st.error("연령 정보가 부족하여 슬라이더를 생성할 수 없습니다.")
    st.stop()

# 🎚️ 슬라이더 안전 설정 (value가 min과 max 사이에서 반드시 유효하게)
min_age_value = ages[0]
max_age_value = ages[-1]
age_range = st.slider(
    "🎚️ 연령 범위를 선택하세요",
    min_value=min_age_value,
    max_value=max_age_value,
    value=(min_age_value, max_age_value)
)

# 📌 선택된 지역 행 추출
row_gender = df_gender[df_gender['행정구역'] == region].iloc[0]
row_sum = df_sum[df_sum['행정구역'] == region].iloc[0]

# 👥 남/여 인구 수 파싱
male_pop = row_gender[male_cols].str.replace(',', '').astype(int).values
female_pop = row_gender[female_cols].str.replace(',', '').astype(int).values

# 📊 인구 피라미드용 DataFrame 생성
df_pyramid = pd.DataFrame({
    '연령': ages * 2,
    '인구수': list(male_pop * -1) + list(female_pop),
    '성별': ['남성'] * len(male_pop) + ['여성'] * len(female_pop)
})
df_pyramid = df_pyramid[(df_pyramid['연령'] >= age_range[0]) & (df_pyramid['연령'] <= age_range[1])]

# 📈 인구 피라미드 시각화
fig1 = px.bar(
    df_pyramid,
    x='인구수',
    y='연령',
    color='성별',
    orientation='h',
    title=f"📊 {region} 인구 피라미드",
    labels={'연령': '연령(세)', '인구수': '인구 수'},
    height=800
)
fig1.update_layout(
    font=dict(family="Malgun Gothic"),
    yaxis=dict(categoryorder='category ascending'),
    xaxis=dict(title='인구 수 (음수: 남성, 양수: 여성)')
)
st.plotly_chart(fig1)

# ─────────────────────────────────────────────

# 📦 people_sum 기반 총인구 시각화
sum_cols = [col for col in df_sum.columns if '_계_' in col and '세' in col]
sum_ages = []
for col in sum_cols:
    match = re.search(r'\d+', col)
    if match:
        sum_ages.append(int(match.group()))
sum_values = row_sum[sum_cols].str.replace(',', '').astype(int).values
