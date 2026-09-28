import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Smart Loan Approval & Risk Analysis",
    page_icon="🏦",
    layout="wide"
)

# =====================================================
# COLORS
# =====================================================

BG     = "#F4F7FB"
BLUE   = "#2563EB"
GREEN  = "#16A34A"
RED    = "#DC2626"
ORANGE = "#EA580C"
PURPLE = "#7C3AED"
WHITE  = "#FFFFFF"
DARK   = "#172033"

# =====================================================
# LOAD + CLEAN DATA
# =====================================================

@st.cache_data
def load_data():
    df = pd.read_csv("loan_prediction.csv")

    num = ["ApplicantIncome", "CoapplicantIncome",
           "LoanAmount", "Loan_Amount_Term", "Credit_History"]
    cat = ["Gender", "Married", "Dependents",
           "Education", "Self_Employed", "Property_Area"]

    for c in num:
        df[c] = pd.to_numeric(df[c], errors="coerce")
        df[c] = df[c].fillna(df[c].median())

    for c in cat:
        df[c] = df[c].fillna("Unknown")

    df = df.drop_duplicates(subset="Loan_ID")
    df["TotalIncome"]       = df["ApplicantIncome"] + df["CoapplicantIncome"]
    df["LoanAmountRupees"]  = df["LoanAmount"] * 1000
    df["Outcome"]           = df["Loan_Status"].map({"Y": "Approved", "N": "Not Approved"})
    return df

df      = load_data()
total   = len(df)
approved = (df.Loan_Status == "Y").sum()
rejected = (df.Loan_Status == "N").sum()
rate    = approved / total * 100

# =====================================================
# SIDEBAR NAVIGATION
# =====================================================

st.sidebar.title("🏦 Smart Loan")
page = st.sidebar.radio(
    "Navigate",
    ["📊 Dashboard", "✅ Eligibility Checker",
     "📈 Analytics", "🔍 Explore Data", "ℹ️ About"]
)

# =====================================================
# ELIGIBILITY LOGIC
# =====================================================

def check_eligibility(income, co_income, loan, education, self_employed, credit):
    score = 0

    if income >= 25000:
        score += 30
    elif income >= 15000:
        score += 20

    if credit == "Good":
        score += 35

    if education == "Graduate":
        score += 10

    if self_employed == "No":
        score += 5

    annual_income = (income + co_income) * 12
    ratio = loan / annual_income if annual_income > 0 else 999

    if ratio <= 3:
        score += 20
    elif ratio <= 5:
        score += 10

    if score >= 70:
        result = "ELIGIBLE"
    elif score >= 50:
        result = "MANUAL REVIEW"
    else:
        result = "NOT ELIGIBLE"

    return score, ratio, result

# =====================================================
# PAGE: DASHBOARD
# =====================================================

if page == "📊 Dashboard":

    st.title("📊 Smart Loan Approval & Risk Analysis")
    st.markdown("---")

    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📋 Total Applications", total)
    col2.metric("✅ Approved",            approved)
    col3.metric("❌ Not Approved",        rejected)
    col4.metric("📈 Approval Rate",       f"{rate:.1f}%")

    st.markdown("---")

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Loan Application Status")
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.pie(
            [approved, rejected],
            labels=["Approved", "Not Approved"],
            autopct="%1.1f%%",
            colors=[GREEN, RED],
            startangle=90
        )
        st.pyplot(fig)
        plt.close(fig)

    with col_right:
        st.subheader("Income vs Loan Amount")
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.scatter(df.TotalIncome, df.LoanAmount, alpha=0.6, color=BLUE)
        ax.set_xlabel("Total Income")
        ax.set_ylabel("Loan Amount")
        st.pyplot(fig)
        plt.close(fig)

    col_left2, col_right2 = st.columns(2)

    with col_left2:
        st.subheader("Applications by Property Area")
        fig, ax = plt.subplots(figsize=(5, 3))
        df.Property_Area.value_counts().plot(kind="bar", ax=ax, color=PURPLE)
        ax.set_xlabel("")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    with col_right2:
        st.subheader("Applications by Education")
        fig, ax = plt.subplots(figsize=(5, 3))
        df.Education.value_counts().plot(kind="bar", ax=ax, color=ORANGE)
        ax.set_xlabel("")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

# =====================================================
# PAGE: ELIGIBILITY CHECKER
# =====================================================

