import argparse
import os
import scipy
import collections
import numpy as np
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.font_manager as font_manager
from matplotlib.colors import BoundaryNorm

from pathlib import Path
from scipy import stats

parser = argparse.ArgumentParser()
parser.add_argument('filename')
parser.add_argument("-o", "--Output", help="Show Output")
parser.add_argument("-ss", "--Substrate_Sequence", help="Insert substrate sequence with GR", required=False)
args = parser.parse_args()

with open(args.filename, 'r') as file:
    filedata = file.read()

# Replace the target string
filedata = filedata.replace('_', ' ')
filedata = filedata.replace('  ', ' ')

# Write the file out again
print('seq' + str(args.filename))
newfile = 'seq' + str(args.filename)

with open(str(newfile), 'w') as file:
    file.write('"N-Terminus" "C-Terminus" x1 y1 z1 x2 y2 z2' + '\n')
    file.write(filedata)

df = pd.read_csv(str(newfile), sep=' ')

df['Distance'] = (((df['x1'] - df['x2'])**2 + (df['y1'] - df['y2'])**2 + (df['z1'] - df['z2'])**2)**(1/2))

df1 = df[['N-Terminus', 'C-Terminus', 'Distance']]

pd.to_numeric(df1["C-Terminus"])
pd.to_numeric(df1["N-Terminus"])

# Table to Data for heatmap
y = pd.DataFrame(df1['C-Terminus'].unique())
x = pd.DataFrame(df1['N-Terminus'].unique())

heatmap_pt = pd.pivot_table(df1, values='Distance', columns='C-Terminus', index='N-Terminus')

# Plotting
fig, (ax0, ax1) = plt.subplots(figsize=(10, 8), ncols=2, gridspec_kw={'width_ratios': [30, 1]})

bounds = [2.5, 5.0, 7.5, 10.0, 12.5, 15.0, 17.5, 20.0, 22.5]
norm = BoundaryNorm(bounds, ncolors=256)  # forces bins instead of gradient

sn.heatmap(
    heatmap_pt,
    cmap="plasma",
    cbar_ax=ax1,
    ax=ax0,
    annot=False,
    vmin=2.5,
    vmax=22.5,
    linewidth=.5,
    linecolor="Black",
    square=True,
    cbar=True,
    cbar_kws=dict(boundaries=bounds, spacing="uniform"),
    norm=norm
    )

# Labels
ax0.set_ylabel("P2                                                                                          P11", weight="bold", fontname="Arial", fontsize=12)
ax0.set_xlabel("P1                                                                      P7'", weight="bold", fontname="Arial", fontsize=12)
ax1.set_ylabel("Distance (Å) ", weight="bold", fontname="Arial", fontsize=12)

# Tick size (and font style will be handled manually)
ax0.tick_params(labelsize=11)
ax1.tick_params(labelsize=11)

# Tick label font properties (manual bold)
tick_font = {'fontname': 'Arial', 'fontsize': 11, 'weight': 'bold'}

for label in ax0.get_xticklabels():
    label.set_fontname(tick_font['fontname'])
    label.set_fontsize(tick_font['fontsize'])
    label.set_fontweight(tick_font['weight'])

for label in ax0.get_yticklabels():
    label.set_fontname(tick_font['fontname'])
    label.set_fontsize(tick_font['fontsize'])
    label.set_fontweight(tick_font['weight'])

for label in ax1.get_yticklabels():
    label.set_fontname(tick_font['fontname'])
    label.set_fontsize(tick_font['fontsize'])
    label.set_fontweight(tick_font['weight'])

# First tick colors
ax0.get_xticklabels()[0].set_color('red')
ax0.get_yticklabels()[0].set_color('red')

# Tick names
left = str(args.Substrate_Sequence).split("GR")[0] + "G"
right = "R" + str(args.Substrate_Sequence).split("GR")[1]

a = ax0.get_xticks().tolist()
b = ax0.get_yticks().tolist()

for element in range(0, len(a)):
    a[element] = right[element]

for element in range(0, len(b)):
    b[element] = left[element]

b.reverse()

ax0.set_xticklabels(a)
ax0.set_yticklabels(b)

# Adds border around colormap
for spine in ax1.spines.values():
    spine.set(visible=True, lw=.8, edgecolor="black")

# To delete the space created by width_ratios
plt.subplots_adjust(wspace=0, hspace=0)
box = ax0.get_position()
box.x0 = box.x0 - 0.05
box.x1 = box.x1 + 0.25
ax0.set_position(box)
ax0.set_ylim([0, 10])

print(args.Output)
fig.savefig(str(args.Output), bbox_inches='tight', dpi=600)

