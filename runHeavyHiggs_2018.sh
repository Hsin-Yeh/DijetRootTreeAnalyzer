#!/usr/bin/env sh

# ./runHeavyHiggs.sh
# export method="full"
export method="genFiducial"
export InterpolateShapePath="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/DijetShapeInterpolator/${method}"
export configFile="config/diphotons_500GeV.config"
export bkgFitResultsPath="test_directory"
export SignalNormFile="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/SignalNorm_genFiducial.txt"
export massInterval=100

############################## fit nominal bkg model ##############################

# mkdir -p ${bkgFitResultsPath}
# cd /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer

# # #2018 Lumi 59670
# for coup in {"0p014","1p4","5p6"}; do echo $coup; for cat in {"EBEB","EBEE"}; do echo $cat; python python/BinnedFit.py -c config/diphotons_dijet.config -l 59670 -b DiPhotons_${coup}_${cat} -d ${bkgFitResultsPath} --fit-spectrum --plot-region Low --coup $coup --cat $cat --year 2018 output/InputShapes_data_${cat}_2018.root; done; done;

# ############################## WriteDataCard.py heavyhiggs ##############################
# #
# # 2018
# # Remember for me the yield was initially normalized to 1000/pb. So, here lumi 41.527 (-d test_directory/2018/${box} omitted)
# # for box in {"DiPhotons_0p014_EBEB","DiPhotons_0p014_EBEE","DiPhotons_1p4_EBEB","DiPhotons_1p4_EBEE","DiPhotons_5p6_EBEB","DiPhotons_5p6_EBEE"}; do
# for box in {"DiPhotons_1p4_EBEB","DiPhotons_1p4_EBEE","DiPhotons_5p6_EBEB","DiPhotons_5p6_EBEE"}; do
#     echo ${box};
#     cat=`echo ${box}| cut -d"_" -f 3`;
#     coup=`echo ${box}| cut -d"_" -f 2`;
#     mkdir -p test_directory/${method}/2018/${box};
#     export masslist=(600 613 621 629 637 645 653 662 670 679 687 696 705 714 723 732 741 751 760 770 779 789 799 809 820 830 840 851 862 872 883 894 906 917 929 940 952 964 976 988 1001 1013 1026 1038 1051 1064 1078 1091 1105 1119 1132 1147 1161 1175 1190 1205 1219 1235 1250 1265 1281 1297 1313 1329 1346 1362 1379 1396 1413 1431 1449 1466 1485 1503 1521 1540 1559 1578 1598 1617 1637 1657 1678 1698 1719 1740 1762 1783 1805 1827 1850 1873 1895 1919 1942 1966 1990 2014 2039 2064 2089 2115 2141 2167 2193 2220 2247 2275 2303 2331 2359 2388 2417 2447 2477 2507 2537 2568 2600 2631 2663 2696 2729 2762 2795 2830 2864 2899 2934 2970 3006 3042 3079 3117 3155 3193 3232 3271 3311 3351 3392 3433 3475 3517 3560 3603 3647 3691 3736 3781 3827 3873 3920 3968 4016 4065 4114 4164 4214 4265 4317 4369 4422 4476 4530 4585 4640 4696 4753 4811 4869 4928 4987 5000)
#     if [[ ${coup} == "1p4" ]]; then
#     masslist=(600 611 622 634 645 657 669 681 694 707 719 732 746 759 773 787 801 816 830 845 860 876 892 908 924 940 957 974 992 1009 1027 1046 1064 1083 1102 1122 1142 1162 1183 1204 1225 1247 1269 1291 1314 1337 1361 1385 1409 1434 1459 1485 1511 1537 1564 1592 1619 1648 1677 1706 1736 1766 1797 1828 1860 1893 1926 1959 1993 2028 2064 2099 2136 2173 2211 2249 2288 2328 2368 2410 2451 2494 2537 2581 2626 2671 2718 2765 2812 2861 2910 2961 3012 3064 3117 3171 3225 3281 3338 3395 3454 3513 3574 3636 3698 3762 3827 3893 3960 4028 4097 4167 4239 4312 4386 4462 4538 4616 4696 4776 4858 4942 5000)
#     elif [[ ${coup} == "5p6" ]]; then
#     masslist=(600 625 653 683 713 745 778 812 848 885 924 964 1005 1049 1094 1141 1190 1241 1293 1348 1405 1465 1527 1591 1658 1727 1800 1875 1953 2034 2119 2207 2298 2393 2492 2595 2702 2813 2929 3050 3175 3305 3440 3581 3728 3880 4038 4203 4374 4553 4738 4931 5000)
#     fi
#     for mass in "${masslist[@]}"; do
#         python python/WriteDataCard.py -m gg --mass ${mass} output/InputShapes_data_${cat}_2018.root -i ${bkgFitResultsPath}/FitResults_${box}_2018.root --lumi 59.670 -c ${configFile} -b ${box} --year 2018 --SigNorm ${SignalNormFile} --eneScStatUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2018_energyScaleStatUp.root   --eneScStatDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2018_energyScaleStatDown.root --eneScSystUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2018_energyScaleSystUp.root   --eneScSystDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2018_energyScaleSystDown.root --eneScGainUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2018_energyScaleGainUp.root   --eneScGainDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2018_energyScaleGainDown.root --eneScSigmaUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2018_energySigmaUp.root       --eneScSigmaDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2018_energySigmaDown.root     --SFUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2018_SFUp.root                --SFDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2018_SFDown.root              --PuUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2018_PuUp.root                --PuDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2018_PuDown.root              --EEPFUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2018_EEPFUp.root              --EEPFDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2018_EEPFDown.root ${InterpolateShapePath}/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_${coup}_${cat}_2018.root;
#         mv diphoton_combine_${mass}_${box}.txt test_directory/${method}/2018/${box}/diphoton_combine_${mass}_${box}_2018.txt;
#         mv diphoton_combine_${mass}_${box}.root test_directory/${method}/2018/${box}/diphoton_combine_${mass}_${box}_2018.root;
#     done;
# done;

