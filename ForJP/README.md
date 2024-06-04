# README

*This code only runs under CentOS7 (lxplus7)*

## Setup
``` bash
export SCRAM_ARCH=slc7_amd64_gcc700
cmsrel CMSSW_10_2_13
cd CMSSW_10_2_13/src
cmsenv

##### DijetRootTreeAnalyzer #####
git clone git@github.com:Hsin-Yeh/DijetRootTreeAnalyzer.git DijetRootTreeAnalyzer
cd DijetRootTreeAnalyzer
git checkout diphotonresonant_hsinyeh
cd -
##### The Combine package #####
git clone git@github.com:apsallid/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit
git checkout diphotfuns
##### Complie #####
cd ../
scram b -j8
```

# Execute
```bash
cd DijetRootTreeAnalyzer/ForJP
./run.sh
```
The output datacards and workspace root files will be in "datacards/grav"
The results (limits, significance...) will be in "FinalResults"
