# Protocol for Generating Figure 2

<p>This repository contains the workflow used to generate <strong>Figure 2</strong> and <strong>Figure S1</strong> for the publication. </p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/d168bb93-e604-4387-850f-ae674ee430a4" alt="Figure 2">
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/917ae179-efb9-4d69-8579-ddb7730d785a" alt="Figure S1">
</p>


---

## System Requirements / Environment Notes

<p>This work was performed using the compute resources from the Academic Leiden Interdisciplinary Cluster Environment (ALICE) provided by Leiden University where Python, Bash, and GPU-enabled tools were already available. The exact versions used may vary, and the protocol does not depend on any single specific setup.</p>

**Users should ensure:**
- Bash available in their shell
- Python 3.x available in the PATH
- Ability to install or load <strong>LocalColabFold</strong>
- Standard Unix command-line tools (`awk`, `sed`, `grep`)
- A Linux-based environment (HPC cluster)
  
<p><em>Note:</em> Since systems vary, users should adapt the environment to their own setup. Any reasonably recent Python/Bash version should work.</p>


---

##  1. Generate AlphaFold-Multimer Input Files

<p>Run:</p>

```
python3 generate_alphafold_input.py
```

<p>This will generate <strong>two CSV files</strong>, one for each substrate.</p>

---

##  2. Prepare the Input Folders

<p>For each generated CSV file:</p>

<p>
1. Create a folder<br>
2. Rename it according to the substrate<br>
3. Place the corresponding <code>input.csv</code> inside the folder. 
</p>

---

##  3. Run AlphaFold-Multimer (LocalColabFold)

<p>Execute the following inside each substrate folder:</p>

```
colabfold_batch --use-gpu-relax --num-recycle 12 --custom-template-path . \
  --model-type alphafold2_multimer_v3 input.csv $location
```

<p><strong>Requirements:</strong><br>
LocalColabFold version <strong>1.3.0</strong><br>
<a href="https://github.com/YoshitakaMo/localcolabfold">https://github.com/YoshitakaMo/localcolabfold</a></p>

---

##  4. Measure Residue Distances

<p>Use the PDB models to compute the distances described in the article:</p>

```
bash get_distances.sh
```

---

##  5. Generate Heatmaps (Figure 2)

### **Figure 2A**
```
python3 make_heatmap.py ARG-C_SER-O.csv \
  -o heatmap_ARG-C_SER-O.png \
  -ss DEDSDRAIEGRTATSEYQ
```

### **Figure 2B**
```
python3 make_heatmap.py ARG-NH1_ASP-OD2.csv \
  -o heatmap_ARG-NH1_ASP-OD2.png \
  -ss DEDSDRAIEGRTATSEYQT
```

### **Figure 2C**
```
python3 make_heatmap.py ARG-C_SER-O.csv \
  -o heatmap_ARG-C_SER-O.png \
  -ss RELLESYIDGRIVEGSDAE
```

### **Figure 2D**
```

python3 make_heatmap.py ARG-NH1_ASP-OD2.csv \
  -o heatmap_ARG-NH1_ASP-OD2.png \
  -ss RELLESYIDGRIVEGSDAE
```
##  5. Generate visualizations (Figure S1)

- From each subfolder generated, load the best ranked structure of each peptide length to PyMol
- Align the structure based on the first residues of Factor Xa (usually Chain A)
- Color the residues as shown in the figure
---
