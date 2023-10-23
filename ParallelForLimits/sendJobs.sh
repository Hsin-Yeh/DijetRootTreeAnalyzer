#!/bin/bash

version="2023-10-23"
# couplist=(4550)
# masslist=(1300)
couplist=(14, 361, 707, 1054, 1400, 2450, 3500, 4550, 5600)
masslist=($(seq 600 10 5000))

for coupling in "${couplist[@]}"; do
    for mass in "${masslist[@]}"; do
        jobDir="${version}/${coupling}/${mass}"
        submitFile="${jobDir}/jobs/limit_${coupling}_${mass}.sub"
        #echo ${run}
        chmod 755 ${submitFile}

        echo "Sending ${submitFile}"
        condor_submit ${submitFile}
        echo "condor_submit ${submitFile}"
    done
done
