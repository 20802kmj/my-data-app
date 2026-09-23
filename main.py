
import pandas as pd
import streamlit as st
import plotly.express as px

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/seoul.csv"

st.set_page_config(
    page_title="서울 기온 데이터",
    page_icon="🌡️",
    layout="wide",
)

st.title("🌡️ 서울 기온 데이터")

st.write(
    "서울의 일별 평균기온 분포를 히스토그램으로 확인합니다. "
    "각 막대는 해당 온도 구간에 속하는 날짜가 며칠인지 나타냅니다."
)


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL, encoding="utf-8-sig")

    df["날짜"] = pd.to_datetime(df["날짜"], errors="coerce")
    df["평균기온"] = pd.to_numeric(df["평균기온"], errors="coerce")

    df = df.dropna(subset=["날짜", "평균기온"])

    return df


df = load_data()

st.subheader("일별 평균기온 분포")

fig = px.histogram(
    df,
    x="평균기온",
    nbins=50,
    labels={
        "평균기온": "평균기온 (℃)",
        "count": "일수",
    },
    title="서울 일별 평균기온 분포",
)

fig.update_layout(
    xaxis_title="평균기온 (℃)",
    yaxis_title="일수",
    bargap=0.05,
)

st.plotly_chart(fig, use_container_width=True)

# 요약 정보
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "전체 관측 일수",
        f"{len(df):,}일",
    )

with col2:
    st.metric(
        "평균기온 평균",
        f"{df['평균기온'].mean():.1f}℃",
    )

with col3:
    st.metric(
        "평균기온 범위",
        f"{df['평균기온'].min():.1f} ~ {df['평균기온'].max():.1f}℃",
    )

st.caption("자료: 제공된 서울 기상 관측 데이터")

