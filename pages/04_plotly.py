import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="인구 피라미드", layout="wide")
st.title("👥 연령별 인구 피라미드 (Plotly)")

# 🔄 상위 폴더에 있는 CSV 불러오기
file_path = "../202505_202505_연령별인구현황_월간.csv"

# 📥 데이터 로딩
try:
    df = pd.read_csv(file_path, encoding='cp949')
    if df.empty:
        raise ValueError("파일은 존재하지만 내용이 비어 있습니다.")
except FileNotFoundError:
    st.error("❌ 파일을 찾을 수 없습니다. 루트 폴더에 CSV 파일이 있는지 확인하세요.")
    st.stop()
except pd.errors.EmptyDataError:
    st.error("❌ CSV 파일이 비어 있습니다. 올바른 형식으로 저장되었는지 확인하세요.")
    st.stop()
except UnicodeDecodeError:
    try:
        df = pd.read_csv(file_path, encoding='utf-8-sig')
    except:
        st.error("❌ 파일 인코딩 오류: 'cp949' 또는 'utf-8-sig' 인코딩을 확인하세요.")
        st.stop()
except Exception as e:
    st.error(f"❌ 예기치 못한 오류 발생: {e}")
    st.stop()

# 🎯 지역 선택
region_list = df['행정구역'].unique()
selected_region = st.selectbox("🔍 행정구역을 선택하세요", region_list)

# 🎯 연령 컬럼 추출
age_columns = [col for col in df.columns if '세' in col]
region_row = df[df['행정구역'] == selected_region].iloc[0]
age_data = region_row[age_columns].str.replace(",", "").astype(int)

# 🎯 연령 정리
age_labels = [col.split('_')[-1].replace('세', '').replace('이상', '100+') for col in age_columns]
age_numbers = [int(a.replace('+', '')) if '+' not in a else 100 for a in age_labels]

# 🎯 슬라이더로 연령 필터
min_age, max_age = st.slider("🎚️ 연령 범위를 선택하세요", 0, 100, (0, 100))
filtered = [(a, p) for a, p in zip(age_numbers, age_data) if min_age <= a <= max_age]
ages_filtered, pops_filtered = zip(*filtered)
age_labels_filtered = [f"{a}세" if a != 100 else "100세 이상" for a in ages_filtered]

# 📊 Plotly 그래프 생성
fig = px.bar(
    x=pops_filtered,
    y=age_labels_filtered,
    orientation='h',
    title=f"{selected_region} 연령별 인구 분포",
    labels={'x': '인구 수', 'y': '연령대'},
    color=pops_filtered,
    height=700
)
fig.update_layout(yaxis=dict(categoryorder='category ascending'))
st.plotly_chart(fig, use_container_width=True)
