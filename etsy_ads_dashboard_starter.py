
import streamlit as st
import pandas as pd
import altair as alt

st.title("Etsy Ads & Sales Analytics Dashboard")

st.sidebar.header("Upload Your Data")
ads_file = st.sidebar.file_uploader("Upload Etsy Ads CSV", type=["csv"])
sales_file = st.sidebar.file_uploader("Upload Etsy Orders CSV", type=["csv"])

if ads_file and sales_file:
    ads_df = pd.read_csv(ads_file)
    sales_df = pd.read_csv(sales_file)

    # Sample columns expected
    # ads_df: date, ad_group, spend, clicks
    # sales_df: date, order_id, product, revenue

    # Merge on date
    ads_df['date'] = pd.to_datetime(ads_df['date'])
    sales_df['date'] = pd.to_datetime(sales_df['date'])

    merged = pd.merge(ads_df, sales_df, on='date', how='left')

    daily = merged.groupby('date').agg({
        'spend': 'sum',
        'revenue': 'sum'
    }).reset_index()
    daily['ROAS'] = daily['revenue'] / daily['spend']

    st.subheader("Daily Spend vs Revenue")
    line_chart = alt.Chart(daily).mark_line().encode(
        x='date:T',
        y=alt.Y('spend:Q', title='Spend'),
        color=alt.value("orange")
    ) + alt.Chart(daily).mark_line().encode(
        x='date:T',
        y=alt.Y('revenue:Q', title='Revenue'),
        color=alt.value("green")
    )
    st.altair_chart(line_chart, use_container_width=True)

    st.subheader("ROAS Over Time")
    roas_chart = alt.Chart(daily).mark_bar().encode(
        x='date:T',
        y='ROAS:Q'
    )
    st.altair_chart(roas_chart, use_container_width=True)

    st.write("Raw Merged Data", merged.head())

else:
    st.info("Please upload both Etsy Ads and Sales CSV files to begin.")
