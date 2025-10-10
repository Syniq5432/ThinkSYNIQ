import gradio as gr
import pandas as pd
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

# === UI Layout ===
with gr.Blocks(theme=gr.themes.Soft(
    primary_hue=gr.themes.colors.slate,
    secondary_hue=gr.themes.colors.blue,
    neutral_hue=gr.themes.colors.gray,
)) as ui:
    gr.Markdown("## 💼 ThinkSYNIQ Company Dashboard")

    with gr.Group():
        table = gr.Radio(["Customers", "Products", "Transactions", "Profit & Loss"], label="Choose a Table")
        output = gr.Dataframe(label="Output")
        submit = gr.Button("Submit")
        submit.click(fn=view_data, inputs=table, outputs=output)

    gr.Markdown("---\n### ➕ Add New Customer")
    new_name = gr.Textbox(label="Customer Name")
    new_region = gr.Textbox(label="Region")
    new_spent = gr.Textbox(label="Total Spent")
    new_email = gr.Textbox(label="Email")
    new_phone = gr.Textbox(label="Phone Number")
    add_btn = gr.Button("Add Customer")
    status = gr.Textbox(label="Status")
    add_btn.click(add_customer, [new_name, new_region, new_spent, new_email, new_phone], status)

print("🚀 Launching ThinkSYNIQ dashboard...")
ui.launch()
