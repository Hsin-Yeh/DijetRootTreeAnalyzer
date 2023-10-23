#!/bin/bash

version="2023-10-22"
couplist=(14, 361, 707, 1054, 1400, 2450, 3500, 4550, 5600)
masslist=($(seq 600 10 5000))

for coupling in "${couplist[@]}"; do
    for mass in "${masslist[@]}"; do
        submitFile="${jobDir}/jobs/limit_${coupling}_${mass}.sub"
        #echo ${run}
        chmod 755 ${workpath}/${run}

        echo "Sending ${run}"
        condor_submit ${workpath}/${run}
        echo "condor_submit ${workpath}/${run}"
    done
done
