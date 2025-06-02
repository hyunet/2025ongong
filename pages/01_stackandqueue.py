import streamlit as st
import plotly.graph_objects as go

# Streamlit 기본 설정
st.set_page_config(page_title="스택과 큐 시각화", layout="centered")

st.title("📚 자료구조 시각화: 스택(Stack)과 큐(Queue)")

# 설명 섹션
st.header("1️⃣ 스택 (Stack)")
st.markdown("""
스택은 **LIFO (Last In, First Out)** 구조입니다.  
즉, 가장 마지막에 들어간 데이터가 가장 먼저 나옵니다.  
참 쉽죠?
대표적인 연산은 `push`(삽입), `pop`(삭제)입니다.
""")

# 스택 시각화
stack_items = ['A', 'B', 'C', 'D']  # Stack 순서: A (bottom) → D (top)
stack_fig = go.Figure()

for i, item in enumerate(reversed(stack_items)):
    stack_fig.add_shape(
        type="rect",
        x0=0, y0=i, x1=1, y1=i+1,
        line=dict(color="RoyalBlue"),
        fillcolor="LightSkyBlue"
    )
    stack_fig.add_annotation(
        x=0.5, y=i+0.5, text=item,
        showarrow=False,
        font=dict(size=16)
    )

stack_fig.update_layout(
    height=300,
    width=200,
    title="스택 구조 (Top: D)",
    xaxis=dict(visible=False),
    yaxis=dict(visible=False),
    margin=dict(t=40, b=10, l=10, r=10)
)

st.plotly_chart(stack_fig)

# 큐 설명
st.header("2️⃣ 큐 (Queue)")
st.markdown("""
큐는 **FIFO (First In, First Out)** 구조입니다.  
즉, 가장 먼저 들어간 데이터가 가장 먼저 나옵니다.  
대표적인 연산은 `enqueue`(삽입), `dequeue`(삭제)입니다.
""")

# 큐 시각화
queue_items = ['1', '2', '3', '4']  # Queue 순서: 1 (front) → 4 (rear)
queue_fig = go.Figure()

for i, item in enumerate(queue_items):
    queue_fig.add_shape(
        type="rect",
        x0=i, y0=0, x1=i+1, y1=1,
        line=dict(color="DarkGreen"),
        fillcolor="PaleGreen"
    )
    queue_fig.add_annotation(
        x=i+0.5, y=0.5, text=item,
        showarrow=False,
        font=dict(size=16)
    )

queue_fig.add_annotation(x=0.5, y=-0.3, text="Front", showarrow=False)
queue_fig.add_annotation(x=3.5, y=-0.3, text="Rear", showarrow=False)

queue_fig.update_layout(
    height=200,
    width=400,
    title="큐 구조 (Front → Rear)",
    xaxis=dict(visible=False),
    yaxis=dict(visible=False),
    margin=dict(t=40, b=10, l=10, r=10)
)

st.plotly_chart(queue_fig)

# 결론
st.header("✅ 요약")
st.markdown("""
| 자료구조 | 특징 | 주요 연산 |
|----------|------|------------|
| 스택(Stack) | LIFO | `push()`, `pop()` |
| 큐(Queue)   | FIFO | `enqueue()`, `dequeue()` |

시각화를 통해 각 구조의 **입출력 순서**를 한눈에 이해할 수 있습니다.
""")
