import streamlit as st
import pandas as pd
import plotly.express as px

# 파일 로드 (CP949 인코딩)
gender_file = 'people_gender.csv'
df_gender = pd.read_csv(gender_file, encoding='cp949')

# 지역 선택
region = st.selectbox("지역을 선택하세요", df_gender['행정구역'].unique())

# 연령대 필터링 슬라이더 (0세~100세 이상 기준)
min_age, max_age = st.slider("연령 범위를 선택하세요", 0, 100, (0, 100))

# 연령 관련 컬럼 필터링
male_cols = [col for col in df_gender.columns if '_남_' in col and '세' in col]
female_cols = [col for col in df_gender.columns if '_여_' in col and '세' in col]
ages = [int(col.split('_')[-1].replace('세', '').replace('이상', '100')) for col in male_cols]

# 해당 지역 데이터 선택
df_selected = df_gender[df_gender['행정구역'] == region]

# 남녀 데이터 파싱
male_pop = df_selected[male_cols].iloc[0].str.replace(',', '').astype(int).values
female_pop = df_selected[female_cols].iloc[0].str.replace(',', '').astype(int).values

# 연령 필터링 적용
df_pyramid = pd.DataFrame({
    '연령': ages * 2,
    '인구수': list(male_pop * -1) + list(female_pop),
    '성별': ['남성'] * len(male_pop) + ['여성'] * len(female_pop)
})
df_pyramid = df_pyramid[(df_pyramid['연령'] >= min_age) & (df_pyramid['연령'] <= max_age)]

# 시각화
fig = px.bar(df_pyramid,
             x='인구수',
             y='연령',
             color='성별',
             orientation='h',
             title=f"{region} 인구 피라미드",
             labels={'연령': '연령(세)', '인구수': '인구 수'},
             height=800)

# 한글 폰트 및 축 설정
fig.update_layout(
    font=dict(family="Malgun Gothic"),
    yaxis=dict(categoryorder='category ascending'),
    xaxis=dict(title='인구 수 (음수: 남성, 양수: 여성)')
)

st.plotly_chart(fig)
