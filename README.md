Set up
============

```

cmsrel cmsrel CMSSW_9_4_0
cd CMSSW_9_4_0/src/
git clone https://github.com/CMSDIJET/DijetRootTreeAnalyzer/tree/bTagAnalyze CMSDIJET/DijetRootTreeAnalyzer
git clone git clone -b dijetpdf_74X https://github.com/RazorCMS/HiggsAnalysis-CombinedLimit HiggsAnalysis/CombinedLimit
cmsenv
cd HiggsAnalysis/CombinedLimit
scram b -j 4
cd $CMSSW_BASE/CMSDIJET/DijetRootTreeAnalyzer

```

Start
===========
```
python step1.py
```
