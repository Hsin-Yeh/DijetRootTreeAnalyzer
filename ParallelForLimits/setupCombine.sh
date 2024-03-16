#!/bin/bash

echo "The script starts now."

clusterid=${1}
procid=${2}
outDir=${3}
coupling=${4}
mass=${5}
signame=${6}

echo ${PWD}
ls "/eos/cms/store/group/phys_exotica/diphoton/fullRun2/hsinyeh/2023-02-01/2016/mc/crab_RSGravToGG_kMpl-001_M-4000_TuneCUEP8M1_13TeV-pythia8__Summer16MiniAODv3-v2__MINIAODSIM/230201_161435/0000/out_RSGravToGG_kMpl-001_M-4000_TuneCUEP8M1_13TeV-pythia8_RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2_numEvent100_1.root"
ls "/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer"

# Initialize cmssw
export mainpath="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer"
cd ${mainpath}
echo ${PWD}
eval `scramv1 runtime -sh`

cd -
echo ${PWD}

# cp script
echo "cp ${mainpath}/run_multi_combine_multiWidth_singleMass_${signame}.sh ./."
cp ${mainpath}/run_multi_combine_multiWidth_singleMass_${signame}.sh ./.
# Run script
echo "./run_multi_combine_multiWidth_singleMass_${signame}.sh ${coupling} ${mass}"
./run_multi_combine_multiWidth_singleMass_${signame}.sh ${coupling} ${mass}

# Copy output file
outfile="finalResults_${signame}_${coupling}_${mass}.txt"
echo ${outfile}
echo "The script completed"
