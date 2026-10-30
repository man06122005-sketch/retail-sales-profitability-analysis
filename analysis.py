
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load the dataset
df = pd.read_csv("data/raw/project1.csv")

# Convert date columns
# Convert dates using Australian date format
df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    format="mixed",
    dayfirst=True
)

df["Ship Date"] = pd.to_datetime(
    df["Ship Date"],
    format="mixed",
    dayfirst=True
)

# Check the data types
print("--- UPDATED DATA TYPES ---")
print(df.dtypes)

# Step 2: Preview the data
print("--- FIRST FIVE ROWS ---")
print(df.head())

# Step 3: Check the dataset size
print("--- DATASET SIZE ---")
print(df.shape)

# Step 4: Check column names
print("--- COLUMN NAMES ---")
print(df.columns.tolist())

# Step 5: Check data types
print("--- DATA TYPES ---")
print(df.dtypes)

# Step 6: Check missing values
print("--- MISSING VALUES ---")
print(df.isna().sum())

# Step 7: Check duplicate rows
print("--- DUPLICATE ROWS ---")
print(df.duplicated().sum())

# Calculate shipping duration
df["Shipping Days"] = (
    df["Ship Date"] - df["Order Date"]
).dt.days

# Extract year and month
df["Order Year"] = df["Order Date"].dt.year
df["Order Month"] = df["Order Date"].dt.month

print("--- NEW COLUMNS ---")
print(df[[
    "Order Date",
    "Ship Date",
    "Shipping Days",
    "Order Year",
    "Order Month"
]].head())

print("Dataset shape:", df.shape)

print("Date data types:")
print(df[["Order Date", "Ship Date"]].dtypes)

print("Shipping duration:")
print(df["Shipping Days"].describe())


# ==================================
# BUSINESS PERFORMANCE - KPI ANALYSIS
# ==================================

# Calculate key metrics
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_quantity = df["Quantity"].sum()

total_orders = df["Order ID"].nunique()
total_customers = df["Customer ID"].nunique()

# Calculate profit margin
profit_margin = (total_profit / total_sales) * 100

# Calculate average order value
average_order_value = total_sales / total_orders

# Calculate average discount
average_discount = df["Discount"].mean() * 100

# Display KPI results
print("\n========== BUSINESS KPI REPORT ==========")

print(f"Total Sales: ${total_sales:,.2f}")
print(f"Total Profit: ${total_profit:,.2f}")
print(f"Total Units Sold: {total_quantity:,}")

print(f"Total Orders: {total_orders:,}")
print(f"Total Customers: {total_customers:,}")

print(f"Profit Margin: {profit_margin:.2f}%")
print(f"Average Order Value: ${average_order_value:,.2f}")
print(f"Average Discount: {average_discount:.2f}%")

print("=========================================")


# ==================================
# PRODUCT CATEGORY ANALYSIS
# ==================================

category_analysis = df.groupby("Category").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum"),
    Units_Sold=("Quantity", "sum")
).reset_index()

# Calculate profit margin for each category
category_analysis["Profit_Margin"] = (
    category_analysis["Total_Profit"] /
    category_analysis["Total_Sales"] * 100
)

# Sort categories by total profit
category_analysis = category_analysis.sort_values(
    by="Total_Profit",
    ascending=False
)

print("\n========== CATEGORY PERFORMANCE ==========")
print(category_analysis.round(2).to_string(index=False))


# ==================================
# REGIONAL PERFORMANCE ANALYSIS
# ==================================

region_analysis = df.groupby("Region").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum"),
    Units_Sold=("Quantity", "sum")
).reset_index()

region_analysis["Profit_Margin"] = (
    region_analysis["Total_Profit"] /
    region_analysis["Total_Sales"] * 100
)

region_analysis = region_analysis.sort_values(
    by="Total_Profit",
    ascending=False
)

print("\n========== REGIONAL PERFORMANCE ==========")
print(region_analysis.round(2).to_string(index=False))


import os

# Create output folder if it doesn't exist
os.makedirs("outputs", exist_ok=True)

