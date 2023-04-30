#!/usr/bin/env bash

year=$1
signal=$2
coupling=$3
method=$4
massInterval=$5
massMin=$6
massMax=$7

masslist=$(seq ${massMin} ${massInterval} ${massMax})

echo $masslist

# Combine_Method in this script are: AsymptoticLimits, ExpSignificance, ExpSignificanceWithPval, ObsSignificance, ObsSignificanceWithPval
#setenv combine_methods "ObsSignificance"
combine_methods="AsymptoticLimits"
mainpath="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/test_directory"

rm -rf combineJobs13TeV/${year}/${signal}/${coupling}/${combine_method}/All
mkdir -p combineJobs13TeV/${year}/${signal}/${coupling}/${combine_method}/All

finalResults="finalResults_${year}_${signal}_${coupling}"
finalResults2="finalResults_${year}_${signal}_${coupling}_2"

rm ${finalResults}
touch ${finalResults}

#a priori limits. I see in the post-fit or a-posteriori expected limit weird
#one and two sigma region above 1.2 TeV. So, I will go to a priori limits at the moment.
time parallel --progress --jobs 10 'mass={1}; echo \"====================================================================\"; echo $mass; datacardfile=${mainpath}/${method}/${year}/diphoton_combine_${mass}_DiPhotons_${coupling}_${year}.txt; echo $datacardfile; echo \"combine -M AsymptoticLimits -s -1 --bypassFrequentistFit $datacardfile\";' ::: $(seq ${massMin} ${massInterval} ${massMax})

#a-posteriori expected limit
# echo "combine -M AsymptoticLimits -s -1 $datacardfile"
# combine -M AsymptoticLimits  -s -1 $datacardfile > ${datacardfile}_results


# cat ${finalResults} | sort -n > ${finalResults2}
# mv ${finalResults2} combineJobs13TeV/${year}/${signal}/${coupling}/${combine_method}/All/finalResults
