#!/bin/bash


cd /afs/cern.ch/work/z/zhixing/private/CMSSW_7_4_14/src/CMSDIJET/DijetRootTreeAnalyzer/GetMass_2016

eval `scramv1 runtime -sh`



python GetMass2016.py -i CondorSubmittion_20190903_171702/FileList_2.txt -o CondorSubmittion_20190903_171702/2016Data_2.root