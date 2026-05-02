import streamlit as st
import pandas as pd
import time
import cloudscraper

st.set_page_config(page_title="NEPSE Floorsheet Fetcher", layout="wide")

st.title("📊 NEPSE Floorsheet Data Fetcher (Stable Version)")

# Inputs
page_size = st.number_input("Rows per page", value=500, step=100)
max_pages = st.number_input("Max pages", value=50, step=5)

fetch = st.button("🚀 Fetch Data")

url = "https://newweb.nepalstock.com/api/nots/nepse-data/floorsheet"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "Origin": "https://newweb.nepalstock.com",
    "Referer": "https://newweb.nepalstock.com/floorsheet",
}

if fetch:

    scraper = cloudscraper.create_scraper()
    all_data = []

    progress = st.progress(0)

    for page in range(1, int(max_pages) + 1):

        payload = {
            "page": page,
            "size": int(page_size),
            "sortBy": "contractId",
            "sortOrder": "desc"
        }

        try:
            response = scraper.post(
                url,
                json=payload,
                headers=headers,
                timeout=15
            )

            if response.status_code != 200:
                st.warning(f"Blocked or error at page {page}")
                break

            data = response.json()

            rows = data.get("floorsheets", [])

            if not rows:
                st.info("No more data available.")
                break

            all_data.extend(rows)

            st.write(f"✔ Page {page} fetched
