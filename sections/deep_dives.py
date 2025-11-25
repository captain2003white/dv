import streamlit as st
from utils.prep import get_feature_types, prepare_brain_map_data
from utils.viz import (
    plot_feature_type_counts,
    plot_pca_analysis,
    plot_covariance_matrix,
    plot_frequency_spectrum,
    plot_brain_map,
    plot_violin_comparison
)

def render(df, active_sensors):
    st.markdown("### 3. Deep Dive Analysis (深度分析)")
    
    # Page Summary
    st.info("""
    **Page Overview (页面概述):** This section provides comprehensive feature analysis including feature type statistics, dimensionality reduction (PCA), covariance matrix visualization, frequency spectrum analysis, and spatial activation maps with distribution comparisons.
    (本节提供全面的特征分析，包括特征类型统计、降维分析(PCA)、协方差矩阵可视化、频率结构分析和空间激活图与分布对比)
    
    **What This Page Does (页面功能):** 
    - Feature Type Statistics: Count and distribution of different feature types (mean, std, skew, etc.) (特征类型统计：统计各类特征的数量分布)
    - PCA Analysis: Dimensionality reduction to visualize data structure in 2D (PCA分析：降维分析将高维数据投影到二维空间)
    - Covariance Matrix: Visualization of feature correlations in covariance matrix features (协方差矩阵：可视化covM特征之间的相关性)
    - Frequency Spectrum: Analysis of frequency domain characteristics (频率结构分析：分析频率域特征)
    - Spatial Analysis: Brain topography maps and distribution comparisons across three dimensions (空间分析：大脑拓扑图和三个维度的分布对比)
    """)
    
    # Get feature type classification
    feature_types = get_feature_types(df)
    
    # --- 1. Feature Type Statistics ---
    st.markdown("#### (1). Feature Type Statistics (特征类型统计)")
    st.info("Count and distribution of different feature types (统计各类特征的数量分布)")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        fig_counts = plot_feature_type_counts(feature_types)
        st.plotly_chart(fig_counts, use_container_width=True)
    
    with col2:
        st.markdown("**Feature Type Descriptions (特征类型说明):**")
        type_descriptions = {
            "mean": "Mean features (均值特征)",
            "std": "Standard deviation features (标准差特征)",
            "skew": "Skewness features (偏度特征)",
            "kurt": "Kurtosis features (峰度特征)",
            "covM": "Covariance matrix (协方差矩阵)",
            "logcovM": "Log covariance matrix (对数协方差矩阵)",
            "eigen": "Eigenvalues (特征值)",
            "freq": "Frequency features (频率特征)",
            "topFreq": "Top frequencies (主要频率)"
        }
        for feat_type, count in sorted([(k, len(v)) for k, v in feature_types.items()], 
                                       key=lambda x: x[1], reverse=True):
            desc = type_descriptions.get(feat_type, "")
            st.metric(feat_type, count, help=desc)
    
    st.markdown("---")
    
    # --- 2. PCA Dimensionality Reduction ---
    st.markdown("#### (2). PCA Dimensionality Reduction (PCA降维分析)")
    st.info("Use principal component analysis to project high-dimensional data into 2D space to observe overall data structure and class separation (使用主成分分析将高维数据投影到二维空间，观察数据的整体结构和类别分离情况)")
    
    pca_fig, explained_var = plot_pca_analysis(df)
    if explained_var:
        col2a, col2b = st.columns([2, 1])
        with col2a:
            st.plotly_chart(pca_fig, use_container_width=True)
        with col2b:
            st.markdown("**Explained Variance Ratio (解释方差比例):**")
            st.metric("PC1 Explained Variance (PC1解释方差)", f"{explained_var['PC1']:.2%}")
            st.metric("PC2 Explained Variance (PC2解释方差)", f"{explained_var['PC2']:.2%}")
            st.metric("Total Explained Variance (累计解释方差)", f"{explained_var['Total']:.2%}")
    else:
        st.plotly_chart(pca_fig, use_container_width=True)
    
    st.markdown("---")
    
    # --- 3. Covariance Matrix Visualization ---
    st.markdown("#### (3). Covariance Matrix Visualization (协方差矩阵可视化)")
    st.info("Visualize correlation matrix of covM features (可视化covM特征之间的相关性矩阵)")
    
    covM_fig = plot_covariance_matrix(df, feature_types)
    st.plotly_chart(covM_fig, use_container_width=True)
    
    st.markdown("---")
    
    # --- 4. Frequency Spectrum Analysis ---
    st.markdown("#### (4). Frequency Spectrum Analysis (频率结构分析)")
    st.info("Analyze frequency domain features. freq features form the longest feature sequence, perfect for spectrum plots (分析频率域特征，freq特征是最长的特征序列，非常适合做频谱图)")
    
    # Let user select sensor
    sensor_options = {
        "Sensor 0 (TP9 - Left Ear) (传感器 0 - TP9 左耳)": "0",
        "Sensor 1 (AF7 - Left Forehead) (传感器 1 - AF7 左前额)": "1",
        "Sensor 2 (AF8 - Right Forehead) (传感器 2 - AF8 右前额)": "2",
        "Sensor 3 (TP10 - Right Ear) (传感器 3 - TP10 右耳)": "3"
    }
    
    selected_sensor_name = st.selectbox(
        "Select Sensor for Analysis (选择要分析的传感器)",
        options=list(sensor_options.keys()),
        index=0
    )
    selected_sensor = sensor_options[selected_sensor_name]
    
    freq_fig = plot_frequency_spectrum(df, feature_types, sensor_id=selected_sensor)
    st.plotly_chart(freq_fig, use_container_width=True)
    
    # Display topFreq analysis
    st.markdown("##### Top Frequency Analysis (Top频率分析)")
    topFreq_cols = feature_types.get('topFreq', [])
    if len(topFreq_cols) > 0:
        sensor_topFreq_cols = [c for c in topFreq_cols if c.endswith(f'_{selected_sensor}')]
        if len(sensor_topFreq_cols) > 0:
            # Display topFreq statistics by state
            from utils.prep import LABEL_MAP
            df_topFreq = df.copy()
            df_topFreq['Label'] = df_topFreq['Label'].map(LABEL_MAP).fillna(df_topFreq['Label'])
            
            topFreq_stats = df_topFreq.groupby('Label')[sensor_topFreq_cols].mean().T
            st.dataframe(topFreq_stats, use_container_width=True)
    
    st.markdown("---")
    
    # --- 5. Spatial Activation Analysis (Brain Maps & Violin Plots) ---
    st.markdown("#### (5). Spatial Activation Analysis (空间激活分析)")
    st.write("Exploring spatial activation and statistical distributions across three dimensions (探索三个维度的空间激活和统计分布)")
    
    # --- DIMENSION 1: MEAN (Signal Power) ---
    st.markdown("##### A. Signal Power Mean Voltage (信号功率 平均电压)")
    
    col1a, col1b = st.columns([1, 1])
    with col1a:
        # Brain Map for Mean
        map_data = prepare_brain_map_data(df, "mean", active_sensors)
        st.plotly_chart(plot_brain_map(map_data, "Mean"), use_container_width=True)
    with col1b:
        # Violin for Mean
        st.plotly_chart(plot_violin_comparison(df, "mean", active_sensors), use_container_width=True)

    st.markdown("---")

    # --- DIMENSION 2: STD (Signal Stability) ---
    st.markdown("##### B. Signal Stability Standard Deviation (信号稳定性 标准差)")
    
    col2a, col2b = st.columns([1, 1])
    with col2a:
        map_data = prepare_brain_map_data(df, "std", active_sensors)
        st.plotly_chart(plot_brain_map(map_data, "Std Dev"), use_container_width=True)
    with col2b:
        st.plotly_chart(plot_violin_comparison(df, "std", active_sensors), use_container_width=True)

    st.markdown("---")

    # --- DIMENSION 3: SKEW (Signal Shape) ---
    st.markdown("##### C. Signal Shape Skewness (信号形状 偏度)")
    
    # Add detailed explanation for skewness visualization
    with st.expander("📊 How to Read Skewness Map (如何解读偏度图)"):
        st.markdown("""
        **Bubble Size (圆的大小):**
        - Represents the **intensity** of skewness (absolute value) (表示偏度的**强度**(绝对值))
        - Larger bubble = more asymmetric signal distribution, more pronounced spikes (球越大 = 信号分布越不对称, 尖峰越明显)
        
        **Color Meaning (颜色含义):**
        - 🔴 **Red/Pink** = **Positive Skew** (正偏度)
          - Right-skewed distribution with long tail on the right (分布右偏, 右侧有长尾)
          - **Sudden upward spikes** in the signal (high-value bursts) (信号中有**突然的向上尖峰**(高值突刺))
          - Indicates occasional high-intensity activation in this brain region (表示该脑区偶尔出现高强度激活)
        
        - 🔵 **Blue/Cyan** = **Negative Skew** (负偏度)
          - Left-skewed distribution with long tail on the left (分布左偏, 左侧有长尾)
          - **Sudden downward spikes** in the signal (low-value bursts) (信号中有**突然的向下尖峰**(低值突刺))
          - Indicates occasional low-intensity or suppression in this brain region (表示该脑区偶尔出现低强度或抑制)
        
        - ⚪ **White/Light** = **Near Symmetric** (接近对称)
          - Relatively symmetric distribution (分布相对对称)
          - Stable signal with no obvious spikes (信号较平稳, 没有明显的尖峰)
        
        **Practical Significance (实际意义):**
        - Skewness reflects the **burst characteristics** of EEG signals (偏度反映了EEG信号的**突发性特征**)
        - Positive skewness may indicate sudden activation during concentration (正偏度可能表示注意力集中时的突然激活)
        - Negative skewness may indicate sudden suppression during relaxation (负偏度可能表示放松时的突然抑制)
        """)
    
    col3a, col3b = st.columns([1, 1])
    with col3a:
        map_data = prepare_brain_map_data(df, "skew", active_sensors)
        st.plotly_chart(plot_brain_map(map_data, "Skew"), use_container_width=True)
    with col3b:
        st.plotly_chart(plot_violin_comparison(df, "skew", active_sensors), use_container_width=True)

    st.markdown("---")
