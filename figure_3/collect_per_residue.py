import os
import pandas as pd

# Set the root folder containing subfolders with CSV files
root_folder = os.getcwd()  # Replace with the actual root folder path

# Initialize variables to store the first column and last columns
first_column = None
last_columns = []

# Iterate through subfolders and their subfolders
for root, dirs, files in os.walk(root_folder):
    for file in files:
        if file.endswith('per_res.csv'):
            file_path = os.path.join(root, file)
            df = pd.read_csv(file_path)
            
            # Extract the first column from the first file only
            if first_column is None:
                first_column = df.iloc[:, 0].tolist()  # Properly extract the first column
            
            # Extract the last column and append to the list
            last_columns.append(df.iloc[:, -1].tolist())  # Properly extract the last column

# Combine the extracted columns into a DataFrame
if first_column is not None and last_columns:
    combined_df = pd.DataFrame({'Residue': first_column})
    for i, last_col in enumerate(last_columns):
        combined_df[f'Total energy {i+1}'] = last_col
    
    # Save the combined DataFrame to a new CSV file
    combined_df.to_csv('Combined_per_residue_data.csv', index=False)
    
    # Print the resulting combined DataFrame
    print("Combined DataFrame:")
    print(combined_df)
else:
    print("No valid CSV files found in the subfolders.")
