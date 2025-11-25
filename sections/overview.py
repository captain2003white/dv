import streamlit as st
from utils.viz import plot_parallel_coordinates

def render(df):
    #st.markdown("### 2. Overview Global Separability (概览 全局可分性)")
    
    #st.info("Visualizing whether the three mental states can be mathematically distinguished (可视化三种心理状态是否在数学上可区分)")
        
    st.plotly_chart(plot_parallel_coordinates(df), use_container_width=True)

    st.markdown("---")