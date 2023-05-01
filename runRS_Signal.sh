#!/usr/bin/env sh

# export method="genFiducial"
export method="full"
export InterpolateShapePath="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/DijetShapeInterpolator/${method}"

############################################################
# Extract shapes
############################################################

mkdir /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/DijetShapeInterpolator/${method}
cd /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/DijetShapeInterpolator/${method}

rm -rf inputs *.root
mkdir inputs

filesToExtractGluGlu=`ls /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/output/${method} |grep .root | grep GluGlu`

for file in ${filesToExtractGluGlu}; do echo ${file}; cp /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/output/${method}/${file} .; filename=`echo ${file} | cut -d'.' -f 1`; rm -rf inputs/${filename}.py; ../extractShapes.py -i ${file} > inputs/${filename}.py; done;

############################################################
# Get Resonance shapes
############################################################

cd /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/DijetShapeInterpolator/${method}

filesToExtractGluGlu=`ls /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/output/${method} |grep .root | grep GluGlu`

for file in ${filesToExtractGluGlu};
do echo ${file}; coup=`echo ${file} | cut -d'_' -f 4`; echo $coup; filename=`echo ${file} | cut -d'.' -f 1`; ../getResonanceShapes.py -i inputs/${filename}.py -c ${coup} -f gg --massrange 500 10000 10 -o ResonanceShapes_${filename}.root; done;

#Copy the root files for later usage
cp /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/DijetShapeInterpolator/${method}/ResonanceShapes*.root /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/DijetShapeInterpolator

############################################################
# Compare shapes - Closure Test - single plot comparison
############################################################

cd /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/
cmsenv
mkdir output/plots

for year in {2016,2017,2018}; do echo $year; for coup in {"0p014","1p4","5p6"}; do echo $coup; files_GluGlu=`ls /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/input/trees/GluGluSpin0ToGammaGamma_W_${coup}*${year}*.root`; python python/CompareShapes.py -e ${method} -d output -c EBEB -w ${coup} ${files_GluGlu}; python python/CompareShapes.py -e ${method} -d output -c EBEE -w ${coup} ${files_GluGlu}; done; done;

############################################################
# Compare shapes - Closure Test - multi plot comparison
############################################################

cd /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/
cmsenv

for year in {2016,2017,2018}; do echo $year; for coup in {"0p014","1p4","5p6"}; do echo $coup; files_GluGlu=`ls /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/input/trees/GluGluSpin0ToGammaGamma_W_${coup}*${year}*.root`; python python/CompareShapes.py -e ${method} -d output -c EBEB -m -w ${coup} ${files_GluGlu}; python python/CompareShapes.py -e ${method} -d output -c EBEE -m -w ${coup} ${files_GluGlu}; done; done;

dateDir=$(date +"%Y%m%d_%H%M%S")
cpwww output/plots ~/www/diphoton-analysis/SignalShapeInterpolation/${method}/${dateDir}
