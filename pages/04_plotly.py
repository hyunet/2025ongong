import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="인구 피라미드", layout="wide")
st.title("👥 연령별 인구 피라미드 (Plotly)")

# 파일 경로 설정 (현재 파일 기준으로 동일 폴더에 있다고 가정)
file_path = os.path.join(os.path.dirname(__file__), "202505_202505_연령별인구현황_월간.csv")

# CSV 파일 불러오기
try:
    df = pd.read_csv(file_path, encoding='cp949')
except FileNotFoundError:
    st.error("❌ 인구 통계 CSV 파일을 찾을 수 없습니다. `pages/` 폴더에 파일이 존재하는지 확인하세요.")
    st.stop()
except UnicodeDecodeError:
    df = pd.read_csv(file_path, encoding='utf-8-sig')

# 지역 선택
region_list = df['행정구역'].unique()
selected_region = st.selectbox("🔍 행정구역을 선택하세요", region_list)

# 연령 컬럼 추출 및 값 정리
age_columns = [col for col in df.columns if '세' in col]
region_row = df[df['행정구역'] == selected_region].iloc[0]
age_data = region_row[age_columns].str.replace(",", "").astype(int)

# 연령 레이블 처리
age_labels = [col.split('_')[-1].replace('세', '').replace('이상', '100+') for col in age_columns]
age_numbers = [int(label.replace('+', '')) if '+' not in label else 100 for label in age_labels]

# 연령 범위 선택 슬라이더
min_age, max_age = st.slider("🎚️ 연령 범위를 선택하세요", 0, 100, (0, 100))

# 필터링
filtered_data = [(age, pop) for age, pop in zip(age_numbers, age_data) if min_age <= age <= max_age]
ages_filtered, pops_filtered = zip(*filtered_data)
age_labels_filtered = [f"{a}세" if a != 100 else "100세 이상" for a in ages_filtered]

# 시각화 (Plotly)
fig = px.bar(
    x=pops_filtered,
    y=age_labels_filtered,
    orientation='h',
    labels={'x': '인구 수', 'y': '연령대'},
    title=f"{selected_region} 연령별 인구 분포",
    color=pops_filtered,
    height=700
)

fig.update_layout(yaxis=dict(categoryorder='category ascending'))  # 낮은 나이 위쪽
st.plotly_chart(fig, use_container_width=True)
