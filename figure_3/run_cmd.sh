#!/bin/bash

#SBATCH --job-name=Amber_cMD
#SBATCH --output=%x_%j.out
#SBATCH --mem=3g 
#SBATCH --nodes=1
#SBATCH --cpus-per-gpu=1
#SBATCH --gpus-per-task=1
#SBATCH --partition="gpu-l4-24g"
#SBATCH --gpus=1
#SBATCH --gres=gpu:1
#SBATCH --distribution=cyclic
#SBATCH --time=4-00:00:00

module purge

#Modules and setups
module load ALICE/default
module load slurm
module load Boost/1.81.0-GCC-12.2.0
module load CUDA/12.3.2
module load GCC/12.2.0
module load CMake/3.24.3-GCCcore-12.2.0
module load OpenMPI/4.1.4-GCC-12.2.0


source /home/dveizaj/data1/software/amber24/amber.sh

# Store the location of the job for later reference.
location=$(pwd)

if [ -z $TMPDIR ]
then
        random=$(echo $RANDOM | shasum | cut -c 1-10)
        magic="/scratchdata/$random"
        mkdir $magic
else
        magic=$TMPDIR
        location=$SLURM_SUBMIT_DIR
fi

# Write some info to the slurm file..
echo "== Starting run at $(date)"
echo "== Job ID     : ${SLURM_JOBID}"
echo "== Node list  : ${SLURM_NODELIST}"
echo "== Local dir. : ${location}"
echo "== Magic dir. : ${magic}"

#Determine input file folder for MD input
scripthome="/home/dveizaj/data1/scripts"

echo "## Number of available CUDA devices: $CUDA_VISIBLE_DEVICES"
echo "## Checking status of CUDA device with nvidia-smi" 
nvidia-smi

#Copy everything to our working directory in scratch, and move ourselves there too.
cp $location/../base/pme*in     $magic/
cp *rst *out                    $magic/
cp inp.prmtop inp.inpcrd        $magic/
cd                              $magic

#Begin ordinary molecular dynamics setup.

## Minimization with single cpu code, slow but useful for clashes
if  grep -q -e "FINAL"  m1.out
then
        cp $location/m1.rst .
else
        sander  -O -i pme_mn_z.in -p inp.prmtop -c inp.inpcrd -inf m1.info -o m1.out -r m1.rst -ref inp.inpcrd
        cp m1.out m1.rst m1.info $location
fi

## Minimization with GPU, fast
if grep -q -e "FINAL"   m2.out
then
                cp $location/m2.rst .
else
        pmemd.cuda_SPFP  -O -i pme_mn_g.in -o m2.out -inf m2.info -p inp.prmtop -c m1.rst -r m2.rst -ref m1.rst
        cp m2.out m2.rst m2.info $location
fi

## System heating 0 - 310K
if grep -q -e "Final Performance"  ht.out
then
                cp $location/ht.rst .
else
        pmemd.cuda_SPFP  -O -i pme_ht.in   -p inp.prmtop -c m2.rst -x ht.nc -inf ht.info -o ht.out -r ht.rst -ref m2.rst
        cp ht.out ht.rst ht.info $location
fi

## Equilibriation pt 1, often the system changes in volume dramatically and stops.
if grep -q -e "Final Performance"  e1.out
then
        cp $location/e1.rst .
else
        pmemd.cuda_SPFP  -O -i pme_eq_1.in   -p inp.prmtop -c ht.rst -x e1.nc -inf eq1.info -o e1.out -r e1.rst -ref ht.rst
        cp e1.out e1.rst e1.info $location
fi

## Equilibriation pt 2, same as the first, but it goes to completion.
if grep -q "Final Performance"  e2.out
then
                cp $location/e2.rst .
else
        pmemd.cuda_SPFP  -O -i pme_eq_2.in -p inp.prmtop -c e1.rst -x e2.nc -inf e2.info -o e2.out -r e2.rst -ref e1.rst
        cp e2.out e2.rst e2.info $location
fi

## Prepratory NVT simulation for determining AMD paramters.
if grep -q -e "Final Performance"  md.out
then
        sleep 1s
else
        pmemd.cuda  -O -i pme_md.in   -o md.out -p inp.prmtop -c e2.rst     -r md.rst -x md.nc
fi

## Cleanup comment out these lines for debugging.
cd $location
cp $magic/md.out $magic/md.rst $magic/md.nc $location && rm -R $magic