plt.figure(figsize=(8, 5))

plt.bar(
    category_analysis["Category"],
    category_analysis["Total_Sales"]
)

plt.title("Total Sales by Product Category")
plt.xlabel("Product Category")
plt.ylabel("Total Sales ($)")
plt.tight_layout()

plt.savefig("outputs/sales_by_category.png", dpi=300)
plt.show()


plt.figure(figsize=(8, 5))

plt.bar(
    category_analysis["Category"],
    category_analysis["Total_Profit"]
)

plt.title("Total Profit by Product Category")
plt.xlabel("Product Category")
plt.ylabel("Total Profit ($)")
plt.tight_layout()

plt.savefig("outputs/profit_by_category.png", dpi=300)
plt.show()


plt.figure(figsize=(8, 5))

plt.bar(
    region_analysis["Region"],
    region_analysis["Profit_Margin"]
)

plt.title("Profit Margin by Region")
plt.xlabel("Region")
plt.ylabel("Profit Margin (%)")
plt.tight_layout()

plt.savefig("outputs/profit_margin_by_region.png", dpi=300)
plt.show()


# Sub-category profitability analysis

subcategory_analysis = df.groupby("Sub-Category").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum"),
    Units_Sold=("Quantity", "sum"),
    Average_Discount=("Discount", "mean")
).reset_index()

subcategory_analysis["Profit_Margin"] = (
    subcategory_analysis["Total_Profit"] /
    subcategory_analysis["Total_Sales"] * 100
)

subcategory_analysis = subcategory_analysis.sort_values(
    by="Profit_Margin",
    ascending=True
)

print("\n========== SUB-CATEGORY ANALYSIS ==========")
print(subcategory_analysis.round(2).to_string(index=False))


# ==================================
# PRODUCT-LEVEL PROFITABILITY ANALYSIS
# ==================================

product_analysis = df.groupby(
    ["Product ID", "Product Name", "Sub-Category"]
).agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum"),
    Units_Sold=("Quantity", "sum"),
    Average_Discount=("Discount", "mean"),
    Orders=("Order ID", "nunique")
).reset_index()

# Identify products with negative total profit
loss_making_products = product_analysis[
    product_analysis["Total_Profit"] < 0
].sort_values(
    by="Total_Profit",
    ascending=True
)

print("\n========== LOSS-MAKING PRODUCTS ==========")

print(
    loss_making_products.head(15)
    .round(2)
    .to_string(index=False)
)

print(
    "\nTotal loss-making products:",
    len(loss_making_products)
)

print(
    "Total distinct products:",
    df["Product ID"].nunique()
)


# ==================================
# DISCOUNT IMPACT ANALYSIS
# ==================================

# Group transactions by discount level
df["Discount Band"] = pd.cut(
    df["Discount"],
    bins=[-0.001, 0.1, 0.2, 0.3, 0.4, 0.5, 1.0],
    labels=[
        "0-10%",
        "10-20%",
        "20-30%",
        "30-40%",
        "40-50%",
        "50-100%"
    ]
)

discount_analysis = df.groupby(
    "Discount Band",
    observed=True
).agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum"),
    Average_Profit=("Profit", "mean"),
    Transaction_Count=("Order ID", "nunique")
).reset_index()

discount_analysis["Profit_Margin"] = (
    discount_analysis["Total_Profit"] /
    discount_analysis["Total_Sales"] * 100
)

print("\n========== DISCOUNT IMPACT ANALYSIS ==========")
print(discount_analysis.round(2).to_string(index=False))


# ==================================
# DISCOUNT IMPACT BY CATEGORY
# ==================================

category_discount = df.groupby(
    ["Category", "Discount Band"],
    observed=True
).agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum"),
    Order_Lines=("Order ID", "size"),
    Unique_Orders=("Order ID", "nunique")
).reset_index()

# Calculate profit margin
category_discount["Profit_Margin"] = (
    category_discount["Total_Profit"] /
    category_discount["Total_Sales"] * 100
)

# Sort results
category_discount = category_discount.sort_values(
    ["Category", "Discount Band"]
)

