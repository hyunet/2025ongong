import streamlit as st

st.set_page_config(page_title="MBTI 성격 분석기", layout="centered")

st.title("🧠 나의 MBTI 성향 분석기")
st.write("아래 질문에 답하고 당신의 MBTI 유형을 확인해보세요!")

questions = {
    "EI": [
        ("사람들과 어울릴 때 에너지가 생긴다.", "E"),
        ("혼자 있는 시간이 더 편하다.", "I"),
        ("말보다는 행동이 빠르다.", "E"),
    ],
    "SN": [
        ("현실적인 편이다.", "S"),
        ("아이디어나 가능성을 먼저 본다.", "N"),
        ("세부적인 사실보다 전체 그림이 중요하다.", "N"),
    ],
    "TF": [
        ("결정할 때 논리와 분석을 중시한다.", "T"),
        ("다른 사람의 감정을 중요하게 생각한다.", "F"),
        ("갈등을 피하려는 경향이 있다.", "F"),
    ],
    "JP": [
        ("계획적으로 움직이는 것을 선호한다.", "J"),
        ("즉흥적인 것을 즐긴다.", "P"),
        ("정해진 일정이 있는 것이 좋다.", "J"),
    ]
}

responses = {}

with st.form("mbti_form"):
    for dimension, qs in questions.items():
        for i, (q, _) in enumerate(qs):
            key = f"{dimension}_{i}"
            responses[key] = st.radio(q, ("그렇다", "아니다"), key=key)
    submitted = st.form_submit_button("MBTI 유형 분석하기")

if submitted:
    scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
    for dimension, qs in questions.items():
        for i, (q, trait) in enumerate(qs):
            key = f"{dimension}_{i}"
            if responses[key] == "그렇다":
                scores[trait] += 1
            else:
                # 반대 성향에 점수 추가
                opposite = {
                    "E": "I", "I": "E",
                    "S": "N", "N": "S",
                    "T": "F", "F": "T",
                    "J": "P", "P": "J"
                }[trait]
                scores[opposite] += 1

    mbti = "".join([
        "E" if scores["E"] >= scores["I"] else "I",
        "S" if scores["S"] >= scores["N"] else "N",
        "T" if scores["T"] >= scores["F"] else "F",
        "J" if scores["J"] >= scores["P"] else "P",
    ])

    descriptions = {
        "ISTJ": "책임감 있고 신중한 관리자형",
        "INFP": "이상주의적이고 감성적인 중재자형",
        "ENTP": "창의적이고 논쟁을 즐기는 발명가형",
        "ESFJ": "사교적이고 타인을 돌보는 돌보미형",
        # 필요 시 모든 16가지 유형 추가
    }

    st.subheader(f"🎯 당신의 MBTI 유형: {mbti}")
    st.write(descriptions.get(mbti, "아직 설명이 준비되지 않은 유형입니다."))

