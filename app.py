import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Invisible 400M",
    page_icon="💳",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.hero {
    padding: 60px 20px;
    border-radius: 20px;
    background: linear-gradient(90deg, #1f4037, #99f2c8);
    color: white;
    text-align: center;
}
.card {
    background-color: #1c1f26;
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    color: white;
}
.footer {
    text-align: center;
    color: gray;
    padding: 20px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("💼 Invisible 400M")
page = st.sidebar.radio("Navigation", ["Home", "Dashboard", "Apply Loan"])

# ---------------- HOME PAGE ----------------
if page == "Home":
    st.markdown("""
    <div class="hero">
        <h1>Financial Identity for the Invisible 400M</h1>
        <p>AI-powered alternative credit scoring for gig workers & informal earners</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## 🚀 Why Our Platform?")
    col1, col2, col3 = st.columns(3)

    col1.markdown("<div class='card'><h3>📊 Behavior Based</h3><p>Transaction-driven scoring engine.</p></div>", unsafe_allow_html=True)
    col2.markdown("<div class='card'><h3>🤖 AI Powered</h3><p>Smart credit score generation.</p></div>", unsafe_allow_html=True)
    col3.markdown("<div class='card'><h3>💳 Inclusive</h3><p>Loans without salary slips.</p></div>", unsafe_allow_html=True)

# ---------------- DASHBOARD ----------------
if page == "Dashboard":
    st.title("📊 Credit Intelligence Dashboard")

    uploaded_file = st.file_uploader("Upload UPI Transaction CSV", type=["csv"])

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)

            df['date'] = pd.to_datetime(df['date'])
            df['month'] = df['date'].dt.to_period('M')

            credits = df[df['type'] == "CREDIT"]
            debits = df[df['type'] == "DEBIT"]

            monthly_income = credits.groupby('month')['amount'].sum()
            monthly_expense = debits.groupby('month')['amount'].sum().abs()

            avg_income = monthly_income.mean()
            avg_expense = monthly_expense.mean()
            savings = avg_income - avg_expense

            if avg_income == 0:
                st.error("No income transactions found.")
            else:
                expense_ratio = avg_expense / avg_income
                stability_score = 100 - (monthly_income.std() / avg_income * 100)
                stability_score = max(0, min(100, stability_score))

                alt_credit_score = (
                    stability_score * 0.4 +
                    (1 - expense_ratio) * 100 * 0.4 +
                    (savings / avg_income) * 100 * 0.2
                )
                alt_credit_score = int(max(300, min(900, alt_credit_score * 9)))

                repayment_probability = int(min(95, max(50, 100 - expense_ratio * 100 + stability_score * 0.3)))

                # -------- METRICS --------
                col1, col2, col3 = st.columns(3)
                col1.metric("💰 Avg Income", f"₹ {avg_income:,.0f}")
                col2.metric("💸 Avg Expense", f"₹ {avg_expense:,.0f}")
                col3.metric("💾 Savings", f"₹ {savings:,.0f}")

                st.markdown("## 🎯 Credit Score Meter")

                gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=alt_credit_score,
                    title={'text': "Alternative Credit Score"},
                    gauge={
                        'axis': {'range': [300, 900]},
                        'steps': [
                            {'range': [300, 600], 'color': "red"},
                            {'range': [600, 750], 'color': "orange"},
                            {'range': [750, 900], 'color': "green"}
                        ],
                    }
                ))

                st.plotly_chart(gauge, use_container_width=True)

                st.markdown("## 📈 Monthly Income Trend")
                bar_fig = px.bar(
                    monthly_income,
                    labels={'value': 'Income', 'month': 'Month'},
                )
                st.plotly_chart(bar_fig, use_container_width=True)

                st.markdown("### 🔮 Repayment Probability")
                st.progress(repayment_probability / 100)
                st.write(f"Repayment Likelihood: **{repayment_probability}%**")

                if alt_credit_score > 650:
                    st.success("✅ Eligible for Micro Loan up to ₹50,000")
                else:
                    st.error("❌ Not Eligible for Loan")

        except Exception as e:
            st.error("Error processing file. Please check CSV format.")
            st.write(e)

# ---------------- APPLY LOAN ----------------
if page == "Apply Loan":
    st.title("💳 Apply for Micro Loan")

    name = st.text_input("Full Name")
    amount = st.number_input("Loan Amount Required", min_value=1000, max_value=100000, step=1000)
    purpose = st.selectbox("Purpose", ["Business", "Personal", "Education", "Medical"])

    if st.button("Submit Application"):
        if name:
            st.success("✅ Application Submitted Successfully!")
            st.write("Our AI engine will evaluate your financial identity.")
        else:
            st.warning("Please enter your name.")

# ---------------- FOOTER ----------------
st.markdown("<div class='footer'>© 2026 Invisible 400M | AI Financial Inclusion Platform</div>", unsafe_allow_html=True)