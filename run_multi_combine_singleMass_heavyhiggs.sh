#!/bin/bash

# for year in {"2016","2017","2018","fullRun2"}; do for coup in {"kMpl001","kMpl01","kMpl02"}; do ./run_multi_combine.sh ${year} ${coup}; done; done;
# for year in {"2016","2017","2018"}; do for coup in {"0p014","1p4","5p6"}; do ./run_multi_combine.sh ${year} ${coup}; done; done;
# for year in {"2016","2017","2018","fullRun2"}; do ./run_multi_combine.sh ${year} kMpl001; done;
# for coup in {"kMpl001","kMpl01","kMpl02"}; do ./run_multi_combine.sh fullRun2 ${coup}; done;
# ./run_multi_combine.sh 2016 kMpl001
# ./run_multi_combine.sh 2016 kMpl01
# ./run_multi_combine.sh 2016 kMpl02
# ./run_multi_combine.sh 2017 kMpl001
# ./run_multi_combine.sh 2017 kMpl01
# ./run_multi_combine.sh 2017 kMpl02
# ./run_multi_combine.sh 2018 kMpl001
# ./run_multi_combine.sh 2018 kMpl01
# ./run_multi_combine.sh 2018 kMpl02
#
# ./run_multi_combine.sh 2016 0p014
# ./run_multi_combine.sh 2016 1p4
# ./run_multi_combine.sh 2016 5p6
# ./run_multi_combine.sh 2017 0p014
# ./run_multi_combine.sh 2017 1p4
# ./run_multi_combine.sh 2017 5p6
# ./run_multi_combine.sh 2018 0p014
# ./run_multi_combine.sh 2018 1p4
# ./run_multi_combine.sh 2018 5p6

export version="2024-03-17-heavyhiggs"
export coupling=$1
export mass=$2


#################### Constants ####################
# Cats
export catlist=("EBEB" "EBEE")
# Lumi
export lumi=35.9
export lumi_1000=35900
if [[ ${year} == "2017" ]]; then
    export lumi=41.527
    export lumi_1000=41527
elif [[ ${year} == "2018" ]]; then
    export lumi=59.670
    export lumi_1000=59670
elif [[ ${year} == "fullRun2" ]]; then
    export lumi=137.600
    export lumi_1000=137600
fi

# method
export method="full"
export signal="grav"
export signal_LongName="RSGravitonToGammaGamma"
if [[ ${coupling} == "0p014" || ${coupling} == "1p4" || ${coupling} == "5p6" ]]; then
    export method="genFiducial"
    export signal="heavyhiggs"
    export signal_LongName="GluGluSpin0ToGammaGamma_W"
fi
# unblind
export unblind=false
if [[ ${year} == "2016" ]]; then
    export unblind=false
fi

#################### Paths ####################
export inputDataDir="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/output/InputShapes_data_backup"
export InterpolateShapePath="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/DijetShapeInterpolator/${method}/"
export configFile="config/diphotons_500GeV.config"
export bkgFitResultsPath="datacards/multi"
export datacardsDir="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/datacards/multi/${version}"
export SignalNormFile="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/SignalNorm_Splines_${method}.txt"

#################### Run flags ####################
export binnedFit_flag=false
export writeDataCard_flag=true
export combineCard_flag=true
export combineLimit_flag=true

