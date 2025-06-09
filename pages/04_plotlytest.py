import streamlit as st
import pandas as pd
import plotly.express as px
import re

# 데이터 불러오기
df_gender = pd.read_csv('people_gender.csv', encoding='cp949')
df_sum = pd.read_csv('people_sum.csv', encoding='cp949')

# 지역 선택
region = st.selectbox("📍 지역을 선택하세요", df_gender['행정구역'].unique())

# 남/여 컬럼 분리
male_cols = [col for col in df_gender.columns if '_남_' in col and '세' in col]
female_cols = [col for col in df_gender.columns if '_여_' in col and '세' in col]

# 연령 숫자 추출 및 정리
ages_raw = []
for col in male_cols:
    match = re.search(r'\d+', col)
    if match:
        ages_raw.append(int(match.group()))
ages = sorted(set(ages_raw))

# ▶ 예외 처리: ages가 비어있을 경우 슬라이더 막기
if not ages:
    st.error("연령 데이터를 찾을 수 없습니다.")
    st.stop()

# 슬라이더 범위 설정
min_age_value = min(ages)
max_age_value = max(ages)
age_range = st.slider("🎚️ 연령 범위를 선택하세요", 
                      min_value=min_age_value, 
                      max_value=max_age_value, 
                      value=(min_age_value, max_age_value))

# 지역 데이터 선택
row_gender = df_gender[df_gender['행정구역'] == region].iloc[0]
row_sum = df_sum[df_sum['행정구역'] == region].iloc[0]

# 남/여 인구수 처리
male_pop = row_gender[male_cols].str.replace(',', '').astype(int).values
female_pop = row_gender[female_cols].str.replace(',', '').astype(int).values

# 피라미드 데이터 생성
df_pyramid = pd.DataFrame({
    '연령': ages * 2,
    '인구수': list(male_pop * -1) + list(female_pop),
    '성별': ['남성'] * len(male_pop) + ['여성'] * len(female_pop)
})
df_pyramid = df_pyramid[(df_pyramid['연령'] >= age_range[0]) & (df_pyramid['연령'] <= age_range[1])]

# 인구 피라미드 시각화
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
    yaxis=dict(categoryorder='category ascending'),
    xaxis=dict(title='인구 수 (음수: 남성, 양수: 여성)')
)
st.plotly_chart(fig1)

# 총인구 시각화
sum_cols = [col for col in df_sum.columns if '_계_' in col and '세' in col]
sum_ages = [int(re.search(r'\d+', col).group()) for col in sum_cols]
sum_values = row_sum[sum_cols].str.replace(',', '').astype(int).values

df_total = pd.DataFrame({
    '연령': sum_ages,
    '총인구': sum_values
})
df_total = df_total[(df_total['연령'] >= age_range[0]) & (df_total['연령'] <= age_range[1])]

fig2 = px.bar(
    df_total,
    x='연령',
    y='총인구',
    title=f"{region} 연령별 총인구 분포",
    labels={'연령': '연령(세)', '총인구': '인구 수'}
)
fig2.update_layout(font=dict(family="Malgun Gothic"))
st.plotly_chart(fig2)
