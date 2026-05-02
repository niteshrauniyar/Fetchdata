import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(page_title="NEPSE Floorsheet Fix", layout="wide")

st.title("📊 NEPSE Floorsheet Combiner (FIXED)")

links_input = st.text_area("Paste Links")

run = st.button("Fetch Data")

# ---------------- SESSION ----------------
session = requests.Session()

def init_session():
    try:
        session.get(
            "https://newweb.nepalstock.com",
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10
        )
    except:
        pass

# ---------------- FETCH FUNCTION ----------------
def fetch_page(page, size=500):

    url = "https://newweb.nepalstock.com/api/nots/nepse-data/floorsheet"

    payload = {
        "page": page,
        "size": size,
        "sortBy": "contractId",
        "sortOrder": "desc"
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Origin": "https://newweb.nepalstock.com",
        "Referer": "https://newweb.nepalstock.com/floorsheet"
    }

    try:
        r = session.post(url, json=payload, headers=headers, timeout=15)

        if r.status_code == 200:
            data = r.json()
            return data.get("floorsheets", [])

    except Exception as e:
        st.warning(f"Request error: {e}")

    return []

# ---------------- MAIN ----------------
if run:

    if not links_input.strip():
        st.warning("Paste links first")
        st.stop()

    init_session()

    links = [l.strip() for l in links_input.split("\n") if l.strip()]

    all_data = []

    progress = st.progress(0)

    for i, link in enumerate(links):

        st.write(f"Processing: {link}")

        try:
            page = int(link.split("page=")[1].split("&")[0])
        except:
            page = 1

        data = fetch_page(page)

        if data:
            all_data.extend(data)

        progress.progress((i + 1) / len(links))

        time.sleep(0.3)

    # ---------------- RESULT ----------------
    if all_data:

        df = pd.DataFrame(all_data)

        st.success(f"Total Rows: {len(df)}")

        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download CSV",
            csv,
            "floorsheet.csv",
            "text/csv"
        )

    else:
        st.error("Still no data → NEPSE is blocking requests from this server.")
