🧬 Protocol for Generating Figure 2

This repository describes the workflow used to generate Figure 2 for the publication.
Follow the steps below to reproduce the sequence retrieval, AlphaFold-Multimer predictions, distance calculations, and heatmap visualizations.

📌 1. Retrieve FXa Protease Domain Sequence

Download the protease domain of Factor Xa (FXa) from:

PDB: 2P16

📌 2. Generate AlphaFold-Multimer Input Files

Run:

python3 generate_alphafold_input.py


This script generates two CSV input files, one for each substrate.

📌 3. Prepare Folders for Each Input File

For each of the generated CSV files:

Create a folder

Rename the folder according to the substrate

Place the corresponding input.csv inside the folder

📌 4. Run AlphaFold-Multimer (LocalColabFold)

Inside each substrate folder, run:

colabfold_batch --use-gpu-relax --num-recycle 12 --custom-template-path . \
  --model-type alphafold2_multimer_v3 input.csv $location


Requirements:

LocalColabFold version 1.3.0
🔗 https://github.com/YoshitakaMo/localcolabfold

Note: Model outputs used in the article can be found on Zenodo.

📌 5. Measure Residue Distances

Use the predicted PDB files to compute the distances described in the publication:

bash get_distances.sh


Distance outputs are available in Zenodo.

📌 6. Generate Heatmaps (Figure 2)
Figure 2A
python3 make_heatmap.py ARG-C_SER-O.csv \
  -o heatmap_ARG-C_SER-O.png \
  -ss DEDSDRAIEGRTATSEYQ

Figure 2B
python3 make_heatmap.py ARG-NH1_ASP-OD2.csv \
  -o heatmap_ARG-NH1_ASP-OD2.png \
  -ss DEDSDRAIEGRTATSEYQT

Figure 2C
python3 make_heatmap.py ARG-C_SER-O.csv \
  -o heatmap_ARG-C_SER-O.png \
  -ss RELLESYIDGRIVEGSDAE

Figure 2D
python3 make_heatmap.py ARG-NH1_ASP-OD2.csv \
  -o heatmap_ARG-NH1_ASP-OD2.png \
  -ss RELLESYIDGRIVEGSDAE

📝 Citation

(Add your publication citation here once available.)

🐛 Issues

If you encounter problems running this pipeline, feel free to open an Issue on this repository.
