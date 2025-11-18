# Protocol for Generating Figure 3

<p>This repository contains the workflow used to generate <strong>Figure 3</strong> for the publication. </p>

---



---

1- The following PDB structures can be used to reproduce figure 3:
  - For Factor Xa - substrate peptide R271 complex:
  - For Factor Xa - substrate peptide R320 complex:

The rest of the procedure can be applied for both complexes. 

3- Initial preparation step:

<p> pdb4amber *unrelaxed* > complex_amber.pdb --nohyd </p>
sed -i "s/ HIS / HIE /g" complex_amber.pdb

sed -i "s/CYS A   7/CYX A   7/g" complex_amber.pdb
sed -i "s/CYS A  12/CYX A  12/g" complex_amber.pdb
sed -i "s/CYS A  27/CYX A  27/g" complex_amber.pdb
sed -i "s/CYS A  43/CYX A  43/g" complex_amber.pdb

4- Add ACE and NME capping to the peptide on the N-terminus and C-terminus respectively. See example: 
<img width="706" height="173" alt="image" src="https://github.com/user-attachments/assets/2d8cdc0f-0d76-403f-bbdc-9335b62fd2dc" />

5- Solvate the system and add the ions

<p>tleap -f leap.in </p>

6- Run the simulations (10 replicates for each complex).

