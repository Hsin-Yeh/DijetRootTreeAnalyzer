#!/bin/bash

version="2023-10-25"
couplist=(14 361 707 1054 1400 2450 3500 4550 5600)
masslist=($(seq 600 10 5000))

for coupling in "${couplist[@]}"; do
    echo ${coupling}
    mkdir ${version}/results/grav/${coupling}
    for mass in "${masslist[@]}"; do
        mv ${version}/finalResults_grav_${coupling}_${mass}.txt ${version}/results/grav/${coupling}
    done

done
