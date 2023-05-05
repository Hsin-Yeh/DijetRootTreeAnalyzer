#!/bin/bash

# ./runHeavyHiggs.sh
# export method="full"
export method="genFiducial"
export InterpolateShapePath="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/DijetShapeInterpolator/${method}"
export configFile="config/diphotons.config"
export bkgFitResultsPath="test_directory"
export SignalNormFile="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/SignalNorm_Splines.txt"
export massInterval=100

############################## signal Interpolation ##############################

cd /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/DijetShapeInterpolator/${method}

filesToExtractGluGlu=`ls /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/output/${method} |grep .root | grep GluGlu`

for file in ${filesToExtractGluGlu};
do echo ${file}; coup=`echo ${file} | cut -d'_' -f 4`; echo $coup; filename=`echo ${file} | cut -d'.' -f 1`; ../getResonanceShapes.py -i inputs/${filename}.py -c ${coup} -f gg --massrange 500 5000 ${massInterval} -o ResonanceShapes_${filename}.root; done;

############################## fit nominal bkg model ##############################

# mkdir -p ${bkgFitResultsPath}
cd /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer

#2016 Lumi 35900
for coup in {"0p014","1p4","5p6"}; do echo $coup; for cat in {"EBEB","EBEE"}; do echo $cat; python python/BinnedFit.py -c config/diphotons_dijet.config -l 35900 -b DiPhotons_${coup}_${cat} -d ${bkgFitResultsPath} --fit-spectrum --plot-region Low --coup $coup --cat $cat --year 2016 output/InputShapes_data_${cat}_2016.root; done; done;

# #2017 Lumi 41527
for coup in {"0p014","1p4","5p6"}; do echo $coup; for cat in {"EBEB","EBEE"}; do echo $cat; python python/BinnedFit.py -c config/diphotons_dijet.config -l 41527 -b DiPhotons_${coup}_${cat} -d ${bkgFitResultsPath} --fit-spectrum --plot-region Low --coup $coup --cat $cat --year 2017 output/InputShapes_data_${cat}_2017.root; done; done;

# #2018 Lumi 59670
for coup in {"0p014","1p4","5p6"}; do echo $coup; for cat in {"EBEB","EBEE"}; do echo $cat; python python/BinnedFit.py -c config/diphotons_dijet.config -l 59670 -b DiPhotons_${coup}_${cat} -d ${bkgFitResultsPath} --fit-spectrum --plot-region Low --coup $coup --cat $cat --year 2018 output/InputShapes_data_${cat}_2018.root; done; done;


############################## WriteDataCard.py heavyhiggs ##############################

export InterpolateShapePath="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/DijetShapeInterpolator/${method}"
export configFile="config/diphotons.config"
#2016
# Remember for me the yield was initially normalized to 1000/pb. So, here lumi 41.527 (-d test_directory/2016/${box} omitted)
for mass in `seq 500 ${massInterval} 5000`; do for box in {"DiPhotons_0p014_EBEB","DiPhotons_0p014_EBEE","DiPhotons_1p4_EBEB","DiPhotons_1p4_EBEE","DiPhotons_5p6_EBEB","DiPhotons_5p6_EBEE"}; do echo ${box}; cat=`echo ${box}| cut -d"_" -f 3`; coup=`echo ${box}| cut -d"_" -f 2`; mkdir -p test_directory/${method}/2016/${box}; python python/WriteDataCard.py -m gg --mass ${mass} output/InputShapes_data_${cat}_2016.root -i ${bkgFitResultsPath}/FitResults_${box}_2016.root --lumi 35.9 -c ${configFile} -b ${box} --year 2016 --SigNorm ${SignalNormFile} --eneScStatUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2016_energyScaleStatUp.root   --eneScStatDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2016_energyScaleStatDown.root --eneScSystUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2016_energyScaleSystUp.root   --eneScSystDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2016_energyScaleSystDown.root --eneScGainUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2016_energyScaleGainUp.root   --eneScGainDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2016_energyScaleGainDown.root --eneScSigmaUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2016_energySigmaUp.root       --eneScSigmaDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2016_energySigmaDown.root     --SFScaleUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2016_SFScaleUp.root           --SFScaleDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2016_SFScaleDown.root         --PUScaleUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2016_PUScaleUp.root           --PUScaleDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2016_PUScaleDown.root ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2016.root; mv diphoton_combine_${mass}_${box}_2016.* test_directory/${method}/2016/${box}/.; done; done;

