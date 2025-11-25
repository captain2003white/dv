import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

def plot_pca_2d(pca_df):
    return px.scatter(pca_df, x='PC1', y='PC2', color='Label',
                      title="2D Data Projection PCA (数据二维投影)",
                      opacity=0.6, template="plotly_white",
                      color_discrete_sequence=px.colors.qualitative.Bold)

def plot_brain_map(map_df, feature_name):
    """
    Draws the Brain Topography Map (3 Heads for 3 States)
    """
    if map_df.empty:
        return px.scatter(title="No Data for Brain Map")

    # --- FIX: Handle negative values for bubble size ---
    # Skewness (偏度) can be negative, but bubble size cannot be negative.
    # We create a new column 'Size_Value' using absolute values for the bubble size.
    # The color will still reflect the real value (positive or negative).
    map_df['Size_Value'] = map_df['Value'].abs()

    # Choose color scale based on feature type
    # For skewness, use a more intuitive color scale that emphasizes the direction
    if feature_name.lower() in ['skew', 'skewness']:
        # For skewness: Red = positive (right tail, upward spikes), Blue = negative (left tail, downward spikes)
        color_scale = "RdYlBu_r"  # Red-Yellow-Blue reversed: Red for positive, Blue for negative
        title_suffix = f"{feature_name} (红色=正偏度/向上尖峰, 蓝色=负偏度/向下尖峰)"
    else:
        color_scale = "RdBu_r"  # Standard Red-Blue for mean/std
        title_suffix = f"{feature_name}"

    # Create scatter plot with facets
    fig = px.scatter(map_df, x="X", y="Y", facet_col="State", 
                     size="Size_Value",  # Use Absolute Value for Size
                     color="Value",      # Use Real Value for Color
                     hover_name="Sensor",
                     # Use appropriate color scale
                     color_continuous_scale=color_scale, 
                     size_max=45,
                     title=f"Spatial Activation Map {title_suffix} (空间激活分布图)",
                     template="plotly_dark")
    
    # Hide axes to look like a map, not a chart
    fig.update_xaxes(showgrid=False, zeroline=False, showticklabels=False)
    fig.update_yaxes(showgrid=False, zeroline=False, showticklabels=False)
    
    # Add a circle shape to represent the head
    fig.update_layout(shapes=[
        dict(type="circle", xref="x", yref="y", x0=-5, y0=-1, x1=5, y1=5, line_color="white")
    ])
    return fig

def plot_violin_comparison(df, feature_family, active_sensors):
    """
    Aggregates selected sensors and plots distribution
    """
    # 1. Select relevant columns
    cols = [f"{feature_family}_{s}" for s in active_sensors if f"{feature_family}_{s}" in df.columns]
    
    if not cols:
        return px.scatter(title="No Data")

    # --- FIX: Map labels for the Violin Plot as well ---
    plot_df = df.copy()
    label_map = {
        0: "Neutral (中性)", 
        1: "Relaxed (放松)", 
        2: "Concentrating (专注)"
    }
    plot_df['Label'] = plot_df['Label'].map(label_map)

    # 2. Average the values across the selected region
    plot_df['Regional_Avg'] = plot_df[cols].mean(axis=1)
    
    # 3. Plot Violin
    fig = px.violin(plot_df, x="Label", y="Regional_Avg", color="Label", box=True,
                    points=False, 
                    title=f"Regional Distribution {feature_family} (区域分布对比)",
                    template="seaborn")
    return fig

