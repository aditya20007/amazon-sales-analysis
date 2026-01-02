import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ===============================
# PROJECT HEADER
# ===============================
print("=" * 60)
print("📦 AMAZON SALES PERFORMANCE ANALYSIS")
print("=" * 60)

# ===============================
# LOAD DATA
# ===============================
print("\n📂 Loading dataset...")

df = pd.read_csv("data/Amazon Sale Report.csv", low_memory=False)

print(f"✅ Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")

# ===============================
# BASIC INFO
# ===============================
print("\n🔍 Dataset Info:")
print(df.info())

# ===============================
# CLEANING DATA
# ===============================
print("\n🧹 Data Cleaning Started...")

# Drop unwanted columns
drop_cols = ['index', 'Unnamed: 22']
df.drop(columns=[c for c in drop_cols if c in df.columns], inplace=True)

# Rename columns for consistency
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Convert date
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Convert numeric columns
df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
df['qty'] = pd.to_numeric(df['qty'], errors='coerce')

# Remove cancelled orders
df = df[df['status'] != 'Cancelled']

# Handle missing values
df.dropna(subset=['amount', 'qty'], inplace=True)

print("✅ Cleaning completed")

# ===============================
# FEATURE ENGINEERING
# ===============================
print("\n🧠 Feature Engineering...")

df['month'] = df['date'].dt.to_period('M').astype(str)
df['year'] = df['date'].dt.year
df['revenue'] = df['amount']

print("✅ New features created")

# ===============================
# KPI CALCULATIONS
# ===============================
print("\n📊 Key Metrics")

total_orders = df['order_id'].nunique()
total_revenue = df['revenue'].sum()
total_quantity = df['qty'].sum()

print(f"🧾 Total Orders   : {total_orders}")
print(f"💰 Total Revenue  : ₹{round(total_revenue, 2)}")
print(f"📦 Total Quantity : {total_quantity}")

# ===============================
# VISUALIZATIONS
# ===============================
os.makedirs("outputs/charts", exist_ok=True)

print("\n📈 Creating visualizations...")

# Monthly Sales Trend
monthly_sales = df.groupby('month')['revenue'].sum()

plt.figure(figsize=(12, 6))
monthly_sales.plot(marker='o')
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("outputs/charts/monthly_sales.png")
plt.close()

# Top Categories
top_categories = df.groupby('category')['revenue'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(10, 6))
sns.barplot(x=top_categories.values, y=top_categories.index)
plt.title("Top 10 Categories by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Category")
plt.tight_layout()
plt.savefig("outputs/charts/top_categories.png")
plt.close()

# Order Status Distribution
plt.figure(figsize=(8, 5))
df['status'].value_counts().plot(kind='bar')
plt.title("Order Status Distribution")
plt.xlabel("Status")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("outputs/charts/order_status.png")
plt.close()

print("✅ Charts saved in outputs/charts")

# ===============================
# SAVE CLEANED DATA FOR POWER BI
# ===============================
df.to_csv("outputs/cleaned_amazon_sales.csv", index=False)

print("\n💾 Cleaned dataset saved for Power BI")
print("📁 File: outputs/cleaned_amazon_sales.csv")

print("\n🎉 ANALYSIS COMPLETED SUCCESSFULLY")
print("=" * 60)
