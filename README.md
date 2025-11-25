# EEG Mental State Decoding Analytics System

## Project Overview

This is an interactive EEG (Electroencephalogram) data analysis and visualization application built with Streamlit. The project analyzes brain activity data collected from Muse Headband devices to decode and visualize three distinct mental states: **Relaxed**, **Neutral**, and **Concentrating**.

Through multi-dimensional statistical analysis and visualization techniques, this project demonstrates the characteristics of EEG signals under different mental states, helping to understand the patterns of brain activity.

## Features

- 📊 **Interactive Data Visualization**: Web-based interface using Streamlit with real-time interaction support
- 📈 **Feature Type Statistics**: Count and distribution analysis of different feature types (mean, std, skew, kurt, covM, freq, etc.)
- 🔍 **PCA Dimensionality Reduction**: 2D projection visualization with explained variance analysis
- 🔗 **Covariance Matrix Visualization**: Correlation matrix visualization of covariance matrix features
- 📡 **Frequency Spectrum Analysis**: Frequency domain analysis with spectrum plots and top frequency analysis
- 🧠 **Multi-dimensional Spatial Analysis**:
  - Signal Power (Mean Voltage)
  - Signal Stability (Standard Deviation)
  - Signal Shape (Skewness)
- 🗺️ **Spatial Activation Mapping**: Brain topography maps showing activation patterns across different brain regions
- 📊 **Statistical Distribution Comparison**: Violin plots displaying distribution characteristics across different states
- 📉 **Global Separability Analysis**: Parallel coordinates plots showing signal flow paths
- 🎯 **Region Filtering**: Support for filtering analysis by brain regions (Frontal Lobe, Temporal Lobe, or All Sensors)

## Project Structure

```
pre/
├── app.py                    # Main application entry point
├── requirements.txt          # Python dependency list
├── README.md                # Project documentation
├── data/
│   └── mental-state.csv     # EEG dataset
├── assets/
│   ├── efrei.png           # EFREI University logo
│   └── WUT-Logo.png        # WUT University logo
├── sections/                # Page modules
│   ├── intro.py            # Introduction page
│   ├── overview.py         # Overview analysis page
│   ├── deep_dives.py       # Deep dive analysis page
│   └── conclusions.py      # Conclusions page
└── utils/                   # Utility functions
    ├── io.py               # Data loading and region filtering
    ├── prep.py             # Data preprocessing (PCA, etc.)
    └── viz.py              # Visualization functions
```

## Running the Application

Run the following command in the project root directory:

```bash
streamlit run app.py
```

The application will automatically open in your browser at `http://localhost:8501`

## Data Description

### Data Sources

