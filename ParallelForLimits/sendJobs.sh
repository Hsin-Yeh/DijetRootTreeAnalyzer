#!/bin/bash

########## Config ##########
signame="heavyhiggs" # grav
Version="2024-01-11"
versionDir="${Version}_${signame}"
masslist=($(seq 600 10 2000))
# couplist=(4550)
# masslist=(1300)
couplist=(14 361 707 1054 1400 2450 3500 4550 5600)
############################

cd ${versionDir}

echo "==========Sending Jobs=========="
for coupling in "${couplist[@]}"; do
    echo ${coupling}
    for mass in "${masslist[@]}"; do
        jobDir="${coupling}/${mass}"
        submitFile="${jobDir}/jobs/limit_${coupling}_${mass}.sub"
        #echo ${run}
        chmod 755 ${submitFile}

        echo "Sending ${submitFile}"
        condor_submit ${submitFile}
        # echo "condor_submit ${submitFile}"
    done
done
