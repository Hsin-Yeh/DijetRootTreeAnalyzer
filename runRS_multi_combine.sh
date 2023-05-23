#!/bin/bash

# ./runRS_multi_combine.sh 2016 kMpl001
# ./runRS_multi_combine.sh 2016 kMpl01
# ./runRS_multi_combine.sh 2016 kMpl02
# ./runRS_multi_combine.sh 2017 kMpl001
# ./runRS_multi_combine.sh 2017 kMpl01
# ./runRS_multi_combine.sh 2017 kMpl02
# ./runRS_multi_combine.sh 2018 kMpl001
# ./runRS_multi_combine.sh 2018 kMpl01
# ./runRS_multi_combine.sh 2018 kMpl02

export year=$1
export coupling=$2

export version="2023-05-23"
export method="full"
export massInterval=10

# Paths
export InterpolateShapePath="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/DijetShapeInterpolator/${method}"
export configFile="config/diphotons_500GeV.config"
export bkgFitResultsPath="datacards/multi"
export datacardsDir="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/datacards/multi"
export SignalNormFile="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/SignalNorm_Splines_${method}.txt"
export datacard_configfile="config/diphotons_bias_${year}_pdf_index_wopip.config"
if [[ ${year} == "2017" ]]; then
    export datacard_configfile="config/diphotons_bias_2017_pdf_index_wopip_wopil.config"
fi

# Run flags
export binnedFit_flag=false
export writeDataCard_flag=true
export combineCard_flag=true
export combineLimit_flag=true

# Constants
# Cats
export catlist=("EBEB" "EBEE")
# Lumi
export lumi=35.9
if [[ ${year} == "2017" ]]; then
    export lumi=41.527
elif [[ ${year} == "2018" ]]; then
    export lumi=59.670
fi
# Mass
export masslist=(600 613 621 629 637 645 653 662 670 679 687 696 705 714 723 732 741 751 760 770 779 789 799 809 820 830 840 851 862 872 883 894 906 917 929 940 952 964 976 988 1001 1013 1026 1038 1051 1064 1078 1091 1105 1119 1132 1147 1161 1175 1190 1205 1219 1235 1250 1265 1281 1297 1313 1329 1346 1362 1379 1396 1413 1431 1449 1466 1485 1503 1521 1540 1559 1578 1598 1617 1637 1657 1678 1698 1719 1740 1762 1783 1805 1827 1850 1873 1895 1919 1942 1966 1990 2014 2039 2064 2089 2115 2141 2167 2193 2220 2247 2275 2303 2331 2359 2388 2417 2447 2477 2507 2537 2568 2600 2631 2663 2696 2729 2762 2795 2830 2864 2899 2934 2970 3006 3042 3079 3117 3155 3193 3232 3271 3311 3351 3392 3433 3475 3517 3560 3603 3647 3691 3736 3781 3827 3873 3920 3968 4016 4065 4114 4164 4214 4265 4317 4369 4422 4476 4530 4585 4640 4696 4753 4811 4869 4928 4987 5000)
if [[ ${coupling} == "kMpl01" ]]; then
    masslist=(600 611 622 634 645 657 669 681 694 707 719 732 746 759 773 787 801 816 830 845 860 876 892 908 924 940 957 974 992 1009 1027 1046 1064 1083 1102 1122 1142 1162 1183 1204 1225 1247 1269 1291 1314 1337 1361 1385 1409 1434 1459 1485 1511 1537 1564 1592 1619 1648 1677 1706 1736 1766 1797 1828 1860 1893 1926 1959 1993 2028 2064 2099 2136 2173 2211 2249 2288 2328 2368 2410 2451 2494 2537 2581 2626 2671 2718 2765 2812 2861 2910 2961 3012 3064 3117 3171 3225 3281 3338 3395 3454 3513 3574 3636 3698 3762 3827 3893 3960 4028 4097 4167 4239 4312 4386 4462 4538 4616 4696 4776 4858 4942 5027 5113 5201 5290 5381 5473 5567 5662 5759 5858 5958 6061 6164 6270 6377 6487 6598 6711 6826 6943 7000)
elif [[ ${coupling} == "kMpl02" ]]; then
    masslist=(600 625 653 683 713 745 778 812 848 885 924 964 1005 1049 1094 1141 1190 1241 1293 1348 1405 1465 1527 1591 1658 1727 1800 1875 1953 2034 2119 2207 2298 2393 2492 2595 2702 2813 2929 3050 3175 3305 3440 3581 3728 3880 4038 4203 4374 4553 4738 4931 5131 5339 5556 5782 6016 6260 6514 6777 7000)
fi
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
    # Remember for me the yield was initially normalized to 1000/pb. So, here lumi 35.9 (-d ${datacardsDir}/2016/${box} omitted)
    for mass in "${masslist[@]}"; do
        echo ${mass}
        for cat in "${catlist[@]}"; do
            box="DiPhotons_${coupling}_${cat}_${year}"
            echo ${box}
            mkdir -p ${datacardsDir}/${method}/${year}/${box}
            python python/WriteDataCard.py --multi -m gg --mass ${mass} output/InputShapes_data_${cat}_${year}.root -i ${bkgFitResultsPath}/FitResults_${box}.root --lumi ${lumi} -c ${datacard_configfile} -b ${box} --year ${year} \
                --SigNorm ${SignalNormFile} \
                --eneScStatUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coupling}_${cat}_${year}_energyScaleStatUp.root \
                --eneScStatDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coupling}_${cat}_${year}_energyScaleStatDown.root \
                --eneScSystUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coupling}_${cat}_${year}_energyScaleSystUp.root \
                --eneScSystDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coupling}_${cat}_${year}_energyScaleSystDown.root \
                --eneScGainUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coupling}_${cat}_${year}_energyScaleGainUp.root \
                --eneScGainDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coupling}_${cat}_${year}_energyScaleGainDown.root \
                --eneScSigmaUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coupling}_${cat}_${year}_energySigmaUp.root \
                --eneScSigmaDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coupling}_${cat}_${year}_energySigmaDown.root \
                --SFScaleUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coupling}_${cat}_${year}_SFScaleUp.root \
                --SFScaleDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coupling}_${cat}_${year}_SFScaleDown.root \
                --PUScaleUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coupling}_${cat}_${year}_PUScaleUp.root \
                --PUScaleDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coupling}_${cat}_${year}_PUScaleDown.root \
                ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coupling}_${cat}_${year}.root;
            mv diphoton_combine_${mass}_${box}.* ${datacardsDir}/${method}/${year}/${box}/.
        done
    done
fi
# ############################## Combine cards ##############################

if $combineCard_flag; then
    echo ${year}
    cd ${datacardsDir}/${method}/${year}
    scenario="DiPhotons_${coup}"
    echo ${scenario}
    for mass in "${masslist[@]}"; do
        echo ${mass}
        combineCards.py \
            ${datacardsDir}/${method}/${year}/${scenario}_EBEB_${year}/diphoton_combine_${mass}_${scenario}_EBEB_${year}.txt \
            ${datacardsDir}/${method}/${year}/${scenario}_EBEE_${year}/diphoton_combine_${mass}_${scenario}_EBEE_${year}.txt \
            > diphoton_combine_${mass}_${scenario}_${year}.txt
    done
fi

# ############################## Combine Limit ##############################

if $combineLimit_flag; then
    export mainpath="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/FinalResults"
    cd /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/FinalResults/

    ./loopAllMassPoints.csh ${year} grav ${coupling} ${method} ${datacardsDir} ${version}
fi
