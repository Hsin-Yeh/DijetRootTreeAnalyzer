#!/usr/bin/env sh

coupling=14
mass=1320

echo ""
echo "########## Run Limit script for RSGraviton 0.014% 1320 GeV ##########"
echo ""
#################### Constants ##########EEEEEEEEEE
yearlist=("2016" "2017" "2018")
# Cats
catlist=("EBEB" "EBEE")
signal="grav"
signal_LongName="RSGravitonToGammaGamma"

#################### Paths ####################
eosDir="/eos/cms/store/group/phys_exotica/diphoton/fullRun2/hsinyeh/CombineExample"
signalDir="${eosDir}/signal"
dataDir="${eosDir}/data"
SignalNormFile="${eosDir}/SignalNorm_Splines_full_multiWidth.txt"
bkgFitResultsDir="${eosDir}/bkgFitResults/"
configDir="../config"
pythonDir="../python"
datacardsDir="datacards/${signal}"
# toysfile created by: combine -M GenerateOnly datacards/diphoton_combine_1300_DiPhotons_4550_fullRun2.txt -n _bkgOnly --toysFrequentist -t 10000 --saveToys --expectSignal=0
toysfile="${eosDir}/ParallelForLimits/higgsCombine_Generate_bkgOnly.root"


#################### mkdirs ####################
mkdir -p ${datacardsDir}
mkdir -p FinalResults

############################## WriteDataCard.py grav ##############################
# The yield was initially normalized to 1000/pb.
echo "########## Write Datacards... ##########"
for year in "${yearlist[@]}"; do
    # Lumi
    lumi=35.9
    if [[ ${year} == "2017" ]]; then
        lumi=41.527
    elif [[ ${year} == "2018" ]]; then
        lumi=59.670
    fi
    for cat in "${catlist[@]}"; do
        box="DiPhotons_${coupling}_${cat}_${year}"
        echo ${year} ${box}
        datacard_configfile="${configDir}/diphotons_bias_${year}_pdf_index_wopip_wopil_multiWidth.config"
        python ${pythonDir}/WriteDataCard.py --multi -m gg --mass ${mass} ${dataDir}/InputShapes_data_${cat}_${year}.root \
            -i ${bkgFitResultsDir}/FitResults_${box}.root --lumi ${lumi} -c ${datacard_configfile} -b ${box} --year ${year} \
            --SigNorm ${SignalNormFile} \
            --eneScStatUp    ${signalDir}/ResonanceShapes_InputShapes_${signal_LongName}_${coupling}_${cat}_${year}_energyScaleStatUp.root   \
            --eneScStatDown  ${signalDir}/ResonanceShapes_InputShapes_${signal_LongName}_${coupling}_${cat}_${year}_energyScaleStatDown.root \
            --eneScSystUp    ${signalDir}/ResonanceShapes_InputShapes_${signal_LongName}_${coupling}_${cat}_${year}_energyScaleSystUp.root   \
            --eneScSystDown  ${signalDir}/ResonanceShapes_InputShapes_${signal_LongName}_${coupling}_${cat}_${year}_energyScaleSystDown.root \
            --eneScGainUp    ${signalDir}/ResonanceShapes_InputShapes_${signal_LongName}_${coupling}_${cat}_${year}_energyScaleGainUp.root   \
            --eneScGainDown  ${signalDir}/ResonanceShapes_InputShapes_${signal_LongName}_${coupling}_${cat}_${year}_energyScaleGainDown.root \
            --eneScSigmaUp   ${signalDir}/ResonanceShapes_InputShapes_${signal_LongName}_${coupling}_${cat}_${year}_energySigmaUp.root       \
            --eneScSigmaDown ${signalDir}/ResonanceShapes_InputShapes_${signal_LongName}_${coupling}_${cat}_${year}_energySigmaDown.root     \
            --SFScaleUp      ${signalDir}/ResonanceShapes_InputShapes_${signal_LongName}_${coupling}_${cat}_${year}_SFScaleUp.root           \
            --SFScaleDown    ${signalDir}/ResonanceShapes_InputShapes_${signal_LongName}_${coupling}_${cat}_${year}_SFScaleDown.root         \
            --PUScaleUp      ${signalDir}/ResonanceShapes_InputShapes_${signal_LongName}_${coupling}_${cat}_${year}_PUScaleUp.root           \
            --PUScaleDown    ${signalDir}/ResonanceShapes_InputShapes_${signal_LongName}_${coupling}_${cat}_${year}_PUScaleDown.root         \
            ${signalDir}/ResonanceShapes_InputShapes_${signal_LongName}_${coupling}_${cat}_${year}.root;
        mv diphoton_combine_${mass}_${box}.* ${datacardsDir}/.
    done
done
# ############################## Combine cards for all years ##############################
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
echo "Combined card for all years: ${datacardfile}"

finalResults="FinalResults/finalResults_${signal}_${coupling}_${mass}.txt"
echo "Final results file: ${finalResults}"
# ############################## Combine Limit ##############################
echo "########## Run AsymptoticLimits ##########"

combine -M AsymptoticLimits -s -1 -d $datacardfile --X-rtd MINIMIZER_freezeDisassociatedParams -n ${year}_${signal}_${coupling} > results

obs=`cat results  | grep  "Observed Limit:" | awk '{print $5}'`
expM2s=`cat results  | grep  "Expected  2.5%:" | awk '{print $5}'`
expM1s=`cat results  | grep  "Expected 16.0%:" | awk '{print $5}'`
exp=`cat results  | grep  "Expected 50.0%:" | awk '{print $5}'`
expP1s=`cat results  | grep  "Expected 84.0%:" | awk '{print $5}'`
expP2s=`cat results  | grep  "Expected 97.5%:" | awk '{print $5}'`

echo $mass $obs $expM2s $expM1s $exp $expP1s $expP2s
echo $mass $obs $expM2s $expM1s $exp $expP1s $expP2s > ${finalResults}

# ############################## Combine local pvalue ##############################
echo "########## Run pvalue ##########"
combine -d ${datacardfile} -M Significance --pval --cminDefaultMinimizerType=Minuit2 -n Observed_pvalue > results_pvalue
rm higgsCombine*.root

pvalue=`cat results_pvalue  | grep  "p-value of background:" | awk '{print $4}'`

echo $mass $pvalue
echo $mass $pvalue >> ${finalResults}

# ############################## Combine zvalue ##############################
echo "########## Run zvalue ##########"
combine -d ${datacardfile} -M Significance --cminDefaultMinimizerType=Minuit2 -n Observed_zvalue > results_zvalue
rm higgsCombine*.root

zvalue=`cat results_zvalue  | grep  "Significance:" | awk '{print $2}'`

echo $mass $zvalue
echo $mass $zvalue >> ${finalResults}

# ############################## Combine Global zvalue ##############################
echo "########## Run Global Significance ##########"
combine -d ${datacardfile} -M Significance --cminDefaultMinimizerType=Minuit2 -n Observed_global --toysFile ${toysfile} -t 1000 > results_global_zvalue
rm higgsCombine*.root

global_zvalue=`cat results_global_zvalue  | grep  "Significance:" | awk '{print $2}'`

echo $mass $global_zvalue
echo $mass $global_zvalue >> ${finalResults}
