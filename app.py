import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Monthly Income Trend", layout="wide")

st.title("📊 Monthly Income Trend")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        # Load CSV
        df = pd.read_csv(uploaded_file)

        # Ensure required columns exist
        if "date" not in df.columns or "income" not in df.columns:
            st.error("CSV must contain 'date' and 'income' columns.")
            st.stop()

        # Convert date column to datetime
        df["date"] = pd.to_datetime(df["date"])

        # ---- FIX FOR PERIOD ERROR ----
        # Group by month using Period, then convert to timestamp
        monthly = (
            df.groupby(df["date"].dt.to_period("M"))["income"]
            .sum()
            .reset_index()
        )

        # Convert Period → Timestamp (THIS FIXES YOUR ERROR)
        monthly["date"] = monthly["date"].dt.to_timestamp()

        # Sort values
        monthly = monthly.sort_values("date")

        # Create Plotly bar chart
        fig = px.bar(
            monthly,
            x="date",
            y="income",
            title="Monthly Income",
            labels={"date": "Month", "income": "Total Income"},
            text_auto=True,
        )

        fig.update_layout(
            xaxis_title="Month",
            yaxis_title="Income",
            xaxis=dict(tickformat="%b %Y"),
        )

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error("Error processing file. Please check CSV format.")
        st.exception(e)
