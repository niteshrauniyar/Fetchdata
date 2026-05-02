import streamlit as st
import pandas as pd

st.set_page_config(page_title="NEPSE Link Table Combiner", layout="wide")

st.title("📊 NEPSE Floorsheet Link Combiner")

st.write("Paste NEPSE pages (one per line)")

links_input = st.text_area("🔗 Paste Links Here")

run = st.button("🚀 Extract & Combine")

def extract_table(url):
    try:
        # read all tables from page
        tables = pd.read_html(url)

        # NEPSE floorsheet is usually first table
        if tables:
            return tables[0]
    except Exception as e:
        st.error(f"Failed: {url} | {e}")
    return None


if run:

    if not links_input.strip():
        st.warning("Please paste at least one link.")
        st.stop()

    links = [x.strip() for x in links_input.split("\n") if x.strip()]

    all_dfs = []

    progress = st.progress(0)

    for i, link in enumerate(links):

        st.write(f"📥 Processing: {link}")

        df = extract_table(link)

        if df is not None:
            df["source_link"] = link   # track source page
            all_dfs.append(df)

        progress.progress((i + 1) / len(links))

    if all_dfs:

        final_df = pd.concat(all_dfs, ignore_index=True)

        st.success(f"✅ Total Rows Combined: {len(final_df)}")

        st.dataframe(final_df, use_container_width=True)

        csv = final_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇ Download Combined CSV",
            csv,
            "nepse_combined_floorsheet.csv",
            "text/csv"
        )

    else:
        st.error("No tables extracted from links.")
