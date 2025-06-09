import streamlit as st
import pandas as pd
import plotly.express as px
import re

# 📁 CSV 불러오기
df_gender = pd.read_csv("people_gender.csv", encoding="cp949")
df_sum = pd.read_csv("people_sum.csv", encoding="cp949")

# 지역 선택
region = st.selectbox("📍 지역을 선택하세요", df_gender['행정구역'].unique())

# 남성/여성 연령별 컬럼
male_cols = [col for col in df_gender.columns if '2025년05월_남_' in col and '세' in col]
female_cols = [col for col in df_gender.columns if '2025년05월_여_' in col and '세' in col]

# 연령 숫자 추출 및 정렬
ages = []
for col in male_cols:
    match = re.search(r'(\d+)', col)
    if match:
        ages.append(int(match.group()))
ages = sorted(set(ages))

# 데이터 부족 예외 처리
if len(ages) < 2:
    st.error("📛 연령 정보가 부족하여 슬라이더를 생성할 수 없습니다.")
    st.stop()

# 슬라이더로 연령대 선택
min_age = min(ages)
max_age = max(ages)
age_range = st.slider("🎚️ 연령 범위를 선택하세요", min_value=min_age, max_value=max_age, value=(min_age, max_age))

# 지역 데이터 추출
row_gender = df_gender[df_gender['행정구역'] == region].iloc[0]
row_sum = df_sum[df_sum['행정구역'] == region].iloc[0]

# 인구수 전처리
male_pop = row_gender[male_cols].str.replace(',', '').astype(int).values
female_pop = row_gender[female_cols].str.replace(',', '').astype(int).values

# 인구 피라미드 데이터프레임
df_pyramid = pd.DataFrame({
    '연령': ages * 2,
    '인구수': list(male_pop * -1) + list(female_pop),
    '성별': ['남성'] * len(male_pop) + ['여성'] * len(female_pop)
})
df_pyramid = df_pyramid[(df_pyramid['연령'] >= age_range[0]) & (df_pyramid['연령'] <= age_range[1])]

# 인구 피라미드 그래프
fig1 = px.bar(
    df_pyramid,
    x='인구수',
    y='연령',
    color='성별',
    orientation='h',
    title=f"{region} 인구 피라미드",
    labels={'연령': '연령(세)', '인구수': '인구 수'},
    height=800
)
fig1.update_layout(
    font=dict(family="Malgun Gothic"),
    yaxis=dict(categoryorder='category ascending')
)
st.plotly_chart(fig1)

# ──────────────────────────────

# 총인구 데이터 준비
sum_cols = [col for col in df_sum.columns if '2025년05월_계_' in col and '세' in col]
sum_ages = []
for col in sum_cols:
    match = re.search(r'(\d+)', col)
    if match:
        sum_ages.append(int(match.group()))
sum_values = row_sum[sum_cols].str.replace(',', '').astype(int).values

df_total = pd.DataFrame({
    '연령': sum_ages,
    '총인구': sum_values
})
df_total = df_total[(df_total['연령'] >= age_range[0]) & (df_total['연령'] <= age_range[1])]

# 총인구 그래프
fig2 = px.bar(
    df_total,
    x='연령',
    y='총인구',
    title=f"{region} 연령별 총인구",
    labels={'연령': '연령(세)', '총인구': '인구 수'}
)
fig2.update_layout(font=dict(family="Malgun Gothic"))
st.plotly_chart(fig2)
