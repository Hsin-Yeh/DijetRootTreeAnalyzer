#!/usr/bin/env bash

export method="full"
export massInterval=100

# Paths
export InterpolateShapePath="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/DijetShapeInterpolator/${method}"
export configFile="config/diphotons_500GeV.config"
export bkgFitResultsPath="datacards/multi"
export datacardsDir="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/datacards/multi"
export SignalNormFile="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/SignalNorm_Splines_${method}.txt"

# Run flags
export binnedFit_flag=false
export writeDataCard_flag=true
export combineCard_flag=true
export combineLimit_flag=true

# ############################## signal interpolation ##############################

# cd /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/DijetShapeInterpolator/${method}

# filesToExtractRS=`ls /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/output/${method} |grep .root | grep RSG`

# for file in ${filesToExtractRS};
# do echo ${file}; coup=`echo ${file} | cut -d'_' -f 3`; echo $coup; filename=`echo ${file} | cut -d'.' -f 1`; ../getResonanceShapes.py -i inputs/${filename}.py -c ${coup} -f gg --massrange 500 10000 ${massInterval} -o ResonanceShapes_${filename}.root; done;


# ############################## bkg model ##############################

cd /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer

mkdir -p ${datacardsDir}


if $binnedFit_flag; then
    # 2016 Lumi 35900
    for coup in {"kMpl001","kMpl01","kMpl02"}; do echo $coup; for cat in {"EBEB","EBEE"}; do echo $cat; python python/BinnedFit.py -c config/diphotons_dijet_2016.config -l 35900 -b DiPhotons_${coup}_${cat}_2016 -d ${bkgFitResultsPath} --fit-spectrum --plot-region Low --coup $coup --cat $cat --year 2016 output/InputShapes_data_${cat}_2016.root; done; done;

    # #2017 Lumi 41527
    for coup in {"kMpl001","kMpl01","kMpl02"}; do echo $coup; for cat in {"EBEB","EBEE"}; do echo $cat; python python/BinnedFit.py -c config/diphotons_dijet_2017.config -l 41527 -b DiPhotons_${coup}_${cat}_2017 -d ${bkgFitResultsPath} --fit-spectrum --plot-region Low --coup $coup --cat $cat --year 2017 output/InputShapes_data_${cat}_2017.root; done; done;

    # #2018 Lumi 59670
    for coup in {"kMpl001","kMpl01","kMpl02"}; do echo $coup; for cat in {"EBEB","EBEE"}; do echo $cat; python python/BinnedFit.py -c config/diphotons_dijet_2018.config -l 59670 -b DiPhotons_${coup}_${cat}_2018 -d ${bkgFitResultsPath} --fit-spectrum --plot-region Low --coup $coup --cat $cat --year 2018 output/InputShapes_data_${cat}_2018.root; done; done;
fi
# #-------
# #UNBLIND
# #-------

# #2016 Lumi 35900
# for bkgmodel in {"dijet","expow1","invpow1","invpowlin1"}; do echo ${bkgmodel}; mkdir -p bkgAltModels/${bkgmodel}/unblind; for coup in {"kMpl001","kMpl01","kMpl02"}; do echo $coup; for cat in {"EBEB","EBEE"}; do echo $cat; python python/BinnedFit.py -c config/diphotons_${bkgmodel}.config -l 35900 -b DiPhotons_${coup}_${cat} -d bkgAltModels/${bkgmodel}/unblind --fit-spectrum --coup $coup --cat $cat --year 2016 output/InputShapes_data_${cat}_2016.root; done; done; done;

# #2017 Lumi 41527
# for bkgmodel in {"dijet","expow1","invpow1","invpowlin1"}; do echo ${bkgmodel}; mkdir -p bkgAltModels/${bkgmodel}/unblind; for coup in {"kMpl001","kMpl01","kMpl02"}; do echo $coup; for cat in {"EBEB","EBEE"}; do echo $cat; python python/BinnedFit.py -c config/diphotons_${bkgmodel}.config -l 41527 -b DiPhotons_${coup}_${cat} -d bkgAltModels/${bkgmodel}/unblind --fit-spectrum --coup $coup --cat $cat --year 2017 output/InputShapes_data_${cat}_2017.root; done; done; done;

