#!/bin/bash

#SBATCH --partition=health
 
# Request 1 hour of computing time
#SBATCH --time=1:00:00
#SBATCH --ntasks=1
 
# Give a name to your job to aid in monitoring
#SBATCH --job-name EPA_EIA_match
 
# Write Standard Output and Error
#SBATCH --output="myjob.%j.%N.out"
 
cd ${SLURM_SUBMIT_DIR} # cd to directory where you submitted the job
 
# launch job
module load anaconda3
module load conda/biostats
python match.py --YEAR=${YEAR}

 
exit
