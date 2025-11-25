import streamlit as st
from utils.io import load_data, filter_by_region
import sections.intro as intro
import sections.overview as overview
import sections.deep_dives as deep_dives
import sections.conclusions as conclusions

st.set_page_config(page_title="EEG Analytics", layout="wide")

def main():
    # --- Fixed Sidebar Content ---
    st.sidebar.image("assets/efrei.png", width=200)
    st.sidebar.image("assets/WUT-Logo.png", width=200)
    st.sidebar.markdown("---")

    st.sidebar.markdown("[GitHub Address](https://github.com/captain2003white/dv)")
    st.sidebar.markdown("**Student Name:** Jingyun Cheng")
    st.sidebar.markdown("**Efrei Email:** jingyun.cheng@efrei.net")
    st.sidebar.markdown("**Email:** 325763@whut.edu.cn")
    st.sidebar.markdown("**Course: Data Visualization 2025**")
    st.sidebar.markdown("**Prof. Mano Mathew**")
    st.sidebar.markdown("[Check out this LinkedIn](https://www.linkedin.com/in/manomathew/)")
    st.sidebar.markdown("---")
    
    st.sidebar.title("References")
    st.sidebar.markdown("[Data Source](https://www.kaggle.com/datasets/birdy654/eeg-brainwave-dataset-mental-state)")
    st.sidebar.markdown("[Feature Extraction Code](https://github.com/jordan-bird/eeg-feature-generation)")
    st.sidebar.markdown("Dataset Author [Jordan J. Bird](https://jordanjamesbird.com/)")
    st.sidebar.markdown("---")

    # --- Sidebar Filter (ONLY Brain Region) ---
    st.sidebar.header("Analysis Focus (分析焦点)")
    
    region_options = [
        "All Sensors (All Regions)", 
        "Frontal Lobe (AF7 AF8)", 
        "Temporal Lobe (TP9 TP10)"
    ]
    
    selected_region = st.sidebar.selectbox(
        "Select Brain Region (选择大脑区域)",
        options=region_options,
        index=0
    )
    
    # Load Data
    df = load_data()
    
    # Get active sensors based on filter (e.g., returns ['1', '2'] for Frontal)
    active_sensors = filter_by_region(df, selected_region)

    # --- Render Sections ---
    intro.render(df)
    
    # Overview (Uses full data usually, or filtered if preferred)
    overview.render(df) 
    
    # Deep Dive (Passes the filtered sensor list to generate specific charts)
    deep_dives.render(df, active_sensors)
    
    conclusions.render()
    
    

if __name__ == "__main__":
    main()