# #2018 Lumi 59670
# for bkgmodel in {"dijet","expow1","invpow1","invpowlin1"}; do echo ${bkgmodel}; mkdir -p bkgAltModels/${bkgmodel}/unblind; for coup in {"kMpl001","kMpl01","kMpl02"}; do echo $coup; for cat in {"EBEB","EBEE"}; do echo $cat; python python/BinnedFit.py -c config/diphotons_${bkgmodel}.config -l 59670 -b DiPhotons_${coup}_${cat} -d bkgAltModels/${bkgmodel}/unblind --fit-spectrum --coup $coup --cat $cat --year 2018 output/InputShapes_data_${cat}_2018.root; done; done; done;

############################## WriteDataCard.py grav ##############################

if $writeDataCard_flag; then
    #2016
    # Remember for me the yield was initially normalized to 1000/pb. So, here lumi 35.9 (-d ${datacardsDir}/2016/${box} omitted)
    for mass in `seq 600 ${massInterval} 5000`; do for box in {"DiPhotons_kMpl001_EBEB_2016","DiPhotons_kMpl001_EBEE_2016"}; do echo ${box}; cat=`echo ${box}| cut -d"_" -f 3`; coup=`echo ${box}| cut -d"_" -f 2`; mkdir -p ${datacardsDir}/${method}/2016/${box}; python python/WriteDataCard.py --multi -m gg --mass ${mass} output/InputShapes_data_${cat}_2016.root -i ${bkgFitResultsPath}/FitResults_${box}.root --lumi 35.9 -c config/diphotons_bias_2016_pdf_index_wopip.config -b ${box} --year 2016 --SigNorm ${SignalNormFile} --eneScStatUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2016_energyScaleStatUp.root   --eneScStatDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2016_energyScaleStatDown.root --eneScSystUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2016_energyScaleSystUp.root   --eneScSystDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2016_energyScaleSystDown.root --eneScGainUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2016_energyScaleGainUp.root   --eneScGainDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2016_energyScaleGainDown.root --eneScSigmaUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2016_energySigmaUp.root       --eneScSigmaDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2016_energySigmaDown.root     --SFScaleUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2016_SFScaleUp.root           --SFScaleDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2016_SFScaleDown.root         --PUScaleUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2016_PUScaleUp.root           --PUScaleDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2016_PUScaleDown.root ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2016.root; mv diphoton_combine_${mass}_${box}.* ${datacardsDir}/${method}/2016/${box}/.; done; done;

    for mass in `seq 600 ${massInterval} 7000`; do for box in {"DiPhotons_kMpl01_EBEB_2016","DiPhotons_kMpl01_EBEE_2016","DiPhotons_kMpl02_EBEB_2016","DiPhotons_kMpl02_EBEE_2016"}; do echo ${box}; cat=`echo ${box}| cut -d"_" -f 3`; coup=`echo ${box}| cut -d"_" -f 2`; mkdir -p ${datacardsDir}/${method}/2016/${box}; python python/WriteDataCard.py --multi -m gg --mass ${mass} output/InputShapes_data_${cat}_2016.root -i ${bkgFitResultsPath}/FitResults_${box}.root --lumi 35.9 -c config/diphotons_bias_2016_pdf_index_wopip.config -b ${box} --year 2016 --SigNorm ${SignalNormFile} --eneScStatUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2016_energyScaleStatUp.root   --eneScStatDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2016_energyScaleStatDown.root --eneScSystUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2016_energyScaleSystUp.root   --eneScSystDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2016_energyScaleSystDown.root --eneScGainUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2016_energyScaleGainUp.root   --eneScGainDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2016_energyScaleGainDown.root --eneScSigmaUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2016_energySigmaUp.root       --eneScSigmaDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2016_energySigmaDown.root     --SFScaleUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2016_SFScaleUp.root           --SFScaleDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2016_SFScaleDown.root         --PUScaleUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2016_PUScaleUp.root           --PUScaleDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2016_PUScaleDown.root ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2016.root; mv diphoton_combine_${mass}_${box}.* ${datacardsDir}/${method}/2016/${box}/.; done; done;

    #2017
    # Remember for me the yield was initially normalized to 1000/pb. So, here lumi 41.527 (-d ${datacardsDir}/2017/${box} omitted)
    for mass in `seq 600 ${massInterval} 5000`; do for box in {"DiPhotons_kMpl001_EBEB_2017","DiPhotons_kMpl001_EBEE_2017"}; do echo ${box}; cat=`echo ${box}| cut -d"_" -f 3`; coup=`echo ${box}| cut -d"_" -f 2`; mkdir -p ${datacardsDir}/${method}/2017/${box}; python python/WriteDataCard.py --multi -m gg --mass ${mass} output/InputShapes_data_${cat}_2017.root -i ${bkgFitResultsPath}/FitResults_${box}.root --lumi 41.527 -c config/diphotons_bias_2017_pdf_index_wopip.config -b ${box} --year 2017 --SigNorm ${SignalNormFile} --eneScStatUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2017_energyScaleStatUp.root   --eneScStatDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2017_energyScaleStatDown.root --eneScSystUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2017_energyScaleSystUp.root   --eneScSystDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2017_energyScaleSystDown.root --eneScGainUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2017_energyScaleGainUp.root   --eneScGainDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2017_energyScaleGainDown.root --eneScSigmaUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2017_energySigmaUp.root       --eneScSigmaDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2017_energySigmaDown.root     --SFScaleUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2017_SFScaleUp.root           --SFScaleDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2017_SFScaleDown.root         --PUScaleUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2017_PUScaleUp.root           --PUScaleDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2017_PUScaleDown.root ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2017.root; mv diphoton_combine_${mass}_${box}.* ${datacardsDir}/${method}/2017/${box}/.; done; done;

    for mass in `seq 600 ${massInterval} 7000`; do for box in {"DiPhotons_kMpl01_EBEB_2017","DiPhotons_kMpl01_EBEE_2017","DiPhotons_kMpl02_EBEB_2017","DiPhotons_kMpl02_EBEE_2017"}; do echo ${box}; cat=`echo ${box}| cut -d"_" -f 3`; coup=`echo ${box}| cut -d"_" -f 2`; mkdir -p ${datacardsDir}/${method}/2017/${box}; python python/WriteDataCard.py --multi -m gg --mass ${mass} output/InputShapes_data_${cat}_2017.root -i ${bkgFitResultsPath}/FitResults_${box}.root --lumi 41.527 -c config/diphotons_bias_2017_pdf_index_wopip.config -b ${box} --year 2017 --SigNorm ${SignalNormFile} --eneScStatUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2017_energyScaleStatUp.root   --eneScStatDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2017_energyScaleStatDown.root --eneScSystUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2017_energyScaleSystUp.root   --eneScSystDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2017_energyScaleSystDown.root --eneScGainUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2017_energyScaleGainUp.root   --eneScGainDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2017_energyScaleGainDown.root --eneScSigmaUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2017_energySigmaUp.root       --eneScSigmaDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2017_energySigmaDown.root     --SFScaleUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2017_SFScaleUp.root           --SFScaleDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2017_SFScaleDown.root         --PUScaleUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2017_PUScaleUp.root           --PUScaleDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2017_PUScaleDown.root ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2017.root; mv diphoton_combine_${mass}_${box}.* ${datacardsDir}/${method}/2017/${box}/.; done; done;
    # for mass in `seq 600 ${massInterval} 7000`; do for box in {"DiPhotons_kMpl02_EBEB_2017","DiPhotons_kMpl02_EBEE_2017"}; do echo ${box}; cat=`echo ${box}| cut -d"_" -f 3`; coup=`echo ${box}| cut -d"_" -f 2`; mkdir -p ${datacardsDir}/${method}/2017/${box}; python python/WriteDataCard.py --multi -m gg --mass ${mass} output/InputShapes_data_${cat}_2017.root -i ${bkgFitResultsPath}/FitResults_${box}.root --lumi 41.527 -c config/diphotons_bias_2017_pdf_index_wopip.config -b ${box} --year 2017 --SigNorm ${SignalNormFile} --eneScStatUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2017_energyScaleStatUp.root   --eneScStatDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2017_energyScaleStatDown.root --eneScSystUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2017_energyScaleSystUp.root   --eneScSystDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2017_energyScaleSystDown.root --eneScGainUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2017_energyScaleGainUp.root   --eneScGainDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2017_energyScaleGainDown.root --eneScSigmaUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2017_energySigmaUp.root       --eneScSigmaDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2017_energySigmaDown.root     --SFScaleUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2017_SFScaleUp.root           --SFScaleDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2017_SFScaleDown.root         --PUScaleUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2017_PUScaleUp.root           --PUScaleDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2017_PUScaleDown.root ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2017.root; mv diphoton_combine_${mass}_${box}.* ${datacardsDir}/${method}/2017/${box}/.; done; done;

    #2018
    # Remember for me the yield was initially normalized to 1000/pb. So, here lumi 59.670 (-d ${datacardsDir}/2018/${box} omitted)
    for mass in `seq 600 ${massInterval} 5000`; do for box in {"DiPhotons_kMpl001_EBEB_2018","DiPhotons_kMpl001_EBEE_2018"}; do echo ${box}; cat=`echo ${box}| cut -d"_" -f 3`; coup=`echo ${box}| cut -d"_" -f 2`; mkdir -p ${datacardsDir}/${method}/2018/${box}; python python/WriteDataCard.py --multi -m gg --mass ${mass} output/InputShapes_data_${cat}_2018.root -i ${bkgFitResultsPath}/FitResults_${box}.root --lumi 59.670 -c config/diphotons_bias_2018_pdf_index_wopip.config -b ${box} --year 2018 --SigNorm ${SignalNormFile} --eneScStatUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2018_energyScaleStatUp.root   --eneScStatDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2018_energyScaleStatDown.root --eneScSystUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2018_energyScaleSystUp.root   --eneScSystDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2018_energyScaleSystDown.root --eneScGainUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2018_energyScaleGainUp.root   --eneScGainDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2018_energyScaleGainDown.root --eneScSigmaUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2018_energySigmaUp.root       --eneScSigmaDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2018_energySigmaDown.root     --SFScaleUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2018_SFScaleUp.root           --SFScaleDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2018_SFScaleDown.root         --PUScaleUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2018_PUScaleUp.root           --PUScaleDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2018_PUScaleDown.root ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2018.root; mv diphoton_combine_${mass}_${box}.* ${datacardsDir}/${method}/2018/${box}/.; done; done;

    for mass in `seq 600 ${massInterval} 7000`; do for box in {"DiPhotons_kMpl01_EBEB_2018","DiPhotons_kMpl01_EBEE_2018","DiPhotons_kMpl02_EBEB_2018","DiPhotons_kMpl02_EBEE_2018"}; do echo ${box}; cat=`echo ${box}| cut -d"_" -f 3`; coup=`echo ${box}| cut -d"_" -f 2`; mkdir -p ${datacardsDir}/${method}/2018/${box}; python python/WriteDataCard.py --multi --multi -m gg --mass ${mass} output/InputShapes_data_${cat}_2018.root -i ${bkgFitResultsPath}/FitResults_${box}.root --lumi 59.670 -c config/diphotons_bias_2018_pdf_index_wopip.config -b ${box} --year 2018 --SigNorm ${SignalNormFile} --eneScStatUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2018_energyScaleStatUp.root   --eneScStatDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2018_energyScaleStatDown.root --eneScSystUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2018_energyScaleSystUp.root   --eneScSystDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2018_energyScaleSystDown.root --eneScGainUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2018_energyScaleGainUp.root   --eneScGainDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2018_energyScaleGainDown.root --eneScSigmaUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2018_energySigmaUp.root       --eneScSigmaDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2018_energySigmaDown.root     --SFScaleUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2018_SFScaleUp.root           --SFScaleDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2018_SFScaleDown.root         --PUScaleUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2018_PUScaleUp.root           --PUScaleDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2018_PUScaleDown.root ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2018.root; mv diphoton_combine_${mass}_${box}.* ${datacardsDir}/${method}/2018/${box}/.; done; done;
    # for mass in `seq 750 ${massInterval} 7000`; do for box in {"DiPhotons_kMpl02_EBEB","DiPhotons_kMpl02_EBEE"}; do echo ${box}; cat=`echo ${box}| cut -d"_" -f 3`; coup=`echo ${box}| cut -d"_" -f 2`; mkdir -p ${datacardsDir}/${method}/2018/${box}; python python/WriteDataCard.py --multi -m gg --mass ${mass} output/InputShapes_data_${cat}_2018.root -i ${bkgFitResultsPath}/FitResults_${box}_2018.root --lumi 59.670 -c ${configFile} -b ${box} --year 2018 --SigNorm ${SignalNormFile} --eneScStatUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2018_energyScaleStatUp.root   --eneScStatDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2018_energyScaleStatDown.root --eneScSystUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2018_energyScaleSystUp.root   --eneScSystDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2018_energyScaleSystDown.root --eneScGainUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2018_energyScaleGainUp.root   --eneScGainDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2018_energyScaleGainDown.root --eneScSigmaUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2018_energySigmaUp.root       --eneScSigmaDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2018_energySigmaDown.root     --SFScaleUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2018_SFScaleUp.root           --SFScaleDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2018_SFScaleDown.root         --PUScaleUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2018_PUScaleUp.root           --PUScaleDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2018_PUScaleDown.root ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_2018.root; mv diphoton_combine_${mass}_${box}_2018.* ${datacardsDir}/${method}/2018/${box}/.; done; done;
