# Smart Loan Approval & Credit Risk Intelligence OS

A full-stack, enterprise-grade Python and Streamlit credit risk underwriting platform engineered to evaluate loan applications, uncover credit risk drivers, and perform transparent, rule-based loan eligibility evaluation with interactive financial modeling.

---

## 📌 Project Overview

The **Smart Loan Approval & Credit Risk Intelligence OS** is designed around real-world retail banking workflows. It ingests borrower data (`loan_prediction.csv`), performs automated data cleaning and feature engineering, generates publication-grade Matplotlib visualizations, and delivers an audit-ready scoring engine with financial capacity modeling, deep interactive exploration, and dynamic visual theming.

### 🌟 Key Interactive Capabilities

1. **🎨 Interactive Theme & Background Switcher:**
   * Eliminates static black backgrounds with bright, clean, interactive styling.
   * Lets users choose between:
     * ☀️ **FinTech Pure Light (Default):** Soft pearl canvas (`#f8fafc`), clean white cards, deep slate text.
     * 💎 **Soft Azure Blue:** Cool azure slate (`#eef4fa`), white cards, sapphire accents.
     * 🌿 **Emerald Wealth Green:** Fresh sage (`#f0fdf4`), white cards, emerald wealth accents.
     * 🌙 **Midnight Slate (Dark Mode):** Modern midnight slate (`#0f172a`), illuminated cards.
     * 🎨 **Custom Canvas Color:** Integrated interactive `st.color_picker` allowing users to choose ANY custom background color in real time!
   * All Matplotlib figures, cards, and labels dynamically adapt their colors to match the chosen theme.

2. **🎛 Interactive Executive Dashboard Cohort Slicers:**
   * Dynamic cohort filtering by Property Area, Education, and Credit History directly on the main dashboard.
   * Executive KPI metric cards (Total Applications, Approved, Rejected, Approval Rate) and charts adapt reactively in real time.

3. **🎨 Interactive Analytics Chart Studio:**
   * Custom variable scatter plotter allowing users to select any X-axis, Y-axis, and color segmentation dimension (`Outcome`, `Credit_History`, `Education`, `Property_Area`, `Self_Employed`) with optional trendline regression.

4. **🎮 Underwriter Challenge (Interactive Intuition Game):**
   * A gamified mode where users are presented with real anonymized applicant dossiers from the dataset and must decide whether to **APPROVE** or **REJECT** the loan before the historical verdict is revealed.
   * Tracks user accuracy, compares against the automated rule engine score, and maintains a live session performance score.

5. **🚀 Prepayment & Accelerated Debt Payoff Simulator:**
   * Interactive slider for monthly prepayments showing compounding interest savings and months shaved off the loan tenure.
   * Side-by-side comparison between standard amortization and accelerated payoff.

6. **⚔️ Head-to-Head Applicant Comparator:**
   * Select any two applicants from the database to compare their financial ratios, credit histories, requested loans, and sanction verdicts side-by-side in a comparative matrix.

7. **⚡ Automated Underwriting Simulator & What-If Optimizer:**
   * Interactive sliders for primary income, co-applicant income, and requested loan amount.
   * Semi-circular polar credit risk speedometer gauge.
   * What-If scenario optimizer calculating max qualified loan limits and required co-borrower earnings.
   * Formal printable/downloadable credit assessment memo and sanction letter.

8. **💰 Dedicated EMI & Debt Obligation (FOIR) Calculator:**
   * Computes monthly EMI, total interest, total repayment, and debt-to-income burden (FOIR) with safe (<40%), moderate (40-50%), and high-risk (>50%) thresholds.
   * Principal vs. Interest cost breakdown donut chart and 6-tenure comparison matrix.

9. **📂 Batch Applicant CSV Upload & Scorer:**
   * Upload new candidate CSV files to run automated batch scoring and export results with one click.

---

## 🗂 Dataset Schema

The system processes `loan_prediction.csv` containing **614 records** across **13 raw columns**:

