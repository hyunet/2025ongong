import streamlit as st
import pandas as pd
import plotly.express as px
import re

# 파일 경로 설정 (예: 상위 폴더에 data 폴더가 있을 경우)
gender_file = '../data/people_gender.csv'

# CSV 읽기 (CP949 인코딩)
df_gender = pd.read_csv(gender_file, encoding='cp949')

# 지역 선택
region = st.selectbox("📍 지역을 선택하세요", df_gender['행정구역'].unique())

# 남성/여성 컬럼 추출
male_cols = [col for col in df_gender.columns if '_남_' in col and '세' in col]
female_cols = [col for col in df_gender.columns if '_여_' in col and '세' in col]

# 연령 정보 추출 (정규표현식 사용으로 안정성 확보)
ages = [int(re.search(r'\d+', col).group()) for col in male_cols]

# 연령 범위 슬라이더
min_age, max_age = st.slider("🎚️ 연령 범위를 선택하세요", min(ages), max(ages), (min(ages), max(ages)))

# 선택한 지역 데이터 추출
df_selected = df_gender[df_gender['행정구역'] == region]

# 남성, 여성 인구 수 배열
male_pop = df_selected[male_cols].iloc[0].str.replace(',', '').astype(int).values
female_pop = df_selected[female_cols].iloc[0].str.replace(',', '').astype(int).values

# 데이터프레임 생성
df_pyramid = pd.DataFrame({
    '연령': ages * 2,
    '인구수': list(male_pop * -1) + list(female_pop),
    '성별': ['남성'] * len(male_pop) + ['여성'] * len(female_pop)
})

# 연령 필터링
df_pyramid = df_pyramid[(df_pyramid['연령'] >= min_age) & (df_pyramid['연령'] <= max_age)]

# 시각화 (Plotly)
fig = px.bar(df_pyramid,
             x='인구수',
             y='연령',
             color='성별',
             orientation='h',
             title=f"📊 {region} 인구 피라미드",
             labels={'연령': '연령(세)', '인구수': '인구 수'},
             height=800)

fig.update_layout(
    font=dict(family="Malgun Gothic"),  # 윈도우 환경 기준 한글 폰트
    yaxis=dict(categoryorder='category ascending'),
    xaxis=dict(title='인구 수 (음수: 남성, 양수: 여성)')
)

st.plotly_chart(fig)
