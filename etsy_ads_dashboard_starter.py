import streamlit as st
import pandas as pd
import altair as alt

# Page setup
st.set_page_config(
    page_title="Etsy Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide Streamlit toolbar (GitHub icon, etc.)
st.markdown(
    """<style>[data-testid="stToolbar"]{ visibility: hidden; }</style>""",
    unsafe_allow_html=True
)

st.title("Etsy Ads & Sales Analytics Dashboard")

# Sidebar upload
st.sidebar.header("Upload Your Data")
ads_file = st.sidebar.file_uploader("Upload Etsy Ads CSV", type=["csv"])
sales_file = st.sidebar.file_uploader("Upload Etsy Orders CSV", type=["csv"])

if ads_file and sales_file:
    ads_df = pd.read_csv(ads_file)
    sales_df = pd.read_csv(sales_file)

    # Convert date columns
    ads_df['date'] = pd.to_datetime(ads_df['date'])
    sales_df['date'] = pd.to_datetime(sales_df['date'])

    # Merge data
    merged = pd.merge(ads_df, sales_df, on='date', how='left')

    # Daily summary
    daily = merged.groupby('date').agg({
        'spend': 'sum',
        'revenue': 'sum'
    }).reset_index()
    daily['ROAS'] = daily['revenue'] / daily['spend']

    # Line chart: Spend vs Revenue
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

    # ROAS chart
    st.subheader("ROAS Over Time")
    roas_chart = alt.Chart(daily).mark_bar().encode(
        x='date:T',
        y='ROAS:Q'
    )
    st.altair_chart(roas_chart, use_container_width=True)

    # Data preview
    st.write("Raw Merged Data", merged.head())

    # Download button
    st.subheader("Download Merged Data")
    csv = merged.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Merged Data as CSV",
        data=csv,
        file_name='etsy_ads_merged.csv',
        mime='text/csv'
    )

else:
    st.info("Please upload both Etsy Ads and Sales CSV files to begin.")


