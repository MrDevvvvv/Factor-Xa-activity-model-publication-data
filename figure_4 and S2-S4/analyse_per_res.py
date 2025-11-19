import pandas as pd

# Read the data file, skip header and footer rows
mmgbsa_per_res = pd.read_table("FRAME_RESULTS_MMGBSA_per_res_adj.dat", sep=',',header=None)

# Extract the desired columns and rename them
df = pd.DataFrame ({
    'Residue': mmgbsa_per_res[0],
    'VDW': mmgbsa_per_res[5],
    'Electrostatic': mmgbsa_per_res[8],
    'Polar solvation': mmgbsa_per_res[11],
    'Non-polar solvation': mmgbsa_per_res[14],
    'Total energy': mmgbsa_per_res[17]
})


# Save the DataFrame to a CSV file
df.to_csv('mmgbsa_per_res.csv', index=False)
