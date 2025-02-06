import os
import pandas as pd
import matplotlib.pyplot as plt

# Function to plot a selected PPG CSV file
def plot_ppg_csv(csv_file_path):
    """
    Plots the PPGG (Green PPG) signal from a CSV file.

    Parameters:
        csv_file_path (str): Path to the PPG CSV file.
    """
    if not os.path.exists(csv_file_path):
        print(f"⚠️ Error: File '{csv_file_path}' not found!")
        return

    try:
        # Load the CSV file
        df = pd.read_csv(csv_file_path)

        # Check if required columns exist
        if "Time" not in df.columns or "PPG_Amplitude" not in df.columns:
            print(f"⚠️ Error: Invalid CSV format! Expected columns: 'Time (s)', 'PPGG'")
            return

        # Plot the PPG signal
        plt.figure(figsize=(10, 5))
        plt.plot(df["Time"], df["PPG_Amplitude"], color="green", alpha=0.8, label="PPGG (Green PPG)")
        plt.xlabel("Time (s)")
        plt.ylabel("PPG Amplitude")
        plt.title(f"PPG Signal from {os.path.basename(csv_file_path)}")
        plt.legend()
        plt.grid()
        plt.show()

    except Exception as e:
        print(f"⚠️ Error reading file: {e}")

# Example usage
csv_file_path = "PPGCSV/149098.csv"  # Replace with actual file path
plot_ppg_csv(csv_file_path)
