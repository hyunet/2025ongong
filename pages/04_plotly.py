import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="인구 피라미드", layout="wide")
st.title("👥 연령별 인구 피라미드 (Plotly)")

# CSV 파일 불러오기
df = pd.read_csv("../202505_202505_연령별인구현황_월간.csv", encoding='cp949')
'''
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, encoding='cp949')
'''


# 지역 선택
region_list = df['행정구역'].unique()
selected_region = st.selectbox("🔍 행정구역을 선택하세요", region_list)

# 연령 관련 컬럼 추출
age_columns = [col for col in df.columns if '세' in col]
region_row = df[df['행정구역'] == selected_region].iloc[0]
age_data = region_row[age_columns].str.replace(",", "").astype(int)

# 연령 숫자 추출 및 정리
age_labels = [col.split('_')[-1].replace('세', '').replace('이상', '100+') for col in age_columns]
age_numbers = [int(label.replace('+', '')) if '+' not in label else 100 for label in age_labels]

# 연령 슬라이더
min_age, max_age = st.slider("🎚️ 연령 범위를 선택하세요", 0, 100, (0, 100))

# 필터링
filtered_data = [(age, pop) for age, pop in zip(age_numbers, age_data) if min_age <= age <= max_age]
ages_filtered, pops_filtered = zip(*filtered_data)
age_labels_filtered = [f"{a}세" if a != 100 else "100세 이상" for a in ages_filtered]

# Plotly 시각화
fig = px.bar(
    x=pops_filtered,
    y=age_labels_filtered,
    orientation='h',
    labels={'x': '인구 수', 'y': '연령대'},
    title=f"{selected_region} 연령별 인구 분포 (Plotly 시각화)",
    color=pops_filtered,
    height=700
)

fig.update_layout(yaxis=dict(categoryorder='category ascending'))  # 낮은 나이 위쪽
st.plotly_chart(fig, use_container_width=True)