- **Dataset**: [Kaggle - EEG Brainwave Dataset Mental State](https://www.kaggle.com/datasets/birdy654/eeg-brainwave-dataset-mental-state)
- **Feature Extraction Code**: [GitHub - EEG Feature Generation](https://github.com/jordan-bird/eeg-feature-generation)

### Data Characteristics

- **Subjects**: 4 (2 male, 2 female)
- **Collection Device**: Muse Headband
- **Recording Duration**: 60 seconds per state
- **Sensor Configuration**:
  - **TP9** (_0): Left Ear, Temporal Lobe, Auditory Processing
  - **AF7** (_1): Left Forehead, Frontal Lobe, Logic & Attention
  - **AF8** (_2): Right Forehead, Frontal Lobe, Emotion & Focus
  - **TP10** (_3): Right Ear, Temporal Lobe, Memory & Spatial

### Label Description

- `0`: Neutral
- `1`: Relaxed
- `2`: Concentrating

### Data Features

The dataset contains 989 features extracted from each sensor, categorized into the following types:
- **mean**: Mean Voltage (Signal Power) - 84 features
- **std**: Standard Deviation (Signal Stability) - 16 features
- **skew**: Skewness (Signal Shape) - 8 features
- **kurt**: Kurtosis - 8 features
- **covM**: Covariance Matrix - 40 features
- **logcovM**: Log Covariance Matrix - 20 features
- **eigen**: Eigenvalues - 8 features
- **freq**: Frequency features - 576 features (longest feature sequence)
- **topFreq**: Top Frequencies - 80 features

Where sensor numbers are indicated by suffixes: `_0` (TP9), `_1` (AF7), `_2` (AF8), `_3` (TP10)

## Technology Stack

- **Streamlit** (≥1.33): Web application framework
- **Pandas** (≥1.5.0): Data processing
- **NumPy** (≥1.21.0): Numerical computation
- **Plotly** (≥5.13.0): Interactive visualization
- **Scikit-learn** (≥1.2.0): Machine learning tools (PCA)

## Main Functional Modules

### 1. Introduction Page (intro.py)

- Data background description
- Sensor configuration introduction
- Dataset overview display
- Class distribution statistics

### 2. Overview Analysis (overview.py)

- **Parallel Coordinates Plot**: Visualizes signal flow paths across different sensors (TP9, AF7, AF8, TP10)

### 3. Deep Dive Analysis (deep_dives.py)

Supports filtering by brain regions and provides comprehensive feature analysis across five major sections:

#### (1) Feature Type Statistics
- Bar chart displaying count and distribution of different feature types
- Feature type descriptions and metrics (mean, std, skew, kurt, covM, logcovM, eigen, freq, topFreq)

#### (2) PCA Dimensionality Reduction
- 2D scatter plot visualization of data projection
- Explained variance ratio metrics for PC1 and PC2
- Color-coded by mental state (Neutral, Relaxed, Concentrating)

#### (3) Covariance Matrix Visualization
- Correlation matrix heatmap of covariance matrix (covM) features
- Shows relationships between different covariance matrix elements

#### (4) Frequency Spectrum Analysis
- Interactive sensor selection for frequency analysis
- Frequency spectrum line plots showing amplitude across frequency indices
- Top frequency analysis table displaying mean top frequencies by mental state

#### (5) Spatial Activation Analysis

Spatial activation maps and distribution comparisons across three dimensions (supports region filtering):

**A. Signal Power (Mean Voltage)**
- Brain Topography Map: Shows activation intensity across brain regions
- Regional Distribution Comparison: Violin plots comparing distributions across different states

**B. Signal Stability (Standard Deviation)**
- Brain Topography Map: Identifies signal fluctuation patterns
- Regional Distribution Comparison: Analyzes high volatility characteristics during concentration states

**C. Signal Shape (Skewness)**
- Brain Topography Map: Detects activity spikes with color-coded positive/negative skewness
- Regional Distribution Comparison: Analyzes signal distribution symmetry
- Detailed explanation of skewness interpretation included

### 4. Conclusions Page (conclusions.py)

Summarizes key findings based on deep dive analysis results:
- Right Frontal Lobe Volatility Analysis
- Hemispheric Lateralization Features
- State Consistency Observations

## Usage Guide

1. **After launching the application**, in the sidebar you can:
   - Select analysis focus (All Sensors, Frontal Lobe, or Temporal Lobe)
   - View data sources and references

2. **Browse through sections**:
   - Learn about data background from the introduction page
   - View signal flow paths in the overview (parallel coordinates plot)
   - Explore comprehensive feature analysis in deep dive section:
     - Feature type statistics
     - PCA dimensionality reduction
     - Covariance matrix visualization
     - Frequency spectrum analysis
     - Spatial activation maps with violin plots
   - View key findings in conclusions

3. **Interactive Features**:
   - All charts support zoom and pan
   - Hover to view detailed values
   - Switch analysis regions via sidebar

## Key Findings

Based on data analysis results:

1. **Right Frontal Lobe Volatility**: During concentration states, the AF8 sensor shows exceptionally high standard deviation (~159), indicating this is an important biomarker for detecting mental focus.

2. **Hemispheric Lateralization**:
   - Left hemisphere (AF7) dominates in baseline activation (Mean)
   - Right hemisphere (AF8) dominates in dynamic fluctuation (Std Dev)

3. **State Consistency**: Concentration state distributions are narrower and more concentrated, indicating it is a more stable and predictable neural state.

## Author Information

- GitHub: [@captain2003white](https://github.com/captain2003white)

## License

This project is for educational and research purposes only.

## Acknowledgments

- Data Provider: Kaggle Community
- Feature Extraction Method: GitHub - jordan-bird/eeg-feature-generation
- Dataset Creator: Jordan j.bird
