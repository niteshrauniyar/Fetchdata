import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="NEPSE Floorsheet Combiner", layout="wide")

st.title("📊 NEPSE Floorsheet Link Combiner (Stable)")

st.write("Paste NEPSE floorsheet links (one per line)")

links_input = st.text_area("🔗 Links")

run = st.button("🚀 Fetch & Combine")

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Origin": "https://nepalstock.com",
    "Referer": "https://nepalstock.com/",
}

def fetch_api(page=1, size=500):
    url = "https://nepalstock.com/api/nots/nepse-data/floorsheet"

    payload = {
        "page": page,
        "size": size,
        "sortBy": "contractId",
        "sortOrder": "desc"
    }

    r = requests.post(url, json=payload, headers=headers, timeout=15)

    if r.status_code == 200:
        return r.json().get("floorsheets", [])

    return []

if run:

    if not links_input.strip():
        st.warning("Paste at least one link")
        st.stop()

    links = [l.strip() for l in links_input.split("\n") if l.strip()]

    all_data = []

    progress = st.progress(0)

    for i, link in enumerate(links):

        st.write(f"📥 Processing link {i+1}")

        # extract page number from URL
        try:
            if "page=" in link:
                page = int(link.split("page=")[1].split("&")[0])
            else:
                page = 1
        except:
            page = 1

        data = fetch_api(page=page)

        for d in data:
            d["source_page"] = page

        all_data.extend(data)

        progress.progress((i + 1) / len(links))

    if all_data:

        df = pd.DataFrame(all_data)

        st.success(f"✅ Total Rows: {len(df)}")

        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇ Download CSV",
            csv,
            "nepse_floorsheet.csv",
            "text/csv"
        )

    else:
        st.error("No data fetched.")
