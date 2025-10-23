import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import csv
import os

# === Ensure folders exist ===
os.makedirs("data", exist_ok=True)
os.makedirs("finance", exist_ok=True)

# === Auto-create missing files ===
def create_file_if_missing(path, headers, rows):
    if not os.path.exists(path):
        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)

create_file_if_missing(
    "data/customers.csv",
    ["customer_id", "customer_name", "region", "total_spent", "email", "phone"],
    [
        {"customer_id": 1, "customer_name": "John Smith", "region": "West", "total_spent": 5400, "email": "john@example.com", "phone": "555-111-2222"},
        {"customer_id": 2, "customer_name": "Emily Jones", "region": "East", "total_spent": 7200, "email": "emily@example.com", "phone": "555-333-4444"},
    ],
)

create_file_if_missing(
    "data/products.csv",
    ["product_id", "product_name", "category", "price"],
    [
        {"product_id": 101, "product_name": "SmartSync AI Assistant", "category": "Software", "price": 149},
        {"product_id": 102, "product_name": "ThinkBoard Dashboard", "category": "Software", "price": 199},
    ],
)

create_file_if_missing(
    "data/transactions.csv",
    ["transaction_id", "customer_id", "product_id", "amount"],
    [
        {"transaction_id": 5001, "customer_id": 1, "product_id": 101, "amount": 149},
        {"transaction_id": 5002, "customer_id": 2, "product_id": 102, "amount": 199},
    ],
)

create_file_if_missing(
    "finance/monthly_pnl.csv",
    ["month", "revenue", "expenses", "profit"],
    [
        {"month": "Jan", "revenue": 2500, "expenses": 1800, "profit": 700},
        {"month": "Feb", "revenue": 3200, "expenses": 2100, "profit": 1100},
    ],
)

# === Load Data ===
customers = pd.read_csv("data/customers.csv")
products = pd.read_csv("data/products.csv")
transactions = pd.read_csv("data/transactions.csv")
pnl = pd.read_csv("finance/monthly_pnl.csv")

print("✅ All data files loaded successfully!")

# === View Data ===
def view_data(table):
    if table == "Customers":
        return pd.read_csv("data/customers.csv")
    elif table == "Products":
        return pd.read_csv("data/products.csv")
    elif table == "Transactions":
        return pd.read_csv("data/transactions.csv")
    elif table == "Profit & Loss":
        return pd.read_csv("finance/monthly_pnl.csv")

# === Add Customer ===
def add_customer(name, region, spent, email, phone):
    if not name or not region or not spent or not email or not phone:
        return "⚠️ Please fill in all fields."

    df = pd.read_csv("data/customers.csv")
    new_id = len(df) + 1
    new_row = {
        "customer_id": new_id,
        "customer_name": name,
        "region": region,
        "total_spent": spent,
        "email": email,
        "phone": phone
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv("data/customers.csv", index=False)
    return f"✅ Added {name} to customer list!"

# ---------------- THINKSYNiQ DASHBOARD ----------------
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="ThinkSYNiQ Dashboard", layout="wide")

# --- Toggle between Admin & Customer ---
role = st.radio("Select Mode:", ["Admin", "Customer"], horizontal=True)

st.markdown("<h1 style='text-align:center; color:#001f3f;'>💼 ThinkSYNiQ Company Dashboard</h1>", unsafe_allow_html=True)

# --- Tabs for Admin View ---
if role == "Admin":
    tabs = st.tabs(["Customers", "Products", "Transactions", "P&L"])

    with tabs[0]:
        st.subheader("Manage Customers")
        st.text_input("Customer Name")
        st.text_input("Email Address")
        st.text_input("Phone Number")
        st.button("Add Customer")

    with tabs[1]:
        st.subheader("Manage Products")
        st.text_input("Product Name")
        st.number_input("Price ($)", min_value=0.0, step=0.01)
        st.button("Add Product")

    with tabs[2]:
        st.subheader("Transactions")
        st.selectbox("Select Customer", ["Sarah Jones", "Michael Brown"])
        st.selectbox("Select Product", ["Consultation", "Website Package"])
        st.number_input("Quantity", min_value=1, step=1)
        st.button("Add Transaction")

    with tabs[3]:
        st.subheader("Profit & Loss Overview")
        st.write("Financial charts and summaries will appear here.")
        sample_data = pd.DataFrame({
            "Month": ["Jan", "Feb", "Mar"],
            "Revenue": [4000, 6000, 8000],
            "Expenses": [2500, 3000, 3500]
        })
        sample_data["Profit"] = sample_data["Revenue"] - sample_data["Expenses"]
        fig = px.line(sample_data, x="Month", y=["Revenue", "Expenses", "Profit"], markers=True)
        st.plotly_chart(fig, use_container_width=True)

# --- Customer Webpage View ---
else:
    st.subheader("Welcome to ThinkSYNiQ Services")
    st.write("Explore our available products and services below:")
    st.dataframe(pd.DataFrame({
        "Product": ["Consultation", "AI Strategy Session", "Website Package"],
        "Price": ["$49.99", "$199.99", "$499.99"]
    }))

# --- Floating Chatbot (bottom-right) ---
st.markdown("""
    <style>
        .chatbot-container {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background-color: #001f3f;
            color: white;
            padding: 15px;
            border-radius: 12px;
            box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
            width: 300px;
        }
        .chatbot-input {
            width: 100%;
            padding: 5px;
            border-radius: 8px;
            margin-top: 10px;
        }
    </style>
    <div class="chatbot-container">
        <strong>💬 ThinkSYNiQ Assistant</strong><br>
        <em>Ask me about products, pricing, or services!</em>
        <input class="chatbot-input" placeholder="Type your question..." />
    </div>
""", unsafe_allow_html=True)

