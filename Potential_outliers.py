import pandas as pd

# Load the data from the CSV files
mouse_metadata = pd.read_csv('Mouse_metadata.csv')
study_results = pd.read_csv('Study_results.csv')

# Merge the dataframes on the Mouse ID
merged_df = pd.merge(mouse_metadata, study_results, on='Mouse ID')

# Remove duplicate entries
cleaned_df = merged_df.drop_duplicates(subset=['Mouse ID', 'Timepoint'])

# Put treatments into a list
treatments = ['Capomulin', 'Ramicane', 'Infubinol', 'Ceftamin']

# Get the last (greatest) timepoint for each mouse
last_timepoint = cleaned_df.groupby('Mouse ID')['Timepoint'].max().reset_index()

# Merge this information back to the original DataFrame
merged_last_timepoint = pd.merge(last_timepoint, cleaned_df, on=['Mouse ID', 'Timepoint'], how='left')

# Filter the DataFrame to include only the selected treatments
filtered_treatment_df = merged_last_timepoint[merged_last_timepoint['Drug Regimen'].isin(treatments)]

# Calculate descriptive statistics and identify potential outliers
summary_stats = filtered_treatment_df.groupby('Drug Regimen')['Tumor Volume (mm3)'].agg(
    mean='mean',
    median='median',
    variance='var',
    std_deviation='std',
    SEM='sem'
).reset_index()

# Print summary statistics
print("Summary Statistics:")
print(summary_stats)

# Identify potential outliers
for drug in treatments:
    drug_data = filtered_treatment_df.loc[filtered_treatment_df['Drug Regimen'] == drug, 'Tumor Volume (mm3)']
    
    # Calculate the IQR
    quartiles = drug_data.quantile([0.25, 0.5, 0.75])
    lowerq = quartiles[0.25]
    upperq = quartiles[0.75]
    iqr = upperq - lowerq
    
    # Determine outliers using upper and lower bounds
    lower_bound = lowerq - (1.5 * iqr)
    upper_bound = upperq + (1.5 * iqr)
    outliers = drug_data[(drug_data < lower_bound) | (drug_data > upper_bound)]
    
    print(f"{drug} potential outliers: {outliers}")

# Optional: Print tumor volume data for further analysis
for drug, data in zip(treatments, tumor_vol_data):
    print(f"\nTumor volumes for {drug}:\n{data.describe()}")