print("\n========== DISCOUNT IMPACT BY CATEGORY ==========")
print(category_discount.round(2).to_string(index=False))


# DISCOUNT IMPACT BY CATEGORY - VISUALISATION

import matplotlib.pyplot as plt
import os

os.makedirs("outputs", exist_ok=True)

# Set the correct order of discount bands
discount_order = [
    "0-10%",
    "10-20%",
    "20-30%",
    "30-40%",
    "40-50%",
    "50-100%"
]

# Convert the table into a format suitable for plotting
margin_pivot = category_discount.pivot(
    index="Discount Band",
    columns="Category",
    values="Profit_Margin"
)

margin_pivot = margin_pivot.reindex(discount_order)

# Create the line chart
plt.figure(figsize=(10, 6))

for category in margin_pivot.columns:
    plt.plot(
        margin_pivot.index.astype(str),
        margin_pivot[category],
        marker="o",
        linewidth=2,
        label=category
    )

# Add a zero-profit reference line
plt.axhline(y=0, linestyle="--", linewidth=1)

plt.title("Impact of Discounts on Profit Margin by Category")
plt.xlabel("Discount Band")
plt.ylabel("Profit Margin (%)")
plt.legend(title="Product Category")
plt.grid(axis="y", alpha=0.3)

plt.tight_layout()

plt.savefig(
    "outputs/discount_impact_by_category.png",
    dpi=300
)

plt.show()


# REGIONAL PROFITABILITY VISUALISATION

import matplotlib.pyplot as plt
import os

os.makedirs("outputs", exist_ok=True)

# Sort regions by profit margin
region_chart = region_analysis.sort_values(
    by="Profit_Margin",
    ascending=False
)

plt.figure(figsize=(9, 6))

plt.bar(
    region_chart["Region"],
    region_chart["Profit_Margin"]
)

plt.title("Profit Margin by Region")
plt.xlabel("Region")
plt.ylabel("Profit Margin (%)")

plt.axhline(y=0, linestyle="--", linewidth=1)
plt.grid(axis="y", alpha=0.3)

plt.tight_layout()

plt.savefig(
    "outputs/profit_margin_by_region.png",
    dpi=300
)

plt.show()


# REGIONAL PERFORMANCE BY PRODUCT CATEGORY

regional_category_analysis = df.groupby(
    ["Region", "Category"]
).agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum"),
    Units_Sold=("Quantity", "sum"),
    Order_Lines=("Order ID", "size")
).reset_index()

# Calculate profit margin
regional_category_analysis["Profit_Margin"] = (
    regional_category_analysis["Total_Profit"] /
    regional_category_analysis["Total_Sales"] * 100
)

# Sort results by region and profit margin
regional_category_analysis = regional_category_analysis.sort_values(
    ["Region", "Profit_Margin"],
    ascending=[True, False]
)

print("\n========== REGIONAL PERFORMANCE BY CATEGORY ==========")

print(
    regional_category_analysis.round(2).to_string(index=False)
)


# CENTRAL REGION - SUB-CATEGORY PROFITABILITY

central_subcategory = df[
    (df["Region"] == "Central") &
    (df["Category"].isin(["Furniture", "Office Supplies"]))
].groupby(
    ["Category", "Sub-Category"]
).agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum"),
    Units_Sold=("Quantity", "sum"),
    Average_Discount=("Discount", "mean"),
    Order_Lines=("Order ID", "size"),
    Unique_Orders=("Order ID", "nunique")
).reset_index()

# Calculate profit margin
central_subcategory["Profit_Margin"] = (
    central_subcategory["Total_Profit"] /
    central_subcategory["Total_Sales"] * 100
)

# Convert average discount into percentage
central_subcategory["Average_Discount"] *= 100

# Sort from lowest to highest profit
central_subcategory = central_subcategory.sort_values(
    by="Total_Profit",
    ascending=True
)

print("\n========== CENTRAL SUB-CATEGORY ANALYSIS ==========")

print(
    central_subcategory.round(2).to_string(index=False)
)


