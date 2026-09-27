"""
Project: Amazon Sales Data - Cleaning & Visualization
Level: Beginner
Tools: Python, Pandas, Matplotlib

WHAT THIS PROJECT DOES:
1. Reads Amazon sales data (amazon_csv_100.csv)
2. Cleans the data (fixes data types, trims text, checks for
   missing values / duplicates, parses dates)
3. Visualizes the cleaned data using FOUR charts, one after another,
   using plt.show():
   - Bar chart   -> total revenue by product category
   - Pie chart   -> share of orders by payment method
   - Line chart  -> monthly revenue trend over time
   - Scatter     -> price vs. rating (colored by category)

HOW TO RUN:
1. Make sure amazon_csv_100.csv is in the same folder as this file
2. Run: python analyze_amazon_data.py
3. It will print cleaning info + a summary in the terminal, then pop
   up each chart window one by one. Close a chart window to move on
   to the next one.
"""

import pandas as pd
import matplotlib.pyplot as plt

# =======================================================
# STEP 1: Load the data
# =======================================================
df = pd.read_csv("amazon_csv_100.csv")

print("Step 1: Data loaded successfully!")
print(f"Total rows: {len(df)}, Total columns: {len(df.columns)}")
print()

# =======================================================
# STEP 2: Explore the data (before cleaning)
# =======================================================
print("Step 2: Initial data check")
print("-" * 40)
print("Missing values per column:")
print(df.isnull().sum()[df.isnull().sum() > 0] if df.isnull().sum().sum() > 0
      else "  None found ✅")
print(f"Duplicate rows: {df.duplicated().sum()}")
print("-" * 40)
print()

# =======================================================
# STEP 3: Clean the data
# =======================================================

# 3a. Remove exact duplicate rows (if any)
before = len(df)
df = df.drop_duplicates()
print(f"Step 3a: Removed {before - len(df)} duplicate row(s)")

# 3b. Trim extra spaces from text columns (common in messy CSVs)
text_columns = df.select_dtypes(include=["object", "str"]).columns
for col in text_columns:
    df[col] = df[col].str.strip()
print("Step 3b: Trimmed whitespace from text columns")

# 3c. Convert purchase_date from text to a real date type
#     (this lets us group/sort by month, year, etc.)
df["purchase_date"] = pd.to_datetime(df["purchase_date"], format="%m/%d/%Y", errors="coerce")
bad_dates = df["purchase_date"].isnull().sum()
print(f"Step 3c: Converted purchase_date to datetime ({bad_dates} unparseable date(s) found)")

# 3d. Make sure numeric columns are actually numeric
#     (protects against stray text/symbols in number columns)
numeric_cols = ["price", "discount", "final_price", "rating",
                 "review_count", "stock", "seller_rating", "shipping_time_days"]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")
print("Step 3d: Ensured price/rating/etc. columns are numeric")

# 3e. Drop any rows that became empty/invalid after cleaning
before = len(df)
df = df.dropna(subset=numeric_cols + ["purchase_date"])
print(f"Step 3e: Dropped {before - len(df)} row(s) with unusable values")

# 3f. Sanity checks - remove impossible values (negative price, rating out of 0-5, etc.)
before = len(df)
df = df[(df["price"] > 0) & (df["final_price"] > 0)]
df = df[(df["rating"].between(0, 5)) & (df["seller_rating"].between(0, 5))]
print(f"Step 3f: Removed {before - len(df)} row(s) with invalid price/rating values")

# Add a helper column for monthly trend chart
df["purchase_month"] = df["purchase_date"].dt.to_period("M").astype(str)

print()
print(f"✅ Cleaning complete! {len(df)} clean rows remain.")
print()

# =======================================================
# STEP 4: Quick summary of the cleaned data
# =======================================================
print("Step 4: Summary of cleaned data")
print("-" * 40)
print(f"Total revenue (final_price sum): ₹{df['final_price'].sum():,.2f}")
print(f"Average rating: {df['rating'].mean():.2f}")
print(f"Return rate: {df['is_returned'].mean() * 100:.1f}%")
print("-" * 40)
print()

# =======================================================
# CHART 1: BAR CHART - total revenue by category
# =======================================================
revenue_by_category = df.groupby("category")["final_price"].sum().sort_values(ascending=False)

plt.figure(figsize=(8, 5))
plt.bar(revenue_by_category.index, revenue_by_category.values, color="#4C72B0")
plt.title("Total Revenue by Product Category")
plt.xlabel("Category")
plt.ylabel("Revenue (₹)")
for i, value in enumerate(revenue_by_category.values):
    plt.text(i, value, f"₹{value:,.0f}", ha="center", va="bottom", fontsize=9)
plt.tight_layout()
plt.show()
print("Chart 1 displayed: Bar Chart (Revenue by Category)")

# =======================================================
# CHART 2: PIE CHART - share of orders by payment method
# =======================================================
payment_counts = df["payment_method"].value_counts()

plt.figure(figsize=(7, 7))
plt.pie(
    payment_counts.values,
    labels=payment_counts.index,
    autopct="%1.1f%%",
    startangle=90,
    colors=["#4C72B0", "#DD8452", "#55A868", "#C44E52"],
)
plt.title("Share of Orders by Payment Method")
plt.tight_layout()
plt.show()
print("Chart 2 displayed: Pie Chart (Payment Method Share)")

# =======================================================
# CHART 3: LINE CHART - monthly revenue trend
# =======================================================
monthly_revenue = df.groupby("purchase_month")["final_price"].sum().sort_index()

plt.figure(figsize=(9, 5))
plt.plot(monthly_revenue.index, monthly_revenue.values, marker="o", color="#55A868", linewidth=2)
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue (₹)")
plt.xticks(rotation=45, ha="right")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
print("Chart 3 displayed: Line Chart (Monthly Revenue Trend)")

# =======================================================
# CHART 4: SCATTER CHART - price vs. rating (by category)
# =======================================================
categories = df["category"].unique()
colors_cycle = plt.cm.tab10.colors
category_color = {cat: colors_cycle[i % len(colors_cycle)] for i, cat in enumerate(categories)}
point_colors = df["category"].map(category_color)

plt.figure(figsize=(9, 5))
plt.scatter(df["price"], df["rating"], c=point_colors, s=70, edgecolors="black", alpha=0.85)
plt.title("Price vs. Rating (by Category)")
plt.xlabel("Price (₹)")
plt.ylabel("Rating")
plt.grid(True, alpha=0.3)

handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=category_color[cat],
                       markeredgecolor='black', markersize=9, label=cat) for cat in categories]
plt.legend(handles=handles, title="Category", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.tight_layout()
plt.show()
print("Chart 4 displayed: Scatter Chart (Price vs Rating)")

print()
print("DONE! All 4 charts were displayed one after another using plt.show().")