elif page == "✅ Eligibility Checker":

    st.title("✅ Loan Eligibility Checker")
    st.markdown("---")

    with st.form("eligibility_form"):
        name       = st.text_input("Applicant Name")
        income     = st.number_input("Monthly Income (₹)", min_value=0, step=1000)
        co_income  = st.number_input("Co-applicant Income (₹)", min_value=0, step=1000)
        loan       = st.number_input("Loan Amount (₹)", min_value=0, step=10000)
        education  = st.selectbox("Education", ["Graduate", "Not Graduate"])
        self_emp   = st.selectbox("Self Employed", ["No", "Yes"])
        credit     = st.selectbox("Credit History", ["Good", "Poor"])
        submitted  = st.form_submit_button("🔍 Check Eligibility")

    if submitted:
        if income == 0 and loan == 0:
            st.warning("⚠️ Please enter valid income and loan amounts.")
        else:
            score, ratio, status = check_eligibility(
                income, co_income, loan, education, self_emp, credit
            )

            color_map = {
                "ELIGIBLE":      "success",
                "MANUAL REVIEW": "warning",
                "NOT ELIGIBLE":  "error"
            }
            icon_map = {
                "ELIGIBLE":      "✅",
                "MANUAL REVIEW": "⚠️",
                "NOT ELIGIBLE":  "❌"
            }

            msg = (
                f"**Applicant:** {name or 'N/A'}  \n"
                f"**Risk Score:** {score}/100  \n"
                f"**Loan-to-Income Ratio:** {ratio:.2f}  \n"
                f"**Final Result:** {icon_map[status]} {status}"
            )

            if status == "ELIGIBLE":
                st.success(msg)
            elif status == "MANUAL REVIEW":
                st.warning(msg)
            else:
                st.error(msg)

# =====================================================
# PAGE: ANALYTICS
# =====================================================

elif page == "📈 Analytics":

    st.title("📈 Loan Analytics")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Applicant Income Distribution")
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.hist(df.ApplicantIncome, bins=20, color=BLUE)
        ax.set_xlabel("Income")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    with col2:
        st.subheader("Credit History")
        fig, ax = plt.subplots(figsize=(5, 3))
        df.Credit_History.value_counts().plot(kind="bar", ax=ax, color=GREEN)
        ax.set_xlabel("")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Loan Amount Distribution")
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.hist(df.LoanAmount, bins=20, color=PURPLE)
        ax.set_xlabel("Loan Amount")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    with col4:
        st.subheader("Property Area")
        fig, ax = plt.subplots(figsize=(5, 3))
        df.Property_Area.value_counts().plot(kind="bar", ax=ax, color=ORANGE)
        ax.set_xlabel("")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

# =====================================================
# PAGE: EXPLORE DATA
# =====================================================

elif page == "🔍 Explore Data":

    st.title("🔍 Explore Loan Data")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.selectbox(
            "Status", ["All", "Approved", "Not Approved"]
        )
    with col2:
        edu_filter = st.selectbox(
            "Education", ["All", "Graduate", "Not Graduate"]
        )
    with col3:
        area_filter = st.selectbox(
            "Property Area", ["All", "Urban", "Semiurban", "Rural"]
        )

    filtered = df.copy()

    if status_filter == "Approved":
        filtered = filtered[filtered.Loan_Status == "Y"]
    elif status_filter == "Not Approved":
        filtered = filtered[filtered.Loan_Status == "N"]

    if edu_filter != "All":
        filtered = filtered[filtered.Education == edu_filter]

    if area_filter != "All":
        filtered = filtered[filtered.Property_Area == area_filter]

    columns = [
        "Loan_ID", "Gender", "Education",
        "ApplicantIncome", "CoapplicantIncome",
        "LoanAmount", "Credit_History",
        "Property_Area", "Loan_Status"
    ]

    st.markdown(
        f"**Showing {len(filtered)} of {total} applications**"
    )
    st.dataframe(filtered[columns], use_container_width=True)

# =====================================================
# PAGE: ABOUT
# =====================================================

elif page == "ℹ️ About":

    st.title("ℹ️ About Smart Loan")
    st.markdown("---")

    st.markdown("""
    ## 🎯 Project Objective
    Analyze loan applications and provide a simple eligibility decision.

    ## 🛠️ Technologies
    - **Python**
    - **Pandas**
    - **NumPy**
    - **Matplotlib**
    - **Streamlit**

    ## 📊 Dataset
    - Loan Prediction Dataset
    - 614 Applications

    ## 🔑 Main Features
    | Feature | Description |
    |---|---|
    | Applicant Income | Monthly income of the applicant |
    | Co-applicant Income | Monthly income of the co-applicant |
    | Loan Amount | Requested loan amount |
    | Credit History | Good / Poor credit history |
    | Education | Graduate / Not Graduate |
    | Property Area | Urban / Semiurban / Rural |
    | Loan Status | Approved (Y) / Not Approved (N) |

    ## 📋 Output
    | Result | Condition |
    |---|---|
    | ✅ ELIGIBLE | Score ≥ 70 |
    | ⚠️ MANUAL REVIEW | Score 50–69 |
    | ❌ NOT ELIGIBLE | Score < 50 |
    """)