# CENTRAL REGION - SUB-CATEGORY PROFITABILITY CHART

import matplotlib.pyplot as plt
import os

os.makedirs("outputs", exist_ok=True)

# Sort by total profit
central_chart = central_subcategory.sort_values(
    by="Total_Profit",
    ascending=True
)

plt.figure(figsize=(11, 7))

plt.barh(
    central_chart["Sub-Category"],
    central_chart["Total_Profit"]
)

plt.axvline(x=0, linestyle="--", linewidth=1)

plt.title("Central Region: Profit by Sub-Category")
plt.xlabel("Total Profit ($)")
plt.ylabel("Sub-Category")

plt.grid(axis="x", alpha=0.3)
plt.tight_layout()

plt.savefig(
    "outputs/central_subcategory_profit.png",
    dpi=300
)

plt.show()


# CENTRAL REGION - LOSS-MAKING PRODUCT ANALYSIS

central_products = df[
    (df["Region"] == "Central") &
    (df["Category"].isin(["Furniture", "Office Supplies"]))
].groupby(
    ["Product ID", "Product Name", "Category", "Sub-Category"]
).agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum"),
    Units_Sold=("Quantity", "sum"),
    Average_Discount=("Discount", "mean"),
    Order_Lines=("Order ID", "size"),
    Unique_Orders=("Order ID", "nunique")
).reset_index()

# Identify products with negative total profit
central_loss_products = central_products[
    central_products["Total_Profit"] < 0
].copy()

# Convert average discount to percentage
central_loss_products["Average_Discount"] *= 100

# Sort by worst financial performance
central_loss_products = central_loss_products.sort_values(
    by="Total_Profit",
    ascending=True
)

print("\n========== CENTRAL LOSS-MAKING PRODUCTS ==========")

print("Number of loss-making products:",
      len(central_loss_products))

print("Combined loss from these products: $",
      round(central_loss_products["Total_Profit"].sum(), 2))

print("\nTop 20 loss-making products:")

print(
    central_loss_products.head(20).round(2).to_string(index=False)
)


# CENTRAL REGION - DISCOUNT IMPACT ANALYSIS

central_discount_analysis = df[
    (df["Region"] == "Central") &
    (df["Category"].isin(["Furniture", "Office Supplies"]))
].groupby(
    ["Category", "Discount Band"],
    observed=True
).agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum"),
    Order_Lines=("Order ID", "size"),
    Unique_Orders=("Order ID", "nunique"),
    Unique_Products=("Product ID", "nunique"),
    Average_Discount=("Discount", "mean")
).reset_index()

# Calculate profit margin
central_discount_analysis["Profit_Margin"] = (
    central_discount_analysis["Total_Profit"] /
    central_discount_analysis["Total_Sales"] * 100
)

# Convert average discount into percentage
central_discount_analysis["Average_Discount"] *= 100

# Sort results
central_discount_analysis = central_discount_analysis.sort_values(
    ["Category", "Discount Band"]
)

print("\n========== CENTRAL DISCOUNT IMPACT ANALYSIS ==========")

print(
    central_discount_analysis.round(2).to_string(index=False)
)


# CENTRAL REGION - HIGH DISCOUNT PRODUCT INVESTIGATION

central_high_discount_rows = df[
    (df["Region"] == "Central") &
    (
        (
            (df["Category"] == "Furniture") &
            (df["Discount"] > 0.2)
        ) |
        (
            (df["Category"] == "Office Supplies") &
            (df["Discount"] > 0.5)
        )
    )
].copy()

# Group high-discount transactions by product
high_discount_products = central_high_discount_rows.groupby(
    ["Product ID", "Product Name", "Category", "Sub-Category"]
).agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum"),
    Units_Sold=("Quantity", "sum"),
    Average_Discount=("Discount", "mean"),
    Order_Lines=("Order ID", "size"),
    Unique_Orders=("Order ID", "nunique")
).reset_index()

# Convert discount into percentage
high_discount_products["Average_Discount"] *= 100

# Keep products with negative profit
high_discount_losses = high_discount_products[
    high_discount_products["Total_Profit"] < 0
].copy()

