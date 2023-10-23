#!/bin/bash

export coupling=$1
export mass=$2

#################### Constants ##########EEEEEEEEEE
yearlist=("2016" "2017" "2018")
# Cats
catlist=("EBEB" "EBEE")
# method
export method="full"
export signal="grav"
export signal_LongName="RSGravitonToGammaGamma"
if [[ ${coupling} == "0p014" || ${coupling} == "1p4" || ${coupling} == "5p6" ]]; then
    export method="genFiducial"
    export signal="heavyhiggs"
    export signal_LongName="GluGluSpin0ToGammaGamma_W"
fi

#################### Paths ####################
export DijetRootTreeAnalyzer="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/"
export DijetShapeInterpolator="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/DijetShapeInterpolator/"
export diphoton="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/"

export inputDataDir="${DijetRootTreeAnalyzer}/output/InputShapes_data_backup"
export configFile="${DijetRootTreeAnalyzer}/config/diphotons_500GeV.config"
export InterpolateShapePath="${DijetShapeInterpolator}/full_backup/width/"
export bkgFitResultsPath="${DijetRootTreeAnalyzer}/datacards/multiWidth/"
export SignalNormFile="${diphoton}/SignalNorm_Splines_full_multiWidth.txt"

#################### mkdirs ####################
mkdir -p signal_shapes/extraShape
mkdir -p signal_shapes/width_interpolated_shapes
mkdir datacards
mkdir FinalResults

#################### Get Width Interpolated shapes ####################
# Nom
for year in "${yearlist[@]}"; do
    echo ${year}
    for cat in "${catlist[@]}"; do
        echo ${cat}
        narrow_file="${InterpolateShapePath}/inputs/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_kMpl001_${cat}_${year}_ratio.root"
        medium_file="${InterpolateShapePath}/inputs/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_kMpl01_${cat}_${year}_ratio.root"
        wide_file="${InterpolateShapePath}/inputs/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_kMpl02_${cat}_${year}_ratio.root"
        filename="InputShapes_RSGravitonToGammaGamma_${cat}_${year}"
        python ${DijetShapeInterpolator}/extractShapes_width.py -n ${narrow_file} -m ${medium_file} -w ${wide_file} --mass ${mass} > signal_shapes/${filename}_${mass}GeV.py
        python ${DijetShapeInterpolator}/getResonanceShapes_width.py -i signal_shapes/${filename}_${mass}GeV.py -m ${mass} -f gg -o signal_shapes/width_${filename}_${mass}GeV.root
    done
done

# Systematics
for year in "${yearlist[@]}"; do
    echo ${year}
    for cat in "${catlist[@]}"; do
        echo ${cat}
        for systematics in {"energyScaleStatUp","energyScaleSystUp","energyScaleGainUp","energySigmaUp",
                            "energyScaleStatDown","energyScaleSystDown","energyScaleGainDown","energySigmaDown","SFScaleUp","SFScaleDown","PUScaleUp","PUScaleDown"}; do
            echo ${systematics}
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

############################## WriteDataCard.py grav ##############################

# The yield was initially normalized to 1000/pb.
for year in "${yearlist[@]}"; do
    echo ${year}
    # Lumi
    export lumi=35.9
    if [[ ${year} == "2017" ]]; then
        export lumi=41.527
    elif [[ ${year} == "2018" ]]; then
        export lumi=59.670
    fi
    for cat in "${catlist[@]}"; do
        box="DiPhotons_${coupling}_${cat}_${year}"
        echo ${box}
        export datacard_configfile="${DijetRootTreeAnalyzer}/config/diphotons_bias_${year}_pdf_index_wopip_wopil.config"
        python python/WriteDataCard.py --multi -m gg --mass ${mass} output/InputShapes_data_${cat}_${year}.root \
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
scenario="DiPhotons_${coupling}"
combineCards.py datacards/diphoton_combine_${mass}_${scenario}_EBEB_2016.txt \
    datacards/diphoton_combine_${mass}_${scenario}_EBEE_2016.txt \
    datacards/diphoton_combine_${mass}_${scenario}_EBEB_2017.txt \
    datacards/diphoton_combine_${mass}_${scenario}_EBEE_2017.txt \
    datacards/diphoton_combine_${mass}_${scenario}_EBEB_2018.txt \
    datacards/diphoton_combine_${mass}_${scenario}_EBEE_2018.txt \
    > datacards/diphoton_combine_${mass}_${scenario}_fullRun2.txt;

# ############################## Combine Limit ##############################

datacardfile="datacards/diphoton_combine_${mass}_${scenario}_fullRun2.txt"
finalResults="finalResults_${signal}_${coupling}_${mass}.txt"

combine -M AsymptoticLimits -s -1 -d $datacardfile --X-rtd MINIMIZER_freezeDisassociatedParams -n ${year}_${signal}_${coupling} > results

export obs=`cat results  | grep  "Observed Limit:" | awk '{print $5}'`
export expM2s=`cat results  | grep  "Expected  2.5%:" | awk '{print $5}'`
export expM1s=`cat results  | grep  "Expected 16.0%:" | awk '{print $5}'`
export exp=`cat results  | grep  "Expected 50.0%:" | awk '{print $5}'`
export expP1s=`cat results  | grep  "Expected 84.0%:" | awk '{print $5}'`
export expP2s=`cat results  | grep  "Expected 97.5%:" | awk '{print $5}'`

echo $mass $obs $expM2s $expM1s $exp $expP1s $expP2s
echo $mass $obs $expM2s $expM1s $exp $expP1s $expP2s >> ${finalResults}

# ############################## Combine Significance ##############################

combine -d ${datacardfile} -M Significance --signif --pval --cminDefaultMinimizerType=Minuit2 -n Observed > results_pvalue
rm higgsCombine*.root

export pvalue=`cat results_pvalue  | grep  "p-value of background:" | awk '{print $4}'`

echo $mass $pvalue
echo $mass $pvalue >> ${finalResults}
