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
THECAT=${14}
THELUMI=${15}
CURRENTTOY=${16}

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

time python python/RunBias.py -c config/diphotons_bias_${THEYEAR}.config -i bkgAltModels/${THEMODEL}/blind/FitResults_DiPhotons_${THECOUP}_${THECAT}_${THEYEAR}.root -b DiPhotons_${THECOUP}_${THECAT} --mass ${THEMASS} -m gg -d signal_bias -r ${THEMUIN} -l ${THELUMI} --year ${THEYEAR} -t ${THENTOYS} --gen-pdf ${THEMODEL} --fit-pdf ${THENOMINALMODEL}

outfile=`ls fitDiagnostics*|grep ${THECOUP}|grep ${THEMODEL}|grep ${THENOMINALMODEL}|grep .root`

echo ${outfile}

mv ${outfile} fitDiagnostics_${THEINSIGNAME}_mu${THEMUIN}_${THECOUP}_${THECAT}_${THEMODEL}_${THEMASS}_${CURRENTTOY}.root

cp fitDiagnostics_${THEINSIGNAME}_mu${THEMUIN}_${THECOUP}_${THECAT}_${THEMODEL}_${THEMASS}_${CURRENTTOY}.root ${THEINOUTPATH}/${THECOUP}/${THECAT}/mu${THEMUIN}/${THEMODEL}/mass${THEMASS}/.

rm -rf *.root

#rm -rf python config output bkgAltModels  




