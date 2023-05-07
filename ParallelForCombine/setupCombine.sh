#!/bin/bash

echo "The script starts now."

clusterid=${1}
procid=${2}
THEINOUTPATH=${3}
THEMODEL=${4}
THENTOYS=${5}
THECOUP=${6}
THEINSIGNAME=${7}
THESEED=${8}
THEYEAR=${9}
THEMUIN=${10}
THEMASS=${11}
THECOMBCHOICE=${12}
THENOMINALMODEL=${13}
THEMETHOD=${14}
THECAT=${15}
THELUMI=${16}
CURRENTTOY=${17}

export mainpath="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer"

cd ${mainpath}
eval `scramv1 runtime -sh`
cd -

export PWD=`pwd`

mkdir -p signal_bias
cp -r ${mainpath}/python .
cp -r ${mainpath}/config .
cp -r ${mainpath}/output .
cp -r ${mainpath}/bkgAltModels .
cp /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/SignalNorm_Splines_${THEMETHOD}.txt ./SignalNorm.txt

time python python/RunBias.py -c config/diphotons_bias_${THEYEAR}.config -i bkgAltModels/${THEMODEL}/blind/FitResults_DiPhotons_${THECOUP}_${THECAT}_${THEYEAR}.root -b DiPhotons_${THECOUP}_${THECAT} --mass ${THEMASS} -m gg -d signal_bias -r ${THEMUIN} --rMin -3 --rMax 3 -l ${THELUMI} --year ${THEYEAR} --fit-pdf ${THEMODEL} --SigNorm SignalNorm.txt

time python python/RunDiphotonCombine.py -c config/diphotons_bias_${THEYEAR}.config -i bkgAltModels/${THEMODEL}/blind/FitResults_DiPhotons_kMpl001_EBEB_2017.root -b DiPhotons_kMpl001_EBEB --mass 4000 -m gg -d signal_bias -r 1 --rMin -3 --rMax 3 -l 41.527 --year 2017 --fit-pdf ${THEMODEL} --SigNorm $SigNormFile

outfile=`ls fitDiagnostics*|grep ${THECOUP}|grep ${THEMODEL}|grep ${THENOMINALMODEL}|grep .root`

echo ${outfile}

mv ${outfile} fitDiagnostics_${THEINSIGNAME}_mu${THEMUIN}_${THECOUP}_${THECAT}_${THEMODEL}_${THEMASS}_${CURRENTTOY}.root

cp fitDiagnostics_${THEINSIGNAME}_mu${THEMUIN}_${THECOUP}_${THECAT}_${THEMODEL}_${THEMASS}_${CURRENTTOY}.root ${THEINOUTPATH}/${THECOUP}/${THECAT}/mu${THEMUIN}/${THEMODEL}/mass${THEMASS}/.

rm -rf *.root

#rm -rf python config output bkgAltModels  




