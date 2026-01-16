import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import base64

# 1. Page Configuration
st.set_page_config(page_title="NTC Centri Map", layout="wide")

# Helper function to convert local image to base64
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return ""

# 2. CSS - Fixed brackets and synchronized class names
st.markdown("""
    <style>
    .block-container {
        padding: 0rem !important;
        max-width: 100% !important;
    }
    
    /* Fixed Header Styling */
    .custom-header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background-color: white;
        display: flex;
        align-items: center;
        padding: 10px 25px;
        z-index: 1001;
        border-bottom: 1px solid #ddd;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }

    .logo-img {
        height: 50px;
        margin-right: 15px;
    }

    .title-text {
        font-size: 24px;
        font-weight: bold;
        color: #333;
    }

    /* Padding for the search bar so it doesn't hide under the header */
    .search-container {
        padding-top: 80px; 
        padding-left: 20px;
        padding-right: 20px;
        background-color: white;
    }
    
    /* Hide Streamlit components */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 3. Display Header (Logo + Title)
# Using a placeholder URL - replace with your image or base64 logic
# --- 1. ENCODE YOUR LOGO ---
# This converts your local 'logo.png' into a format the HTML can read
logo_base64 = get_base64_of_bin_file("logo.png")

# --- 2. DISPLAY HEADER ---
# We change the 'src' to use the base64 data instead of just the filename
if logo_base64:
    logo_html = f'data:image/png;base64,{logo_base64}'
else:
    # Fallback if file is missing
    logo_html = ""

st.markdown(f"""
    <div class="custom-header">
        <img src="{logo_html}" class="logo-img">
        <span class="title-text">NTC edukacioni centri 2025/26</span>
    </div>
    """, unsafe_allow_html=True)




@st.cache_data
def load_data():
    # Make sure ntc_centri.xlsx is in the same folder
    df = pd.read_excel("ntc_centri.xlsx", sheet_name="NTC centri 2526", header=1)
    df.columns = df.columns.astype(str).str.strip()
    df = df[df["Grad"].notna()]
    df["Grad"] = df["Grad"].astype(str).str.strip()
    return df

df = load_data()
cities = sorted(df["Grad"].unique().tolist())

if 'selected_city' not in st.session_state:
    st.session_state.selected_city = "Svi gradovi"

# 4. Search Bar (placed inside a div with top padding so it's visible)
st.markdown('<div class="search-container">', unsafe_allow_html=True)
selected = st.selectbox(
    "🔍 Pronađi NTC centar:", 
    ["Svi gradovi"] + cities,
    index=0 if st.session_state.selected_city == "Svi gradovi" else cities.index(st.session_state.selected_city) + 1
)
st.markdown('</div>', unsafe_allow_html=True)

if selected != st.session_state.selected_city:
    st.session_state.selected_city = selected
    st.rerun()

# 5. Create Map
m = folium.Map(location=[44.5, 20.5], zoom_start=7, control_scale=True)

for _, row in df.iterrows():
    lat, lon = row.get("Latitude"), row.get("Longitude")
    city = str(row.get("Grad", "")).strip()
    level = str(row.get("Nivo NTC centra", ""))

    if st.session_state.selected_city != "Svi gradovi" and city != st.session_state.selected_city:
        continue

    if pd.notna(lat) and pd.notna(lon):
        color = "red" if "🏆" in level else "blue"
        folium.CircleMarker(
            location=[lat, lon],
            radius=12 if color=="red" else 7,
            popup=folium.Popup(f"<b>📍 {city}</b><br>NTC centar", max_width=250),
            tooltip=city,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7
        ).add_to(m)

# 6. Display Map
st_folium(m, width="100%", height=850, use_container_width=True)