import streamlit as st
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import matplotlib.font_manager as fm

# 한글 폰트 설정
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['NanumGothic', 'Malgun Gothic', 'AppleGothic', 'sans-serif']
matplotlib.rcParams['axes.unicode_minus'] = False
matplotlib.rcParams['font.size'] = 12

# ✅ 페이지 설정은 반드시 최상단에
st.set_page_config(page_title="정렬 알고리즘 시각화", page_icon="📊", layout="centered")

# 타이틀
st.title("📊 정렬 알고리즘 시각화")
st.markdown("다양한 정렬 알고리즘의 동작 과정을 시각적으로 확인해보세요!")

# 사이드바 설정
st.sidebar.header("설정")
array_size = st.sidebar.slider("배열 크기", 5, 50, 20)
speed = st.sidebar.select_slider("정렬 속도", options=[125.0, 250.0, 375.0, 500.0], value=250.0)
sort_order = st.sidebar.radio("정렬 방향", ["오름차순", "내림차순"])

# 정렬 알고리즘 선택 (라디오 버튼)
st.sidebar.header("정렬 알고리즘 선택")
selected_algorithm = st.sidebar.radio("알고리즘", ["버블 정렬", "선택 정렬", "삽입 정렬"])

# 정렬 시작 버튼
if st.sidebar.button("정렬 시작", type="primary"):
    st.session_state.sorting = True
else:
    st.session_state.sorting = False

# 형성평가 버튼
st.sidebar.markdown("""
<div style='text-align: center; margin: 20px 0;'>
    <a href='https://forms.gle/2hc8i1iKb7LLwuVK7' target='_blank' style='padding: 10px 20px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 5px;'>
        형성평가 시작
    </a>
</div>
""", unsafe_allow_html=True)

# 랜덤 배열 생성
if 'array' not in st.session_state or 'array_size' not in st.session_state or st.session_state.array_size != array_size:
    st.session_state.array = np.random.randint(1, 100, array_size)
    st.session_state.array_size = array_size

# 정렬 함수들
def bubble_sort(arr, frames, sorted_indices, current_indices):
    n = len(arr)
    start_time = time.time()
    for i in range(n):
        for j in range(0, n-i-1):
            current_indices.clear()
            current_indices.extend([j, j+1])
            if (sort_order == "오름차순" and arr[j] > arr[j+1]) or \
               (sort_order == "내림차순" and arr[j] < arr[j+1]):
                arr[j], arr[j+1] = arr[j+1], arr[j]
            frames.append((arr.copy(), sorted_indices.copy(), current_indices.copy()))
        sorted_indices.append(n-i-1)
    return time.time() - start_time

def selection_sort(arr, frames, sorted_indices, current_indices):
    n = len(arr)
    start_time = time.time()
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            current_indices.clear()
            current_indices.extend([i, j])
            if (sort_order == "오름차순" and arr[j] < arr[min_idx]) or \
               (sort_order == "내림차순" and arr[j] > arr[min_idx]):
                min_idx = j
            frames.append((arr.copy(), sorted_indices.copy(), current_indices.copy()))
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        frames.append((arr.copy(), sorted_indices.copy(), current_indices.copy()))
        sorted_indices.append(i)
    return time.time() - start_time

def insertion_sort(arr, frames, sorted_indices, current_indices):
    start_time = time.time()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        while j >= 0 and ((sort_order == "오름차순" and arr[j] > key) or \
                         (sort_order == "내림차순" and arr[j] < key)):
            current_indices.clear()
            current_indices.extend([j, j+1])
            arr[j+1] = arr[j]
            j -= 1
            frames.append((arr.copy(), sorted_indices.copy(), current_indices.copy()))
        arr[j+1] = key
        frames.append((arr.copy(), sorted_indices.copy(), current_indices.copy()))
        sorted_indices.append(i)
    return time.time() - start_time

# 초기 배열 표시
st.subheader("초기 배열")
initial_plot = st.empty()
fig, ax = plt.subplots(figsize=(10, 4))
bars = ax.bar(range(len(st.session_state.array)), st.session_state.array, color='blue')
ax.set_title("정렬 전 배열")
initial_plot.pyplot(fig)
plt.close()

# 정렬 실행 버튼
if st.session_state.sorting:
    # 선택된 알고리즘에 대한 결과를 저장할 딕셔너리
    results = {}
    frames = {}
    execution_times = {}
    
    # 선택된 알고리즘 실행
    if selected_algorithm == "버블 정렬":
        arr = st.session_state.array.copy()
        frames["버블 정렬"] = []
        sorted_indices = []
        current_indices = []
        execution_times["버블 정렬"] = bubble_sort(arr, frames["버블 정렬"], sorted_indices, current_indices)
        results["버블 정렬"] = arr.copy()
    
    elif selected_algorithm == "선택 정렬":
        arr = st.session_state.array.copy()
        frames["선택 정렬"] = []
        sorted_indices = []
        current_indices = []
        execution_times["선택 정렬"] = selection_sort(arr, frames["선택 정렬"], sorted_indices, current_indices)
        results["선택 정렬"] = arr.copy()
    
    elif selected_algorithm == "삽입 정렬":
        arr = st.session_state.array.copy()
        frames["삽입 정렬"] = []
        sorted_indices = []
        current_indices = []
        execution_times["삽입 정렬"] = insertion_sort(arr, frames["삽입 정렬"], sorted_indices, current_indices)
        results["삽입 정렬"] = arr.copy()
    
    # 애니메이션 표시
    for algo_name in results.keys():
        st.subheader(f"{algo_name} 진행 중")
        plot_placeholder = st.empty()
        
        for frame, sorted_idx, current_idx in frames[algo_name]:
            fig, ax = plt.subplots(figsize=(10, 4))
            bars = ax.bar(range(len(frame)), frame)
            
            # 막대 색상 설정
            for i, bar in enumerate(bars):
                if i in sorted_idx:
                    bar.set_color('green')  # 정렬 완료된 막대
                elif i in current_idx:
                    bar.set_color('pink')   # 현재 비교/교환 중인 막대
                else:
                    bar.set_color('blue')   # 아직 정렬되지 않은 막대
            
            ax.set_title(f"{algo_name} 진행 중")
            plot_placeholder.pyplot(fig)
            plt.close()
            time.sleep(1.0/speed)  # 속도 조절
    
    # 정렬 완료 후 결과 표시
    st.subheader("정렬 완료!")
    for algo_name, result in results.items():
        fig, ax = plt.subplots(figsize=(10, 4))
        bars = ax.bar(range(len(result)), result, color='green')
        ax.set_title(f"{algo_name} 결과 (실행 시간: {execution_times[algo_name]:.3f}초)")
        st.pyplot(fig)
        plt.close()
