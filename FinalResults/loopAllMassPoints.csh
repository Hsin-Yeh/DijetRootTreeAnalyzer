#!/bin/tcsh

setenv year $1
setenv signal $2
setenv coupling $3
setenv method $4
setenv massInterval $5
setenv datacardsDir $6

# setenv masslist `seq 600 ${massInterval} 7000`

# if ($coupling == "kMpl001" || $coupling == "0p014" || $coupling == "1p4" || $coupling == "5p6") then
# setenv masslist `seq 600 ${massInterval} 5000`
# endif

setenv masslist "600 613 621 629 637 645 653 662 670 679 687 696 705 714 723 732 741 751 760 770 779 789 799 809 820 830 840 851 862 872 883 894 906 917 929 940 952 964 976 988 1001 1013 1026 1038 1051 1064 1078 1091 1105 1119 1132 1147 1161 1175 1190 1205 1219 1235 1250 1265 1281 1297 1313 1329 1346 1362 1379 1396 1413 1431 1449 1466 1485 1503 1521 1540 1559 1578 1598 1617 1637 1657 1678 1698 1719 1740 1762 1783 1805 1827 1850 1873 1895 1919 1942 1966 1990 2014 2039 2064 2089 2115 2141 2167 2193 2220 2247 2275 2303 2331 2359 2388 2417 2447 2477 2507 2537 2568 2600 2631 2663 2696 2729 2762 2795 2830 2864 2899 2934 2970 3006 3042 3079 3117 3155 3193 3232 3271 3311 3351 3392 3433 3475 3517 3560 3603 3647 3691 3736 3781 3827 3873 3920 3968 4016 4065 4114 4164 4214 4265 4317 4369 4422 4476 4530 4585 4640 4696 4753 4811 4869 4928 4987 5000"
if (${coupling} == "1p4"); then
setenv masslist "600 611 622 634 645 657 669 681 694 707 719 732 746 759 773 787 801 816 830 845 860 876 892 908 924 940 957 974 992 1009 1027 1046 1064 1083 1102 1122 1142 1162 1183 1204 1225 1247 1269 1291 1314 1337 1361 1385 1409 1434 1459 1485 1511 1537 1564 1592 1619 1648 1677 1706 1736 1766 1797 1828 1860 1893 1926 1959 1993 2028 2064 2099 2136 2173 2211 2249 2288 2328 2368 2410 2451 2494 2537 2581 2626 2671 2718 2765 2812 2861 2910 2961 3012 3064 3117 3171 3225 3281 3338 3395 3454 3513 3574 3636 3698 3762 3827 3893 3960 4028 4097 4167 4239 4312 4386 4462 4538 4616 4696 4776 4858 4942 5000"
endif
if (${coupling} == "5p6"); then
setenv masslist "600 625 653 683 713 745 778 812 848 885 924 964 1005 1049 1094 1141 1190 1241 1293 1348 1405 1465 1527 1591 1658 1727 1800 1875 1953 2034 2119 2207 2298 2393 2492 2595 2702 2813 2929 3050 3175 3305 3440 3581 3728 3880 4038 4203 4374 4553 4738 4931 5000"
endif

echo $masslist

# setenv masslist "500 600 700 800 900 1000 1100 1200 1300 1400 1500 1600 1700 1800 1900 2000 2100 2200 2300 2400 2500 2600 2700 2800 2900 3000 3100 3200 3300 3400 3500 3600 3700 3800 3900 4000 4100 4200 4300 4400 4500 4600 4700 4800 4900 5000"
# setenv masslist "4500 4600 4700 4800 4900 5000"


#setenv masslist "555 580 605 630"

# Combine_Method in this script are: AsymptoticLimits, ExpSignificance, ExpSignificanceWithPval, ObsSignificance, ObsSignificanceWithPval
#setenv combine_methods "ObsSignificance"
setenv combine_methods "AsymptoticLimits"

foreach combine_method ($combine_methods)

rm -rf combineJobs13TeV/${year}/${signal}/${coupling}/${combine_method}/All
mkdir -p combineJobs13TeV/${year}/${signal}/${coupling}/${combine_method}/All