def plot_parallel_coordinates(df):
    """
    平行坐标图:展示每个样本在4个传感器上的原始数值路径
    """
    # 1. 选择要展示的列（这里选 Mean 电压，因为它最直观）
    cols = ['mean_0', 'mean_1', 'mean_2', 'mean_3']
    
    # 2. 数据准备
    plot_df = df[cols + ['Label']].copy()
    
    # 平行坐标图在 Plotly 中需要数字作为颜色映射，所以我们需要手动映射一下
    # 但为了图例显示文字，我们用稍微 trick 一点的方法：使用 px.line_polars 的逻辑或者直接用 scatter 模拟
    # 不过 px.parallel_coordinates 是最标准的
    
    # 为了颜色能正确显示类别，我们需要把 Label 映射回数字，但作为 color_continuous_scale 使用
    label_map_reverse = {
        "Neutral (中性)": 0,
        "Relaxed (放松)": 1, 
        "Concentrating (专注)": 2
    }
    # 处理可能已经是数字的情况
    if plot_df['Label'].dtype == 'O': # 如果是字符串
         plot_df['Color_ID'] = plot_df['Label'].map(label_map_reverse)
    else:
         plot_df['Color_ID'] = plot_df['Label']

    fig = px.parallel_coordinates(plot_df, 
                                  dimensions=cols,
                                  color="Color_ID",
                                  # 使用红蓝绿配色
                                  color_continuous_scale=[(0.0, "blue"), (0.5, "green"), (1.0, "red")],
                                  labels={
                                      "mean_0": "TP9 (Left Ear)",
                                      "mean_1": "AF7 (Left Front)",
                                      "mean_2": "AF8 (Right Front)",
                                      "mean_3": "TP10 (Right Ear)"
                                  },
                                  title="Global Signal Path: Raw Voltage Flow (全局信号路径：原始电压流向)")
    
    # 隐藏侧边的颜色条数字，因为只有0,1,2没意义
    fig.update_layout(coloraxis_showscale=False)
    
    return fig

def plot_feature_type_counts(feature_types):
    """
    绘制特征类型统计柱状图
    """
    type_counts = {k: len(v) for k, v in feature_types.items()}
    df_counts = pd.DataFrame(list(type_counts.items()), columns=['Feature Type', 'Count'])
    df_counts = df_counts.sort_values('Count', ascending=False)
    
    fig = px.bar(df_counts, x='Feature Type', y='Count',
                 title='Feature Type Statistics (特征类型统计)',
                 labels={'Count': 'Number of Features (特征数量)', 
                        'Feature Type': 'Feature Type (特征类型)'},
                 text='Count',
                 template='plotly_white')
    fig.update_traces(textposition='outside')
    fig.update_layout(xaxis_tickangle=-45)
    return fig

def plot_pca_analysis(df):
    """
    PCA降维分析，返回PCA图和解释方差比例
    """
    # 选择数值特征
    features = df.select_dtypes(include=[np.number])
    # 排除Label列（如果它是数值类型）
    if 'Label' in features.columns:
        features = features.drop('Label', axis=1)
    
    if features.shape[0] == 0 or features.shape[1] == 0:
        return px.scatter(title="No Data"), None
    
    # 标准化
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)
    
    # PCA降维
    pca = PCA(n_components=2)
    components = pca.fit_transform(scaled_features)
    
    # 创建PCA DataFrame
    pca_df = pd.DataFrame(data=components, columns=['PC1', 'PC2'])
    label_map = {
        0: "Neutral (中性)", 
        1: "Relaxed (放松)", 
        2: "Concentrating (专注)"
    }
    pca_df['Label'] = df['Label'].map(label_map).fillna(df['Label'])
    
    # 绘制PCA散点图
    fig = px.scatter(pca_df, x='PC1', y='PC2', color='Label',
                     title='PCA Dimensionality Reduction (PCA降维可视化)',
                     labels={'PC1': f'PC1 ({pca.explained_variance_ratio_[0]:.2%} variance)',
                            'PC2': f'PC2 ({pca.explained_variance_ratio_[1]:.2%} variance)'},
                     opacity=0.6,
                     template='plotly_white',
                     color_discrete_sequence=px.colors.qualitative.Bold)
    
    # 计算解释方差比例
    explained_var = {
        'PC1': pca.explained_variance_ratio_[0],
        'PC2': pca.explained_variance_ratio_[1],
        'Total': pca.explained_variance_ratio_[0] + pca.explained_variance_ratio_[1]
    }
    
    return fig, explained_var