# ############################## bkg model ##############################
if $binnedFit_flag; then
    mkdir ${bkgFitResultsPath}
    mkdir ${bkgFitResultsPath}/blind
    mkdir ${bkgFitResultsPath}/unblind
    echo $coupling;
    fitconfigFile="config/diphotons_dijet_${year}.config"
    fitconfigFile_multi="config/diphotons_multiplot_500GeV.config"
    for cat in "${catlist[@]}"; do
        echo ${cat};
        # blind
        python python/BinnedFitForPlottingMulti.py -c ${fitconfigFile_multi} -l ${lumi_1000} -b DiPhotons_${coupling}_${cat} -d ${bkgFitResultsPath}/blind --fit-spectrum --plot-region Low --coup $coupling --cat $cat --year ${year} ${inputDataDir}/InputShapes_data_${cat}_${year}.root;
        python python/BinnedFit.py -c ${fitconfigFile} -l ${lumi_1000} -b DiPhotons_${coupling}_${cat}_${year} -d ${bkgFitResultsPath}/blind --fit-spectrum --plot-region Low --coup $coupling --cat $cat --year ${year} ${inputDataDir}/InputShapes_data_${cat}_${year}.root;
        # unblind
        python python/BinnedFitForPlottingMulti.py -c ${fitconfigFile_multi} -l ${lumi_1000} -b DiPhotons_${coupling}_${cat} -d ${bkgFitResultsPath}/unblind --fit-spectrum --coup $coupling --cat $cat --year ${year} ${inputDataDir}/InputShapes_data_${cat}_${year}.root;
        python python/BinnedFit.py -c ${fitconfigFile} -l ${lumi_1000} -b DiPhotons_${coupling}_${cat}_${year} -d ${bkgFitResultsPath}/unblind --fit-spectrum --coup $coupling --cat $cat --year ${year} ${inputDataDir}/InputShapes_data_${cat}_${year}.root;
        # For datacards
        python python/BinnedFit.py -c ${fitconfigFile} -l ${lumi_1000} -b DiPhotons_${coupling}_${cat}_${year} -d ${bkgFitResultsPath} --fit-spectrum --plot-region Low --coup $coupling --cat $cat --year ${year} ${inputDataDir}/InputShapes_data_${cat}_${year}.root;
    done
fi
############################## WriteDataCard.py grav ##############################
# The yield was initially normalized to 1000/pb.
echo "########## Write Datacards... ##########"
for year in "${yearlist[@]}"; do
    # Lumi
    export lumi=35.9
    if [[ ${year} == "2017" ]]; then
        export lumi=41.527
    elif [[ ${year} == "2018" ]]; then
        export lumi=59.670
    fi
    for cat in "${catlist[@]}"; do
        box="DiPhotons_${coupling}_${cat}_${year}"
        echo ${year} ${box}
        export datacard_configfile="config/diphotons_bias_${year}_pdf_index_wopip_wopil.config"
        python ${DijetRootTreeAnalyzer}/python/WriteDataCard.py --multi -m gg --mass ${mass} ${inputDataDir}/InputShapes_data_${cat}_${year}.root \
            -i ${bkgFitResultsPath}/FitResults_${box}.root --lumi ${lumi} -c ${datacard_configfile} -b ${box} --year ${year} \
            --SigNorm ${SignalNormFile} \
            --eneScStatUp    signal_shapes/ResonanceShapes_InputShapes_${signal_LongName}_${coupling}_${cat}_${year}_energyScaleStatUp.root   \
            --eneScStatDown  signal_shapes/ResonanceShapes_InputShapes_${signal_LongName}_${coupling}_${cat}_${year}_energyScaleStatDown.root \
            --eneScSystUp    signal_shapes/ResonanceShapes_InputShapes_${signal_LongName}_${coupling}_${cat}_${year}_energyScaleSystUp.root   \
            --eneScSystDown  signal_shapes/ResonanceShapes_InputShapes_${signal_LongName}_${coupling}_${cat}_${year}_energyScaleSystDown.root \
            --eneScGainUp    signal_shapes/ResonanceShapes_InputShapes_${signal_LongName}_${coupling}_${cat}_${year}_energyScaleGainUp.root   \
            --eneScGainDown  signal_shapes/ResonanceShapes_InputShapes_${signal_LongName}_${coupling}_${cat}_${year}_energyScaleGainDown.root \
            --eneScSigmaUp   signal_shapes/ResonanceShapes_InputShapes_${signal_LongName}_${coupling}_${cat}_${year}_energySigmaUp.root       \
            --eneScSigmaDown signal_shapes/ResonanceShapes_InputShapes_${signal_LongName}_${coupling}_${cat}_${year}_energySigmaDown.root     \
            --SFScaleUp      signal_shapes/ResonanceShapes_InputShapes_${signal_LongName}_${coupling}_${cat}_${year}_SFScaleUp.root           \
            --SFScaleDown    signal_shapes/ResonanceShapes_InputShapes_${signal_LongName}_${coupling}_${cat}_${year}_SFScaleDown.root         \
            --PUScaleUp      signal_shapes/ResonanceShapes_InputShapes_${signal_LongName}_${coupling}_${cat}_${year}_PUScaleUp.root           \
            --PUScaleDown    signal_shapes/ResonanceShapes_InputShapes_${signal_LongName}_${coupling}_${cat}_${year}_PUScaleDown.root         \
            signal_shapes/ResonanceShapes_InputShapes_${signal_LongName}_${coupling}_${cat}_${year}.root;
        mv diphoton_combine_${mass}_${box}.* ${datacardsDir}/.
    done
