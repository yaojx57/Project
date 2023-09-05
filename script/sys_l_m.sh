#!/bin/bash
#SBATCH --partition=gpu
#SBATCH --qos=gpu
#SBATCH --nodes=1
#SBATCH --gpus-per-node=1
#SBATCH --mem=32G
#SBATCH --cpus-per-task=4
#SBATCH --time=24:00:00
#SBATCH --mail-user=jyao28@sheffield.ac.uk
#SBATCH --job-name=sys_l_m_1.0
#SBATCH --output=script/out/sys_l_m.%j.out


module load Anaconda3/2019.07
module load FFmpeg/4.2.2-GCCcore-9.3.0

# We assume that the conda environment 'myexperiment' has already been created
source activate project
python main.py -whisper s -model medium -path /fastdata/acu21jy -ratio 1.0 -level l