setenv finalResults "finalResults_${year}_${signal}_${coupling}"
setenv finalResults2 "finalResults_${year}_${signal}_${coupling}_2"

rm ${finalResults}
touch ${finalResults}

foreach mass ($masslist)

echo "====================================================================="
echo $mass

setenv datacardfile `echo ${datacardsDir}/${method}/${year}/diphoton_combine_${mass}_DiPhotons_${coupling}_${year}.txt`

if ($year == "fullRun2") then
setenv datacardfile `echo ${datacardsDir}/${method}/fullRun2/diphoton_combine_${mass}_DiPhotons_${coupling}.txt`
endif

echo $datacardfile

##
##    
##    Expected Significance 
##
##

if ($combine_method == "ExpSignificance") then
  combine -d $datacardfile -M Significance --signif --pval --cminDefaultMinimizerType=Minuit2 -t -1 --expectSignal=1.0 -n Expected
  mv higgsCombineExpected.Significance.mH$mass.root combineJobs13TeV/${year}/${signal}/${coupling}/${combine_method}/All/.
endif

if ($combine_method == "ObsSignificance") then
  combine -d $datacardfile -M Significance --signif --pval --cminDefaultMinimizerType=Minuit2 -n Observed
  mv higgsCombineObserved.Significance.mH$mass.root combineJobs13TeV/${year}/${signal}/${coupling}/${combine_method}/All/.
endif

##
##    
##    Asymptotic Limits
##
##

if ($combine_method == "AsymptoticLimits") then

#a priori limits. I see in the post-fit or a-posteriori expected limit weird 
#one and two sigma region above 1.2 TeV. So, I will go to a priori limits at the moment. 
# echo "combine -M AsymptoticLimits -s -1 --bypassFrequentistFit $datacardfile"
# combine -M AsymptoticLimits  -s -1 --bypassFrequentistFit $datacardfile > ${datacardfile}_results

#a-posteriori expected limit
echo "combine -M AsymptoticLimits -s -1 $datacardfile"
combine -M AsymptoticLimits -s -1 -d $datacardfile > ${datacardfile}_results

#echo "combine -M AsymptoticLimits -s -1 --bypassFrequentistFit /afs/cern.ch/work/a/apsallid/CMS/Hgg/exodiphotons/seconditeration/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/test_directory/diphoton_combine_${mass}_DiPhotons_${coupling}_${year}.txt"
#combine -M AsymptoticLimits  -s -1 --bypassFrequentistFit /afs/cern.ch/work/a/apsallid/CMS/Hgg/exodiphotons/seconditeration/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/test_directory/diphoton_combine_${mass}_DiPhotons_${coupling}_${year}.txt > /afs/cern.ch/work/a/apsallid/CMS/Hgg/exodiphotons/seconditeration/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/test_directory/diphoton_combine_${mass}_DiPhotons_${coupling}_${year}.txt_results
mv higgsCombineTest.AsymptoticLimits.mH*.root combineJobs13TeV/${year}/${signal}/${coupling}/${combine_method}/All/.

setenv obs    `cat ${datacardfile}_results  | grep  "Observed Limit:" | awk '{print $5}'`
setenv expM2s `cat ${datacardfile}_results  | grep  "Expected  2.5%:" | awk '{print $5}'`
setenv expM1s `cat ${datacardfile}_results  | grep  "Expected 16.0%:" | awk '{print $5}'`
setenv exp    `cat ${datacardfile}_results  | grep  "Expected 50.0%:" | awk '{print $5}'`
setenv expP1s `cat ${datacardfile}_results  | grep  "Expected 84.0%:" | awk '{print $5}'`
setenv expP2s `cat ${datacardfile}_results  | grep  "Expected 97.5%:" | awk '{print $5}'`

echo $mass $obs $expM2s $expM1s $exp $expP1s $expP2s
echo $mass $obs $expM2s $expM1s $exp $expP1s $expP2s >> ${finalResults}

endif

#end of loop over masses
end

cat ${finalResults} | sort -n > ${finalResults2}
mv ${finalResults2} combineJobs13TeV/${year}/${signal}/${coupling}/${combine_method}/All/finalResults

#end of loop over combine_methods
end 




