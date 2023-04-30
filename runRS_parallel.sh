#!/usr/bin/env sh

export method="full"
export InterpolateShapePath="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/DijetShapeInterpolator/${method}"
export configFile="config/diphotons_500GeV.config"
export bkgFitResultsPath="test_directory"
export SignalNormFile="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/SignalNorm_Splines_${method}.txt"
export massInterval=500
export massMin=500
export massMax=7000


# ############################## signal interpolation ##############################

# cd /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/DijetShapeInterpolator/${method}

# filesToExtractRS=`ls /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/output/${method} |grep .root | grep RSG`

# for file in ${filesToExtractRS};
# do echo ${file}; coup=`echo ${file} | cut -d'_' -f 3`; echo $coup; filename=`echo ${file} | cut -d'.' -f 1`; ../getResonanceShapes.py -i inputs/${filename}.py -c ${coup} -f gg --massrange 500 10000 ${massInterval} -o ResonanceShapes_${filename}.root; done;


# ############################## bkg model ##############################

cd /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer

# mkdir -p ${bkgFitResultsPath}
#
time parallel --progress --jobs 10 'echo year={1}; echo Lumi={2}; echo coup={3}; echo cat={4}; python python/BinnedFit.py -c config/diphotons_dijet.config -l {2} -b DiPhotons_{3}_{4} -d ${bkgFitResultsPath} --fit-spectrum --plot-region Low --coup {3} --cat {4} --year {1} output/InputShapes_data_{4}_{1}.root' ::: 2016 2017 2018 :::+ 35900 41527 59670 ::: "kMpl001" "kMpl01" "kMpl02" ::: "EBEB" "EBEE"

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

#2016
# Remember for me the yield was initially normalized to 1000/pb. So, here lumi 35.9 (-d test_directory/2016/${box} omitted)
time parallel --progress --jobs 1 'year={1}; Lumi={2}; coup={3}; cat={4}; mass={5}; box=DiPhotons_${coup}_${cat}; echo year=${year}; echo Lumi=${Lumi}; echo coup=${coup}; echo cat=${cat}; echo box=${box}; echo mass=${mass}; mkdir -p test_directory/${method}/{year}/${box}; python python/WriteDataCard.py -m gg --mass ${mass} output/InputShapes_data_${cat}_${year}.root -i ${bkgFitResultsPath}/FitResults_${box}_${year}.root --lumi ${Lumi} -c ${configFile} -b ${box} --year ${year} --SigNorm ${SignalNormFile} --eneScStatUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_${year}_energyScaleStatUp.root   --eneScStatDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_${year}_energyScaleStatDown.root --eneScSystUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_${year}_energyScaleSystUp.root   --eneScSystDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_${year}_energyScaleSystDown.root --eneScGainUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_${year}_energyScaleGainUp.root   --eneScGainDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_${year}_energyScaleGainDown.root --eneScSigmaUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_${year}_energySigmaUp.root       --eneScSigmaDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_${year}_energySigmaDown.root     --SFScaleUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_${year}_SFScaleUp.root           --SFScaleDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_${year}_SFScaleDown.root         --PUScaleUp ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_${year}_PUScaleUp.root           --PUScaleDown ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_${year}_PUScaleDown.root ${InterpolateShapePath}/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_${coup}_${cat}_${year}.root; mv diphoton_combine_${mass}_${box}_${year}.* test_directory/${method}/${year}/${box}/.' ::: 2016 2017 2018 :::+ 35.9 41.527 59.670 ::: "kMpl001" "kMpl01" "kMpl02" ::: "EBEB" "EBEE" ::: $(seq ${massMin} ${massInterval} ${massMax})

# combine years and channels
themainpath="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/test_directory"
time parallel --progress --jobs 10 'year={1}; coup={2}; mass={3}; echo ${year}; echo ${coup}; echo ${mass}; cd ${themainpath}/${method}/${year}; combineCards.py ${themainpath}/${method}/${year}/DiPhotons_${coup}_EBEB/diphoton_combine_${mass}_DiPhotons_${coup}_EBEB_${year}.txt    ${themainpath}/${method}/${year}/DiPhotons_${coup}_EBEE/diphoton_combine_${mass}_DiPhotons_${coup}_EBEE_${year}.txt  > diphoton_combine_${mass}_DiPhotons_${coup}_${year}.txt' ::: 2016 2017 2018 ::: "kMpl001" "kMpl01" "kMpl02" ::: $(seq ${massMin} ${massInterval} ${massMax})

mkdir ${themainpath}/${method}/fullRun2
cd ${themainpath}/${method}/fullRun2
time parallel --progress --jobs 10 'year={1}; coup={2}; mass={3}; echo ${year}; echo ${coup}; echo ${mass}; combineCards.py ${themainpath}/${method}/2016/DiPhotons_${coup}_EBEB/diphoton_combine_${mass}_DiPhotons_${coup}_EBEB_2016.txt ${themainpath}/${method}/2016/DiPhotons_${coup}_EBEE/diphoton_combine_${mass}_DiPhotons_${coup}_EBEE_2016.txt ${themainpath}/${method}/2017/DiPhotons_${coup}_EBEB/diphoton_combine_${mass}_DiPhotons_${coup}_EBEB_2017.txt ${themainpath}/${method}/2017/DiPhotons_${coup}_EBEE/diphoton_combine_${mass}_DiPhotons_${coup}_EBEE_2017.txt ${themainpath}/${method}/2018/DiPhotons_${coup}_EBEB/diphoton_combine_${mass}_DiPhotons_${coup}_EBEB_2018.txt ${themainpath}/${method}/2018/DiPhotons_${coup}_EBEE/diphoton_combine_${mass}_DiPhotons_${coup}_EBEE_2018.txt > diphoton_combine_${mass}_DiPhotons_${coup}_fullRun2.txt;' ::: 2016 2017 2018 ::: "kMpl001" "kMpl01" "kMpl02" ::: $(seq ${massMin} ${massInterval} ${massMax})


# ############################## combine yields ##############################

export mainpath="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/FinalResults"
cd /afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/FinalResults/

#Then, run (will take some time depending on the mass points number)
#2016 RS
./loopAllMassPoints.sh 2016 grav kMpl001 ${method} ${massInterval} 500 5000
./loopAllMassPoints.sh 2016 grav kMpl01 ${method} ${massInterval} 500 7000
./loopAllMassPoints.sh 2016 grav kMpl02 ${method} ${massInterval} 500 7000
# #2017 RS
./loopAllMassPoints.sh 2017 grav kMpl001 ${method} ${massInterval} 500 5000
./loopAllMassPoints.sh 2017 grav kMpl01 ${method} ${massInterval} 500 7000
./loopAllMassPoints.sh 2017 grav kMpl02 ${method} ${massInterval} 500 7000
#2018 RS
./loopAllMassPoints.sh 2018 grav kMpl001 ${method} ${massInterval} 500 5000
./loopAllMassPoints.sh 2018 grav kMpl01 ${method} ${massInterval} 500 7000
./loopAllMassPoints.sh 2018 grav kMpl02 ${method} ${massInterval} 500 7000
#Full Run2 RS
./loopAllMassPoints.sh fullRun2 grav kMpl001 ${method} ${massInterval} 500 5000
./loopAllMassPoints.sh fullRun2 grav kMpl01 ${method} ${massInterval} 500 7000
./loopAllMassPoints.sh fullRun2 grav kMpl02 ${method} ${massInterval} 500 7000
