import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="NTC Centri Map", layout="wide")
st.title("📍 NTC Educational Centers 2025/26")

@st.cache_data
def load_data():
    df = pd.read_excel(
        "ntc_centri.xlsx",
        sheet_name="NTC centri 2526",
        header=1
    )

    df.columns = df.columns.astype(str).str.strip()
    df["Grad"] = df["Grad"].astype(str)
    print(df["Grad"])

    return df

df = load_data()
#st.write(df["Grad"])


# ---- SEARCH BOX (ONLY ONCE, BEFORE THE MAP) ----
cities = sorted(df["Grad"].dropna().unique().tolist())
selected_city = st.selectbox("🔍 Search for a city:", ["All"] + cities)

# ---- CREATE MAP ----
m = folium.Map(location=[44.5, 20.5], zoom_start=7)

for _, row in df.iterrows():

    lat = row.get("Latitude") or row.get("Lat") or row.get("latitude")
    lon = row.get("Longitude") or row.get("Lon") or row.get("longitude")

    city = str(row.get("Grad", "")).strip()
    level = str(row["Nivo NTC centra"])

    # ---- APPLY SEARCH FILTER ----
    if selected_city != "All" and city != selected_city:
        continue

    if pd.notna(lat) and pd.notna(lon):

        color = "red" if "🏆" in level else "blue"

        folium.CircleMarker(
            location=[lat, lon],
            radius=12 if color=="red" else 7,
            popup=folium.Popup(
                f"""
                <b>📍 {city}</b><br>
                NTC centar<br>
                """,
                max_width=250
            ),
            tooltip=city,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7
        ).add_to(m)

st_folium(m, width="100%", height=700)
