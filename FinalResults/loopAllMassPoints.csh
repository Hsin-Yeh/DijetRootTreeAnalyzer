#!/bin/tcsh

setenv year $1
setenv signal $2
setenv coupling $3

#setenv masslist `seq 500 100 5000`
setenv masslist "500 600 700 800 900 1000 1100 1200 1300 1400 1500 1600 1700 1800 1900 2000 2100 2200 2300 2400 2500 2600 2700 2800 2900 3000 3100 3200 3300 3400 3500 3600 3700 3800 3900 4000 4100 4200 4300 4400 4500 4600 4700 4800 4900 5000" 
#setenv masslist "500 600"


#setenv masslist "555 580 605 630"

# Method in this script are: AsymptoticLimits, ExpSignificance, ExpSignificanceWithPval, ObsSignificance, ObsSignificanceWithPval 
#setenv methods "ObsSignificance"
setenv methods "AsymptoticLimits"

foreach method ($methods)

rm -rf combineJobs13TeV/${year}/${signal}/${coupling}/${method}/All
mkdir -p combineJobs13TeV/${year}/${signal}/${coupling}/${method}/All

rm finalResults
touch finalResults

foreach mass ($masslist)

echo "====================================================================="
echo $mass

setenv datacardfile `echo /afs/cern.ch/work/a/apsallid/CMS/Hgg/exodiphotons/seconditeration/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/test_directory/diphoton_combine_${mass}_DiPhotons_${coupling}_${year}.txt`

if ($year == "fullRun2") then
setenv datacardfile `echo /afs/cern.ch/work/a/apsallid/CMS/Hgg/exodiphotons/seconditeration/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/test_directory/fullRun2/diphoton_combine_${mass}_DiPhotons_${coupling}.txt`
endif

echo $datacardfile

##
##    
##    Expected Significance 
##
##

if ($method == "ExpSignificance") then
  combine -d $datacardfile -M Significance --signif --pval --cminDefaultMinimizerType=Minuit2 -t -1 --expectSignal=1.0 -n Expected
  mv higgsCombineExpected.Significance.mH$mass.root combineJobs13TeV/${year}/${signal}/${coupling}/${method}/All/.
endif

if ($method == "ObsSignificance") then
  combine -d $datacardfile -M Significance --signif --pval --cminDefaultMinimizerType=Minuit2 -n Observed
  mv higgsCombineObserved.Significance.mH$mass.root combineJobs13TeV/${year}/${signal}/${coupling}/${method}/All/.
endif

##
##    
##    Asymptotic Limits
##
##

if ($method == "AsymptoticLimits") then

#a priori limits. I see in the post-fit or a-posteriori expected limit weird 
#one and two sigma region above 1.2 TeV. So, I will go to a priori limits at the moment. 
echo "combine -M AsymptoticLimits -s -1 --bypassFrequentistFit $datacardfile"
combine -M AsymptoticLimits  -s -1 --bypassFrequentistFit $datacardfile > ${datacardfile}_results

#echo "combine -M AsymptoticLimits -s -1 --bypassFrequentistFit /afs/cern.ch/work/a/apsallid/CMS/Hgg/exodiphotons/seconditeration/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/test_directory/diphoton_combine_${mass}_DiPhotons_${coupling}_${year}.txt"
#combine -M AsymptoticLimits  -s -1 --bypassFrequentistFit /afs/cern.ch/work/a/apsallid/CMS/Hgg/exodiphotons/seconditeration/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/test_directory/diphoton_combine_${mass}_DiPhotons_${coupling}_${year}.txt > /afs/cern.ch/work/a/apsallid/CMS/Hgg/exodiphotons/seconditeration/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/test_directory/diphoton_combine_${mass}_DiPhotons_${coupling}_${year}.txt_results
mv higgsCombineTest.AsymptoticLimits.mH*.root combineJobs13TeV/${year}/${signal}/${coupling}/${method}/All/.

setenv obs    `cat ${datacardfile}_results  | grep  "Observed Limit:" | awk '{print $5}'`
setenv expM2s `cat ${datacardfile}_results  | grep  "Expected  2.5%:" | awk '{print $5}'`
setenv expM1s `cat ${datacardfile}_results  | grep  "Expected 16.0%:" | awk '{print $5}'`
setenv exp    `cat ${datacardfile}_results  | grep  "Expected 50.0%:" | awk '{print $5}'`
setenv expP1s `cat ${datacardfile}_results  | grep  "Expected 84.0%:" | awk '{print $5}'`
setenv expP2s `cat ${datacardfile}_results  | grep  "Expected 97.5%:" | awk '{print $5}'`

echo $mass $obs $expM2s $expM1s $exp $expP1s $expP2s
echo $mass $obs $expM2s $expM1s $exp $expP1s $expP2s >> finalResults

endif

#end of loop over masses
end

cat finalResults | sort -n > finalResults2
mv finalResults2 combineJobs13TeV/${year}/${signal}/${coupling}/${method}/All/finalResults

#end of loop over methods
end 




