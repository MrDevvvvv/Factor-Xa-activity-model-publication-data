# Protocol for Generating Figures 4, S2, S3, and S4

This repository contains the full workflow used to generate the
following figures from the publication:

-   **Figure 4**\
    https://github.com/user-attachments/assets/3509c8dd-86aa-41e3-839d-1b8c46a58d36\
-   **Figure S2**\
    https://github.com/user-attachments/assets/6e46cee4-d179-4964-89cf-c762d62dec12\
-   **Figure S3**\
    https://github.com/user-attachments/assets/fa65c773-0a41-48b0-8393-df66de53af25\
-   **Figure S4**\
    https://github.com/user-attachments/assets/bf3219fa-0651-45f2-9f47-045272aa0b43

------------------------------------------------------------------------

## 1. System Requirements

This workflow was originally executed on the **Academic Leiden
Interdisciplinary Cluster Environment (ALICE)**. However, it should run
on any modern Linux environment with the following available:

### Required software

-   **Bash**
-   **Python 3.x**
-   **Amber / AmberTools**
-   Standard Unix tools: `awk`, `sed`, `grep`
-   Access to an **HPC cluster** (Slurm examples provided)

> **Note:** Your environment may differ. Adjust job scripts and module
> loads as needed.

------------------------------------------------------------------------

## 2. Required PDB Structures

Use the following structures to reproduce Figures 4, S2, S3, and S4:

-   `FXa-selected_substrate_1.pdb` --- FXa bound to peptide **R271**
-   `FXa-selected_substrate_2.pdb` --- FXa bound to peptide **R320**

All steps below must be applied **separately** to each complex.

------------------------------------------------------------------------

## 3. Initial File Preparation

### Clean PDB with `pdb4amber`

``` bash
pdb4amber FXa-selected* > complex_amber.pdb --nohyd
```

### Standardize histidines and disulfides

``` bash
sed -i "s/ HIS / HIE /g" complex_amber.pdb

sed -i "s/CYS A   7/CYX A   7/g" complex_amber.pdb
sed -i "s/CYS A  12/CYX A  12/g" complex_amber.pdb
sed -i "s/CYS A  27/CYX A  27/g" complex_amber.pdb
sed -i "s/CYS A  43/CYX A  43/g" complex_amber.pdb
```

------------------------------------------------------------------------

## 4. Add ACE and NME Caps

Capping the N-terminus (ACE) and C-terminus (NME) is required before
generating variants.

------------------------------------------------------------------------

## 5. Generate Variants

For each variant:

1.  Remove all side-chain atoms (keep **CA, C, O, N**).
2.  Rename the residue to the new amino acid.

### Residue number mapping (AlphaFold → chymotrypsin notation)

  Chymo \#   AlphaFold \#
  ---------- --------------
  99         85
  174        162
  192        182
  218        208
  222        211

Each variant must be processed **independently** for each complex.

------------------------------------------------------------------------

## 6. System Preparation with TLeaP

``` bash
tleap -f leap.in
```

------------------------------------------------------------------------

## 7. Molecular Dynamics Simulations

Run **10 replicates per complex per variant**.

Make sure `run_cmd.sh` points to the correct base directory before
submitting:

``` bash
sbatch run_cmd.sh
```

------------------------------------------------------------------------

## 8. Prepare Files for MMGBSA

Identify peptide atom range:

``` bash
p0=$(grep "TER" -A 1 ../*postLEap.pdb | head -2 | tail -1 | awk '{print $5}')
pt=$(grep "TER" -B 1 ../*postLEap.pdb | head -5 | tail -2 | head -1 | awk '{print $5}')
echo ":$p0-$pt"
```

Generate topology files:

``` bash
ante-MMPBSA.py -p inp.prmtop -c com.prmtop -r rec.prmtop -l lig.prmtop -s :WAT,Cl-,Na+ -n :$p0-$pt --radii mbondi2
```

------------------------------------------------------------------------

# Figure 4 and Figure S4 Procedures

## 9. MMGBSA (Per-Residue) Calculations

``` bash
sbatch run_per_residue.sh
```

------------------------------------------------------------------------

## 10. Extract Per-Residue Energies

``` bash
sed '0,/NME /{/ILE   1/,/NME /p}' FRAME_RESULTS_MMGBSA_per_res.dat -n > FRAME_RESULTS_MMGBSA_per_res_adj.dat

python analyse_per_res.py
```

------------------------------------------------------------------------

## 11. Collect Results Across Replicates

``` bash
python collect_per_residue.py
```

The aggregated values were plotted in **GraphPad Prism** as described in
the article.

------------------------------------------------------------------------

# Figure S2 Procedure

## 12. MMPBSA (Total Energy) Calculations

``` bash
sbatch run_mmpbsa.sh
```

------------------------------------------------------------------------

## 13. Plot ΔTOTAL Energies

Plot the `DELTA TOTAL` column from each `MMPBSA.dat` file in GraphPad
Prism.

------------------------------------------------------------------------

# Figure S3 Procedure

## 14. Calculate RMSD Over Time

``` bash
cpptraj -f rmsd.in
```

------------------------------------------------------------------------

## 15. Plot RMSD

``` bash
python plot_rmsd_lig_all.py
```
