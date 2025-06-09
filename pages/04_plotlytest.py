import streamlit as st
import pandas as pd
import plotly.express as px
import re

# CP949 인코딩된 CSV 파일 불러오기
df_gender = pd.read_csv('people_gender.csv', encoding='cp949')
df_sum = pd.read_csv('people_sum.csv', encoding='cp949')

# ▶ 지역 선택
region = st.selectbox("📍 지역을 선택하세요", df_gender['행정구역'].unique())

# ▶ 연령 컬럼 추출
male_cols = [col for col in df_gender.columns if '_남_' in col and '세' in col]
female_cols = [col for col in df_gender.columns if '_여_' in col and '세' in col]

# ▶ 연령 값 추출 (예: '0세', '1세', '100세 이상' → 숫자만 추출)
ages = [int(re.search(r'\d+', col).group()) for col in male_cols]

# ▶ 연령대 필터링 슬라이더
min_age, max_age = st.slider("🎚️ 연령 범위를 선택하세요", min(ages), max(ages), (min(ages), max(ages)))

# ▶ 선택한 지역 데이터 추출
row_gender = df_gender[df_gender['행정구역'] == region].iloc[0]
row_sum = df_sum[df_sum['행정구역'] == region].iloc[0]

# ▶ 인구수 전처리
male_pop = row_gender[male_cols].str.replace(',', '').astype(int).values
female_pop = row_gender[female_cols].str.replace(',', '').astype(int).values

# ▶ 인구 피라미드용 데이터프레임 생성
df_pyramid = pd.DataFrame({
    '연령': ages * 2,
    '인구수': list(male_pop * -1) + list(female_pop),
    '성별': ['남성'] * len(male_pop) + ['여성'] * len(female_pop)
})

# ▶ 연령 필터링 적용
df_pyramid = df_pyramid[(df_pyramid['연령'] >= min_age) & (df_pyramid['연령'] <= max_age)]

# ▶ 인구 피라미드 시각화
fig1 = px.bar(df_pyramid,
             x='인구수',
             y='연령',
             color='성별',
             orientation='h',
             title=f"📊 {region} 인구 피라미드",
             labels={'연령': '연령(세)', '인구수': '인구 수'},
             height=800)

fig1.update_layout(
    font=dict(family="Malgun Gothic"),  # 한글 폰트
    yaxis=dict(categoryorder='category ascending'),
    xaxis=dict(title='인구 수 (음수: 남성, 양수: 여성)')
)

st.plotly_chart(fig1)

# ──────────────────────────────

# ▶ 총인구 연령별 분포 시각화 (people_sum 활용)
sum_cols = [col for col in df_sum.columns if '_계_' in col and '세' in col]
sum_ages = [int(re.search(r'\d+', col).group()) for col in sum_cols]
sum_values = row_sum[sum_cols].str.replace(',', '').astype(int).values

df_total = pd.DataFrame({
    '연령': sum_ages,
    '총인구': sum_values
})
df_total = df_total[(df_total['연령'] >= min_age) & (df_total['연령'] <= max_age)]

# ▶ 총인구 그래프
fig2 = px.bar(df_total,
              x='연령',
              y='총인구',
              title=f"📈 {region} 연령별 총인구 분포",
              labels={'연령': '연령(세)', '총인구': '인구 수'})

fig2.update_layout(font=dict(family="Malgun Gothic"))

st.plotly_chart(fig2)
