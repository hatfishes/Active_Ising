#!/bin/bash
#SBATCH --job-name=ActiveIsingPy
#SBATCH --mem-per-cpu=2gb
#SBATCH --nodes=1
#SBATCH --output=Soutput/outputForMe%j.txt
#SBATCH --cpus-per-task=20
#SBATCH --partition=cpu_2020

# load the environment
module purge
#module load apps/python/3.6.1
module load apps/anaconda/python
module load compiler/gnu/7.2.0

make

# run python
#python --version
#srun python run.py
#python plot.py
#python newnewplot.py	