done
# ############################## Combine cards ##############################
echo "########## Combine Datacards ##########"
scenario="DiPhotons_${coupling}"
datacardfile="${datacardsDir}/diphoton_combine_${mass}_${scenario}_fullRun2.txt"
combineCards.py ${datacardsDir}/diphoton_combine_${mass}_${scenario}_EBEB_2016.txt \
    ${datacardsDir}/diphoton_combine_${mass}_${scenario}_EBEE_2016.txt \
    ${datacardsDir}/diphoton_combine_${mass}_${scenario}_EBEB_2017.txt \
    ${datacardsDir}/diphoton_combine_${mass}_${scenario}_EBEE_2017.txt \
    ${datacardsDir}/diphoton_combine_${mass}_${scenario}_EBEB_2018.txt \
    ${datacardsDir}/diphoton_combine_${mass}_${scenario}_EBEE_2018.txt \
    > ${datacardsDir}/diphoton_combine_${mass}_${scenario}_fullRun2.txt;
echo ${datacardfile}

# ############################## Combine Limit ##############################
echo "########## Run AsymptoticLimits ##########"
finalResults="finalResults_${signame}_${coupling}_${mass}.txt"

combine -M AsymptoticLimits -s -1 -d $datacardfile --X-rtd MINIMIZER_freezeDisassociatedParams -n ${year}_${signal}_${coupling} > results

export obs=`cat results  | grep  "Observed Limit:" | awk '{print $5}'`
export expM2s=`cat results  | grep  "Expected  2.5%:" | awk '{print $5}'`
export expM1s=`cat results  | grep  "Expected 16.0%:" | awk '{print $5}'`
export exp=`cat results  | grep  "Expected 50.0%:" | awk '{print $5}'`
export expP1s=`cat results  | grep  "Expected 84.0%:" | awk '{print $5}'`
export expP2s=`cat results  | grep  "Expected 97.5%:" | awk '{print $5}'`

echo $mass $obs $expM2s $expM1s $exp $expP1s $expP2s
echo $mass $obs $expM2s $expM1s $exp $expP1s $expP2s > ${finalResults}

# ############################## Combine local pvalue ##############################
echo "########## Run Combine local pvalue ##########"
combine -d ${datacardfile} -M Significance --signif --pval --cminDefaultMinimizerType=Minuit2 -n Observed > results_pvalue
rm higgsCombine*.root

export pvalue=`cat results_pvalue  | grep  "p-value of background:" | awk '{print $4}'`

echo $mass $pvalue
echo $mass $pvalue >> ${finalResults}

# ############################## Combine local zvalue ##############################
echo "########## Run Combine local zvalue ##########"
combine -d ${datacardfile} -M Significance --signif --cminDefaultMinimizerType=Minuit2 -n Observed > results_zvalue
rm higgsCombine*.root

export zvalue=`cat results_zvalue  | grep  "Significance:" | awk '{print $2}'`

echo $mass $zvalue
echo $mass $zvalue >> ${finalResults}

############################## Combine Global zvalue ##############################
echo "########## Run Global Significance ##########"
combine -d ${datacardfile} -M Significance --cminDefaultMinimizerType=Minuit2 -n Observed_global --toysFile ${toysfile} -t 1000 > results_global_zvalue
rm higgsCombine*.root

export global_zvalue=`cat results_global_zvalue  | grep  "Significance:" | awk '{print $2}'`

echo $mass $global_zvalue
echo $mass $global_zvalue >> ${finalResults}
