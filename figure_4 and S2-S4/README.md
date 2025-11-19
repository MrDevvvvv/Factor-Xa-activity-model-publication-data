# Protocol for Generating Figure 4, S2, S3, and S4

This repository contains the workflow used to generate the following figures for the publication:

- [Figure 4](https://github.com/user-attachments/assets/3509c8dd-86aa-41e3-839d-1b8c46a58d36)
- [Figure S2](https://github.com/user-attachments/assets/6e46cee4-d179-4964-89cf-c762d62dec12)
- [Figure S3](https://github.com/user-attachments/assets/fa65c773-0a41-48b0-8393-df66de53af25)
- [Figure S4](https://github.com/user-attachments/assets/bf3219fa-0651-45f2-9f47-045272aa0b43)

---

## System Requirements / Environment Notes

<p>This work was performed using the compute resources from the Academic Leiden Interdisciplinary Cluster Environment (ALICE) provided by Leiden University where Python, Bash, and GPU-enabled tools were already available. The exact versions used may vary, and the protocol does not depend on any single specific setup.</p>

**Users should ensure:**

- Bash available in their shell
- Python 3.x available in the PATH
- Ability to install or load <strong>Amber and AmberTools</strong>
- Standard Unix command-line tools (`awk`, `sed`, `grep`)
- A Linux-based environment (HPC cluster)

<p><em>Note:</em> Since systems vary, users should adjust the environment to match their own setup. Any reasonably recent version of Python or Bash should work. For Slurm jobs, be sure to modify the scripts according to your cluster’s configuration.</p>

---

## 1. Required PDB Structures

The following PDB structures can be used to reproduce Figure 4, S1, S2, S4:

- Factor Xa – substrate peptide R271 complex: `FXa-selected_substrate_1.pdb`
- Factor Xa – substrate peptide R320 complex: `FXa-selected_substrate_2.pdb`

The remainder of the procedure should be applied **independently to each complex**.

---

## 2. Initial Preparation

```
pdb4amber FXa-selected* > complex_amber.pdb --nohyd
```

```
sed -i "s/ HIS / HIE /g" complex_amber.pdb

sed -i "s/CYS A   7/CYX A   7/g" complex_amber.pdb
sed -i "s/CYS A  12/CYX A  12/g" complex_amber.pdb
sed -i "s/CYS A  27/CYX A  27/g" complex_amber.pdb
sed -i "s/CYS A  43/CYX A  43/g" complex_amber.pdb
```

---

## 3. Add ACE and NME Caps

Add ACE (N‑terminus) and NME (C‑terminus) capping groups to the peptide.

Example:

<img width="706" height="173" alt="image" src="https://github.com/user-attachments/assets/2d8cdc0f-0d76-403f-bbdc-9335b62fd2dc" />

---

## 4. Prepare the variants

For each variant, remove all side-chain atoms (keeping only CA, C, O, and N) and rename the residue to the target amino acid.
Example for variant F174A:

<img width="805" height="325" alt="Variant F174 example" src="https://github.com/user-attachments/assets/b310c09b-5647-4b66-824a-5b0d349be3dd" />

Because the residue numbering differs between chymotrypsin numbering and the AlphaFold structure, use the following mapping to locate the correct positions:

- Residue 99 → 85
- Residue 174 → 162
- Residue 192 → 182
- Residue 218 → 208
- Residue 222 → 211

The remainder of the procedure should be applied **independently to each variant and complex**.

---

## 4. System Preparation Using TLeaP

```
tleap -f leap.in
```

---

## 5. Run Molecular Dynamics Simulations

Run **10 replicates per complex per variant**. Ensure that the script correctly identifies the folder named `base`. You can use the `base` subfolder from `figure_3` subfolder. 

```
sbatch run_cmd.sh
```

---

## 6. Generate Files for MMGBSA Binding Free Energy Calculations

Identify peptide atom range:

```
p0=$(grep "TER" -A 1 ../*postLEap.pdb | head -2 | tail -1 | awk '{print $5}')
pt=$(grep "TER" -B 1 ../*postLEap.pdb | head -5 | tail -2 | head -1 | awk '{print $5}')
echo ":$p0-$pt"
```

Run ante-MMPBSA preparation:

```
ante-MMPBSA.py -p inp.prmtop -c com.prmtop -r rec.prmtop -l lig.prmtop -s :WAT,Cl-,Na+ -n :$p0-$pt --radii mbondi2
```

---

## 7. Perform MMGBSA Free Energy Calculations

Ensure that the job script correctly identifies the location of `mmgbsa_per_residue.in`.

```
sbatch run_per_residue.sh
```

---

## 8. Extract Per‑Residue Binding Free Energy Results

```
sed '0,/NME /{/ILE   1/,/NME /p}' FRAME_RESULTS_MMGBSA_per_res.dat -n > FRAME_RESULTS_MMGBSA_per_res_adj.dat
python analyse_per_res.py
```

---

## 9. Collect Results Across Replicates

```
python collect_per_residue.py
```

---


## 10. The output was analyzed in GraphPadPrism as described in the article. This output can be used for figure 4 and S4.