# #2017
# # Remember for me the yield was initially normalized to 1000/pb. So, here lumi 41.527 (-d test_directory/2017/${box} omitted)
# for mass in `seq 800 ${massInterval} 5000`; do for box in {"DiPhotons_0p014_EBEB","DiPhotons_0p014_EBEE","DiPhotons_1p4_EBEB","DiPhotons_1p4_EBEE","DiPhotons_5p6_EBEB","DiPhotons_5p6_EBEE"}; do echo ${box}; cat=`echo ${box}| cut -d"_" -f 3`; coup=`echo ${box}| cut -d"_" -f 2`; mkdir -p test_directory/${method}/2017/${box}; python python/WriteDataCard.py -m gg --mass ${mass} output/InputShapes_data_${cat}_2017.root -i ${bkgFitResultsPath}/FitResults_${box}_2017.root --lumi 41.527 -c ${configFile} -b ${box} --year 2017 --SigNorm ${SignalNormFile} --eneScStatUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2017_energyScaleStatUp.root   --eneScStatDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2017_energyScaleStatDown.root --eneScSystUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2017_energyScaleSystUp.root   --eneScSystDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2017_energyScaleSystDown.root --eneScGainUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2017_energyScaleGainUp.root   --eneScGainDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2017_energyScaleGainDown.root --eneScSigmaUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2017_energySigmaUp.root       --eneScSigmaDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2017_energySigmaDown.root     --SFScaleUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2017_SFScaleUp.root           --SFScaleDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2017_SFScaleDown.root         --PUScaleUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2017_PUScaleUp.root           --PUScaleDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2017_PUScaleDown.root ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2017.root; mv diphoton_combine_${mass}_${box}_2017.* test_directory/${method}/2017/${box}/.; done; done;

# #2018
# # Remember for me the yield was initially normalized to 1000/pb. So, here lumi 41.527 (-d test_directory/2018/${box} omitted)
# for mass in `seq 500 ${massInterval} 5000`; do for box in {"DiPhotons_0p014_EBEB","DiPhotons_0p014_EBEE","DiPhotons_1p4_EBEB","DiPhotons_1p4_EBEE","DiPhotons_5p6_EBEB","DiPhotons_5p6_EBEE"}; do echo ${box}; cat=`echo ${box}| cut -d"_" -f 3`; coup=`echo ${box}| cut -d"_" -f 2`; mkdir -p test_directory/${method}/2018/${box}; python python/WriteDataCard.py -m gg --mass ${mass} output/InputShapes_data_${cat}_2018.root -i ${bkgFitResultsPath}/FitResults_${box}_2018.root --lumi 59.670 -c ${configFile} -b ${box} --year 2018 --SigNorm ${SignalNormFile} --eneScStatUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2018_energyScaleStatUp.root   --eneScStatDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2018_energyScaleStatDown.root --eneScSystUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2018_energyScaleSystUp.root   --eneScSystDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2018_energyScaleSystDown.root --eneScGainUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2018_energyScaleGainUp.root   --eneScGainDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2018_energyScaleGainDown.root --eneScSigmaUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2018_energySigmaUp.root       --eneScSigmaDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2018_energySigmaDown.root     --SFScaleUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2018_SFScaleUp.root           --SFScaleDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2018_SFScaleDown.root         --PUScaleUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2018_PUScaleUp.root           --PUScaleDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2018_PUScaleDown.root ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2018.root; mv diphoton_combine_${mass}_${box}_2018.* test_directory/${method}/2018/${box}/.; done; done;

#combine years and channels
themainpath="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/test_directory"

