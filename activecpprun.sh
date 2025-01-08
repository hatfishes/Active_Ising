#!/bin/sh
#SBATCH --job-name=ActiveIsing
#SBATCH --mem-per-cpu=10gb
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --partition=fat1t
# load the environment
module purge
module load compiler/gnu/7.2.0  

#clean the environment

# running the command
./active_1D 0.45