# Rank products by financial loss
high_discount_losses = high_discount_losses.sort_values(
    by="Total_Profit",
    ascending=True
)

print("\n========== CENTRAL HIGH-DISCOUNT PRODUCT LOSSES ==========")

print(
    "Number of loss-making products:",
    len(high_discount_losses)
)

print(
    "Total losses: $",
    round(high_discount_losses["Total_Profit"].sum(), 2)
)

print("\nTop 20 loss-making products:")

print(
    high_discount_losses.head(20).round(2).to_string(index=False)
)


# RECONCILE HIGH-DISCOUNT PRODUCT LOSSES

# Net profit across all selected high-discount transactions
net_profit = central_high_discount_rows["Profit"].sum()

# Separate product-level profits and losses
product_profit = central_high_discount_rows.groupby(
    "Product ID"
)["Profit"].sum()

gross_losses = product_profit[product_profit < 0].sum()

positive_offsets = product_profit[product_profit > 0].sum()

print("\n========== HIGH-DISCOUNT PROFIT RECONCILIATION ==========")

print("Net profit across all transactions: $",
      round(net_profit, 2))

print("Gross losses from loss-making products: $",
      round(gross_losses, 2))

print("Profit from profitable products: $",
      round(positive_offsets, 2))

print("Reconciliation check: $",
      round(gross_losses + positive_offsets, 2))


# ==========================================
# EXPORT ANALYSIS RESULTS
# ==========================================

import os

# Create output folders
os.makedirs("outputs/charts", exist_ok=True)
os.makedirs("outputs/tables", exist_ok=True)

# Export summary tables
tables = {
    "category_analysis.csv": category_analysis,
    "regional_analysis.csv": region_analysis,
    "discount_analysis.csv": discount_analysis,
    "category_discount_analysis.csv": category_discount,
    "regional_category_analysis.csv": regional_category_analysis,
    "central_subcategory_analysis.csv": central_subcategory,
    "central_high_discount_losses.csv": high_discount_losses
}

for filename, table in tables.items():
    table.to_csv(
        f"outputs/tables/{filename}",
        index=False
    )

print("\n========== EXPORT COMPLETED ==========")
print("Analysis tables saved successfully!")


# ==========================================
# FINAL PORTFOLIO CHARTS
# ==========================================

import matplotlib.pyplot as plt
import os

os.makedirs("outputs/charts", exist_ok=True)

# 1. SALES BY CATEGORY
plt.figure(figsize=(8, 5))

plt.bar(
    category_analysis["Category"],
    category_analysis["Total_Sales"]
)

plt.title("Total Sales by Product Category")
plt.xlabel("Category")
plt.ylabel("Sales ($)")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

plt.savefig("outputs/charts/sales_by_category.png", dpi=300)
plt.close()


# 2. PROFIT BY CATEGORY
plt.figure(figsize=(8, 5))

plt.bar(
    category_analysis["Category"],
    category_analysis["Total_Profit"]
)

plt.title("Total Profit by Product Category")
plt.xlabel("Category")
plt.ylabel("Profit ($)")
plt.axhline(y=0, linestyle="--", linewidth=1)
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

plt.savefig("outputs/charts/profit_by_category.png", dpi=300)
plt.close()


# 3. TOP 10 LOSS-MAKING PRODUCTS
top_10_losses = high_discount_losses.head(10).sort_values(
    by="Total_Profit",
    ascending=True
)

plt.figure(figsize=(12, 7))

plt.barh(
    top_10_losses["Product Name"],
    top_10_losses["Total_Profit"]
)

plt.title("Top 10 Loss-Making Products - Central Region")
plt.xlabel("Total Profit ($)")
plt.ylabel("Product")
plt.axvline(x=0, linestyle="--", linewidth=1)
plt.grid(axis="x", alpha=0.3)
plt.yticks(fontsize=8)
plt.tight_layout()

plt.savefig("outputs/charts/top_10_loss_making_products.png", dpi=300)
plt.close()

print("\nAll final charts exported successfully!")
