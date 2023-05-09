#!/usr/bin/env sh

# export method="genFiducial"
export method="full"
export InterpolateShapePath="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/DijetShapeInterpolator/${method}"

########## Add Samples ##########

cd /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/
cmsenv
mkdir -p output/plots

mkdir -p output/${method}
#RS
for year in {2016,2017,2018}; do echo $year; for coup in {"kMpl001","kMpl01","kMpl02"}; do echo $coup; files_RS=`ls /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/input/trees/RSGravitonToGammaGamma_${coup}*${year}*.root`; python python/AddSignalShapes.py -e ${method} -t nom -d output/${method} -c EBEB ${files_RS}; python python/AddSignalShapes.py -e ${method} -t nom -d output/${method} -c EBEE ${files_RS}; done; done;
for year in {2016,2017,2018}; do echo $year; for coup in {"kMpl001","kMpl01","kMpl02"}; do echo $coup; files_RS=`ls /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/input/trees/RSGravitonToGammaGamma_${coup}*${year}*.root`; for syst in {"energyScaleStatUp","energyScaleSystUp","energyScaleGainUp","energySigmaUp","energyScaleStatDown","energyScaleSystDown","energyScaleGainDown","energySigmaDown","SFScaleUp","SFScaleDown","PUScaleUp","PUScaleDown"}; do echo ${syst}; python python/AddSignalShapes.py -e ${method} -t systematics -s ${syst} -d output/${method} -c EBEB ${files_RS}; python python/AddSignalShapes.py -e ${method} -t systematics -s ${syst} -d output/${method} -c EBEE ${files_RS}; done; done; done;


# export mainpath="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/"
# cd $mainpath
# #With the createJson option the insigname argument is dull and the code will run through all signals.
# #2016 (Both RS and heavy higgs)
# signalNorm.exe 2016 createJson "${mainpath}/output/2016/FinalParametricShape/workspaces" "${mainpath}/datacards" "${mainpath}/output/2016/signalNorm" "grav" ${method}
# #2017 (Both RS and heavy higgs)
# signalNorm.exe 2017 createJson "${mainpath}/output/2017/FinalParametricShape/workspaces" "${mainpath}/datacards" "${mainpath}/output/2017/signalNorm" "grav" ${method}
# #2018 (Both RS and heavy higgs)
# signalNorm.exe 2018 createJson "${mainpath}/output/2018/FinalParametricShape/workspaces" "${mainpath}/datacards" "${mainpath}/output/2018/signalNorm" "grav" ${method}
# #2016 (Both RS and heavy higgs)
# rm SignalNorm_${method}.txt
# rm SignalNorm_Splines_${method}.txt
# #2016 RS
# signalNorm.exe 2016 readJson "${mainpath}/output/2016/FinalParametricShape/workspaces" "${mainpath}/datacards" "${mainpath}/output/2016/signalNorm" "grav" "${method}"
# #2017 RS
# signalNorm.exe 2017 readJson "${mainpath}/output/2017/FinalParametricShape/workspaces" "${mainpath}/datacards" "${mainpath}/output/2017/signalNorm" "grav" "${method}"
# #2018 RS
# signalNorm.exe 2018 readJson "${mainpath}/output/2018/FinalParametricShape/workspaces" "${mainpath}/datacards" "${mainpath}/output/2018/signalNorm" "grav" "${method}"
# #2016 Heavy Higgs
# signalNorm.exe 2016 readJson "${mainpath}/output/2016/FinalParametricShape/workspaces" "${mainpath}/datacards" "${mainpath}/output/2016/signalNorm" "heavyhiggs" "${method}"
# #2017 Heavy Higgs
# signalNorm.exe 2017 readJson "${mainpath}/output/2017/FinalParametricShape/workspaces" "${mainpath}/datacards" "${mainpath}/output/2017/signalNorm" "heavyhiggs" "${method}"
# #2018 Heavy Higgs
# signalNorm.exe 2018 readJson "${mainpath}/output/2018/FinalParametricShape/workspaces" "${mainpath}/datacards" "${mainpath}/output/2018/signalNorm" "heavyhiggs" "${method}"

# # cp SignalNorm.txt SignalNorm_${method}.txt
# # cp SignalNorm_Splines.txt SignalNorm_Splines_${method}.txt
# dateDir=$(date +"%Y%m%d_%H%M%S")
# for year in {"2016","2017","2018"};
# do
#     cpwww output/${year}/signalNorm ~/www/diphoton-analysis/${year}/signalNorm/${method}/${dateDir}
# done


############################################################
# Extract shapes
############################################################

mkdir /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/DijetShapeInterpolator/${method}
cd /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/DijetShapeInterpolator/${method}

rm -rf inputs *.root
mkdir inputs

filesToExtractRS=`ls /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/output/${method} |grep .root | grep RSG`

for file in ${filesToExtractRS}; do echo ${file}; cp /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/output/${method}/${file} .; filename=`echo ${file} | cut -d'.' -f 1`; rm -rf inputs/${filename}.py; ../extractShapes.py -i ${file} > inputs/${filename}.py; done;

############################################################
# Get Resonance shapes
############################################################

cd /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/DijetShapeInterpolator/${method}

filesToExtractRS=`ls /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/output/${method} |grep .root | grep RSG`

for file in ${filesToExtractRS};
do echo ${file}; coup=`echo ${file} | cut -d'_' -f 3`; echo $coup; filename=`echo ${file} | cut -d'.' -f 1`; ../getResonanceShapes.py -i inputs/${filename}.py -c ${coup} -f gg --massrange 500 8000 10 -o ResonanceShapes_${filename}.root; done;

############################################################
# Compare shapes - Closure Test - single plot comparison
############################################################

cd /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/
cmsenv
mkdir output/plots

for year in {2016,2017,2018}; do echo $year; for coup in {"kMpl001","kMpl01","kMpl02"}; do echo $coup; files_RS=`ls /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/input/trees/RSGravitonToGammaGamma_${coup}*${year}*.root`; python python/CompareShapes.py -e ${method} -d output -c EBEB -w ${coup} ${files_RS}; python python/CompareShapes.py -e ${method} -d output -c EBEE -w ${coup} ${files_RS}; done; done;

############################################################
# Compare shapes - Closure Test - multi plot comparison
############################################################

cd /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/
cmsenv

for year in {2016,2017,2018}; do echo $year; for coup in {"kMpl001","kMpl01","kMpl02"}; do echo $coup; files_Selection_RS=`ls /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/input/trees/RSGravitonToGammaGamma_${coup}*${year}*.root`; python python/CompareShapes.py -e ${method} -d output -c EBEB -m -w ${coup} ${files_Selection_RS}; python python/CompareShapes.py -e ${method} -d output -c EBEE -m -w ${coup} ${files_Selection_RS}; done; done;

dateDir=$(date +"%Y%m%d_%H%M%S")
cpwww output/plots ~/www/diphoton-analysis/SignalShapeInterpolation/${method}/${dateDir}
