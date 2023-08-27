#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --mail-user=jyao28@sheffield.ac.uk

export SLURM_EXPORT_ENV=ALL
module load Anaconda3/2019.07
module load FFmpeg/4.2.2-GCCcore-9.3.0

# We assume that the conda environment 'myexperiment' has already been created
source activate project
srun python main.py -whisper l -model medium -path /fastdata/acu21jy -ratio 0.5
