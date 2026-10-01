import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# SMART LOAN APPROVAL & RISK ANALYSIS DASHBOARD
# Streamlit UI + Pandas + NumPy + Matplotlib
# ============================================================

st.set_page_config(
    page_title="Smart Loan Dashboard",
    page_icon="💰",
    layout="wide"
)

# -------------------- COLORS --------------------
BG = "#F4F7FB"
BLUE = "#2563EB"
GREEN = "#16A34A"
RED = "#DC2626"
ORANGE = "#EA580C"
PURPLE = "#7C3AED"
WHITE = "#FFFFFF"
DARK = "#172033"

# -------------------- CUSTOM CSS --------------------
st.markdown("""
<style>
.main {
    background-color: #F4F7FB;
}
.block-container {
    padding-top: 1.5rem;
}
.title-box {
    background: #2563EB;
    color: white;
    padding: 18px;
    border-radius: 12px;
    text-align: center;
    margin-bottom: 20px;
}
.kpi {
    padding: 18px;
    border-radius: 12px;
    text-align: center;
    min-height: 110px;
}
.kpi-title {
    font-size: 14px;
    font-weight: 700;
}
.kpi-value {
    font-size: 28px;
    font-weight: 800;
}
.result-box {
    padding: 18px;
    border-radius: 12px;
    color: white;
    text-align: center;
    margin-top: 15px;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# DATA
# ============================================================

@st.cache_data
def load_data():
    data = pd.read_csv("loan_prediction.csv")

    num = [
        "ApplicantIncome",
        "CoapplicantIncome",
        "LoanAmount",
        "Loan_Amount_Term",
        "Credit_History"
    ]

    cat = [
        "Gender",
        "Married",
        "Dependents",
        "Education",
        "Self_Employed",
        "Property_Area"
    ]

    for c in num:
        data[c] = pd.to_numeric(data[c], errors="coerce")
        data[c] = data[c].fillna(data[c].median())

    for c in cat:
        data[c] = data[c].fillna("Unknown")

    data = data.drop_duplicates("Loan_ID")

    data["TotalIncome"] = (
        data["ApplicantIncome"] +
        data["CoapplicantIncome"]
    )

    data["LoanAmountRupees"] = data["LoanAmount"] * 1000

    data["Outcome"] = data["Loan_Status"].map({
        "Y": "Approved",
        "N": "Not Approved"
    })

    return data


try:
    df = load_data()
except FileNotFoundError:
    st.error("loan_prediction.csv was not found. Keep the CSV file in the same GitHub repository as app7.py.")
    st.stop()


# ============================================================
# SUMMARY VALUES
# ============================================================

total = len(df)
approved = int((df["Loan_Status"] == "Y").sum())
rejected = int((df["Loan_Status"] == "N").sum())
rate = approved / total * 100 if total > 0 else 0


# ============================================================
# ELIGIBILITY LOGIC
# ============================================================

def check_eligibility(income, co_income, loan, education, self_emp, credit):
    score = 0

    if income >= 25000:
        score += 30
    elif income >= 15000:
        score += 20

    if credit == "Good":
        score += 35

    if education == "Graduate":
        score += 10

    if self_emp == "No":
        score += 5

    annual = (income + co_income) * 12
    ratio = loan / annual if annual > 0 else 999

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


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="title-box">
    <h1>💰 SMART LOAN APPROVAL & RISK ANALYSIS</h1>
    <p>Data Analysis • Eligibility Checking • Risk Analysis</p>
</div>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR MENU
# ============================================================

st.sidebar.title("📌 Navigation")

page = st.sidebar.radio(
    "Select Module",
    [
        "Dashboard",
        "Eligibility Checker",
        "Analytics",
        "Explore Data",
        "About Project"
    ]
)


# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":

    st.header("📊 Dashboard")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div class="kpi" style="background:#DBEAFE;">
                <div class="kpi-title">TOTAL APPLICATIONS</div>
                <div class="kpi-value">{total}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div class="kpi" style="background:#DCFCE7;">
                <div class="kpi-title">APPROVED</div>
                <div class="kpi-value">{approved}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""
            <div class="kpi" style="background:#FEE2E2;">
                <div class="kpi-title">NOT APPROVED</div>
                <div class="kpi-value">{rejected}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:
        st.markdown(
            f"""
            <div class="kpi" style="background:#FEF3C7;">
                <div class="kpi-title">APPROVAL RATE</div>
                <div class="kpi-value">{rate:.1f}%</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.pie(
            [approved, rejected],
            labels=["Approved", "Not Approved"],
            autopct="%1.1f%%",
            colors=[GREEN, RED]
        )
        ax.set_title("Loan Application Status")
        st.pyplot(fig)
        plt.close(fig)

    with col2:
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.scatter(
            df["TotalIncome"],
            df["LoanAmount"],
            color=BLUE,
            alpha=0.6
        )
        ax.set_title("Income vs Loan Amount")
        ax.set_xlabel("Total Income")
        ax.set_ylabel("Loan Amount")
        st.pyplot(fig)
        plt.close(fig)

    col3, col4 = st.columns(2)

    with col3:
        fig, ax = plt.subplots(figsize=(6, 4))
        df["Property_Area"].value_counts().plot(
            kind="bar",
            ax=ax,
            color=PURPLE
        )
        ax.set_title("Applications by Property Area")
        ax.set_xlabel("Property Area")
        ax.set_ylabel("Applications")
        st.pyplot(fig)
        plt.close(fig)

    with col4:
        fig, ax = plt.subplots(figsize=(6, 4))
        df["Education"].value_counts().plot(
            kind="bar",
            ax=ax,
            color=ORANGE
        )
        ax.set_title("Applications by Education")
        ax.set_xlabel("Education")
        ax.set_ylabel("Applications")
        st.pyplot(fig)
        plt.close(fig)


# ============================================================
# ELIGIBILITY CHECKER
# ============================================================

elif page == "Eligibility Checker":

    st.header("🧮 Loan Eligibility Checker")
    st.write("Enter applicant details to calculate the risk score.")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Applicant Name")

        income = st.number_input(
            "Monthly Income",
            min_value=0.0,
            value=0.0,
            step=1000.0
        )

        co_income = st.number_input(
            "Co-applicant Income",
            min_value=0.0,
            value=0.0,
            step=1000.0
        )

        loan = st.number_input(
            "Loan Amount",
            min_value=0.0,
            value=0.0,
            step=1000.0
        )

    with col2:
        education = st.selectbox(
            "Education",
            ["Select", "Graduate", "Not Graduate"]
        )

        self_emp = st.selectbox(
            "Self Employed",
            ["Select", "Yes", "No"]
        )

        credit = st.selectbox(
            "Credit History",
            ["Select", "Good", "Poor"]
        )

    check = st.button(
        "🔍 CHECK ELIGIBILITY",
        use_container_width=True
    )

    if check:

        if (
            not name.strip()
            or income <= 0
            or loan <= 0
            or education == "Select"
            or self_emp == "Select"
            or credit == "Select"
        ):
            st.error("⚠️ Please enter all required details correctly.")

        else:
            score, ratio, status = check_eligibility(
                income,
                co_income,
                loan,
                education,
                self_emp,
                credit
            )

            if status == "ELIGIBLE":
                result_color = GREEN
                risk = "LOW RISK"

            elif status == "MANUAL REVIEW":
                result_color = ORANGE
                risk = "MEDIUM RISK"

            else:
                result_color = RED
                risk = "HIGH RISK"

            st.markdown(
                f"""
                <div class="result-box" style="background:{result_color};">
                    <h2>{status}</h2>
                    <p>Applicant: {name}</p>
                    <p>Risk Score: {score}/100</p>
                    <p>Loan Ratio: {ratio:.2f}</p>
                    <p>Risk Level: {risk}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.write("")

            # Risk score graph
            fig, ax = plt.subplots(figsize=(10, 3.5))
            ax.barh(
                ["Risk Score"],
                [score],
                color=result_color
            )
            ax.set_xlim(0, 100)
            ax.set_xlabel("Score (0 - 100)")
            ax.set_title(f"Final Result: {status}")

            ax.text(
                min(score + 2, 92),
                0,
                f"{score}/100",
                va="center",
                fontweight="bold"
            )

            st.pyplot(fig)
            plt.close(fig)

            st.info(
                f"Risk: {risk}  |  Loan Ratio: {ratio:.2f}"
            )


# ============================================================
# ANALYTICS
# ============================================================

elif page == "Analytics":

    st.header("📈 Loan Analytics")

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.hist(
            df["ApplicantIncome"],
            bins=20,
            color=BLUE
        )
        ax.set_title("Applicant Income")
        ax.set_xlabel("Income")
        ax.set_ylabel("Number of Applications")
        st.pyplot(fig)
        plt.close(fig)

    with col2:
        fig, ax = plt.subplots(figsize=(6, 4))
        df["Credit_History"].value_counts().plot(
            kind="bar",
            ax=ax,
            color=GREEN
        )
        ax.set_title("Credit History")
        ax.set_xlabel("Credit History")
        ax.set_ylabel("Applications")
        st.pyplot(fig)
        plt.close(fig)

    col3, col4 = st.columns(2)

    with col3:
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.hist(
            df["LoanAmount"],
            bins=20,
            color=PURPLE
        )
        ax.set_title("Loan Amount")
        ax.set_xlabel("Loan Amount")
        ax.set_ylabel("Number of Applications")
        st.pyplot(fig)
        plt.close(fig)

    with col4:
        fig, ax = plt.subplots(figsize=(6, 4))
        df["Property_Area"].value_counts().plot(
            kind="bar",
            ax=ax,
            color=ORANGE
        )
        ax.set_title("Property Area")
        ax.set_xlabel("Property Area")
        ax.set_ylabel("Applications")
        st.pyplot(fig)
        plt.close(fig)


# ============================================================
# EXPLORE DATA
# ============================================================

elif page == "Explore Data":

    st.header("🔎 Explore Loan Data")

    st.write(
        f"Dataset contains **{len(df)} applications** "
        f"and **{len(df.columns)} columns**."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        status_filter = st.selectbox(
            "Status",
            ["All", "Approved", "Not Approved"]
        )

    with col2:
        education_filter = st.selectbox(
            "Education",
            ["All", "Graduate", "Not Graduate"]
        )

    with col3:
        property_filter = st.selectbox(
            "Property Area",
            ["All", "Urban", "Semiurban", "Rural"]
        )

    filtered = df.copy()

    if status_filter == "Approved":
        filtered = filtered[
            filtered["Loan_Status"] == "Y"
        ]

    elif status_filter == "Not Approved":
        filtered = filtered[
            filtered["Loan_Status"] == "N"
        ]

    if education_filter != "All":
        filtered = filtered[
            filtered["Education"] == education_filter
        ]

    if property_filter != "All":
        filtered = filtered[
            filtered["Property_Area"] == property_filter
        ]

    st.info(
        f"Showing {len(filtered)} of {len(df)} applications"
    )

    columns = [
        "Loan_ID",
        "Gender",
        "Education",
        "ApplicantIncome",
        "CoapplicantIncome",
        "LoanAmount",
        "Credit_History",
        "Property_Area",
        "Loan_Status"
    ]

    st.dataframe(
        filtered[columns],
        use_container_width=True,
        height=500
    )


# ============================================================
# ABOUT PROJECT
# ============================================================

elif page == "About Project":

    st.header("ℹ️ About Smart Loan")

    st.markdown("""
    ## SMART LOAN APPROVAL & RISK ANALYSIS

    ### PROJECT OBJECTIVE

    Analyze loan applications and provide
    a simple eligibility decision.

    ### TECHNOLOGIES

    • Python  
    • Pandas  
    • NumPy  
    • Matplotlib  
    • Streamlit

    ### DATASET

    Loan Prediction Dataset

    ### MAIN FEATURES

    • Applicant Income  
    • Co-applicant Income  
    • Loan Amount  
    • Credit History  
    • Education  
    • Property Area  
    • Loan Status

    ### OUTPUT

    • ELIGIBLE  
    • MANUAL REVIEW  
    • NOT ELIGIBLE

    ### PROJECT MODULES

    1. Dashboard
    2. Eligibility Checker
    3. Analytics
    4. Explore Data
    5. About Project
    """)

    st.success(
        "The dashboard analyzes historical loan application data "
        "and provides a rule-based eligibility score."
    )
