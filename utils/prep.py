import streamlit as st
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import numpy as np

# 定义标签映射字典：将数字转换为人类可读的文字
LABEL_MAP = {
    0: "Neutral (中性)", 
    1: "Relaxed (放松)", 
    2: "Concentrating (专注)"
}

@st.cache_data
def get_pca_data(df):
    features = df.select_dtypes(include=[np.number])
    # 确保有数据才运行
    if features.shape[0] > 0 and features.shape[1] > 0:
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(features)
        
        pca = PCA(n_components=2)
        components = pca.fit_transform(scaled_features)
        
        pca_df = pd.DataFrame(data=components, columns=['PC1', 'PC2'])
        
        # --- 核心修改：将 0,1,2 映射为文字 ---
        # fillna 是为了防止有未知标签报错，虽然这里应该不会有
        pca_df['Label'] = df['Label'].map(LABEL_MAP).fillna(df['Label'])
        
        return pca_df
    return pd.DataFrame()

def get_feature_types(df):
    """
    将特征按类型分类
    返回一个字典，键为特征类型，值为该类型的所有特征列名列表
    """
    cols = [c for c in df.columns if c != 'Label']
    types = {
        "mean": [c for c in cols if "_mean_" in c or c.startswith("mean")],
        "std": [c for c in cols if "_std_" in c or c.startswith("std")],
        "skew": [c for c in cols if "_skew_" in c or c.startswith("skew")],
        "kurt": [c for c in cols if "_kurt_" in c or c.startswith("kurt")],
        "covM": [c for c in cols if "covM" in c],
        "logcovM": [c for c in cols if "logcovM" in c],
        "eigen": [c for c in cols if "eigenval" in c],
        "freq": [c for c in cols if "freq_" in c and "topFreq" not in c],
        "topFreq": [c for c in cols if "topFreq" in c],
    }
    return types

def prepare_brain_map_data(df, feature_family, active_sensors):
    """
    为大脑拓扑图聚合数据
    """
    from utils.io import get_sensor_meta
    meta = get_sensor_meta()
    
    # --- 核心修改：先创建一个带有文字标签的临时副本 ---
    df_mapped = df.copy()
    df_mapped['Label'] = df_mapped['Label'].map(LABEL_MAP).fillna(df_mapped['Label'])
    
    map_data = []
    # 只循环过滤器允许的传感器
    for s_id in active_sensors:
        col = f"{feature_family}_{s_id}"
        if col in df.columns:
            # 按文字标签分组计算均值
            grouped = df_mapped.groupby('Label')[col].mean()
            for label, value in grouped.items():
                map_data.append({
                    "State": label,  # 这里现在是 "Neutral (中性)" 等文字了
                    "Sensor": meta[s_id]["name"],
                    "X": meta[s_id]["x"],
                    "Y": meta[s_id]["y"],
                    "Value": value
                })
    return pd.DataFrame(map_data)