def plot_covariance_matrix(df, feature_types):
    """
    可视化协方差矩阵(covM特征)
    """
    covM_cols = feature_types.get('covM', [])
    if len(covM_cols) == 0:
        return px.imshow([[0]], title="No covM features found")
    
    # 提取covM特征数据
    covM_data = df[covM_cols].values
    
    # 计算协方差矩阵（如果covM特征数量合理）
    # 注意：covM特征本身可能已经是协方差矩阵的元素，我们需要理解其结构
    # 这里我们计算这些特征之间的相关性矩阵
    if covM_data.shape[1] > 1:
        corr_matrix = np.corrcoef(covM_data.T)
        
        # 如果特征太多，只取前30x30
        max_size = 30
        if corr_matrix.shape[0] > max_size:
            corr_matrix = corr_matrix[:max_size, :max_size]
            labels = covM_cols[:max_size]
        else:
            labels = covM_cols
        
        fig = px.imshow(corr_matrix,
                       title='Covariance Matrix Features Correlation (协方差矩阵特征相关性)',
                       labels=dict(x='Features (特征)', y='Features (特征)', color='Correlation (相关性)'),
                       color_continuous_scale='RdBu',
                       aspect='auto')
        return fig
    else:
        return px.scatter(title="Insufficient covM features for correlation matrix")

def plot_frequency_spectrum(df, feature_types, sensor_id='0'):
    """
    频率结构分析 - 绘制频谱图
    freq_xxx_sensor_id 是频率特征，例如 lag1_freq_010_0
    """
    freq_cols = feature_types.get('freq', [])
    # 筛选特定传感器的频率特征
    sensor_freq_cols = [c for c in freq_cols if c.endswith(f'_{sensor_id}')]
    
    if len(sensor_freq_cols) == 0:
        return px.line(title=f"No frequency features for sensor {sensor_id}")
    
    # 按状态分组计算平均频率值
    label_map = {
        0: "Neutral (中性)", 
        1: "Relaxed (放松)", 
        2: "Concentrating (专注)"
    }
    df_mapped = df.copy()
    df_mapped['Label'] = df_mapped['Label'].map(label_map).fillna(df_mapped['Label'])
    
    # 提取频率编号（例如：lag1_freq_010_0 -> 010）
    freq_values = []
    freq_cols_sorted = sorted(sensor_freq_cols)
    
    for col in freq_cols_sorted:
        # 尝试从列名提取频率值
        # 格式通常是：lag1_freq_010_0 或 lag1_freq_020_0
        parts = col.split('_')
        freq_val = None
        for part in parts:
            if part.isdigit() and len(part) >= 2:
                freq_val = int(part)
                break
        if freq_val is None:
            # 如果找不到，使用列名的hash作为频率值（用于排序）
            freq_val = hash(col) % 1000
        freq_values.append(freq_val)
    
    # 按状态分组计算平均值
    plot_data = []
    for state in df_mapped['Label'].unique():
        state_data = df_mapped[df_mapped['Label'] == state][freq_cols_sorted].mean()
        for freq, val in zip(freq_values, state_data):
            plot_data.append({
                'Frequency': freq,
                'Amplitude': val,
                'State': state
            })
    
    plot_df = pd.DataFrame(plot_data)
    
    # 按频率排序
    plot_df = plot_df.sort_values('Frequency')
    
    # 绘制频谱图
    fig = px.line(plot_df, x='Frequency', y='Amplitude', color='State',
                  title=f'Frequency Spectrum Analysis - Sensor {sensor_id} (频率结构分析 - 传感器 {sensor_id})',
                  labels={'Frequency': 'Frequency Index (频率索引)', 
                         'Amplitude': 'Amplitude (幅值)',
                         'State': 'State (状态)'},
                  template='plotly_white')
    
    return fig

