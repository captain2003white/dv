import streamlit as st

def render():
    st.markdown("### 4. Conclusions and Observations (结论与观察)")
    
    # Feature Analysis Summary
    st.write("""
    In this EEG data, freq represents the complete frequency spectrum sequence, mean is the overall energy of the segment, and topFreq represents the frequency point with the highest energy. The first two principal components of PCA explain approximately 26% of the variance, which is normal to moderately high for high-dimensional EEG data, demonstrating that frequency domain differences have structural characteristics. The covariance matrix shows strong correlations between frequencies, and the three mental states exhibit distinguishable covariance patterns. In frequency spectrum analysis, we observe that Relaxed shows enhancement in the alpha band, while Concentrating shows enhancement in the beta band, which aligns with neuroscience principles. The topFreq analysis further indicates that the three mental states have different dominant frequencies, which is a key basis for frequency domain classification.
    (在这个EEG数据中, freq是完整的频谱序列, mean是该片段的整体能量, topFreq则是能量最高的频率点. PCA的前两主成分解释了约26%的变化, 对于高维EEG数据属于正常偏高水平, 证明频域差异具有结构性. 协方差矩阵显示频率之间存在强相关, 三种心理状态具有可区分的协方差模式. 频谱分析中, 我们看到Relaxed在alpha带增强, Concentrating在beta带增强, 符合脑科学规律. topFreq的分析进一步表明三种心理状态的主导频率不同, 这是频域分类的关键依据)
    """)

    # --- Spatial Activation Analysis ---
    st.markdown("#### Spatial Activation Analysis (空间激活分析)")
    
    # Combined conclusion 1, 2, 3
    st.write("""
    **Right Frontal Volatility (右前额叶波动性)**: In the Standard Deviation map, the AF8 sensor (Right Forehead) shows a dramatic increase during Concentration (Value ~159) compared to Neutral (~11) and Relaxed (~32) states. This indicates that high-intensity signal fluctuation in the right frontal lobe is the most significant biomarker for detecting mental focus. While the mean voltage is moderate, the variability is extreme, suggesting rapid neural processing.
    (右前额叶波动性: 在标准差图中, AF8传感器(右前额)在专注时显示出剧烈增加(数值约159), 相比于中性(约11)和放松(约32)状态. 这表明右前额叶的高强度信号波动是检测精神专注最显著的生物标记. 虽然平均电压适中, 但变异性极大, 暗示了快速的神经处理)
    
    **Hemispheric Lateralization (大脑半球侧化)**: Regarding Mean Voltage during Concentration, AF7 (Left) records a value of 29 while AF8 (Right) records 14. We observe a dissociation between signal power and volatility. The left hemisphere dominates in baseline activation (Mean), while the right hemisphere dominates in dynamic fluctuation (Std), supporting the theory of functional asymmetry.
    (大脑半球侧化: 关于专注时的平均电压, AF7(左侧)记录值为29, 而AF8(右侧)记录值为14. 我们观察到信号功率与波动性的分离. 左半球在基线激活(均值)上占主导, 而右半球在动态波动(标准差)上占主导, 支持了功能不对称理论)
    
    **State Consistency (状态一致性)**: In the Violin Plots, the distribution shape for 'Concentrating' is notably narrow and elongated, whereas 'Relaxed' and 'Neutral' shapes are wide and flat. A narrow distribution implies low variance among samples, proving that Concentration is a highly consistent and stable neural state. Conversely, Relaxation is characterized by high variability and lower predictability.
    (状态一致性: 在小提琴图中, 专注的分布形状显著狭窄且细长, 而放松和中性的形状则宽且扁. 狭窄的分布意味着样本间方差低, 证明专注是一种高度一致且稳定的神经状态. 相反, 放松的特征是高变异性和较低的可预测性)
    """)
