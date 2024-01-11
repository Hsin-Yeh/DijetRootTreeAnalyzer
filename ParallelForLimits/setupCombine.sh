#!/bin/bash

echo "The script starts now."

clusterid=${1}
procid=${2}
outDir=${3}
coupling=${4}
mass=${5}
signame=${6}

# Initialize cmssw
export mainpath="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer"
cd ${mainpath}
eval `scramv1 runtime -sh`
cd -

# Run script
cp ${mainpath}/run_multi_combine_multiWidth_singleMass_${signame}.sh ./.
./run_multi_combine_multiWidth_singleMass_${signame}.sh ${coupling} ${mass}

# Copy output file
outfile="finalResults_${signame}_${coupling}_${mass}.txt"
echo ${outfile}
echo "The script completed"