| Column Name | Type | Description |
| :--- | :--- | :--- |
| `Loan_ID` | String | Unique application identifier |
| `Gender` | String | Applicant gender (`Male` / `Female`) |
| `Married` | String | Marital status (`Yes` / `No`) |
| `Dependents` | String | Number of dependents (`0`, `1`, `2`, `3+`) |
| `Education` | String | Educational status (`Graduate` / `Not Graduate`) |
| `Self_Employed` | String | Employment status (`Yes` / `No`) |
| `ApplicantIncome`| Numeric | Primary applicant monthly income (₹) |
| `CoapplicantIncome`| Numeric | Co-applicant monthly income (₹) |
| `LoanAmount` | Numeric | Loan amount in ₹ Thousands |
| `Loan_Amount_Term`| Numeric | Repayment term in months |
| `Credit_History` | Numeric | Repayment history (`1.0` = Good, `0.0` = Poor) |
| `Property_Area` | String | Collateral area (`Urban`, `Semiurban`, `Rural`) |
| `Loan_Status` | String | Historical sanction decision (`Y` / `N`) |

---

## 📐 Scoring Rules Specification

The simulator evaluates applicants on a **0 to 100 point scale**:

### 1. Applicant Monthly Income
* `Income >= ₹25,000` $\rightarrow$ **+30 points**
* `Income >= ₹15,000` $\rightarrow$ **+20 points**
* `Income < ₹15,000` $\rightarrow$ **+0 points**

### 2. Credit History (CIBIL / Experian)
* `Good Credit History (1.0)` $\rightarrow$ **+35 points**
* `Poor / Adverse Credit (0.0)` $\rightarrow$ **+0 points**

### 3. Education Qualification
* `Graduate` $\rightarrow$ **+10 points**
* `Not Graduate` $\rightarrow$ **+0 points**

### 4. Employment Stability
* `Self Employed = No (Salaried)` $\rightarrow$ **+5 points**
* `Self Employed = Yes` $\rightarrow$ **+0 points**

### 5. Loan-to-Annual-Income Ratio
$$\text{Annual Income} = (\text{Applicant Income} + \text{Co-applicant Income}) \times 12$$
$$\text{Loan Ratio} = \frac{\text{Loan Amount}}{\text{Annual Income}}$$

* `Loan Ratio <= 3.0` $\rightarrow$ **+20 points**
* `Loan Ratio <= 5.0` $\rightarrow$ **+10 points**
* `Loan Ratio > 5.0` $\rightarrow$ **+0 points**

---

## 🏆 Decision Tiers

| Score Range | Verdict | Action & Risk Tier |
| :---: | :---: | :--- |
| **70 – 100** | 🟢 **ELIGIBLE** | Low credit risk. Meets all primary solvency benchmarks. Fast-track sanction. |
| **50 – 69** | 🟡 **MANUAL REVIEW** | Moderate risk. Referred to credit underwriting committee for secondary verification. |
| **0 – 49** | 🔴 **NOT ELIGIBLE** | Elevated risk of default. Fails baseline debt-to-income or credit track record. |

---

## 🖥 Application Navigation

1. **🏠 Executive Dashboard:** Dynamic cohort slicers, portfolio KPIs, Donut chart, and Income vs Loan scatter.
2. **📊 Portfolio Analytics:** Categorical approval charts, financial distributions, Interactive Chart Studio, and statistical crosstabs.
3. **📝 Eligibility Checker & Optimizer:** Live underwriting simulator with sliders, semi-circular risk gauge, What-If optimizer, printable sanction memo, and Underwriter Challenge game.
4. **💰 EMI & Debt Capacity Calculator:** Monthly EMI calculator, FOIR debt burden meter, interest breakdown chart, multi-tenure matrix, and accelerated prepayment savings simulator.
5. **🔍 Loan Application Explorer:** Multi-criteria filters, `Loan_ID` search, applicant deep-dive dossiers, head-to-head comparison battle, and CSV export.
6. **ℹ️ Data Pipeline & Model Benchmark:** 10-step data processing verification, historical model validation matrix, and batch CSV upload tool.

---

## 🚀 Execution Instructions

### Running with Streamlit
```powershell
.\venv\Scripts\streamlit run app.py
```

### Running with Direct Python
```powershell
.\venv\Scripts\python app.py
```
*(Direct execution automatically spins up the Streamlit server and opens `http://localhost:8501`)*

---

## 📦 Technology Stack
* **Python 3.10+**
* **Pandas** — Vectorized data transformations and missing value imputation
* **NumPy** — Mathematical operations and conditional arrays
* **Matplotlib** — High-resolution publication charts, polar gauges, and financial distributions
* **Streamlit** — Modern reactive web application framework
