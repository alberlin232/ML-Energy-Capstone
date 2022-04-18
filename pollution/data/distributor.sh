#!bin/bash

while IFS="," read -r YEAR Q STRING; do
    echo Sending $STRING          # MARK progress
    sbatch $YEAR $Q $STRING SLURMrunner.sh # SUBMIT JOB
done < RUNS.csv
