import pandas as pd
import plotly.graph_objects as go

# CSV 불러오기 (예: cp949 또는 utf-8-sig)
df = pd.read_csv("people.csv", encoding='cp949')

# 남/여 연령별 컬럼 추출
male_cols = [col for col in df.columns if '남_' in col and '세' in col]
female_cols = [col for col in df.columns if '여_' in col and '세' in col]

# 연령 이름 추출
def extract_age(col): return col.split('_')[-1].replace('세', '').replace('이상', '100+')
ages = [extract_age(col) for col in male_cols]
ages_num = [int(a.replace('+','')) if '+' not in a else 100 for a in ages]

# 지역 선택 예: 종로구
row = df[df['행정구역'].str.contains("종로구")].iloc[0]

# 문자열 숫자 제거 및 결측치 처리
male = pd.to_numeric(row[male_cols].str.replace(",", ""), errors='coerce').fillna(0).astype(int)
female = pd.to_numeric(row[female_cols].str.replace(",", ""), errors='coerce').fillna(0).astype(int)

# 데이터프레임 구성
pyramid = pd.DataFrame({
    '연령': ages_num,
    '남': -male.values,   # 좌측
    '여': female.values   # 우측
}).sort_values(by='연령')

# Plotly 피라미드 그리기
fig = go.Figure()
fig.add_trace(go.Bar(y=pyramid['연령'], x=pyramid['남'], name='남성', orientation='h', marker_color='blue'))
fig.add_trace(go.Bar(y=pyramid['연령'], x=pyramid['여'], name='여성', orientation='h', marker_color='salmon'))

fig.update_layout(
    title='서울특별시 종로구 인구 피라미드',
    barmode='relative',
    xaxis_title='인구 수',
    yaxis_title='연령대',
    height=800
)
fig.update_yaxes(type='category', categoryorder='category ascending')
fig.show()
