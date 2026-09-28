import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk

# =====================================================
# LOAD + CLEAN DATA
# =====================================================

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

df["TotalIncome"] = df["ApplicantIncome"] + df["CoapplicantIncome"]
df["LoanAmountRupees"] = df["LoanAmount"] * 1000
df["Outcome"] = df["Loan_Status"].map({"Y": "Approved", "N": "Not Approved"})

total = len(df)
approved = (df.Loan_Status == "Y").sum()
rejected = (df.Loan_Status == "N").sum()
rate = approved / total * 100

print("\nSMART LOAN APPROVAL & RISK ANALYSIS")
print("=" * 50)
print("Dataset loaded:", total, "applications")
print("Approved:", approved)
print("Not Approved:", rejected)
print("Approval Rate:", round(rate, 2), "%")


# =====================================================
# COLORS
# =====================================================

BG = "#F4F7FB"
BLUE = "#2563EB"
GREEN = "#16A34A"
RED = "#DC2626"
ORANGE = "#EA580C"
PURPLE = "#7C3AED"
WHITE = "#FFFFFF"
DARK = "#172033"


# =====================================================
# DASHBOARD
# =====================================================

def dashboard():

    fig = plt.figure(figsize=(12, 8), facecolor=BG)
    fig.canvas.manager.set_window_title("Smart Loan - Dashboard")

    fig.suptitle(
        "SMART LOAN APPROVAL & RISK ANALYSIS",
        fontsize=20, fontweight="bold", color=DARK
    )

    cards = [
        ("TOTAL APPLICATIONS", total, "#DBEAFE"),
        ("APPROVED", approved, "#DCFCE7"),
        ("NOT APPROVED", rejected, "#FEE2E2"),
        ("APPROVAL RATE", f"{rate:.1f}%", "#FEF3C7")
    ]

    for i, (title, value, color) in enumerate(cards):
        ax = fig.add_axes([.04+i*.24, .75, .21, .12])
        ax.set_facecolor(color)
        ax.axis("off")
        ax.text(.5, .5, f"{title}\n{value}",
                ha="center", va="center",
                fontsize=14, fontweight="bold", color=DARK)

    ax = fig.add_axes([.07, .40, .38, .27])
    ax.pie(
        [approved, rejected],
        labels=["Approved", "Not Approved"],
        autopct="%1.1f%%",
        colors=[GREEN, RED],
        startangle=90
    )
    ax.set_title("Loan Application Status", color=DARK)

    ax = fig.add_axes([.55, .40, .38, .27])
    ax.scatter(
        df.TotalIncome,
        df.LoanAmount,
        alpha=.6,
        color=BLUE
    )
    ax.set_title("Income vs Loan Amount")
    ax.set_xlabel("Total Income")
    ax.set_ylabel("Loan Amount")

    ax = fig.add_axes([.07, .07, .38, .24])
    df.Property_Area.value_counts().plot(
        kind="bar", ax=ax, color=PURPLE
    )
    ax.set_title("Applications by Property Area")

    ax = fig.add_axes([.55, .07, .38, .24])
    df.Education.value_counts().plot(
        kind="bar", ax=ax, color=ORANGE
    )
    ax.set_title("Applications by Education")

    plt.show()


# =====================================================
# ELIGIBILITY LOGIC
# =====================================================

def check_eligibility(income, co_income, loan,
                      education, self_employed, credit):

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
# ELIGIBILITY CHECKER
# =====================================================