fi

# ############################## Combine cards ##############################

if $combineCard_flag; then
    for year in {2016,2017,2018}
    do
        echo ${year}
        cd ${datacardsDir}/${method}/${year}
        for scenario in {"DiPhotons_kMpl001","DiPhotons_kMpl01","DiPhotons_kMpl02"}
        do
            echo ${scenario}
            for mass in `seq 600 ${massInterval} 7000`
            do echo ${mass}
               combineCards.py ${datacardsDir}/${method}/${year}/${scenario}_EBEB_${year}/diphoton_combine_${mass}_${scenario}_EBEB_${year}.txt    ${datacardsDir}/${method}/${year}/${scenario}_EBEE_${year}/diphoton_combine_${mass}_${scenario}_EBEE_${year}.txt  > diphoton_combine_${mass}_${scenario}_${year}.txt
            done
        done
    done

    mkdir ${datacardsDir}/${method}/fullRun2
    cd ${datacardsDir}/${method}/fullRun2
    for scenario in {"DiPhotons_kMpl001","DiPhotons_kMpl01","DiPhotons_kMpl02"}
    do
        echo ${scenario}
        for mass in `seq 600 ${massInterval} 7000`
        do
            echo ${mass}
            combineCards.py ${datacardsDir}/${method}/2016/${scenario}_EBEB_2016/diphoton_combine_${mass}_${scenario}_EBEB_2016.txt ${datacardsDir}/${method}/2016/${scenario}_EBEE_2016/diphoton_combine_${mass}_${scenario}_EBEE_2016.txt ${datacardsDir}/${method}/2017/${scenario}_EBEB_2017/diphoton_combine_${mass}_${scenario}_EBEB_2017.txt ${datacardsDir}/${method}/2017/${scenario}_EBEE_2017/diphoton_combine_${mass}_${scenario}_EBEE_2017.txt ${datacardsDir}/${method}/2018/${scenario}_EBEB_2018/diphoton_combine_${mass}_${scenario}_EBEB_2018.txt ${datacardsDir}/${method}/2018/${scenario}_EBEE_2018/diphoton_combine_${mass}_${scenario}_EBEE_2018.txt > diphoton_combine_${mass}_${scenario}.txt;
        done
    done
