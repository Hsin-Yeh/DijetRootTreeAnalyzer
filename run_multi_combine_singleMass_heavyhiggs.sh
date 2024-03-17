#!/bin/bash

export coupling=$1
export mass=$2
echo ""
echo "########## Run Limit script for Heavyhiggs ${coupling} ${mass}GeV ##########"
echo ""
#################### Constants ##########EEEEEEEEEE
yearlist=("2016" "2017" "2018")
# Cats
catlist=("EBEB" "EBEE")
# method
signame="heavyhiggs"
signal_LongName="GluGluSpin0ToGammaGamma_W"

#################### Constants ####################
# Cats
export catlist=("EBEB" "EBEE")

# method
signame="heavyhiggs"
signal_LongName="GluGluSpin0ToGammaGamma_W"

#################### Paths ####################
DijetRootTreeAnalyzer="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/"
DijetShapeInterpolator="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/DijetShapeInterpolator/"
diphoton="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/"

inputDataDir="${DijetRootTreeAnalyzer}/output/InputShapes_data_backup"
configFile="${DijetRootTreeAnalyzer}/config/diphotons_500GeV.config"
InterpolateShapePath="${DijetShapeInterpolator}/genFiducial/"
bkgFitResultsPath="${DijetRootTreeAnalyzer}/datacards/multi"
SignalNormFile="${diphoton}/SignalNorm_Splines_genFiducial.txt"
datacardsDir="datacards/${signame}"
# toysfile created by: combine -M GenerateOnly datacards/diphoton_combine_1300_DiPhotons_4550_fullRun2.txt -n _bkgOnly --toysFrequentist -t 10000 --saveToys --expectSignal=0
toysfile="${DijetRootTreeAnalyzer}/ParallelForLimits/higgsCombine_Generate_bkgOnly.root"

#################### Run flags ####################
export binnedFit_flag=false
export writeDataCard_flag=true
export combineCard_flag=true
export combineLimit_flag=true

#################### mkdirs ####################
mkdir -p ${datacardsDir}
mkdir -p FinalResults

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
        export datacard_configfile="${DijetRootTreeAnalyzer}/config/diphotons_bias_${year}_pdf_index_wopip_wopil.config"
        python ${DijetRootTreeAnalyzer}/python/WriteDataCard.py --multi -m gg --mass ${mass} ${inputDataDir}/InputShapes_data_${cat}_${year}.root \
            -i ${bkgFitResultsPath}/FitResults_${box}.root --lumi ${lumi} -c ${datacard_configfile} -b ${box} --year ${year} \
            --SigNorm ${SignalNormFile} \
            --eneScStatUp    ${InterpolateShapePath}/ResonanceShapes_InputShapes_${signal_LongName}_${coupling}_${cat}_${year}_energyScaleStatUp.root   \
            --eneScStatDown  ${InterpolateShapePath}/ResonanceShapes_InputShapes_${signal_LongName}_${coupling}_${cat}_${year}_energyScaleStatDown.root \
            --eneScSystUp    ${InterpolateShapePath}/ResonanceShapes_InputShapes_${signal_LongName}_${coupling}_${cat}_${year}_energyScaleSystUp.root   \
            --eneScSystDown  ${InterpolateShapePath}/ResonanceShapes_InputShapes_${signal_LongName}_${coupling}_${cat}_${year}_energyScaleSystDown.root \
            --eneScGainUp    ${InterpolateShapePath}/ResonanceShapes_InputShapes_${signal_LongName}_${coupling}_${cat}_${year}_energyScaleGainUp.root   \
            --eneScGainDown  ${InterpolateShapePath}/ResonanceShapes_InputShapes_${signal_LongName}_${coupling}_${cat}_${year}_energyScaleGainDown.root \
            --eneScSigmaUp   ${InterpolateShapePath}/ResonanceShapes_InputShapes_${signal_LongName}_${coupling}_${cat}_${year}_energySigmaUp.root       \
            --eneScSigmaDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_${signal_LongName}_${coupling}_${cat}_${year}_energySigmaDown.root     \
            --SFScaleUp      ${InterpolateShapePath}/ResonanceShapes_InputShapes_${signal_LongName}_${coupling}_${cat}_${year}_SFScaleUp.root           \
            --SFScaleDown    ${InterpolateShapePath}/ResonanceShapes_InputShapes_${signal_LongName}_${coupling}_${cat}_${year}_SFScaleDown.root         \
            --PUScaleUp      ${InterpolateShapePath}/ResonanceShapes_InputShapes_${signal_LongName}_${coupling}_${cat}_${year}_PUScaleUp.root           \
            --PUScaleDown    ${InterpolateShapePath}/ResonanceShapes_InputShapes_${signal_LongName}_${coupling}_${cat}_${year}_PUScaleDown.root         \
            ${InterpolateShapePath}/ResonanceShapes_InputShapes_${signal_LongName}_${coupling}_${cat}_${year}.root;
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
