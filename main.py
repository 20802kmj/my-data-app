import pandas as pd
import streamlit as st

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/seoul.csv"

st.set_page_config(
    page_title="서울 연평균 기온 변화",
    page_icon="🌡️",
    layout="wide",
)

st.title("🌡️ 서울의 100년 연평균 기온 변화")
st.write("서울의 일별 기온 데이터를 연도별로 집계하여 연평균 기온의 변화를 보여줍니다.")

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL, encoding="utf-8-sig")

    df["날짜"] = pd.to_datetime(df["날짜"], errors="coerce")
    df["평균기온"] = pd.to_numeric(df["평균기온"], errors="coerce")

    df = df.dropna(subset=["날짜", "평균기온"])
    df["연도"] = df["날짜"].dt.year

    annual = (
        df.groupby("연도", as_index=False)["평균기온"]
        .mean()
        .rename(columns={"평균기온": "연평균기온"})
    )

    return annual


df = load_data()

# 가장 최근 100개 연도 선택
years = sorted(df["연도"].unique())
if len(years) > 100:
    years = years[-100:]

annual = df[df["연도"].isin(years)].copy()

# 요약 정보
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("분석 기간", f"{annual['연도'].min()}~{annual['연도'].max()}년")

with col2:
    st.metric("가장 낮은 연평균", f"{annual['연평균기온'].min():.1f}℃")

with col3:
    st.metric("가장 높은 연평균", f"{annual['연평균기온'].max():.1f}℃")

st.subheader("연도별 연평균 기온")

chart_data = annual.set_index("연도")[["연평균기온"]]

st.line_chart(
    chart_data,
    y="연평균기온",
    x_label="연도",
    y_label="연평균 기온 (℃)",
)

st.caption("자료: 제공된 서울 기상 관측 데이터 / 단위: ℃")

with st.expander("연도별 데이터 보기"):
    display_df = annual.copy()
    display_df["연평균기온"] = display_df["연평균기온"].round(1)
    display_df = display_df.rename(
        columns={
            "연도": "연도",
            "연평균기온": "연평균 기온 (℃)",
        }
    )
    st.dataframe(display_df, use_container_width=True, hide_index=True)
