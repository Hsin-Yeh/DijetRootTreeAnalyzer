#!/bin/bash

echo "The script starts now."

clusterid=${1}
procid=${2}
outDir=${3}
coupling=${4}
mass=${5}
signame=${6}
limitType=${7}

echo ${PWD}

# Initialize cmssw
export mainpath="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer"
cd ${mainpath}
echo ${PWD}
eval `scramv1 runtime -sh`

cd -
echo ${PWD}

if [[ ${limitType} == "1D" ]]; then
    # cp script
    echo "cp ${mainpath}/run_multi_combine_singleMass_${signame}.sh ./."
    cp ${mainpath}/run_multi_combine_singleMass_${signame}.sh ./.
    # Run script
    echo "./run_multi_combine_singleMass_${signame}.sh ${coupling} ${mass}"
    ./run_multi_combine_singleMass_${signame}.sh ${coupling} ${mass}
elif [[ ${limitType} == "2D" ]]; then
    # cp script
    echo "cp ${mainpath}/run_multi_combine_multiWidth_singleMass_${signame}.sh ./."
    cp ${mainpath}/run_multi_combine_multiWidth_singleMass_${signame}.sh ./.
    # Run script
    echo "./run_multi_combine_multiWidth_singleMass_${signame}.sh ${coupling} ${mass}"
    ./run_multi_combine_multiWidth_singleMass_${signame}.sh ${coupling} ${mass}
fi
# Copy output file
outfile="finalResults_${signame}_${coupling}_${mass}.txt"
echo ${outfile}
echo "The script completed"
