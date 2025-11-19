import pandas as pd
import matplotlib.pyplot as plt


# Define column headers
headers = ["Replicate 10", "Replicate 1", "Replicate 2", "Replicate 3", "Replicate 4", "Replicate 5", "Replicate 6", "Replicate 7", "Replicate 8", "Replicate 9"]

# Read the CSV file
df1 = pd.read_csv("lig_bb.csv", delim_whitespace=True, header=None, names=headers)
df2 = pd.read_csv("../../variants_6_7/F174A/lig_bb.csv", delim_whitespace=True, header=None, names=headers)
df3 = pd.read_csv("../../variants_6_7/F174S/lig_bb.csv", delim_whitespace=True, header=None, names=headers)
df4 = pd.read_csv("../../variants_6_7/V213E/lig_bb.csv", delim_whitespace=True, header=None, names=headers) 
df5 = pd.read_csv("../../variants_6_7/G216D/lig_bb.csv", delim_whitespace=True, header=None, names=headers)
df6 = pd.read_csv("../../variants_6_7/G218F/lig_bb.csv", delim_whitespace=True, header=None, names=headers)

# Calculate average and standard deviation of each row
avg1 = df1.mean(axis=1)
std_dev1 = df1.std(axis=1)

avg2 = df2.mean(axis=1)
std_dev2 = df2.std(axis=1)

avg3 = df3.mean(axis=1)
std_dev3 = df3.std(axis=1)

avg4 = df4.mean(axis=1)
std_dev4 = df4.std(axis=1)

avg5 = df5.mean(axis=1)
std_dev5 = df5.std(axis=1)

avg6 = df6.mean(axis=1)
std_dev6 = df6.std(axis=1)


# Plot
plt.plot(range(len(avg1)), avg1, color='red', linewidth=2, label='Wild-type')
plt.fill_between(range(len(avg1)), avg1 - std_dev1, avg1 + std_dev1, color='red', alpha=0.3)

plt.plot(range(len(avg2)), avg2, color='blue', linewidth=2, label='F174A')
plt.fill_between(range(len(avg2)), avg2 - std_dev2, avg2 + std_dev2, color='blue', alpha=0.3)

plt.plot(range(len(avg3)), avg3, color='orange', linewidth=2, label='F174S')
plt.fill_between(range(len(avg3)), avg3 - std_dev3, avg3 + std_dev3, color='orange', alpha=0.3)

plt.plot(range(len(avg4)), avg4, color='teal', linewidth=2, label='V213E')
plt.fill_between(range(len(avg4)), avg4 - std_dev4, avg4 + std_dev4, color='teal', alpha=0.3)

plt.plot(range(len(avg5)), avg5, color='purple', linewidth=2, label='G216D')
plt.fill_between(range(len(avg5)), avg5 - std_dev5, avg5 + std_dev5, color='purple', alpha=0.3)

plt.plot(range(len(avg6)), avg6, color='black', linewidth=2, label='G218F')
plt.fill_between(range(len(avg6)), avg6 - std_dev6, avg6 + std_dev6, color='black', alpha=0.3)
#Details

max_value=10
upper_limit=max_value

#Graphics
plt.xlabel('Time (ns)')
plt.ylabel('RMSD (Å)')
#plt.title('Average and Standard Deviation of Each Row')
plt.ylim(0, upper_limit)
plt.xlim(0,100)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
