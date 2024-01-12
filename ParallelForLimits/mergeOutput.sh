#!/bin/bash

version="2023-10-25"
couplist=(14 361 707 1054 1400 2450 3500 4550 5600)
masslist=($(seq 600 10 5000))
########## Config ##########
signame="heavyhiggs" # grav
Version="2024-01-11"
versionDir="${Version}_${signame}"
masslist=($(seq 600 10 2000))
# couplist=(4550)
# masslist=(1300)
couplist=(14 361 707 1054 1400 2450 3500 4550 5600)
############################


for coupling in "${couplist[@]}"; do
    echo ${coupling}
    mkdir -p ${version}/results/grav/${coupling}
    for mass in "${masslist[@]}"; do
        mv ${version}/finalResults_grav_${coupling}_${mass}.txt ${version}/results/grav/${coupling}
    done

done
