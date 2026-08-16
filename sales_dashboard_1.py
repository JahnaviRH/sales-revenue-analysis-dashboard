import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Sales & Revenue Analysis Dashboard",
    layout="wide"
)

df = pd.read_csv(
    r"sales_revenue_dashboard_raw (1).csv"
)

df = df.drop_duplicates()

df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")

df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce").fillna(0)
df["Profit"] = pd.to_numeric(df["Profit"], errors="coerce").fillna(0)
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce").fillna(0)

df["Product"] = df["Product"].fillna("Unknown")
df["Region"] = df["Region"].fillna("Unknown")
df["Category"] = df["Category"].fillna("Unknown")
df["Customer_Segment"] = df["Customer_Segment"].fillna("Unknown")

st.title("Sales & Revenue Analysis Dashboard")

st.write("Analyze sales, revenue, products and business performance.")

st.sidebar.header("Filters")

region = st.sidebar.multiselect(
    "Region",
    df["Region"].unique(),
    default=df["Region"].unique()
)

category = st.sidebar.multiselect(
    "Category",
    df["Category"].unique(),
    default=df["Category"].unique()
)

filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category))
]

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_quantity = filtered_df["Quantity"].sum()
total_orders = filtered_df["Order_ID"].nunique()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", f"₹{total_sales:,.2f}")
col2.metric("Total Profit", f"₹{total_profit:,.2f}")
col3.metric("Total Quantity", f"{total_quantity:,.0f}")
col4.metric("Total Orders", f"{total_orders:,}")

st.divider()

monthly_sales = (
    filtered_df
    .groupby(filtered_df["Order_Date"].dt.to_period("M"))["Sales"]
    .sum()
    .reset_index()
)

monthly_sales["Order_Date"] = monthly_sales["Order_Date"].astype(str)

fig1 = px.line(
    monthly_sales,
    x="Order_Date",
    y="Sales",
    markers=True,
    title="Revenue Trend"
)

st.plotly_chart(fig1, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    top_products = (
        filtered_df
        .groupby("Product")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )

    fig2 = px.bar(
        top_products,
        x="Sales",
        y="Product",
        orientation="h",
        title="Top 5 Products"
    )

    st.plotly_chart(fig2, use_container_width=True)

with col2:
    category_sales = (
        filtered_df
        .groupby("Category")["Sales"]
        .sum()
        .reset_index()
    )

    fig3 = px.pie(
        category_sales,
        names="Category",
        values="Sales",
        title="Sales by Category"
    )

    st.plotly_chart(fig3, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    region_sales = (
        filtered_df
        .groupby("Region")["Sales"]
        .sum()
        .reset_index()
    )

    fig4 = px.bar(
        region_sales,
        x="Region",
        y="Sales",
        title="Sales by Region"
    )

    st.plotly_chart(fig4, use_container_width=True)

with col2:
    segment_sales = (
        filtered_df
        .groupby("Customer_Segment")["Sales"]
        .sum()
        .reset_index()
    )

    fig5 = px.bar(
        segment_sales,
        x="Customer_Segment",
        y="Sales",
        title="Sales by Customer Segment"
    )

    st.plotly_chart(fig5, use_container_width=True)

st.subheader("Product Performance")

product_table = (
    filtered_df
    .groupby("Product")
    .agg(
        Sales=("Sales", "sum"),
        Quantity=("Quantity", "sum"),
        Profit=("Profit", "sum")
    )
    .sort_values("Sales", ascending=False)
    .reset_index()
)

st.dataframe(
    product_table,
    use_container_width=True,
    hide_index=True
)

st.subheader("Business Insights")

if len(filtered_df) > 0:
    best_product = filtered_df.groupby("Product")["Sales"].sum().idxmax()
    best_region = filtered_df.groupby("Region")["Sales"].sum().idxmax()
    best_category = filtered_df.groupby("Category")["Sales"].sum().idxmax()

    st.write("Top Product:", best_product)
    st.write("Best Region:", best_region)
    st.write("Best Category:", best_category)
else:
    st.warning("No data available for the selected filters.")