# mkdir ${themainpath}/${method}/fullRun2
# cd ${themainpath}/${method}/fullRun2
# for scenario in {"DiPhotons_0p014","DiPhotons_1p4","DiPhotons_5p6"}; do echo ${scenario}; for mass in `seq 500 ${massInterval} 6000`; do echo ${mass}; combineCards.py ${themainpath}/${method}/2016/${scenario}_EBEB/diphoton_combine_${mass}_${scenario}_EBEB_2016.txt ${themainpath}/${method}/2016/${scenario}_EBEE/diphoton_combine_${mass}_${scenario}_EBEE_2016.txt ${themainpath}/${method}/2017/${scenario}_EBEB/diphoton_combine_${mass}_${scenario}_EBEB_2017.txt ${themainpath}/${method}/2017/${scenario}_EBEE/diphoton_combine_${mass}_${scenario}_EBEE_2017.txt ${themainpath}/${method}/2018/${scenario}_EBEB/diphoton_combine_${mass}_${scenario}_EBEB_2018.txt ${themainpath}/${method}/2018/${scenario}_EBEE/diphoton_combine_${mass}_${scenario}_EBEE_2018.txt > diphoton_combine_${mass}_${scenario}.txt; done; done;

cd ${themainpath}/${method}/2016
for scenario in {"DiPhotons_0p014","DiPhotons_1p4","DiPhotons_5p6"}; do echo ${scenario}; for mass in `seq 500 ${massInterval} 6000`; do echo ${mass}; combineCards.py  ${themainpath}/${method}/2016/${scenario}_EBEB/diphoton_combine_${mass}_${scenario}_EBEB_2016.txt ${themainpath}/${method}/2016/${scenario}_EBEE/diphoton_combine_${mass}_${scenario}_EBEE_2016.txt  > diphoton_combine_${mass}_${scenario}_2016.txt; done; done;

# cd ${themainpath}/${method}/2017
# for scenario in {"DiPhotons_0p014","DiPhotons_1p4","DiPhotons_5p6"}; do echo ${scenario}; for mass in `seq 800 ${massInterval} 6000`; do echo ${mass}; combineCards.py  ${themainpath}/${method}/2017/${scenario}_EBEB/diphoton_combine_${mass}_${scenario}_EBEB_2017.txt ${themainpath}/${method}/2017/${scenario}_EBEE/diphoton_combine_${mass}_${scenario}_EBEE_2017.txt  > diphoton_combine_${mass}_${scenario}_2017.txt; done; done;

# cd ${themainpath}/${method}/2018
# for scenario in {"DiPhotons_0p014","DiPhotons_1p4","DiPhotons_5p6"}; do echo ${scenario}; for mass in `seq 500 ${massInterval} 6000`; do echo ${mass}; combineCards.py  ${themainpath}/${method}/2018/${scenario}_EBEB/diphoton_combine_${mass}_${scenario}_EBEB_2018.txt ${themainpath}/${method}/2018/${scenario}_EBEE/diphoton_combine_${mass}_${scenario}_EBEE_2018.txt  > diphoton_combine_${mass}_${scenario}_2018.txt; done; done;

export mainpath="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/FinalResults"
cd ${mainpath}

#Then, run (will take some time depending on the mass points number)
#2016 heavyhiggs
./loopAllMassPoints.csh 2016 heavyhiggs 0p014 ${method} &
./loopAllMassPoints.csh 2016 heavyhiggs 1p4 ${method} &
./loopAllMassPoints.csh 2016 heavyhiggs 5p6 ${method} &
#2017 RS
# ./loopAllMassPoints.csh 2017 heavyhiggs 0p014 ${method} &
# ./loopAllMassPoints.csh 2017 heavyhiggs 1p4 ${method} &
# ./loopAllMassPoints.csh 2017 heavyhiggs 5p6 ${method} &
# #2018 RS
# ./loopAllMassPoints.csh 2018 heavyhiggs 0p014 ${method} &
# ./loopAllMassPoints.csh 2018 heavyhiggs 1p4 ${method} &
# ./loopAllMassPoints.csh 2018 heavyhiggs 5p6 ${method} &
# #Full Run2 RS
# ./loopAllMassPoints.csh fullRun2 heavyhiggs 0p014 ${method} &
# ./loopAllMassPoints.csh fullRun2 heavyhiggs 1p4 ${method} &
# ./loopAllMassPoints.csh fullRun2 heavyhiggs 5p6 ${method} &