def eligibility_checker():

    root = tk.Tk()
    root.title("Smart Loan - Eligibility Checker")
    root.geometry("650x600")
    root.configure(bg=BG)

    tk.Label(
        root,
        text="LOAN ELIGIBILITY CHECKER",
        font=("Arial", 20, "bold"),
        bg=BLUE,
        fg=WHITE,
        pady=12
    ).pack(fill="x")

    frame = tk.Frame(root, bg=BG)
    frame.pack(pady=20)

    def add_label(text, row):
        tk.Label(
            frame, text=text,
            font=("Arial", 11, "bold"),
            bg=BG, fg=DARK
        ).grid(row=row, column=0, sticky="w", pady=8)

    add_label("Applicant Name", 0)
    name = tk.Entry(frame, width=32)
    name.grid(row=0, column=1)

    add_label("Monthly Income", 1)
    income = tk.Entry(frame, width=32)
    income.grid(row=1, column=1)

    add_label("Co-applicant Income", 2)
    co_income = tk.Entry(frame, width=32)
    co_income.grid(row=2, column=1)

    add_label("Loan Amount", 3)
    loan = tk.Entry(frame, width=32)
    loan.grid(row=3, column=1)

    add_label("Education", 4)
    edu = ttk.Combobox(
        frame, values=["Graduate", "Not Graduate"],
        state="readonly", width=29
    )
    edu.set("Graduate")
    edu.grid(row=4, column=1)

    add_label("Self Employed", 5)
    self_emp = ttk.Combobox(
        frame, values=["Yes", "No"],
        state="readonly", width=29
    )
    self_emp.set("No")
    self_emp.grid(row=5, column=1)

    add_label("Credit History", 6)
    credit = ttk.Combobox(
        frame, values=["Good", "Poor"],
        state="readonly", width=29
    )
    credit.set("Good")
    credit.grid(row=6, column=1)

    result = tk.Label(
        root,
        text="",
        font=("Arial", 13, "bold"),
        bg=BG,
        fg=DARK,
        justify="center"
    )
    result.pack(pady=15)

    def calculate():

        try:
            score, ratio, status = check_eligibility(
                float(income.get()),
                float(co_income.get()),
                float(loan.get()),
                edu.get(),
                self_emp.get(),
                credit.get()
            )

            colors = {
                "ELIGIBLE": GREEN,
                "MANUAL REVIEW": ORANGE,
                "NOT ELIGIBLE": RED
            }

            result.config(
                text=f"Applicant: {name.get()}\n"
                     f"Risk Score: {score}/100\n"
                     f"Loan Ratio: {ratio:.2f}\n"
                     f"FINAL RESULT: {status}",
                bg=colors[status],
                fg=WHITE,
                padx=20,
                pady=10
            )

        except ValueError:
            result.config(
                text="⚠ Please enter valid numeric values!",
                bg=RED,
                fg=WHITE,
                padx=20,
                pady=10
            )

    tk.Button(
        root,
        text="CHECK ELIGIBILITY",
        command=calculate,
        font=("Arial", 12, "bold"),
        bg=BLUE,
        fg=WHITE,
        activebackground=PURPLE,
        activeforeground=WHITE,
        padx=25,
        pady=8
    ).pack()

    root.mainloop()


# =====================================================
# ANALYTICS
# =====================================================

def analytics():

    fig, ax = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle(
        "LOAN ANALYTICS",
        fontsize=20,
        fontweight="bold",
        color=DARK
    )

    ax[0,0].hist(
        df.ApplicantIncome,
        bins=20,
        color=BLUE
    )
    ax[0,0].set_title("Applicant Income")

    df.Credit_History.value_counts().plot(
        kind="bar",
        ax=ax[0,1],
        color=GREEN
    )
    ax[0,1].set_title("Credit History")

    ax[1,0].hist(
        df.LoanAmount,
        bins=20,
        color=PURPLE
    )
    ax[1,0].set_title("Loan Amount")

    df.Property_Area.value_counts().plot(
        kind="bar",
        ax=ax[1,1],
        color=ORANGE
    )
    ax[1,1].set_title("Property Area")

    plt.tight_layout()
    plt.show()


# =====================================================
# EXPLORE DATA
# =====================================================

