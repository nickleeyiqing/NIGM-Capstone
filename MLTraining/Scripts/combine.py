import pandas as pd

# Load subject info & quality annotation files
subject_info_path = "SP_PPG\subject-info.csv"
quality_hr_path = "SP_PPG\quality-hr-ann.csv"

df_subjects = pd.read_csv(subject_info_path)
df_quality = pd.read_csv(quality_hr_path)

# Merge both files using the common 'Subject ID' column
df_merged = df_subjects.merge(df_quality, on="ID", how="inner")  # 'inner' keeps only matching records

# Save the merged dataset
merged_output_path = "SP_PPG/merged_subjects_quality.csv"
df_merged.to_csv(merged_output_path, index=False)

print(f"✅ Merged file saved to: {merged_output_path}")

# Display first few rows
import ace_tools as tools
tools.display_dataframe_to_user(name="Merged Subject & Quality Data", dataframe=df_merged)
