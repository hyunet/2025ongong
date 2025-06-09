import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📈 인구 트렌드 및 성비 분석")

df = pd.read_csv("people.csv", encoding='cp949')
male_cols = [col for col in df.columns if '남_' in col and '세' in col]
female_cols = [col for col in df.columns if '여_' in col and '세' in col]

# 지표 계산
insights = []
for _, row in df.iterrows():
    region = row['행정구역']
    male_total = pd.to_numeric(row[male_cols].str.replace(',', ''), errors='coerce').sum()
    female_total = pd.to_numeric(row[female_cols].str.replace(',', ''), errors='coerce').sum()
    total = male_total + female_total
    elderly_male = pd.to_numeric(row[[c for c in male_cols if '70' in c or '80' in c or '90' in c or '100' in c]].str.replace(',', ''), errors='coerce').sum()
    elderly_female = pd.to_numeric(row[[c for c in female_cols if '70' in c or '80' in c or '90' in c or '100' in c]].str.replace(',', ''), errors='coerce').sum()
    elderly_ratio = round(((elderly_male + elderly_female) / total) * 100, 2) if total else 0
    sex_ratio = round((male_total / female_total) * 100, 2) if female_total else 0
    insights.append({
        "지역": region,
        "총인구": total,
        "남성": male_total,
        "여성": female_total,
        "성비 (%)": sex_ratio,
        "고령 인구 비율 (%)": elderly_ratio
    })

insight_df = pd.DataFrame(insights)

# 시각화
col_option = st.selectbox("📌 분석 항목 선택", ['성비 (%)', '고령 인구 비율 (%)', '총인구'])
fig = px.bar(insight_df.sort_values(col_option, ascending=False),
             x="지역", y=col_option,
             title=f"{col_option} 기준 정렬", color=col_option)
st.plotly_chart(fig, use_container_width=True)
