import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# Initialize session state
if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=['Date', 'Category', 'Item', 'Amount'])

st.title("🧾 Expense Logger Chatbot")
st.write("Log your expense below:")

# Input fields
with st.form(key='expense_form'):
    col1, col2 = st.columns(2)
    category = col1.selectbox("Category", ["groceries", "entertainment", "transport", "food", "others"])
    item = col2.text_input("Item Name (e.g., soap, movie, pizza)")
    amount = st.number_input("Amount Spent (₹)", min_value=0.0, format="%.2f")
    submitted = st.form_submit_button("Log Expense")

if submitted:
    date = datetime.now()  # Full timestamp
    new_entry = pd.DataFrame([[date, category, item, amount]],
                             columns=['Date', 'Category', 'Item', 'Amount'])
    st.session_state.expenses = pd.concat([st.session_state.expenses, new_entry], ignore_index=True)
    st.success(f"📝 Logged ₹{amount:.2f} for *{item}* under *{category}*")

# 📊 Analytics
st.subheader("📊 Expense Analytics")
df = st.session_state.expenses

if not df.empty:
    df['Date'] = pd.to_datetime(df['Date'])  # Ensure Date is datetime type
    df['Day'] = df['Date'].dt.date  # Extract only date (without time)

    # 🗓️ Line Chart - Daily Spending
    daily_totals = df.groupby('Day')['Amount'].sum().reset_index()
    line_fig = px.line(daily_totals, x='Day', y='Amount', title='Daily Spending Trend')
    st.plotly_chart(line_fig, use_container_width=True)

    # 🥧 Pie Chart - Category Breakdown
    category_totals = df.groupby('Category')['Amount'].sum().reset_index()
    pie_fig = px.pie(category_totals, values='Amount', names='Category', title='Spending by Category')
    st.plotly_chart(pie_fig, use_container_width=True)

    # 📄 Show full table
    with st.expander("🔍 View Logged Expenses"):
        st.dataframe(df.drop(columns=['Day']))  # Optional: hide 'Day' column from display
else:
    st.info("No expenses logged yet.")
