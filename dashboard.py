import streamlit as st
import pandas as pd
import plotly.express as px



st.set_page_config(layout='wide')
st.markdown("""
    <style>
        body {
            background-color: #0A0F24; 
            color: white;
        }
        .stApp {
            background-color: #0A0F24;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <h1 style='background-color:#1E1E2F; color:white; padding:15px; border-radius:8px; text-align:center;'>
        📈 Relatório de Faturamento - SuperMarket
    </h1>
""", unsafe_allow_html=True)
df = pd.read_csv("supermarket_sales.csv", sep=";", decimal=",")
df["Date"] = pd.to_datetime(df["Date"])
df=df.sort_values(["Date"])
df["Month"] = df["Date"].dt.to_period("M").astype(str)

col_top1, col_top2 = st.columns([1, 4])
df["Month"] = df["Date"].apply(lambda x: str(x.year) + "-" + str(x.month))
with col_top1:
    month = st.selectbox("",df["Month"].unique())

df_filtered = df[df["Month"] == month]

px.defaults.template = "plotly_dark"

col1, col2, col3 = st.columns(3)
col4, col5 = st.columns(2)

fig_date = px.bar(df_filtered, x="Date", y="Total", color="City", title="Faturamento Diario")
col1.plotly_chart(fig_date, use_container_width=True)

fig_prod = px.bar(df_filtered, x="Date", y="Product line", color="City", title="Faturamento por tipo de produto", orientation="h")
col2.plotly_chart(fig_prod, use_container_width=True)

city_total = df_filtered.groupby("City")[["Total"]].sum().reset_index()
fig_city = px.bar(df_filtered, x="City", y="Total", title="Faturamento por filial")
col3.plotly_chart(fig_city, use_container_width=True)


fig_kind = px.pie(df_filtered, values="Total", names="Payment", title="Faturamento por tipo de pagamento")
col4.plotly_chart(fig_kind, use_container_width=True)

city_total = df_filtered.groupby("City")[["Total"]].mean().reset_index()
fig_rating = px.bar(df_filtered, y="Rating", x="City", title="Avaliação")
col5.plotly_chart(fig_rating, use_container_width=True)


df_month = df.groupby("Month")[["Total"]].sum().reset_index()
fig_trend = px.line(df_month,x="Month", y="Total", title="Evolução do Faturamento Mês a Mês",markers=True)
st.plotly_chart(fig_trend, use_container_width=True)
