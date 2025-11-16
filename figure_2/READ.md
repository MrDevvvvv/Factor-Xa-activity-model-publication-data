# Protocol for Generating Figure 2

<p>This repository contains the workflow used to generate <strong>Figure 2</strong> for the publication. It includes sequence retrieval, AlphaFold-Multimer predictions, distance measurements, and heatmap generation.</p>

---

## System Requirements / Environment Notes

<p>This workflow was originally executed on an HPC environment where Python, Bash, and GPU-enabled tools were already available. The exact versions used may vary, and the protocol does not depend on any single specific setup.</p>

**Users should ensure:**
- A Linux-based environment (HPC cluster, workstation, or cloud VM)
- Bash available in their shell
- Python 3.x available in the PATH
- Ability to install or load <strong>LocalColabFold</strong>
- NVIDIA GPU recommended for speed (CPU works but is slower)
- Standard Unix command-line tools (`awk`, `sed`, `grep`)

<p><em>Note:</em> Since systems vary, users should adapt the environment to their own setup. Any reasonably recent Python/Bash version should work.</p>

---

##  1. Retrieve FXa Protease Domain Sequence

<p>Download the protease domain of <strong>Factor Xa (FXa)</strong> from:</p>

<p><a href="https://www.rcsb.org/structure/2P16"><strong>PDB: 2P16</strong></a></p>

---

##  2. Generate AlphaFold-Multimer Input Files

<p>Run:</p>

```
python3 generate_alphafold_input.py
```

<p>This will generate <strong>two CSV files</strong>, one for each substrate.</p>

---

##  3. Prepare the Input Folders

<p>For each generated CSV file:</p>

<p>
1. Create a folder<br>
2. Rename it according to the substrate<br>
3. Place the corresponding <code>input.csv</code> inside the folder
</p>

---

##  4. Run AlphaFold-Multimer (LocalColabFold)

<p>Execute the following inside each substrate folder:</p>

```
colabfold_batch --use-gpu-relax --num-recycle 12 --custom-template-path . \
  --model-type alphafold2_multimer_v3 input.csv $location
```

<p><strong>Requirements:</strong><br>
LocalColabFold version <strong>1.3.0</strong><br>
<a href="https://github.com/YoshitakaMo/localcolabfold">https://github.com/YoshitakaMo/localcolabfold</a></p>

---

##  5. Measure Residue Distances

<p>Use the PDB models to compute the distances described in the article:</p>

```
bash get_distances.sh
```

---

##  6. Generate Heatmaps (Figure 2)

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

---

## System Requirements / Environment Notes

<p> This work was performed using the compute resources from the Academic Leiden Interdisciplinary Cluster Environment (ALICE) provided by Leiden University. </p>
