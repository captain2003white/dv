import streamlit as st

def render(df):
    st.title("EEG brainwave data visualization")
    
    st.markdown("### 1. Data Context (数据背景)")
    
    # --- Data Origin & Methodology ---
    st.write("""
    This dataset captures electrical brain activity (EEG) from 4 subjects (2 men 2 women) using a Muse Headband 
    The data was collected for 60 seconds per state to classify three distinct mental states Relaxed Neutral and Concentrating 
    (此数据集捕捉来自4名受试者 2男2女 使用Muse头环的脑电活动 数据为每种状态采集60秒 用于分类三种心理状态 放松 中性 和 专注)
    """)
    
    # --- Detailed Sensor Explanation ---
    st.markdown("#### Sensor Configuration (传感器介绍)")
    
    # Using 4 columns to create 'cards' for each sensor
    s1, s2, s3, s4 = st.columns(4)
    
    with s1:
        st.info("**TP9 --> end-Listed '_0'**\n\nLeft Ear (左耳)\n\n*Temporal Lobe Auditory processing (颞叶 听觉处理)*")
    with s2:
        st.info("**AF7 --> end-Listed '_1'**\n\nLeft Forehead (左前额)\n\n*Frontal Lobe Logic & Attention (前额叶 逻辑与注意)*")
    with s3:
        st.info("**AF8 --> end-Listed '_2'**\n\nRight Forehead (右前额)\n\n*Frontal Lobe Emotion & Focus (前额叶 情绪与专注)*")
    with s4:
        st.info("**TP10 --> end-Listed '_3'**\n\nRight Ear (右耳)\n\n*Temporal Lobe Memory & Spatial (颞叶 记忆与空间)*")
        
    st.markdown("---")

    st.markdown("#### Methods for Processing Raw EEG Data: How Datasets Are Born (原始脑电数据处理方法————数据集诞生之法)")
    st.info("The dataset is generated from an EEG-based experiment in which participants with different diagnostic groups (such as schizophrenia patients and healthy controls) perform several cognitive tasks while their brain electrical activity is continuously recorded using a multi-channel EEG system. (该数据集来源于一个基于脑电实验的研究，参与者包含不同诊断组别，如精神分裂症患者与健康对照，他们在执行多种认知任务的同时，其脑部电活动通过多通道脑电系统被持续记录)")
    st.info("Raw EEG signals are first collected at high temporal resolution, capturing the voltage changes produced by neuronal activity. (原始脑电信号以高时间分辨率采集，用于捕捉神经活动产生的电压变化)")
    st.info("After acquisition, the data undergo standard EEG preprocessing procedures—including filtering, artifact removal, re-referencing, and epoching—to transform the continuous recordings into clean, analysis-ready segments. (随后，数据经过标准脑电预处理流程，包括滤波、伪迹去除、重参考以及分段，从而将连续记录转化为干净、可用于分析的数据片段)")
    st.info("From these preprocessed EEG signals, a series of computational features are generated to convert time-domain brain activity into structured, machine-learning-friendly representations. (在预处理后的脑电信号基础上，研究者生成了一系列计算特征，将时域脑活动转化为结构化、适合机器学习的表达方式)")
    st.info("Typical features include power spectral density from different frequency bands (theta, alpha, beta, gamma), time-frequency representations, statistical summaries of signal amplitude, and spatial patterns across electrodes. (典型特征包括不同频段的功率谱密度〔θ、α、β、γ〕、时频表示、信号幅度的统计特征以及跨电极的空间分布模式)")
    st.info("In image-based EEG feature generation, these multidimensional characteristics are further organized into 2D matrices—such as frequency-by-channel, time-frequency maps, or spatial topography plots—so that each EEG sample can be treated as an image input to a neural network classifier. (在图像化脑电特征生成中，这些多维特征进一步被组织成二维矩阵，如频率-通道图、时频图或空间拓扑图，从而使每个脑电样本都可以作为图像输入到神经网络分类器中)")
    st.info("Thus, the dataset's columns arise from different steps of EEG preprocessing and feature extraction, each representing a numerical descriptor derived from brain electrical activity. (因此，数据集中的列来自脑电预处理与特征提取的不同步骤，每一列都代表从脑部电活动中计算得到的数值特征)")
    # --- Metrics (One Row) ---
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Total Samples (样本数)", len(df))
    with c2:
        st.metric("Recording Duration (录制时长)", "60s per state (每状态60秒)")
    with c3:
        st.metric("Missing Values (缺失值)", df.isna().sum().sum())
    
    st.markdown("---")
    
    # --- Data Tables (No Charts) ---
    st.markdown("### 2. Dataset Overview (数据集概况)")
    
    col_table1, col_table2 = st.columns([1, 3])
    
    with col_table1:
        st.markdown("**Class Distribution Data (类别分布数据)**")
        # Display the count of each label
        st.dataframe(df['Label'].value_counts(), use_container_width=True)
        
    with col_table2:
        st.markdown("**Raw Data Preview (原始数据预览)**")
        # Display first few rows to show data structure
        st.dataframe(df.head(), use_container_width=True)
    
    st.markdown("---")