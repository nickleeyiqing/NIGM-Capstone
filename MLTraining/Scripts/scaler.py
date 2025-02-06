import os
import pandas as pd

import matplotlib.pyplot as plt


def extract_scaling_factor_and_offset(hea_file):
    """
    Extracts the scaling factor and offset for the Green channel (PPGG) from a .hea file.
    """
    scaling_factor = None
    offset = None
    with open(hea_file, "r") as file:
        for line in file:
            if "PPG_G" in line:
                try:
                    scaling_factor = float(line.split()[2].split("(")[0])  # Extract scaling factor
                    offset = float(line.split()[2].split("(")[1].split(")")[0])  # Extract offset
                    print(f"Scaling factor for {hea_file}: {scaling_factor}")
                    print(f"Offset for {hea_file}: {offset}")
                except ValueError:
                    print(f"Error extracting scaling or offset from {hea_file}")
    return scaling_factor, offset


def fix_scaling_for_segment(segment_id, csv_folder, hea_folder):
    """
    Fixes scaling for a PPG segment based on the .hea file.

    Parameters:
        segment_id (str): The segment ID (e.g., '100001').
        csv_folder (str): Path to the folder containing PPG CSV files.
        hea_folder (str): Path to the folder containing .hea files.

    Returns:
        pd.DataFrame: DataFrame with corrected PPGG values.
    """
    # File paths
    csv_file = os.path.join(csv_folder, f"{segment_id}.csv")
    hea_file = os.path.join(hea_folder, segment_id, f"{segment_id}_PPG.hea")
    
    # Check if files exist
    if not os.path.exists(hea_file):
        print(f"⚠️ Missing HEA file for segment ID: {segment_id}")
        return None
    if not os.path.exists(csv_file):
        print(f"⚠️ Missing CSV file for segment ID: {segment_id}")
        return None

    # Extract scaling factor and offset
    scaling_factor, offset = extract_scaling_factor_and_offset(hea_file)
    if not scaling_factor:
        print(f"⚠️ Could not extract scaling factor for segment ID: {segment_id}")
        return None

    # Load the PPG CSV file
    df = pd.read_csv(csv_file)

    # Debug: Print raw values
    print("Raw PPGG values (from CSV):")
    print(df["PPGG"].head())

    # Apply scaling and offset
    if offset is not None:
        df["PPGG"] = (df["PPGG"] + offset) / scaling_factor
    else:
        df["PPGG"] = df["PPGG"] / scaling_factor

    # Debug: Print corrected values
    print(f"Corrected PPGG values for segment {segment_id}:")
    print(df["PPGG"].head())

    # Optional: Normalize the PPGG values
    # Keep raw scaled values
    df["PPGG"] = (df["PPGG"] + offset) / scaling_factor if offset is not None else df["PPGG"] / scaling_factor
    print(f"Normalized PPGG values for segment {segment_id}:")
    print(df["PPGG"].head())

    return df


# Process all CSV files for corresponding HEA files
csv_folder = "PPGCSV"  # Update with the path to your CSV files
hea_folder = "SP_PPG"         # Update with the path to your HEA files

# Initialize a list to store corrected DataFrames
all_data = []

for folder in os.listdir(hea_folder):
    segment_id = folder  # Each folder represents a segment ID (e.g., '100001')
    segment_folder = os.path.join(hea_folder, folder)
    
    if os.path.isdir(segment_folder):  # Check if it's a directory
        df_corrected = fix_scaling_for_segment(segment_id, csv_folder, hea_folder)
        if df_corrected is not None:
            # Add Segment ID to the DataFrame
            df_corrected["Segment_ID"] = segment_id
            all_data.append(df_corrected)

# Combine all corrected DataFrames
if all_data:
    combined_df = pd.concat(all_data, ignore_index=True)

    # Save the combined data to a CSV file
    combined_csv_path = os.path.join(csv_folder, "combined_ppg_data2.csv")
    combined_df.to_csv(combined_csv_path, index=False)
    print(f"✅ Combined and corrected data with Segment_ID saved to: {combined_csv_path}")
else:
    print("⚠️ No valid data to combine.")

