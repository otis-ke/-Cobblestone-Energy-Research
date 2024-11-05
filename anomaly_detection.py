# real_time_anomaly_detection_improved.py

# Import necessary libraries
import pandas as pd               # For handling time series data
import numpy as np                # For numerical operations
import random                     # To simulate random transaction values
import matplotlib.pyplot as plt   # For plotting the data and anomalies
from datetime import datetime     # To handle timestamps
from collections import deque     # For efficient data stream handling
import time                       # For adding delays to mimic real-time streaming

# Enable interactive plotting mode for real-time updates
plt.ion()
fig, ax = plt.subplots(figsize=(12, 6))  # Set up a plot for displaying data

# Initialize deque to store the latest data points for memory efficiency
stream_data = deque(maxlen=3600)  # Keeps only the most recent hour of data (3600 points)

# Function to generate a single transaction data point with occasional anomalies
def generate_data_point():
    """Simulates a single data point for financial transactions, with a small chance of anomaly."""
    # Normal transaction values between 50 and 150
    value = random.uniform(50, 150)
    
    # 2% chance to introduce an anomaly
    if random.random() < 0.02:
        # If anomaly, decide if it’s unusually high or low
        if random.choice([True, False]):
            value = random.uniform(300, 500)  # High anomaly
        else:
            value = random.uniform(0, 20)     # Low anomaly
    return value  # Return the simulated transaction value

# Function to detect anomalies based on rolling statistics
def detect_anomaly(series, window_size=100, threshold=3):
    """Detects anomalies based on rolling mean and standard deviation."""
    # Convert deque to Series for anomaly detection
    series = pd.Series(series)
    
    # If there are not enough data points, return a Series of False (no anomalies)
    if len(series) < window_size:
        return pd.Series([False] * len(series), index=series.index)
    
    # Calculate rolling mean and standard deviation
    rolling_mean = series.rolling(window=window_size).mean()
    rolling_std = series.rolling(window=window_size).std()
    
    # Identify anomalies as points more than 'threshold' standard deviations away from the rolling mean
    anomalies = abs(series - rolling_mean) > (threshold * rolling_std)
    
    # Fill missing values (from initial rolling mean computation) with False
    return anomalies.fillna(False)

def real_time_anomaly_detection():
    """Continuously simulates data and performs real-time anomaly detection and visualization."""
    while True:
        # Generate a new data point with timestamp
        timestamp = datetime.now()
        new_value = generate_data_point()  # Get a single simulated transaction value
        
        # Append the new data point to the deque (efficient, keeps latest 3600 points)
        stream_data.append(new_value)
        
        # Detect anomalies in the current data window
        anomalies = detect_anomaly(list(stream_data))
        
        # Plot the latest transaction data and highlight anomalies
        ax.clear()  # Clear previous plot
        series = pd.Series(list(stream_data))
        ax.plot(series.index, series, color='blue', label='Transaction Value')  # Plot data
        
        # Highlight detected anomalies in red
        anomaly_points = series[anomalies == True]
        ax.scatter(anomaly_points.index, anomaly_points, color='red', label='Anomaly')
        
        # Add labels and title for the plot
        ax.set_xlabel("Time (seconds)")
        ax.set_ylabel("Transaction Value")
        ax.set_title("Real-Time Transaction Data with Anomalies Detected")
        ax.legend()  # Display legend
        
        # Render the plot with the latest data point
        plt.draw()
        
        # Brief pause to simulate real-time streaming
        plt.pause(1)  # Wait 1 second before the next data point

# Run the real-time anomaly detection if the script is executed directly
if __name__ == "__main__":
    real_time_anomaly_detection()
