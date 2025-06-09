import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="인구 피라미드 시각화", layout="wide")
st.title("👥 지역별 연령대 인구 피라미드")

# ✅ CSV 파일 경로 (루트 기준)
csv_path = Path.cwd() / "people.csv"

# ✅ 데이터 불러오기 (cp949 우선, 실패 시 utf-8-sig)
try:
    df = pd.read_csv(csv_path, encoding='cp949')
except UnicodeDecodeError:
    df = pd.read_csv(csv_path, encoding='utf-8-sig')

# ✅ 남녀 연령 컬럼 추출
male_cols = [col for col in df.columns if '남_' in col and '세' in col]
female_cols = [col for col in df.columns if '여_' in col and '세' in col]

# 연령 숫자 정리 (0세 ~ 100+세)
def extract_age(col):
    return col.split('_')[-1].replace('세', '').replace('이상', '100+')
ages = [extract_age(c) for c in male_cols]
ages_num = [int(a.replace('+', '')) if '+' not in a else 100 for a in ages]

# ✅ 지역 선택
region = st.selectbox("🏙️ 지역을 선택하세요", df['행정구역'].unique())

# ✅ 연령 슬라이더
min_age, max_age = st.slider("🎚️ 연령 범위 선택", 0, 100, (0, 100))

# ✅ 선택한 지역 데이터 정리
row = df[df['행정구역'] == region].iloc[0]

male = pd.to_numeric(row[male_cols].str.replace(",", ""), errors='coerce').fillna(0).astype(int)
female = pd.to_numeric(row[female_cols].str.replace(",", ""), errors='coerce').fillna(0).astype(int)

# ✅ 연령 필터링
filtered = [(a, m, f) for a, m, f in zip(ages_num, male, female) if min_age <= a <= max_age]
ages_f, male_f, female_f = zip(*filtered)
age_labels = [f"{a}세" if a != 100 else "100세 이상" for a in ages_f]

# ✅ 피라미드용 데이터프레임
df_pyramid = pd.DataFrame({
    "연령": age_labels,
    "남성": [-m for m in male_f],   # 좌측
    "여성": female_f                # 우측
})

# ✅ Long-form 변환
df_long = df_pyramid.melt(id_vars="연령", var_name="성별", value_name="인구수")

# ✅ Plotly 시각화
fig = px.bar(
    df_long,
    x="인구수",
    y="연령",
    color="성별",
    orientation="h",
    title=f"📊 {region} 연령별 인구 피라미드",
    height=800,
    color_discrete_map={"남성": "royalblue", "여성": "salmon"}
)
fig.update_layout(
    yaxis=dict(categoryorder="category ascending"),
    xaxis_title="인구 수",
    yaxis_title="연령대",
    bargap=0.05
)

st.plotly_chart(fig, use_container_width=True)