def explore_data():

    root = tk.Tk()
    root.title("Smart Loan - Explore Data")
    root.geometry("1250x700")
    root.configure(bg=BG)

    tk.Label(
        root,
        text="EXPLORE LOAN DATA",
        font=("Arial", 20, "bold"),
        bg=BLUE,
        fg=WHITE,
        pady=10
    ).pack(fill="x")

    filters = tk.Frame(root, bg=BG)
    filters.pack(pady=10)

    def combo(text, values):
        tk.Label(
            filters,
            text=text,
            bg=BG,
            fg=DARK,
            font=("Arial", 10, "bold")
        ).pack(side="left", padx=5)

        box = ttk.Combobox(
            filters,
            values=values,
            state="readonly",
            width=15
        )
        box.set("All")
        box.pack(side="left", padx=8)
        return box

    status = combo(
        "Status:",
        ["All", "Approved", "Not Approved"]
    )

    education = combo(
        "Education:",
        ["All", "Graduate", "Not Graduate"]
    )

    property_area = combo(
        "Property:",
        ["All", "Urban", "Semiurban", "Rural"]
    )

    columns = [
        "Loan_ID", "Gender", "Education",
        "ApplicantIncome", "CoapplicantIncome",
        "LoanAmount", "Credit_History",
        "Property_Area", "Loan_Status"
    ]

    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True, padx=15)

    tree = ttk.Treeview(
        frame,
        columns=columns,
        show="headings"
    )

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=130, anchor="center")

    scroll_y = ttk.Scrollbar(
        frame, orient="vertical",
        command=tree.yview
    )

    scroll_x = ttk.Scrollbar(
        frame, orient="horizontal",
        command=tree.xview
    )

    tree.configure(
        yscrollcommand=scroll_y.set,
        xscrollcommand=scroll_x.set
    )

    tree.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")
    scroll_x.grid(row=1, column=0, sticky="ew")

    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    # Row colors
    tree.tag_configure(
        "approved",
        background="#DCFCE7"
    )

    tree.tag_configure(
        "rejected",
        background="#FEE2E2"
    )

    def display():

        filtered = df.copy()

        if status.get() == "Approved":
            filtered = filtered[filtered.Loan_Status == "Y"]

        elif status.get() == "Not Approved":
            filtered = filtered[filtered.Loan_Status == "N"]

        if education.get() != "All":
            filtered = filtered[
                filtered.Education == education.get()
            ]

        if property_area.get() != "All":
            filtered = filtered[
                filtered.Property_Area == property_area.get()
            ]

        tree.delete(*tree.get_children())

        for _, row in filtered.iterrows():

            tag = (
                "approved"
                if row.Loan_Status == "Y"
                else "rejected"
            )

            tree.insert(
                "",
                "end",
                values=[row[c] for c in columns],
                tags=(tag,)
            )

        count.config(
            text=f"Showing {len(filtered)} of {len(df)} applications"
        )

    count = tk.Label(
        root,
        text="",
        font=("Arial", 11, "bold"),
        bg=BG,
        fg=BLUE
    )
    count.pack(pady=7)

    for box in [status, education, property_area]:
        box.bind(
            "<<ComboboxSelected>>",
            lambda e: display()
        )

    display()
    root.mainloop()


# =====================================================
# ABOUT
# =====================================================

def about_project():

    root = tk.Tk()
    root.title("About Smart Loan")
    root.geometry("650x550")
    root.configure(bg=BG)

    tk.Label(
        root,
        text="SMART LOAN APPROVAL & RISK ANALYSIS",
        font=("Arial", 18, "bold"),
        bg=BLUE,
        fg=WHITE,
        pady=15
    ).pack(fill="x")

    text = """
PROJECT OBJECTIVE

Analyze loan applications and provide
a simple eligibility decision.

TECHNOLOGIES

• Python
• Pandas
• NumPy
• Matplotlib
• Tkinter

DATASET

Loan Prediction Dataset
614 Applications

MAIN FEATURES

• Applicant Income
• Co-applicant Income
• Loan Amount
• Credit History
• Education
• Property Area
• Loan Status

OUTPUT

• ELIGIBLE
• MANUAL REVIEW
• NOT ELIGIBLE
"""

    tk.Label(
        root,
        text=text,
        font=("Arial", 12),
        bg=BG,
        fg=DARK,
        justify="left"
    ).pack(pady=25)

    root.mainloop()


# =====================================================
# MAIN MENU
# =====================================================

while True:

    print("\n" + "="*50)
    print("SMART LOAN APPROVAL & RISK ANALYSIS")
    print("="*50)

    print("1. Dashboard")
    print("2. Eligibility Checker")
    print("3. Analytics")
    print("4. Explore Data")
    print("5. About Project")
    print("6. Exit")

    choice = input("\nEnter choice (1-6): ")

    if choice == "1":
        dashboard()

    elif choice == "2":
        eligibility_checker()

    elif choice == "3":
        analytics()

    elif choice == "4":
        explore_data()

    elif choice == "5":
        about_project()

    elif choice == "6":
        print("\nThank you!")
        break

    else:
        print("Invalid choice!")