import ROOT as rt
import math as math
import sys, os
from bTag_signalStudies import *
from optparse import OptionParser
from rootTools import tdrstyle as setTDRStyle

### plots for signals ###
# tagging rate vs mass for signals (b, udcs, g)
# scale factors vs mass for signals with uncertainty
# selections acceptance vs mass for signals
# shape comparison before and after b-tag selection (normalized to 1)

usage = """usage: python python/bTag_signalStudies.py -f bb -m qq"""

#eosPrefix = "root://eoscms.cern.ch//eos/cms"
#eosPath = "/store/group/phys_exotica/dijet/Dijet13TeV/deguio/fall16_red_MC/RSGravitonToQuarkQuark_kMpl01_Spring16_20161201_145940/"
eosPrefix = ""
eosPath = "/tmp/TylerW/"
sampleNames_DMgq0p25={}
sampleNames_DMgq0p2={}
sampleNames_DMgq0p2['central'] = {
500:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation/2016DMAVgDM1gq0p2Z500DM1W14bb_reduced_skim.root',
750:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation/2016DMAVgDM1gq0p2Z750DM1W22bb_reduced_skim.root',
1000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation/2016DMAVgDM1gq0p2Z1000DM1W29bb_reduced_skim.root',
2000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation/2016DMAVgDM1gq0p2Z2000DM1W59bb_reduced_skim.root',
3000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation/2016DMAVgDM1gq0p2Z3000DM1W89bb_reduced_skim.root',
4000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation/2016DMAVgDM1gq0p2Z4000DM1W118bb_reduced_skim.root',
5000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation/2016DMAVgDM1gq0p2Z5000DM1W148bb_reduced_skim.root',
6000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation/2016DMAVgDM1gq0p2Z6000DM1W178bb_reduced_skim.root',
7000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation/2016DMAVgDM1gq0p2Z7000DM1W207bb_reduced_skim.root',
8000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation/2016DMAVgDM1gq0p2Z8000DM1W237bb_reduced_skim.root',
9000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation/2016DMAVgDM1gq0p2Z9000DM1W267bb_reduced_skim.root',}

sampleNames_DMgq0p25['central'] = {
500:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation/2016DMAVgq0p25gDM1Z500DM1W15bb_reduced_skim.root',
750:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation/2016DMAVgq0p25gDM1Z750DM1W23bb_reduced_skim.root',
1000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation/2016DMAVgq0p25gDM1Z1000DM1W31bb_reduced_skim.root',
2000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation/2016DMAVgq0p25gDM1Z2000DM1W62bb_reduced_skim.root',
3000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation/2016DMAVgq0p25gDM1Z3000DM1W94bb_reduced_skim.root',
4000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation/2016DMAVgq0p25gDM1Z4000DM1W125bb_reduced_skim.root',
5000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation/2016DMAVgq0p25gDM1Z5000DM1W157bb_reduced_skim.root',
6000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation/2016DMAVgq0p25gDM1Z6000DM1W188bb_reduced_skim.root',
7000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation/2016DMAVgq0p25gDM1Z7000DM1W220bb_reduced_skim.root',
8000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation/2016DMAVgq0p25gDM1Z8000DM1W251bb_reduced_skim.root',
9000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation/2016DMAVgq0p25gDM1Z9000DM1W283bb_reduced_skim.root',
}

sampleNames_DMgq0p25['down'] = {
500:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation_down/2016DMAVgq0p25gDM1Z500DM1W15bb_reduced_skim.root',
750:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation_down/2016DMAVgq0p25gDM1Z750DM1W23bb_reduced_skim.root',
1000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation_down/2016DMAVgq0p25gDM1Z1000DM1W31bb_reduced_skim.root',
2000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation_down/2016DMAVgq0p25gDM1Z2000DM1W62bb_reduced_skim.root',
3000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation_down/2016DMAVgq0p25gDM1Z3000DM1W94bb_reduced_skim.root',
4000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation_down/2016DMAVgq0p25gDM1Z4000DM1W125bb_reduced_skim.root',
5000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation_down/2016DMAVgq0p25gDM1Z5000DM1W157bb_reduced_skim.root',
6000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation_down/2016DMAVgq0p25gDM1Z6000DM1W188bb_reduced_skim.root',
7000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation_down/2016DMAVgq0p25gDM1Z7000DM1W220bb_reduced_skim.root',
8000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation_down/2016DMAVgq0p25gDM1Z8000DM1W251bb_reduced_skim.root',
9000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation_down/2016DMAVgq0p25gDM1Z9000DM1W283bb_reduced_skim.root',
}
sampleNames_DMgq0p2['down'] = {
500:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation_down/2016DMAVgDM1gq0p2Z500DM1W14bb_reduced_skim.root',
750:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation_down/2016DMAVgDM1gq0p2Z750DM1W22bb_reduced_skim.root',
1000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation_down/2016DMAVgDM1gq0p2Z1000DM1W29bb_reduced_skim.root',
2000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation_down/2016DMAVgDM1gq0p2Z2000DM1W59bb_reduced_skim.root',
3000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation_down/2016DMAVgDM1gq0p2Z3000DM1W89bb_reduced_skim.root',
4000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation_down/2016DMAVgDM1gq0p2Z4000DM1W118bb_reduced_skim.root',
5000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation_down/2016DMAVgDM1gq0p2Z5000DM1W148bb_reduced_skim.root',
6000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation_down/2016DMAVgDM1gq0p2Z6000DM1W178bb_reduced_skim.root',
7000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation_down/2016DMAVgDM1gq0p2Z7000DM1W207bb_reduced_skim.root',
8000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation_down/2016DMAVgDM1gq0p2Z8000DM1W237bb_reduced_skim.root',
9000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation_down/2016DMAVgDM1gq0p2Z9000DM1W267bb_reduced_skim.root',}

sampleNames_DMgq0p25['up'] = {
500:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation_up/2016DMAVgq0p25gDM1Z500DM1W15bb_reduced_skim.root',
750:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation_up/2016DMAVgq0p25gDM1Z750DM1W23bb_reduced_skim.root',
1000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation_up/2016DMAVgq0p25gDM1Z1000DM1W31bb_reduced_skim.root',
2000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation_up/2016DMAVgq0p25gDM1Z2000DM1W62bb_reduced_skim.root',
3000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation_up/2016DMAVgq0p25gDM1Z3000DM1W94bb_reduced_skim.root',
4000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation_up/2016DMAVgq0p25gDM1Z4000DM1W125bb_reduced_skim.root',
5000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation_up/2016DMAVgq0p25gDM1Z5000DM1W157bb_reduced_skim.root',
6000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation_up/2016DMAVgq0p25gDM1Z6000DM1W188bb_reduced_skim.root',
7000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation_up/2016DMAVgq0p25gDM1Z7000DM1W220bb_reduced_skim.root',
8000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation_up/2016DMAVgq0p25gDM1Z8000DM1W251bb_reduced_skim.root',
9000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation_up/2016DMAVgq0p25gDM1Z9000DM1W283bb_reduced_skim.root',
}
sampleNames_DMgq0p2['up'] = {
500:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation_up/2016DMAVgDM1gq0p2Z500DM1W14bb_reduced_skim.root',
750:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation_up/2016DMAVgDM1gq0p2Z750DM1W22bb_reduced_skim.root',
1000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation_up/2016DMAVgDM1gq0p2Z1000DM1W29bb_reduced_skim.root',
2000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation_up/2016DMAVgDM1gq0p2Z2000DM1W59bb_reduced_skim.root',
3000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation_up/2016DMAVgDM1gq0p2Z3000DM1W89bb_reduced_skim.root',
4000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation_up/2016DMAVgDM1gq0p2Z4000DM1W118bb_reduced_skim.root',
5000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation_up/2016DMAVgDM1gq0p2Z5000DM1W148bb_reduced_skim.root',
6000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation_up/2016DMAVgDM1gq0p2Z6000DM1W178bb_reduced_skim.root',
7000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation_up/2016DMAVgDM1gq0p2Z7000DM1W207bb_reduced_skim.root',
8000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation_up/2016DMAVgDM1gq0p2Z8000DM1W237bb_reduced_skim.root',
9000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/DM_Generation_up/2016DMAVgDM1gq0p2Z9000DM1W267bb_reduced_skim.root',
}


sampleNames_qg={}
sampleNames_qg['central'] = {
500:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/bstar/bstar_500GeV_reduced_skim.root',
1000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/bstar/bstar_1000GeV_reduced_skim.root',
2000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/bstar/bstar_2000GeV_reduced_skim.root',
3000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/bstar/bstar_3000GeV_reduced_skim.root',
4000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/bstar/bstar_4000GeV_reduced_skim.root',
5000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/bstar/bstar_5000GeV_reduced_skim.root',
6000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/bstar/bstar_6000GeV_reduced_skim.root',
7000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/bstar/bstar_7000GeV_reduced_skim.root',
8000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/bstar/bstar_8000GeV_reduced_skim.root',
9000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/bstar/bstar_9000GeV_reduced_skim.root',
                  }

sampleNames_qg['down'] = {
500:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/bstar_up/bstar_500GeV_reduced_skim.root',
1000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/bstar_up/bstar_1000GeV_reduced_skim.root',
2000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/bstar_up/bstar_2000GeV_reduced_skim.root',
3000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/bstar_up/bstar_3000GeV_reduced_skim.root',
4000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/bstar_up/bstar_4000GeV_reduced_skim.root',
5000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/bstar_up/bstar_5000GeV_reduced_skim.root',
6000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/bstar_up/bstar_6000GeV_reduced_skim.root',
7000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/bstar_up/bstar_7000GeV_reduced_skim.root',
8000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/bstar_up/bstar_8000GeV_reduced_skim.root',
9000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/bstar_up/bstar_9000GeV_reduced_skim.root',
                  }

sampleNames_qg['up'] = {
500:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/bstar_down/bstar_500GeV_reduced_skim.root',
1000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/bstar_down/bstar_1000GeV_reduced_skim.root',
2000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/bstar_down/bstar_2000GeV_reduced_skim.root',
3000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/bstar_down/bstar_3000GeV_reduced_skim.root',
4000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/bstar_down/bstar_4000GeV_reduced_skim.root',
5000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/bstar_down/bstar_5000GeV_reduced_skim.root',
6000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/bstar_down/bstar_6000GeV_reduced_skim.root',
7000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/bstar_down/bstar_7000GeV_reduced_skim.root',
8000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/bstar_down/bstar_8000GeV_reduced_skim.root',
9000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/bstar_down/bstar_9000GeV_reduced_skim.root',
}

#CHANGE FILE NAME AS SOON AS THE NTUPLES ARE READY
sampleNames_qq = {}
sampleNames_qq['central'] = {
500: '/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/RSG/RSG_500GeV_reduced_skim.root',
1000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/RSG/RSG_1000GeV_reduced_skim.root',
2000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/RSG/RSG_2000GeV_reduced_skim.root',
3000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/RSG/RSG_3000GeV_reduced_skim.root',
4000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/RSG/RSG_4000GeV_reduced_skim.root',
5000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/RSG/RSG_5000GeV_reduced_skim.root',
6000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/RSG/RSG_6000GeV_reduced_skim.root',
7000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/RSG/RSG_7000GeV_reduced_skim.root',
8000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/RSG/RSG_8000GeV_reduced_skim.root',
9000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/RSG/RSG_9000GeV_reduced_skim.root',
                  }
sampleNames_qq['down'] = {
500: '/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/RSG_down/RSG_500GeV_reduced_skim.root',
1000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/RSG_down/RSG_1000GeV_reduced_skim.root',
2000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/RSG_down/RSG_2000GeV_reduced_skim.root',
3000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/RSG_down/RSG_3000GeV_reduced_skim.root',
4000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/RSG_down/RSG_4000GeV_reduced_skim.root',
5000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/RSG_down/RSG_5000GeV_reduced_skim.root',
6000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/RSG_down/RSG_6000GeV_reduced_skim.root',
7000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/RSG_down/RSG_7000GeV_reduced_skim.root',
8000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/RSG_down/RSG_8000GeV_reduced_skim.root',
9000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/RSG_down/RSG_9000GeV_reduced_skim.root',
                  }

sampleNames_qq['up'] = {
500: '/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/RSG_up/RSG_500GeV_reduced_skim.root',
1000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/RSG_up/RSG_1000GeV_reduced_skim.root',
2000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/RSG_up/RSG_2000GeV_reduced_skim.root',
3000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/RSG_up/RSG_3000GeV_reduced_skim.root',
4000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/RSG_up/RSG_4000GeV_reduced_skim.root',
5000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/RSG_up/RSG_5000GeV_reduced_skim.root',
6000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/RSG_up/RSG_6000GeV_reduced_skim.root',
7000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/RSG_up/RSG_7000GeV_reduced_skim.root',
8000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/RSG_up/RSG_8000GeV_reduced_skim.root',
9000:'/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/2016JetHT_reduced/RSG_up/RSG_9000GeV_reduced_skim.root',
        }

#CSV_Value = [0.3093]
CSV_Value = [0.0614,0.1,0.15,0.2, 0.2217,0.25, 0.3093,0.35,0.4,0.45,0.5, 0.5426,0.6, 0.6321, 0.7221,0.8, 0.8484, 0.8953, 0.9535] 
#CSV_Value = [0.3]

treeName = "rootTupleTree/tree"
massRange  = {500: [75,0,1500],
	      750:[75,0,1500],
              1000: [50,0,2000],
              2000: [50,0,5000],
              3000: [50,0,5000],
              4000: [35,0,7000],
              5000: [35,0,8000],
              6000: [30,0,9000],
              7000: [20,0,10000],
              8000: [20,0,12000],
              9000: [20,0,12000]
              }


def bookAndFill(mass,sample,flavour,SFfile):
    #book histos
    hDict={}
    for i in CSV_Value:
      hDict[i] = {}

   
 
    for i in CSV_Value:
      prefix = str(mass)+"_"+str(int(i*1000))
      hDict[i]["h_mass_all"]    = rt.TH1F(prefix+"_mass_all",   prefix+"_mass_all",   massRange[mass][0],massRange[mass][1],massRange[mass][2])
      hDict[i]["h_mass_passed"] = rt.TH1F(prefix+"_mass_passed_deepCSV",prefix+"_mass_passed_deepCSV",massRange[mass][0],massRange[mass][1],massRange[mass][2])
      hDict[i]["h_mass_passed"].SetLineColor(rt.kOrange+8)
      hDict[i]["h_mass_passed"].SetMarkerColor(rt.kOrange+8)
      hDict[i]["h_mass_passed"].SetLineWidth(3)
      hDict[i]["h_mass_passed"].GetXaxis().SetTitle("Resonance Mass [GeV]")


      hDict[i]["h_mass_passed_0b"] = rt.TH1F(prefix+"_mass_passed_deepCSV_0b",prefix+"_mass_passed_deepCSV_0b",massRange[mass][0],massRange[mass][1],massRange[mass][2])
      hDict[i]["h_mass_passed_0b"].SetMarkerSize(0.5)
  
      hDict[i]["h_mass_passed_1b"] = rt.TH1F(prefix+"_mass_passed_deepCSV_1b",prefix+"_mass_passed_deepCSV_1b",massRange[mass][0],massRange[mass][1],massRange[mass][2])
      hDict[i]["h_mass_passed_1b"].SetLineColor(rt.kRed)
      hDict[i]["h_mass_passed_1b"].SetMarkerColor(rt.kRed)
      hDict[i]["h_mass_passed_1b"].SetMarkerSize(0.5)
    
      hDict[i]["h_mass_passed_2b"] = rt.TH1F(prefix+"_mass_passed_deepCSV_2b",prefix+"_mass_passed_deepCSV_2b",massRange[mass][0],massRange[mass][1],massRange[mass][2])
      hDict[i]["h_mass_passed_2b"].SetLineColor(rt.kBlue)
      hDict[i]["h_mass_passed_2b"].SetMarkerColor(rt.kBlue)
      hDict[i]["h_mass_passed_2b"].SetMarkerSize(0.5)

      hDict[i]["h_mass_passed_le1b"] = rt.TH1F(prefix+"_mass_passed_deepCSV_le1b",prefix+"_mass_passed_deepCSV_le1b",massRange[mass][0],massRange[mass][1],massRange[mass][2])
      hDict[i]["h_mass_passed_le1b"].SetLineColor(rt.kGreen)
      hDict[i]["h_mass_passed_le1b"].SetMarkerColor(rt.kGreen)
      hDict[i]["h_mass_passed_le1b"].SetMarkerSize(0.5)

      hDict[i]["h_weight_0b"] = rt.TH1F(prefix+"_weight_0b",prefix+"_weight_0b",2000,0.,2.)
      hDict[i]["h_weight_1b"] = rt.TH1F(prefix+"_weight_1b",prefix+"_weight_1b",2000,0.,2.)
      hDict[i]["h_weight_2b"] = rt.TH1F(prefix+"_weight_2b",prefix+"_weight_2b",2000,0.,2.)



    #loop over the tree and fill the histos
    tchain = rt.TChain(treeName)
    tchain.Add(sample)
    nEntries = tchain.GetEntries()

    for k in progressbar(range(nEntries), "Mass "+str(mass)+": ", 40):
        tchain.GetEntry(k)

        #implement analysis
	for i in CSV_Value:
           hDict[i]["h_mass_all"].Fill(tchain.mjj)
        

           SFs = []

           if not (abs(tchain.deltaETAjj)<1.1       and
                abs(tchain.etaWJ_j1)<2.5         and
                abs(tchain.etaWJ_j2)<2.5         and

                tchain.pTWJ_j1>60                and
                #tchain.pTWJ_j1<6500              and
                tchain.pTWJ_j2>30                and
                #tchain.pTWJ_j2<6500              and

                #tchain.mjj > 1246                and
                #tchain.mjj < 14000               and

                tchain.PassJSON):
             continue

           hDict[i]["h_mass_passed"].Fill(tchain.mjj)

           for jet in ['j1','j2']:
	    if getattr(tchain,'jetDeepJetAK4_%s'%jet) > i:
             if abs(getattr(tchain,'jetpflavour_%s'%jet)) == 5:
               SFs.append(TGraph2DEval(SFfile.Get('SFDeepJetBdis%s'%(str(int(i*1000)))),getattr(tchain,'pTAK4_%s'%jet),getattr(tchain,'etaAK4_%s'%jet)))
             elif abs(getattr(tchain,'jetpflavour_%s'%jet)) == 4:
               SFs.append(TGraph2DEval(SFfile.Get('SFDeepJetCdis%s'%(str(int(i*1000)))),getattr(tchain,'pTAK4_%s'%jet),getattr(tchain,'etaAK4_%s'%jet)))
             else:
               SFs.append(0)


#	   if i == 0.3033:
#	     print 
#	     print k,' ',SFs
#	     print tchain.jetpflavour_j1,tchain.jetpflavour_j2 

           hDict[i]["h_mass_passed_0b"].Fill(tchain.mjj,bWeight(SFs,0))
           hDict[i]["h_mass_passed_1b"].Fill(tchain.mjj,bWeight(SFs,1))
           hDict[i]["h_mass_passed_2b"].Fill(tchain.mjj,bWeight(SFs,2))
           hDict[i]["h_mass_passed_le1b"].Fill(tchain.mjj,bWeight(SFs,1))
           hDict[i]["h_mass_passed_le1b"].Fill(tchain.mjj,bWeight(SFs,2))

    return hDict



if __name__ == '__main__':

    rt.gROOT.SetBatch()
    setTDRStyle.setTDRStyle()
    ###################################################################
    parser = OptionParser(usage=usage)
    parser.add_option('-f','--flavour',dest="flavour",type="string",default="none",
                      help="Name of the signal flavour")
    parser.add_option('-m','--model',dest="model",type="string",default="qq",
                      help="Name of the signal model")
    parser.add_option('-s','--su',dest='su',type = 'string',default='central',help='central/up/down')

    (options,args) = parser.parse_args()
    flavour = options.flavour
    model   = options.model
    su = options.su


    print "selected flavour:",flavour
    print "signal model    :",model
    ###################################################################

#    CSV_Value = [0.05,0.1,0.1522,0.2,0.25,0.3,0.35,0.4,0.45,0.4941,0.5803,0.6,0.65,0.7,0.75,0.8,0.85,0.8838,0.9693]

    # book histos and graphs
    mDict = {}
    sampleNames = {}

    # loop over the MC samples

    
    if (model == "qq"):
        sampleNames = sampleNames_qq[su]
    elif (model == "qg"):
        sampleNames = sampleNames_qg[su]
    elif model=='DMgq0p2':
        sampleNames = sampleNames_DMgq0p2[su]
    elif model=='DMgq0p25':
        sampleNames = sampleNames_DMgq0p25[su]
    else:
        print "model unknown"
        exit

    SF_file = rt.TFile('/afs/cern.ch/work/z/zhixing/private/CMSSW_7_4_14/src/CMSDIJET/DijetRootTreeAnalyzer/SF_Interpolation_File_2016/Mapping_%s_Interpolation.root'%su)

    for mass, sample in sorted(sampleNames.iteritems()):
        mDict[mass] = bookAndFill(mass,sample,flavour,SF_file)

    #Create ROOT file and save plain histos
    outName = "signalHistos_"+flavour
    outFolder = "signalHistos_"+model+'_'+flavour+'_NovInter_For2016Scan_DeepJet_'+su

    if not os.path.exists(outFolder):
        os.makedirs(outFolder)

    if (flavour == "none"):
        outName = ("ResonanceShapes_%s_13TeV_Spring16.root"%model)

    g_an_acc={}
    g_mtbtag_rate={}
    g_0btag_rate={}
    g_1btag_rate={}
    g_2btag_rate={}
    g_le1btag_rate={}
    g_0btag_weight={}
    g_1btag_weight={}
    g_2btag_weight={}

    #make analysis vs mass
    for i in CSV_Value:
      g_an_acc[i]    = rt.TGraphAsymmErrors()
  
      g_mtbtag_rate[i] = rt.TGraphAsymmErrors()
      g_mtbtag_rate[i].SetTitle("g_mtbtag_rate;Resonance Mass [GeV];Tagging Rate")
      g_mtbtag_rate[i].SetLineWidth(2)

      g_0btag_rate[i] = rt.TGraphAsymmErrors()

      g_1btag_rate[i] = rt.TGraphAsymmErrors()
      g_1btag_rate[i].SetMarkerColor(rt.kRed)
      g_1btag_rate[i].SetLineColor(rt.kRed)
      g_1btag_rate[i].SetLineWidth(2)
      g_2btag_rate[i] = rt.TGraphAsymmErrors()
      g_2btag_rate[i].SetMarkerColor(rt.kBlue)
      g_2btag_rate[i].SetLineColor(rt.kBlue)
      g_2btag_rate[i].SetLineWidth(2)
 
      g_le1btag_rate[i] = rt.TGraphAsymmErrors()
      g_le1btag_rate[i].SetMarkerColor(rt.kGreen)
      g_le1btag_rate[i].SetLineColor(rt.kGreen)
      g_le1btag_rate[i].SetLineWidth(2)
 
      g_0btag_weight[i] = rt.TGraphAsymmErrors()
      g_1btag_weight[i] = rt.TGraphAsymmErrors()
      g_2btag_weight[i] = rt.TGraphAsymmErrors()
  

    bin=0 
    for mass,hDict in sorted(mDict.iteritems()):
      for i in CSV_Value: 


        den = hDict[i]["h_mass_passed"].GetSumOfWeights()
#        den = hDict[i]["h_mass_all"].GetSumOfWeights()
        #g_an_acc.SetPoint(bin,mass,num/den)  #wrong. the reduced ntuples have already the selection implemented

	num = hDict[i]["h_mass_passed_0b"].GetSumOfWeights()
        g_0btag_rate[i].SetPoint(bin,mass,num/den)

        num = hDict[i]["h_mass_passed_1b"].GetSumOfWeights()
        g_1btag_rate[i].SetPoint(bin,mass,num/den)

        num = hDict[i]["h_mass_passed_2b"].GetSumOfWeights()
        g_2btag_rate[i].SetPoint(bin,mass,num/den)

	num = hDict[i]["h_mass_passed_le1b"].GetSumOfWeights()
	g_le1btag_rate[i].SetPoint(bin,mass,num/den)
      bin += 1       

    for i in CSV_Value: 
      rootFile = rt.TFile(outFolder+"/"+outName+"_"+str(int(i*1000))+".root", 'recreate')
      for mass,hDict in sorted(mDict.iteritems()):
        # shape comparison 0 btag
        h1 = rt.TCanvas()
        h1.SetGridx()
        h1.SetGridy()
        h1.cd()  

        hDict[i]["h_mass_passed"].DrawNormalized()
        hDict[i]["h_mass_passed_1b"].DrawNormalized("sames")
        hDict[i]["h_mass_passed_2b"].DrawNormalized("sames")

        leg = rt.TLegend(0.87, 0.80, 0.96, 0.89)
        leg.AddEntry(hDict[i]["h_mass_passed"],"untagged","L")
        leg.AddEntry(hDict[i]["h_mass_passed_1b"],"1-tag","P")
        leg.AddEntry(hDict[i]["h_mass_passed_2b"],"2-tag","P")
        leg.Draw("same")

        h1.Print(outFolder+"/shapes_"+str(mass)+"_"+flavour+"_"+str(int(i*1000))+".pdf")

        for n,h in hDict[i].items():
            h.Write()
      g_an_acc[i].Write("g_an_acc")
      g_0btag_rate_Q=Do_Inter(g_0btag_rate[i])
      g_1btag_rate_Q=Do_Inter(g_1btag_rate[i])
      g_2btag_rate_Q=Do_Inter(g_2btag_rate[i])
      g_le1btag_rate_Q=Do_Inter(g_le1btag_rate[i])


#        g_0btag_rate_Q.Write("g_0btag_rate")
#        g_1btag_rate_Q.Write("g_1btag_rate")
      g_1btag_rate_Q.SetMarkerColor(rt.kRed)
      g_1btag_rate_Q.SetLineColor(rt.kRed)
      g_1btag_rate_Q.SetLineWidth(2)
#        g_2btag_rate_Q.Write("g_2btag_rate")
      g_2btag_rate_Q.SetMarkerColor(rt.kBlue)
      g_2btag_rate_Q.SetLineColor(rt.kBlue)
      g_2btag_rate_Q.SetLineWidth(2)

      g_le1btag_rate_Q.SetMarkerColor(rt.kGreen)
      g_le1btag_rate_Q.SetLineColor(rt.kGreen)
      g_le1btag_rate_Q.SetLineWidth(2)
   
      g_0btag_rate_Q.Write("g_0btag_rate")
      g_1btag_rate_Q.Write("g_1btag_rate")
      g_2btag_rate_Q.Write("g_2btag_rate")
      g_le1btag_rate_Q.Write("g_le1btag_rate")


      rootFile.Close()


    for i in CSV_Value:
       # Draw and print
       # tagging rate vs mass
       c1 = rt.TCanvas()
       c1.SetGridx()
       c1.SetGridy()
       c1.cd()

       
       g_0btag_rate_Q=Do_Inter(g_0btag_rate[i]) 
       g_1btag_rate_Q=Do_Inter(g_1btag_rate[i])
       g_2btag_rate_Q=Do_Inter(g_2btag_rate[i])
       g_le1btag_rate_Q=Do_Inter(g_le1btag_rate[i])

       g_1btag_rate_Q.SetMarkerColor(rt.kRed)
       g_1btag_rate_Q.SetLineColor(rt.kRed)
       g_1btag_rate_Q.SetLineWidth(2)
       #g_1btag_rate_Q.Write("g_1btag_rate")

       g_2btag_rate_Q.SetMarkerColor(rt.kBlue)
       g_2btag_rate_Q.SetLineColor(rt.kBlue)
       g_2btag_rate_Q.SetLineWidth(2)
       #g_2btag_rate_Q.Write("g_2btag_rate")

       g_le1btag_rate_Q.SetMarkerColor(rt.kGreen)
       g_le1btag_rate_Q.SetLineColor(rt.kGreen)
       g_le1btag_rate_Q.SetLineWidth(2)
       #g_le1btag_rate_Q.Write("g_le1btag_rate")
 
       g_1btag_rate_Q.Draw("APL")
       g_1btag_rate_Q.GetYaxis().SetRangeUser(0,1)
       g_2btag_rate_Q.Draw("PL,sames")
       g_le1btag_rate_Q.Draw("PL,sames")
   
       leg = rt.TLegend(0.87, 0.80, 0.96, 0.89)
       leg.AddEntry(g_1btag_rate_Q,"1-tag","L")
       leg.AddEntry(g_2btag_rate_Q,"2-tag","L")
       leg.AddEntry(g_le1btag_rate_Q,"le1-tag","L")
       leg.Draw("same")
   
       c1.Print(outFolder+"/tagRate_"+flavour+"_"+str(int(i*1000))+".pdf")
   
   
       # close file
       #raw_input("Press Enter to continue...")
   
   
