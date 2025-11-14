# 💰 Simple Personal Finance Tracker with Delete Option
# Made with Streamlit

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# ---------------------------
# 🎨 Page Configuration
# ---------------------------
st.set_page_config(page_title="Finance Tracker", page_icon="💰", layout="centered")

st.title("💰 Personal Finance Tracker")
st.markdown("A clean, simple, and easy-to-use app to manage your income & expenses. 💵")
st.divider()

# ---------------------------
# 🏦 Initialize Session Data
# ---------------------------
if "transactions" not in st.session_state:
    st.session_state.transactions = []

# ---------------------------
# 🧾 Add Transaction Section
# ---------------------------
st.subheader("➕ Add New Transaction")

with st.form("add_form", clear_on_submit=True):
    date = st.date_input("Date", datetime.now())
    trans_type = st.radio("Transaction Type", ["Income", "Expense"], horizontal=True)
    category = st.text_input("Category (e.g., Food, Salary, Rent)")
    amount = st.number_input("Amount (₹)", min_value=0.0, step=100.0)
    note = st.text_area("Note (optional)", height=50)
    add_btn = st.form_submit_button("Add Transaction")

    if add_btn and amount > 0 and category.strip() != "":
        st.session_state.transactions.append({
            "Date": date,
            "Type": trans_type,
            "Category": category.strip(),
            "Amount": amount,
            "Note": note.strip()
        })
        st.success(f"{trans_type} of ₹{amount:.2f} added under {category} ✅")

# ---------------------------
# 📋 Transaction Table
# ---------------------------
if st.session_state.transactions:
    st.divider()
    st.subheader("📊 Transaction History")

    df = pd.DataFrame(st.session_state.transactions)
    df["Date"] = pd.to_datetime(df["Date"]).dt.date

    # Show the table
    st.dataframe(df, use_container_width=True)

    # ---------------------------
    # ❌ Delete Transaction Section
    # ---------------------------
    st.subheader("🗑️ Delete a Transaction")

    delete_index = st.number_input(
        "Enter the row number to delete (starting from 0):",
        min_value=0,
        max_value=len(df) - 1,
        step=1,
    )
    if st.button("Delete Selected Transaction"):
        removed = st.session_state.transactions.pop(delete_index)
        st.warning(f"Deleted {removed['Type']} of ₹{removed['Amount']} ({removed['Category']})")

    # ---------------------------
    # 💡 Summary Section
    # ---------------------------
    st.divider()
    st.subheader("💡 Summary")

    total_income = df[df["Type"] == "Income"]["Amount"].sum()
    total_expense = df[df["Type"] == "Expense"]["Amount"].sum()
    balance = total_income - total_expense

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"₹{total_income:,.2f}")
    col2.metric("Total Expense", f"₹{total_expense:,.2f}")
    col3.metric("Balance", f"₹{balance:,.2f}")

    # ---------------------------
    # 📈 Expense Breakdown Chart
    # ---------------------------
    st.divider()
    st.subheader("📉 Expense Breakdown")

    expense_df = df[df["Type"] == "Expense"].groupby("Category")["Amount"].sum()

    if not expense_df.empty:
        fig, ax = plt.subplots()
        ax.pie(expense_df, labels=expense_df.index, autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
        ax.set_title("Expenses by Category")
        st.pyplot(fig) 
    else:
        st.info("No expense data available for chart.")
else:
    st.info("No transactions yet. Add one above 👆")

# ---------------------------
# ✅ Footer
# ---------------------------
st.divider()
st.caption("💻 Built with Streamlit | Simple Finance Tracker with Delete Feature")