fi

# ############################## Combine Limit ##############################

if $combineLimit_flag; then
    export mainpath="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/FinalResults"
    cd /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/FinalResults/

    #Then, run (will take some time depending on the mass points number)
    #2016 RS
    ./loopAllMassPoints.csh 2016 grav kMpl001 ${method} ${massInterval} ${datacardsDir} &
    ./loopAllMassPoints.csh 2016 grav kMpl01 ${method} ${massInterval} ${datacardsDir} &
    ./loopAllMassPoints.csh 2016 grav kMpl02 ${method} ${massInterval} ${datacardsDir} &
    #2017 RS
    ./loopAllMassPoints.csh 2017 grav kMpl001 ${method} ${massInterval} ${datacardsDir} &
    ./loopAllMassPoints.csh 2017 grav kMpl01 ${method} ${massInterval} ${datacardsDir} &
    ./loopAllMassPoints.csh 2017 grav kMpl02 ${method} ${massInterval} ${datacardsDir} &
    #2018 RS
    ./loopAllMassPoints.csh 2018 grav kMpl001 ${method} ${massInterval} ${datacardsDir} &
    ./loopAllMassPoints.csh 2018 grav kMpl01 ${method} ${massInterval} ${datacardsDir} &
    ./loopAllMassPoints.csh 2018 grav kMpl02 ${method} ${massInterval} ${datacardsDir} &
    #Full Run2 RS
    ./loopAllMassPoints.csh fullRun2 grav kMpl001 ${method} ${massInterval} ${datacardsDir} &
    ./loopAllMassPoints.csh fullRun2 grav kMpl01 ${method} ${massInterval} ${datacardsDir} &
    ./loopAllMassPoints.csh fullRun2 grav kMpl02 ${method} ${massInterval} ${datacardsDir} &
fi
