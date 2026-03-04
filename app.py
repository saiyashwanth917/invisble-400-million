import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Invisible 400M",
    page_icon="💳",
    layout="wide",
)

# ---------------- GLOBAL DARK THEME ----------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
}

.block-container {
    padding-top: 2rem;
}

.metric-card {
    background: linear-gradient(145deg, #1c1f26, #111418);
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.4);
    text-align: center;
}

.metric-title {
    font-size: 14px;
    color: #9aa4b2;
}

.metric-value {
    font-size: 28px;
    font-weight: 600;
    color: white;
}

.hero-section {
    padding: 80px 20px;
    border-radius: 25px;
    background: linear-gradient(90deg, #141e30, #243b55);
    color: white;
    text-align: center;
}

.stButton>button {
    background: linear-gradient(90deg,#00c6ff,#0072ff);
    color: white;
    border-radius: 10px;
    padding: 0.5rem 1.5rem;
    border: none;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.markdown("## 💼 Invisible 400M")
st.sidebar.markdown("AI Credit Scoring for the Informal Economy")
page = st.sidebar.radio("", ["Home", "Dashboard", "Apply Loan"])

# ---------------- HOME ----------------
if page == "Home":
    st.markdown("""
    <div class="hero-section">
        <h1>Financial Identity for the Invisible 400M</h1>
        <p>AI-powered alternative credit scoring for gig workers & informal earners</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## 🌍 Why It Matters")

    col1, col2, col3 = st.columns(3)

    col1.markdown("""
    <div class="metric-card">
        <h3>📊 Transaction Based</h3>
        <p>We analyze behavioral cashflow data.</p>
    </div>
    """, unsafe_allow_html=True)

    col2.markdown("""
    <div class="metric-card">
        <h3>🤖 AI Powered</h3>
        <p>Dynamic credit scoring engine.</p>
    </div>
    """, unsafe_allow_html=True)

    col3.markdown("""
    <div class="metric-card">
        <h3>💳 Financial Inclusion</h3>
        <p>No salary slip required.</p>
    </div>
    """, unsafe_allow_html=True)

# ---------------- DASHBOARD ----------------
if page == "Dashboard":

    st.title("📊 Credit Intelligence Dashboard")

    uploaded_file = st.file_uploader("Upload UPI Transaction CSV", type=["csv"])

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)

            required_cols = {"date", "type", "amount"}
            if not required_cols.issubset(df.columns):
                st.error("CSV must contain: date, type, amount")
                st.stop()

            df["date"] = pd.to_datetime(df["date"], errors="coerce")
            df = df.dropna(subset=["date"])

            df["month"] = df["date"].dt.strftime("%Y-%m")

            credits = df[df["type"].str.upper() == "CREDIT"]
            debits = df[df["type"].str.upper() == "DEBIT"]

            monthly_income = credits.groupby("month")["amount"].sum().reset_index()
            monthly_expense = debits.groupby("month")["amount"].sum().abs().reset_index()

            avg_income = monthly_income["amount"].mean()
            avg_expense = monthly_expense["amount"].mean()
            savings = avg_income - avg_expense

            if avg_income > 0:

                expense_ratio = avg_expense / avg_income
                stability_score = 100 - (monthly_income["amount"].std() / avg_income * 100)
                stability_score = max(0, min(100, stability_score))

                alt_credit_score = int(max(300, min(900, (
                    stability_score * 0.4 +
                    (1 - expense_ratio) * 100 * 0.4 +
                    (savings / avg_income) * 100 * 0.2
                ) * 9)))

                repayment_probability = int(
                    min(95, max(50, 100 - expense_ratio * 100 + stability_score * 0.3))
                )

                # -------- KPI CARDS --------
                col1, col2, col3 = st.columns(3)

                col1.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Average Income</div>
                    <div class="metric-value">₹ {avg_income:,.0f}</div>
                </div>
                """, unsafe_allow_html=True)

                col2.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Average Expense</div>
                    <div class="metric-value">₹ {avg_expense:,.0f}</div>
                </div>
                """, unsafe_allow_html=True)

                col3.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Savings</div>
                    <div class="metric-value">₹ {savings:,.0f}</div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("## 🎯 Credit Score")

                gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=alt_credit_score,
                    gauge={'axis': {'range': [300, 900]}},
                ))

                gauge.update_layout(
                    paper_bgcolor="#0e1117",
                    font={'color': "white"}
                )

                st.plotly_chart(gauge, use_container_width=True)

                # -------- CHART --------
                st.markdown("## 📈 Monthly Income Trend")

                bar_fig = px.bar(
                    monthly_income,
                    x="month",
                    y="amount",
                    text_auto=True,
                )

                bar_fig.update_layout(
                    paper_bgcolor="#0e1117",
                    plot_bgcolor="#0e1117",
                    font=dict(color="white")
                )

                st.plotly_chart(bar_fig, use_container_width=True)

                st.markdown("### 🔮 Repayment Probability")
                st.progress(repayment_probability / 100)
                st.write(f"Likelihood: **{repayment_probability}%**")

            else:
                st.error("No income transactions found.")

        except Exception as e:
            st.error("Error processing file.")
            st.write(e)

# ---------------- APPLY LOAN ----------------
if page == "Apply Loan":

    st.title("💳 Apply for Micro Loan")

    name = st.text_input("Full Name")
    amount = st.number_input("Loan Amount", min_value=1000, max_value=100000, step=1000)
    purpose = st.selectbox("Purpose", ["Business", "Personal", "Education", "Medical"])

    if st.button("Submit Application"):
        if name:
            st.success("Application Submitted Successfully!")
        else:
            st.warning("Please enter your name.")

# ---------------- FOOTER ----------------
st.markdown(
    "<div style='text-align:center; color:gray; padding:30px;'>© 2026 Invisible 400M | Financial Inclusion Platform</div>",
    unsafe_allow_html=True
)