def plot_feature_correlation_network(df, feature_types, selected_types=['mean', 'std', 'skew'], 
                                     top_n=30, threshold=0.7):
    """
    特征相关性网络图
    选择特定类型的特征，计算相关性，绘制网络图
    使用简单的力导向布局算法
    """
    # 收集选定的特征
    selected_features = []
    for feat_type in selected_types:
        selected_features.extend(feature_types.get(feat_type, []))
    
    if len(selected_features) == 0:
        return px.scatter(title="No features selected")
    
    # 限制特征数量
    if len(selected_features) > top_n:
        selected_features = selected_features[:top_n]
    
    # 提取特征数据并计算相关性
    feat_data = df[selected_features].values
    corr_matrix = np.corrcoef(feat_data.T)
    
    # 构建边的列表（相关性高于阈值）
    edges = []
    for i in range(len(selected_features)):
        for j in range(i+1, len(selected_features)):
            corr_val = corr_matrix[i, j]
            if abs(corr_val) >= threshold:
                edges.append((i, j, abs(corr_val)))
    
    if len(edges) == 0:
        return px.scatter(title=f"No correlations above threshold {threshold}")
    
    # 简单的力导向布局（简化版）
    n_nodes = len(selected_features)
    pos = np.random.rand(n_nodes, 2) * 2 - 1  # 初始随机位置
    
    # 迭代几次更新位置（简单的力导向算法）
    for _ in range(50):
        new_pos = pos.copy()
        for i in range(n_nodes):
            force = np.zeros(2)
            for j in range(n_nodes):
                if i != j:
                    diff = pos[i] - pos[j]
                    dist = np.linalg.norm(diff) + 0.01
                    # 排斥力
                    force += diff / dist * 0.1
                    # 如果有边，添加吸引力
                    for edge in edges:
                        if (edge[0] == i and edge[1] == j) or (edge[0] == j and edge[1] == i):
                            force -= diff * 0.05
            new_pos[i] += force
        pos = new_pos
        # 归一化到[-1, 1]范围
        pos = (pos - pos.mean(axis=0)) / (pos.std(axis=0) + 0.01) * 0.5
    
    # 提取节点和边的位置
    edge_x = []
    edge_y = []
    for edge in edges:
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    
    # 创建边的trace
    edge_trace = go.Scatter(x=edge_x, y=edge_y,
                           line=dict(width=0.5, color='#888'),
                           hoverinfo='none',
                           mode='lines')
    
    # 创建节点的trace
    node_x = []
    node_y = []
    node_text = []
    node_hover = []
    node_color = []
    type_colors = {'mean': '#ef553b', 'std': '#636efa', 'skew': '#00cc96', 'kurt': '#ffa15a'}
    
    for i, feat in enumerate(selected_features):
        x, y = pos[i]
        node_x.append(x)
        node_y.append(y)
        # 确定特征类型
        feat_type = None
        for t in selected_types:
            if feat in feature_types.get(t, []):
                feat_type = t
                break
        if feat_type is None:
            feat_type = 'unknown'
        
        node_text.append(feat.split('_')[-1])  # 显示最后一个部分（通常是传感器ID）
        node_hover.append(f"{feat}<br>Type: {feat_type}")
        node_color.append(type_colors.get(feat_type, 'gray'))
    
    node_trace = go.Scatter(x=node_x, y=node_y,
                           mode='markers+text',
                           hoverinfo='text',
                           hovertext=node_hover,
                           text=node_text,
                           textposition="middle center",
                           marker=dict(size=15,
                                     color=node_color,
                                     line=dict(width=2, color='white'),
                                     opacity=0.8))
    
    # 创建图形
    fig = go.Figure(data=[edge_trace, node_trace],
                   layout=go.Layout(
                       title=f'特征相关性网络 (Feature Correlation Network) - Threshold: {threshold}',
                       showlegend=False,
                       hovermode='closest',
                       margin=dict(b=20, l=5, r=5, t=60),
                       annotations=[dict(text=f"Features: {selected_types}, Top {len(selected_features)} features",
                                       showarrow=False,
                                       xref="paper", yref="paper",
                                       x=0.005, y=-0.002,
                                       xanchor="left", yanchor="bottom",
                                       font=dict(size=12))],
                       xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                       yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
    
    return fig