themainpath="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/test_directory"
cd ${themainpath}/${method}/2018
for scenario in {"DiPhotons_0p014","DiPhotons_1p4","DiPhotons_5p6"}; do
    echo ${scenario};
    coup=`echo ${scenario}| cut -d"_" -f 2`;
    export masslist=(600 613 621 629 637 645 653 662 670 679 687 696 705 714 723 732 741 751 760 770 779 789 799 809 820 830 840 851 862 872 883 894 906 917 929 940 952 964 976 988 1001 1013 1026 1038 1051 1064 1078 1091 1105 1119 1132 1147 1161 1175 1190 1205 1219 1235 1250 1265 1281 1297 1313 1329 1346 1362 1379 1396 1413 1431 1449 1466 1485 1503 1521 1540 1559 1578 1598 1617 1637 1657 1678 1698 1719 1740 1762 1783 1805 1827 1850 1873 1895 1919 1942 1966 1990 2014 2039 2064 2089 2115 2141 2167 2193 2220 2247 2275 2303 2331 2359 2388 2417 2447 2477 2507 2537 2568 2600 2631 2663 2696 2729 2762 2795 2830 2864 2899 2934 2970 3006 3042 3079 3117 3155 3193 3232 3271 3311 3351 3392 3433 3475 3517 3560 3603 3647 3691 3736 3781 3827 3873 3920 3968 4016 4065 4114 4164 4214 4265 4317 4369 4422 4476 4530 4585 4640 4696 4753 4811 4869 4928 4987 5000)
    if [[ ${coup} == "1p4" ]]; then
    masslist=(600 611 622 634 645 657 669 681 694 707 719 732 746 759 773 787 801 816 830 845 860 876 892 908 924 940 957 974 992 1009 1027 1046 1064 1083 1102 1122 1142 1162 1183 1204 1225 1247 1269 1291 1314 1337 1361 1385 1409 1434 1459 1485 1511 1537 1564 1592 1619 1648 1677 1706 1736 1766 1797 1828 1860 1893 1926 1959 1993 2028 2064 2099 2136 2173 2211 2249 2288 2328 2368 2410 2451 2494 2537 2581 2626 2671 2718 2765 2812 2861 2910 2961 3012 3064 3117 3171 3225 3281 3338 3395 3454 3513 3574 3636 3698 3762 3827 3893 3960 4028 4097 4167 4239 4312 4386 4462 4538 4616 4696 4776 4858 4942 5000)
    elif [[ ${coup} == "5p6" ]]; then
    masslist=(600 625 653 683 713 745 778 812 848 885 924 964 1005 1049 1094 1141 1190 1241 1293 1348 1405 1465 1527 1591 1658 1727 1800 1875 1953 2034 2119 2207 2298 2393 2492 2595 2702 2813 2929 3050 3175 3305 3440 3581 3728 3880 4038 4203 4374 4553 4738 4931 5000)
    for mass in "${masslist[@]}"; do
        echo ${mass};
        combineCards.py  ${themainpath}/${method}/2018/${scenario}_EBEB/diphoton_combine_${mass}_${scenario}_EBEB_2018.txt ${themainpath}/${method}/2018/${scenario}_EBEE/diphoton_combine_${mass}_${scenario}_EBEE_2018.txt  > diphoton_combine_${mass}_${scenario}_2018.txt;
    done;
done;

export mainpath="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/FinalResults"
cd ${mainpath}
#Then, run (will take some time depending on the mass points number)
#2018 RS
./loopAllMassPoints.csh 2018 heavyhiggs 0p014 ${method} ${massInterval} ../test_directory &
./loopAllMassPoints.csh 2018 heavyhiggs 1p4 ${method} ${massInterval} ../test_directory &
./loopAllMassPoints.csh 2018 heavyhiggs 5p6 ${method} ${massInterval} ../test_directory &
