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
choose the right model and then put it in to step1.py
```
python step1.py
```
Then excute the command printed


choose the right model, data year and Folder produced in the last step into step2_Inter.py
```
python step2.py
```
excute step2_Inter_*.sh

choose the Folder produced in the first step and put it into step3_Inter_2018_*p.py
```
python step3_Inter_2018_*p.py
```
excute aloha_0.sh first(adding all tag and uncerntainty file to the right position)
then excute other aloha file
