# Protocol for Generating Figure 2

<p>This repository contains the workflow used to generate <strong>Figure 3</strong> for the publication. </p>

---

## System Requirements / Environment Notes

<p>This work was performed using the compute resources from the Academic Leiden Interdisciplinary Cluster Environment (ALICE) provided by Leiden University where Python, Bash, and GPU-enabled tools were already available. The exact versions used may vary, and the protocol does not depend on any single specific setup.</p>

**Users should ensure:**

- Bash available in their shell
- Python 3.x available in the PATH
- Ability to install or load <strong>Amber and AmberTools</strong>
- Standard Unix command-line tools (`awk`, `sed`, `grep`)

<p><em>Note:</em> Since systems vary, users should adapt the environment to their own setup. Any reasonably recent Python/Bash version should work.</p>

---

1- The following PDB structures can be used to reproduce figure 3:
  - For Factor Xa - substrate peptide R271 complex:
  - For Factor Xa - substrate peptide R320 complex:

The rest of the procedure can be applied for both complexes. 

3- Initial preparation step:
<p>pdb4amber </p>

4- Add ACE and NME capping to the peptide on the N-terminus and C-terminus respectively. See example: 
<img width="706" height="173" alt="image" src="https://github.com/user-attachments/assets/2d8cdc0f-0d76-403f-bbdc-9335b62fd2dc" />

5- Solvate the system and add the ions

<p>tleap -f leap.in </p>

6- Run CPU-based minimization step
7- Run the first GPU-based minimization step
8- Run the second GPU-based minimization step
9- Run temperature equilibration
10- Run pressure equilibration
11- Run production 
