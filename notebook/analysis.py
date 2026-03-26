# Smart City Sensor Data Analysis 2026
# Python script ready to run in Jupyter Notebook

# ------------------------------
# Install required packages (run once)
# ------------------------------
!pip install pandas matplotlib seaborn scipy --quiet

# ------------------------------
# Imports
# ------------------------------
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

sns.set(style='whitegrid')

# ------------------------------
# Load CSV Files
# ------------------------------
data_path = 'data/processed/'  # Change to 'data/raw/' or 'data/sample/' if needed

traffic = pd.read_csv(data_path + 'traffic_sensors_processed.csv')
air_quality = pd.read_csv(data_path + 'air_quality_sensors_processed.csv')
weather = pd.read_csv(data_path + 'weather_station_processed.csv')
energy = pd.read_csv(data_path + 'energy_grid_processed.csv')

# ------------------------------
# Preview Data
# ------------------------------
print('Traffic Sensors Preview:')
display(traffic.head())

print('Air Quality Sensors Preview:')
display(air_quality.head())

print('Weather Stations Preview:')
display(weather.head())

print('Energy Grid Preview:')
display(energy.head())

# ------------------------------
# Descriptive Statistics
# ------------------------------
print('Traffic Sensors Stats:')
display(traffic.describe())

print('Air Quality Sensors Stats:')
display(air_quality.describe())

print('Weather Stations Stats:')
display(weather.describe())

print('Energy Grid Stats:')
display(energy.describe())

# ------------------------------
# Merge Datasets by Timestamp and Location
# ------------------------------
merged = pd.merge(traffic, air_quality, on=['timestamp','location'], how='outer')
merged = pd.merge(merged, weather, on=['timestamp','location'], how='outer')
merged = pd.merge(merged, energy, on=['timestamp','location'], how='outer')

print('Merged Dataset Preview:')
display(merged.head())

# ------------------------------
# Visualizations
# ------------------------------
# Traffic count over time per zone
plt.figure(figsize=(10,5))
sns.lineplot(data=traffic, x='timestamp', y='traffic_count', hue='location')
plt.xticks(rotation=45)
plt.title('Traffic Count per Zone')
plt.xlabel('Timestamp')
plt.ylabel('Traffic Count')
plt.tight_layout()
plt.show()

# PM2.5 over time per zone
plt.figure(figsize=(10,5))
sns.lineplot(data=air_quality, x='timestamp', y='pm25', hue='location')
plt.xticks(rotation=45)
plt.title('Air Quality PM2.5 per Zone')
plt.xlabel('Timestamp')
plt.ylabel('PM2.5 (µg/m³)')
plt.tight_layout()
plt.show()

# ------------------------------
# Correlation Heatmap
# ------------------------------
numeric_cols = merged.select_dtypes(include='number')
corr = numeric_cols.corr()

plt.figure(figsize=(12,8))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Heatmap')
plt.show()

# ------------------------------
# Simple Anomaly Detection (Z-Score)
# ------------------------------
z_scores = numeric_cols.apply(stats.zscore)
anomalies = (z_scores.abs() > 3).any(axis=1)
print(f'Number of anomalies detected: {anomalies.sum()}')
display(merged[anomalies])
