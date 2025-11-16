To generate Figure 2, follow this protocol:
1. Retrieve the sequence of the protease domain of FXa from PDB file: 2P16 (https://www.rcsb.org/structure/2P16)
2. Run the following to generate the input files necessary for AlphaFold-Multimer:
   <p>python3 generate_alphafold_input.py</p>
   This will generate two csv files. One for each substrate.
3. Create one folder for each of the input files and rename the folder depending on the substrate. Change the name to input.csv file.
4. You can now run:
  <p>colabfold_batch --use-gpu-relax --num-recycle 12 --custom-template-path . --model-type alphafold2_multimer_v3 input.csv $location </p>
   Requirements: LocalColabFold 1.3.0 Found at: [https://github.com/sokrypton/ColabFold](https://github.com/YoshitakaMo/localcolabfold]
