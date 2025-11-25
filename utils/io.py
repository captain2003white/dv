import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    return pd.read_csv("data/mental-state.csv")

def get_sensor_meta():
    # Defines metadata for sensors including coordinates for the Brain Map
    # 0=TP9 (Left Ear), 1=AF7 (Left Front), 2=AF8 (Right Front), 3=TP10 (Right Ear)
    return {
        "0": {"name": "TP9", "region": "Temporal", "x": -4, "y": 0},
        "1": {"name": "AF7", "region": "Frontal",  "x": -1.5, "y": 3},
        "2": {"name": "AF8", "region": "Frontal",  "x": 1.5, "y": 3},
        "3": {"name": "TP10", "region": "Temporal", "x": 4, "y": 0}
    }

def filter_by_region(df, region_selection):
    """
    Returns a list of column suffixes (e.g. ['0', '3']) based on selection
    """
    meta = get_sensor_meta()
    
    if region_selection == "Frontal Lobe (AF7 AF8)":
        return ["1", "2"]
    elif region_selection == "Temporal Lobe (TP9 TP10)":
        return ["0", "3"]
    else: # All Sensors
        return ["0", "1", "2", "3"]