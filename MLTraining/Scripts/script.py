import os
import numpy as np
import pandas as pd

# Function to extract scaling factors from .hea file
def extract_scaling_factors(hea_file):
    """Extracts the scaling factor for the Green channel (PPG_G) from .hea file."""
    with open(hea_file, "r") as file:
        for line in file:
            if "PPG_G" in line:
                try:
                    return float(line.split()[2].split("(")[0])  # Extract only the numeric scaling factor
                except ValueError:
                    return None  # Handle errors safely
    return None  # Return None if no PPG_G factor is found

# Function to read and scale only the Green PPG channel from a .dat file
def read_ppg_green(dat_file, scaling_factor, sampling_rate=30, num_channels=3):
    """Reads a .dat file and extracts the scaled Green PPG signal (PPGG)."""
    try:
        # Read raw binary data
        raw_data = np.fromfile(dat_file, dtype=np.int16)

        # Reshape into separate channels (R, G, B)
        ppg_data = raw_data.reshape(-1, num_channels)

        # Extract & scale only the Green channel (middle column)
        scaled_ppg_g = ppg_data[:, 1] * scaling_factor

        return {
            "Time (s)": np.arange(ppg_data.shape[0]) / sampling_rate,
            "PPGG": scaled_ppg_g
        }

    except Exception as e:
        print(f"⚠️ Error reading {dat_file}: {e}")
        return None

# Main function to convert BRNO PPG dataset to CSV (only Green channel)
def convert_brno_ppg_green_to_csv(dataset_path, output_csv_path):
    """
    Converts BRNO PPG dataset to CSV files with only the Green channel (PPGG).

    Parameters:
        dataset_path (str): Path to the root dataset directory.
        output_csv_path (str): Directory to save optimized CSV files.
    """
    os.makedirs(output_csv_path, exist_ok=True)  # Ensure output directory exists

    subject_dirs = [d for d in os.listdir(dataset_path) if d.isdigit()]  # Get subject directories

    for subject_id in subject_dirs:
        subject_path = os.path.join(dataset_path, subject_id)

        ppg_dat_file = os.path.join(subject_path, f"{subject_id}_PPG.dat")
        ppg_hea_file = os.path.join(subject_path, f"{subject_id}_PPG.hea")

        # Ensure both .dat and .hea files exist
        if os.path.exists(ppg_dat_file) and os.path.exists(ppg_hea_file):
            scaling_factor = extract_scaling_factors(ppg_hea_file)  # Extract Green channel factor

            if scaling_factor:
                ppg_green = read_ppg_green(ppg_dat_file, scaling_factor)  # Read and scale Green channel

                if ppg_green:
                    # Convert to DataFrame
                    df = pd.DataFrame(ppg_green)

                    # Save as CSV
                    csv_filename = f"{subject_id}.csv"
                    csv_filepath = os.path.join(output_csv_path, csv_filename)
                    df.to_csv(csv_filepath, index=False)
                    print(f"✅ Saved: {csv_filename}")

    print(f"\n🎉 Conversion Complete! CSV files saved to: {output_csv_path}")

# Example usage (update these paths)
dataset_root = "SP_PPG"
csv_output_dir = "PPGCSV"

# Run the conversion
convert_brno_ppg_green_to_csv(dataset_root, csv_output_dir)