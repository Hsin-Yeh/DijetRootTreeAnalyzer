#!/bin/bash

export coupling=$1
export mass=$2
echo ""
echo "########## Run Limit script for RSGraviton ${coupling} ${mass}GeV ##########"
echo ""
#################### Constants ##########EEEEEEEEEE
yearlist=("2016" "2017" "2018")
# Cats
catlist=("EBEB" "EBEE")
# method
method="full"
signal="grav"
signal_LongName="RSGravitonToGammaGamma"

#################### Paths ####################
DijetRootTreeAnalyzer="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/"
DijetShapeInterpolator="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/DijetShapeInterpolator/"
diphoton="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/"

inputDataDir="${DijetRootTreeAnalyzer}/output/InputShapes_data_backup"
configFile="${DijetRootTreeAnalyzer}/config/diphotons_500GeV.config"
InterpolateShapePath="${DijetShapeInterpolator}/full_backup/width/"
bkgFitResultsPath="${DijetRootTreeAnalyzer}/datacards/multiWidth/"
SignalNormFile_input="${diphoton}/SignalNorm_Splines_full.txt"
SignalNormFile="SignalNorm_Splines_full_multiWidth.txt"
# toysfile created by: combine -M GenerateOnly datacards/diphoton_combine_1300_DiPhotons_4550_fullRun2.txt -n _bkgOnly --toysFrequentist -t 100 --saveToys --expectSignal=0
toysfile="${DijetRootTreeAnalyzer}/ParallelForLimits/higgsCombine_Generate_bkgOnly.root"



#################### mkdirs ####################
mkdir -p signal_shapes
mkdir -p datacards
mkdir -p FinalResults

#################### Get Width Interpolated shapes ####################

# Nom
echo "########## Get Interpolated Shapes... ##########"
for year in "${yearlist[@]}"; do
    for cat in "${catlist[@]}"; do
        echo ${year} ${cat}
        narrow_file="${InterpolateShapePath}/inputs/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_kMpl001_${cat}_${year}_ratio.root"
        medium_file="${InterpolateShapePath}/inputs/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_kMpl01_${cat}_${year}_ratio.root"
        wide_file="${InterpolateShapePath}/inputs/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_kMpl02_${cat}_${year}_ratio.root"
        filename="InputShapes_RSGravitonToGammaGamma_${cat}_${year}"
        python ${DijetShapeInterpolator}/extractShapes_width.py -n ${narrow_file} -m ${medium_file} -w ${wide_file} --mass ${mass} > signal_shapes/${filename}_${mass}GeV.py
        python ${DijetShapeInterpolator}/getResonanceShapes_width.py -i signal_shapes/${filename}_${mass}GeV.py -m ${mass} -f gg -o signal_shapes/width_${filename}_${mass}GeV.root
    done
done

# Systematics
echo "########## Get Interpolated Systematic Shapes... ##########"
for year in "${yearlist[@]}"; do
    for cat in "${catlist[@]}"; do
        for systematics in {"energyScaleStatUp","energyScaleSystUp","energyScaleGainUp","energySigmaUp","energyScaleStatDown","energyScaleSystDown","energyScaleGainDown","energySigmaDown","SFScaleUp","SFScaleDown","PUScaleUp","PUScaleDown"}; do
            echo ${year} ${cat} ${systematics}
            narrow_file="${InterpolateShapePath}/inputs/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_kMpl001_${cat}_${year}_${systematics}_ratio.root"
            medium_file="${InterpolateShapePath}/inputs/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_kMpl01_${cat}_${year}_${systematics}_ratio.root"
            wide_file="${InterpolateShapePath}/inputs/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_kMpl02_${cat}_${year}_${systematics}_ratio.root"
            filename="InputShapes_RSGravitonToGammaGamma_${cat}_${year}_${systematics}"
            python ${DijetShapeInterpolator}/extractShapes_width.py -n ${narrow_file} -m ${medium_file} -w ${wide_file} --mass ${mass} > signal_shapes/${filename}_${mass}GeV.py
            python ${DijetShapeInterpolator}/getResonanceShapes_width.py -i signal_shapes/${filename}_${mass}GeV.py -m ${mass} -f gg -o signal_shapes/width_${filename}_${mass}GeV.root
        done
    done
done
# Merge
python ${DijetShapeInterpolator}/Merge_width_interpolation.py --mass ${mass} --width ${coupling}

############################## Signal Norm ##############################
echo "########## Calculate Signal Norm... ##########"
python ${DijetRootTreeAnalyzer}/python/signalNorm_interpolate.py -i ${SignalNormFile_input} --mass ${mass} --width ${coupling} -o ${SignalNormFile}

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
        export datacard_configfile="${DijetRootTreeAnalyzer}/config/diphotons_bias_${year}_pdf_index_wopip_wopil_multiWidth.config"
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
        mv diphoton_combine_${mass}_${box}.* datacards/.
    done
done
# ############################## Combine cards ##############################
echo "########## Combine Datacards ##########"
scenario="DiPhotons_${coupling}"
datacardfile="datacards/diphoton_combine_${mass}_${scenario}_fullRun2.txt"
combineCards.py datacards/diphoton_combine_${mass}_${scenario}_EBEB_2016.txt \
    datacards/diphoton_combine_${mass}_${scenario}_EBEE_2016.txt \
    datacards/diphoton_combine_${mass}_${scenario}_EBEB_2017.txt \
    datacards/diphoton_combine_${mass}_${scenario}_EBEE_2017.txt \
    datacards/diphoton_combine_${mass}_${scenario}_EBEB_2018.txt \
    datacards/diphoton_combine_${mass}_${scenario}_EBEE_2018.txt \
    > datacards/diphoton_combine_${mass}_${scenario}_fullRun2.txt;
echo ${datacardfile}

# ############################## Combine Limit ##############################
echo "########## Run AsymptoticLimits ##########"
finalResults="finalResults_${signal}_${coupling}_${mass}.txt"

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
echo "########## Run Significance ##########"
combine -d ${datacardfile} -M Significance --pval --cminDefaultMinimizerType=Minuit2 -n Observed_pvalue > results_pvalue
rm higgsCombine*.root

export pvalue=`cat results_pvalue  | grep  "p-value of background:" | awk '{print $4}'`

echo $mass $pvalue
echo $mass $pvalue >> ${finalResults}

# ############################## Combine zvalue ##############################
echo "########## Run Significance ##########"
combine -d ${datacardfile} -M Significance --cminDefaultMinimizerType=Minuit2 -n Observed_zvalue > results_zvalue
rm higgsCombine*.root

export zvalue=`cat results_zvalue  | grep  "Significance:" | awk '{print $2}'`

echo $mass $zvalue
echo $mass $zvalue >> ${finalResults}

# ############################## Combine Global zvalue ##############################
echo "########## Run Global Significance ##########"
combine -d ${datacardfile} -M Significance --cminDefaultMinimizerType=Minuit2 -n Observed_global --toysFile ${toysfile} -t 10000 > results_global_zvalue
rm higgsCombine*.root

export global_zvalue=`cat results_global_zvalue  | grep  "Significance:" | awk '{print $2}'`

echo $mass $global_zvalue
echo $mass $global_zvalue >> ${finalResults}
