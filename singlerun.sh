#!/bin/bash
#SBATCH --job-name=ActiveIsingPy
#SBATCH --mem-per-cpu=2gb
#SBATCH --nodes=1
#SBATCH --output=Soutput/outputForMe%j.txt
#SBATCH --cpus-per-task=1
#SBATCH --partition=hcpu

# load the environment
module purge
#module load apps/python/3.6.1
module load apps/anaconda/python
module load compiler/gnu/7.2.0

make

./active_1D 1.033

# run python
#python --version
#srun python run.py
#python plot.py
#python newnewplot.py	
