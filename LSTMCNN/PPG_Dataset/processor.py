import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, resample


# Define filtering functions
def lowpass_filter(data, cutoff=15, fs=2175, order=4):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low')
    return filtfilt(b, a, data)


def bandpass_filter(data, lowcut=0.5, highcut=8, fs=30, order=4):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, data)


# Function to process a single pair of signal and label files
def process_ppg_file(signal_path, label_path, target_sampling_rate=30):
    # Load data
    signal_data = pd.read_csv(signal_path, header=None).values.flatten()
    label_data = pd.read_csv(label_path)

    # Apply low-pass filter to prevent aliasing before downsampling
    filtered_signal = lowpass_filter(signal_data)

    # Downsample the signal
    original_sampling_rate = 2175
    num_samples = int(len(filtered_signal) * (target_sampling_rate / original_sampling_rate))
    downsampled_signal = resample(filtered_signal, num_samples)

    # Apply band-pass filter after downsampling
    processed_signal = bandpass_filter(downsampled_signal, fs=target_sampling_rate)

    # Normalize the signal (Z-score normalization)
    processed_signal = (processed_signal - np.mean(processed_signal)) / np.std(processed_signal)

    # Extract relevant labels (Glucose level, Age, Gender, etc.)
    glucose_level = label_data['Glucose'].values[0]
    age = label_data['Age'].values[0]
    gender = 1 if label_data['Gender'].values[0] == 'Male' else 0  # Encode gender as 1 (Male) and 0 (Female)

    return processed_signal, glucose_level, age, gender


# Process all files in the given directory
def process_all_ppg_files(root_folder, output_file):
    signal_folder = os.path.join(root_folder, "RawData")
    label_folder = os.path.join(root_folder, "Labels")

    # Check if folders exist
    if not os.path.exists(signal_folder):
        raise FileNotFoundError(f"Error: Signal folder not found at {signal_folder}")
    if not os.path.exists(label_folder):
        raise FileNotFoundError(f"Error: Label folder not found at {label_folder}")

    processed_data = []

    # Loop through all signal files
    for signal_file in os.listdir(signal_folder):
        if signal_file.startswith('signal') and signal_file.endswith('.csv'):
            # Get corresponding label file
            label_file = signal_file.replace('signal', 'label')
            signal_path = os.path.join(signal_folder, signal_file)
            label_path = os.path.join(label_folder, label_file)

            if os.path.exists(label_path):
                processed_signal, glucose_level, age, gender = process_ppg_file(signal_path, label_path)
                processed_data.append([processed_signal, glucose_level, age, gender])
            else:
                print(f"Warning: No matching label file for {signal_file}")

    # Convert to DataFrame and save
    df = pd.DataFrame(processed_data, columns=['PPG_Signal', 'Glucose_Level', 'Age', 'Gender'])
    df.to_pickle(output_file)  # Save as a pickle file for easy loading later
    print(f"Processed data saved to {output_file}")


# Function to visualize PPG signals
def plot_ppg_signals(pickle_file, num_samples=5):
    df = pd.read_pickle(pickle_file)
    plt.figure(figsize=(12, 6))
    for i in range(min(num_samples, len(df))):
        ppg_signal = df.iloc[i]["PPG_Signal"]
        plt.plot(ppg_signal, label=f"Sample {i + 1} (Glucose: {df.iloc[i]['Glucose_Level']} mg/dL)")
    plt.xlabel("Time (samples at 30Hz)")
    plt.ylabel("Normalized PPG Amplitude")
    plt.title("Visualization of Processed PPG Signals")
    plt.legend()
    plt.show()

# Example usage
# process_all_ppg_files(r"C:\Users\Tiddie Destroyer\Downloads\PPG_Dataset", "processed_ppg_data.pkl")
plot_ppg_signals("processed_ppg_data.pkl")
