import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="NEPSE Floorsheet App", layout="wide")

st.title("📊 NEPSE Floorsheet Auto Fetcher")

# User input
page_size = st.number_input("Rows per page", value=500, step=100)
max_pages = st.number_input("Max pages to fetch", value=50, step=10)

if st.button("🚀 Fetch Floorsheet Data"):

    all_data = []
    progress = st.progress(0)

    url = "https://newweb.nepalstock.com/api/nots/nepse-data/floorsheet"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json"
    }

    for page in range(1, max_pages + 1):

        payload = {
            "page": page,
            "size": page_size,
            "sortBy": "contractId",
            "sortOrder": "desc"
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code != 200:
            st.error(f"Error at page {page}")
            break

        data = response.json()

        if "floorsheets" not in data or len(data["floorsheets"]) == 0:
            break

        all_data.extend(data["floorsheets"])

        progress.progress(page / max_pages)

    if len(all_data) == 0:
        st.warning("No data found.")
    else:
        df = pd.DataFrame(all_data)

        st.success(f"✅ Fetched {len(df)} rows")

        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode('utf-8')

        st.download_button(
            "⬇ Download CSV",
            csv,
            "floorsheet_data.csv",
            "text/csv"
        )
