import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from scipy import stats

sns.set(style='whitegrid')


def plot_line(df, x_col, y_col, hue_col=None, title="", xlabel="", ylabel="", save_path=None):
    """Plot a line chart with optional hue (category)."""
    plt.figure(figsize=(10,5))
    sns.lineplot(data=df, x=x_col, y=y_col, hue=hue_col, marker='o')
    plt.xticks(rotation=45)
    plt.title(title)
    plt.xlabel(xlabel or x_col)
    plt.ylabel(ylabel or y_col)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.show()


def plot_correlation_heatmap(df, numeric_cols=None, save_path=None):
    """Plot correlation heatmap for numeric columns."""
    if numeric_cols is None:
        numeric_cols = df.select_dtypes(include='number')
    corr = numeric_cols.corr()
    plt.figure(figsize=(12,8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
    plt.title('Correlation Heatmap')
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.show()


def plot_anomalies(df, numeric_cols=None, method='zscore', z_threshold=3, iqr_factor=1.5):
    """
    Detect and highlight anomalies.
    
    method: 'zscore' or 'iqr'
    z_threshold: threshold for z-score
    iqr_factor: multiplier for IQR
    """
    if numeric_cols is None:
        numeric_cols = df.select_dtypes(include='number')

    anomalies = pd.Series(False, index=df.index)

    if method == 'zscore':
        z_scores = numeric_cols.apply(stats.zscore)
        anomalies = (z_scores.abs() > z_threshold).any(axis=1)
    elif method == 'iqr':
        Q1 = numeric_cols.quantile(0.25)
        Q3 = numeric_cols.quantile(0.75)
        IQR = Q3 - Q1
        anomalies = ((numeric_cols < (Q1 - iqr_factor * IQR)) | 
                     (numeric_cols > (Q3 + iqr_factor * IQR))).any(axis=1)
    else:
        raise ValueError("method must be 'zscore' or 'iqr'")

    print(f"Number of anomalies detected: {anomalies.sum()}")
    if anomalies.any():
        print("Anomalous rows:")
        display(df[anomalies])

    # Plot anomalies if numeric_cols has only 1 column, otherwise skip plotting
    if len(numeric_cols.columns) == 1:
        col = numeric_cols.columns[0]
        plt.figure(figsize=(10,5))
        plt.plot(df.index, numeric_cols[col], label=col)
        plt.scatter(df.index[anomalies], numeric_cols.loc[anomalies, col], color='red', label='Anomaly')
        plt.title(f'Anomaly Detection ({method})')
        plt.xlabel('Index')
        plt.ylabel(col)
        plt.legend()
        plt.tight_layout()
        plt.show()


def plot_histogram(df, col, bins=30, save_path=None):
    """Simple histogram."""
    plt.figure(figsize=(8,5))
    sns.histplot(df[col], bins=bins, kde=True)
    plt.title(f'Histogram of {col}')
    plt.xlabel(col)
    plt.ylabel('Frequency')
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.show()


def plot_boxplot(df, col, save_path=None):
    """Simple boxplot."""
    plt.figure(figsize=(8,5))
    sns.boxplot(y=df[col])
    plt.title(f'Boxplot of {col}')
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.show()
