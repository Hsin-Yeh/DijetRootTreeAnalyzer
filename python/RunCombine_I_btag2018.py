from optparse import OptionParser
import os
import ROOT as rt
from array import *
from framework import Config
import sys
import glob
import rootTools
import time

NSIGMA = 10.0

def massIterable(massList):
    if len(massList.split(','))==1:
        massIterableList = [massList]
    else:
        massIterableList = list(eval(massList))
    return massIterableList

def exec_me(command,dryRun=True):
    print command
    if not dryRun: os.system(command)

def writeBashScript(options,massPoint,iJob=0):

    lumiFloat = [float(lumiStr) for lumiStr in options.lumi.split('_')]
    lumiTotal = sum(lumiFloat)

    submitDir = options.outDir
    massPoint = str(massPoint)


    signalSys = ''
    if options.noSignalSys:
        signalSys = '--no-signal-sys'
    elif options.noSys:
        signalSys = '--no-sys'

    penaltyString = ''
    if options.penalty:
        penaltyString = '--penalty'

    decoString = ''
    if options.deco:
        decoString  ='--deco'

    bayesString = ''
    if options.bayes:
        bayesString  ='--bayes'

    toyString = ''
    if options.toys>-1:
        toyString  ='--toys %i'%options.toys

    xsecString = '--xsec %f'%options.xsec

    signifString = ''
    if options.signif:
        signifString = '--signif'

    # prepare the script to run
    outputname = submitDir+"/submit_"+options.model+"_"+massPoint+"_lumi-%.3f_"%(lumiTotal)+options.box+"_%i"%(iJob)+".src"

    ffDir = submitDir+"/logs_"+options.model+"_"+massPoint+"_"+options.box+"_%i"%(iJob)
    user = os.environ['USER']
    pwd = os.environ['PWD']

    if options.noSys:
        combineDir = "/afs/cern.ch/work/%s/%s/DIJET/Limits/%s_nosys/"%(user[0],user,options.model) # directory where combine output files will be copied
    else:
        combineDir = "/afs/cern.ch/work/%s/%s/DIJET/Limits/%s/"%(user[0],user,options.model) # directory where combine output files will be copied
    cmsswBase = "/afs/cern.ch/work/%s/%s/DIJET/CMSSW_7_4_14"%(user[0],user) # directory where 'cmsenv' will be run (needs to have combine setup)

    script =  '#!/usr/bin/env bash -x\n'
    script += 'mkdir -p %s\n'%combineDir
    script += 'echo $SHELL\n'
    script += 'pwd\n'
    script += 'cd %s/src/CMSDIJET/DijetRootTreeAnalyzer \n'%(cmsswBase)
    script += 'pwd\n'
    script += "export SCRAM_ARCH=slc6_amd64_gcc491\n"
    script += "export CMSSW_BASE=%s\n"%(cmsswBase)
    script += 'eval `scramv1 runtime -sh`\n'
    script += 'cd - \n'
    script += "export TWD=${PWD}/%s_%s_lumi-%.3f_%s\n"%(options.model,massPoint,lumiTotal,options.box)
    script += "mkdir -p $TWD\n"
    script += "cd $TWD\n"
    script += 'pwd\n'
    script += 'git clone git@github.com:CMSDIJET/DijetRootTreeAnalyzer CMSDIJET/DijetRootTreeAnalyzer\n'
    script += 'cd CMSDIJET/DijetRootTreeAnalyzer\n'
    script += 'git checkout -b Limits %s\n'%(options.tag)
    script += 'mkdir -p %s\n'%submitDir
    if 'CaloDijet2015' in options.box.split('_') or options.box=='CaloDijet20152016':
        script += 'wget https://github.com/CMSDIJET/DijetShapeInterpolator/raw/master/ResonanceShapes_%s_13TeV_CaloScouting_Spring15.root -P inputs/\n'%(options.model)
        for sys in ['JERUP','JERDOWN','JESUP','JESDOWN']:
            script += 'wget https://github.com/CMSDIJET/DijetShapeInterpolator/raw/master/ResonanceShapes_%s_13TeV_CaloScouting_Spring15_%s.root -P inputs/\n'%(options.model,sys)
    if 'CaloDijet2016' in options.box.split('_'):
        script += 'wget https://github.com/CMSDIJET/DijetShapeInterpolator/raw/master/ResonanceShapes_%s_13TeV_CaloScouting_Spring16.root -P inputs/\n'%(options.model)
        for sys in ['JERUP','JERDOWN','JESUP','JESDOWN']:
            script += 'wget https://github.com/CMSDIJET/DijetShapeInterpolator/raw/master/ResonanceShapes_%s_13TeV_CaloScouting_Spring16_%s.root -P inputs/\n'%(options.model,sys)
    if 'PFDijet2016' in options.box.split('_'):
        script += 'wget https://github.com/CMSDIJET/DijetShapeInterpolator/raw/master/ResonanceShapes_%s_13TeV_Spring16.root -P inputs/\n'%(options.model)
        for sys in ['JERUP','JESUP','JESDOWN']:
            script += 'wget https://github.com/CMSDIJET/DijetShapeInterpolator/raw/master/ResonanceShapes_%s_13TeV_Spring16_%s.root -P inputs/\n'%(options.model,sys)
    script += 'python python/RunCombine.py -i %s -m %s --mass %s -c %s --lumi %s -d %s -b %s %s %s --min-tol %e --min-strat %i --rMax %f %s %s %s %s %s\n'%(options.inputFitFile,
                                                                                                                                                         options.model,
                                                                                                                                                         massPoint,
                                                                                                                                                         options.config,
                                                                                                                                                         options.lumi,
                                                                                                                                                         submitDir,
                                                                                                                                                         options.box,
                                                                                                                                                         penaltyString,
                                                                                                                                                         signalSys,
                                                                                                                                                         options.min_tol,
                                                                                                                                                         options.min_strat,
                                                                                                                                                         options.rMax,
                                                                                                                                                         decoString,
                                                                                                                                                         bayesString,
                                                                                                                                                         toyString,
                                                                                                                                                         xsecString,
                                                                                                                                                         signifString)
    script += 'cp %s/higgsCombine* %s/\n'%(submitDir,combineDir)
    script += 'cd ../..\n'
    script += 'rm -rf $TWD\n'

    outputfile = open(outputname,'w')
    outputfile.write(script)
    outputfile.close

    return outputname,ffDir

def submit_jobs(options,args):

    for massPoint in massIterable(options.mass):

        for iJob in range(0,options.jobs):
            outputname,ffDir = writeBashScript(options,massPoint,iJob)

            pwd = os.environ['PWD']
            os.system("mkdir -p "+pwd+"/"+ffDir)
            os.system("echo bsub -q "+options.queue+" -o "+pwd+"/"+ffDir+"/log.log source "+pwd+"/"+outputname)
            if not options.dryRun:
                time.sleep(3)
                os.system("bsub -q "+options.queue+" -o "+pwd+"/"+ffDir+"/log.log source "+pwd+"/"+outputname)

def main(options,args):

    boxes = options.box.split('_')

    signif = options.signif

    model = options.model

    lumiFloat = [float(lumiStr) for lumiStr in options.lumi.split('_')]

    rRangeStringList = []
    sysStringList = []

    pdfIndexMap = {'modexp': 0,
                   'fiveparam': 1,
                   'atlas': 2,
                   }

    for box,lumi in zip(boxes,lumiFloat):

        paramDict = {}
        if options.inputFitFile is not None and options.bayes:
            inputRootFile = rt.TFile.Open(options.inputFitFile,"r")
            wIn = inputRootFile.Get("w"+box).Clone("wIn"+box)
            if wIn.obj("fitresult_extDijetPdf_data_obs") != None:
                frIn = wIn.obj("fitresult_extDijetPdf_data_obs")
            elif wIn.obj("nll_extDijetPdf_data_obs") != None:
                frIn = wIn.obj("nll_extDijetPdf_data_obs")
            elif wIn.obj("fitresult_extDijetPdf_data_obs_with_constr") != None:
                fr = wIn.obj("fitresult_extDijetPdf_data_obs_with_constr")
            elif wIn.obj("nll_extDijetPdf_data_obs_with_constr") != None:
                frIn = wIn.obj("nll_extDijetPdf_data_obs_with_constr")
            elif wIn.obj("simNll") != None:
                frIn = wIn.obj("simNll")
            paramDict = {}
            for p in rootTools.RootIterator.RootIterator(frIn.floatParsFinal()):
                paramDict[p.GetName()] = [p.getVal(), p.getError()]
            print "grabbing parameter ranges +-%gsigma for bayesian"%NSIGMA


        signalSys = ''
        if options.noSignalSys or options.noSys:
            signalSys = '--no-signal-sys'
        else:
            if box=='CaloDijet2015' or box=='CaloDijet20152016':
                signalSys  =   '--jesUp inputs/ResonanceShapes_%s_13TeV_CaloScouting_Spring15_JESUP.root --jesDown inputs/ResonanceShapes_%s_13TeV_CaloScouting_Spring15_JESDOWN.root'%(model,model)
                signalSys += ' --jerUp inputs/ResonanceShapes_%s_13TeV_CaloScouting_Spring15_JERUP.root --jerDown inputs/ResonanceShapes_%s_13TeV_CaloScouting_Spring15_JERDOWN.root'%(model,model)
            elif box=='CaloDijet2016':
                signalSys  =   '--jesUp inputs/ResonanceShapes_%s_13TeV_CaloScouting_Spring16_JESUP.root --jesDown inputs/ResonanceShapes_%s_13TeV_CaloScouting_Spring16_JESDOWN.root'%(model,model)
                signalSys += ' --jerUp inputs/ResonanceShapes_%s_13TeV_CaloScouting_Spring16_JERUP.root --jerDown inputs/ResonanceShapes_%s_13TeV_CaloScouting_Spring16_JERDOWN.root'%(model,model)
            elif box=='PFDijet2016':
                signalSys  =   '--jesUp inputs/ResonanceShapes_%s_13TeV_Spring16_JESUP.root --jesDown inputs/ResonanceShapes_%s_13TeV_Spring16_JESDOWN.root'%(model,model)
                signalSys += ' --jerUp inputs/ResonanceShapes_%s_13TeV_Spring16_JERUP.root'%(model)
            elif box=='PFDijetbg20161tt':
                signalSys  = '--jesUp inputs/Inter_U/ResonanceShapes_qg_bg_13TeV_Spring16_Interpolation_JESUP_rescale.root --jesDown  inputs/Inter_U/ResonanceShapes_qg_bg_13TeV_Spring16_Interpolation_JESDOWN_rescale.root'
                signalSys += ' --jerUp inputs/Inter_U/ResonanceShapes_qg_bg_13TeV_Spring16_Interpolation_JER_rescale.root'
	    elif box=='PFDijetbb20162tt':	
	         signalSys = '--jesUp inputs/Med_Inter_U/ResonanceShapes_qq_bb_13TeV_Spring16_med_Interpolation_JESUP_rescale.root --jesDown inputs/Med_Inter_U/ResonanceShapes_qq_bb_13TeV_Spring16_med_Interpolation_JESDOWN_rescale.root'
	         signalSys += ' --jerUp inputs/Med_Inter_U/ResonanceShapes_qq_bb_13TeV_Spring16_med_Interpolation_JER_rescale.root'
            elif box=='PFNo70DMgq0p25Dijet2017bbDeepJetNon100':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_Non/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_100_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_Non/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_100_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_up_Non/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_100_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_down_Non/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_100_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_Non/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_100_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2017bbDeepJetle1b52':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_52_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_52_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_52_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_52_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_52_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2017bbDeepJetle1b100':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_100_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_100_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_100_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_100_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_100_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2017bbDeepJetle1b152':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_152_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_152_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_152_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_152_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_152_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2017bbDeepJetle1b200':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_200_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_200_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_200_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_200_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_200_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2017bbDeepJetle1b250':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_250_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_250_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_250_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_250_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_250_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2017bbDeepJetle1b303':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_303_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_303_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_303_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_303_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_303_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2017bbDeepJetle1b350':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_350_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_350_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_350_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_350_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_350_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2017bbDeepJetle1b400':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_400_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_400_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_400_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_400_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_400_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2017bbDeepJetle1b450':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_450_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_450_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_450_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_450_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_450_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2017bbDeepJetle1b494':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_494_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_494_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_494_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_494_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_494_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2017bbDeepJetle1b550':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_550_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_550_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_550_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_550_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_550_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2017bbDeepJetle1b580':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_580_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_580_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_580_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_580_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_580_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2017bbDeepJetle1b600':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_600_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_600_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_600_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_600_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_600_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2017bbDeepJetle1b650':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_650_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_650_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_650_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_650_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_650_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2017bbDeepJetle1b700':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_700_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_700_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_700_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_700_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_700_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2017bbDeepJetle1b748':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_748_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_748_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_748_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_748_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_748_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2017bbDeepJetle1b800':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_800_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_800_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_800_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_800_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_800_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2017bbDeepJetle1b850':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_850_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_850_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_850_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_850_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_850_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2017bbDeepJetle1b883':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_883_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_883_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_883_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_883_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_883_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2017bbDeepJetle1b900':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_900_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_900_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_900_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_900_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_900_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2017bbDeepJetle1b969':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_969_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_969_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_969_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_969_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_969_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2017bbDeepJetNon100':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_Non/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_100_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_Non/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_100_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_up_Non/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_100_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_down_Non/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_100_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_Non/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_100_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2017bbDeepJetle1b52':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_52_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_52_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_52_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_52_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_52_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2017bbDeepJetle1b100':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_100_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_100_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_100_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_100_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_100_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2017bbDeepJetle1b152':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_152_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_152_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_152_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_152_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_152_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2017bbDeepJetle1b200':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_200_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_200_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_200_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_200_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_200_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2017bbDeepJetle1b250':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_250_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_250_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_250_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_250_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_250_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2017bbDeepJetle1b303':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_303_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_303_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_303_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_303_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_303_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2017bbDeepJetle1b350':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_350_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_350_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_350_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_350_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_350_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2017bbDeepJetle1b400':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_400_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_400_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_400_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_400_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_400_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2017bbDeepJetle1b450':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_450_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_450_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_450_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_450_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_450_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2017bbDeepJetle1b494':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_494_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_494_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_494_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_494_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_494_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2017bbDeepJetle1b550':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_550_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_550_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_550_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_550_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_550_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2017bbDeepJetle1b580':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_580_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_580_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_580_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_580_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_580_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2017bbDeepJetle1b600':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_600_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_600_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_600_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_600_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_600_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2017bbDeepJetle1b650':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_650_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_650_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_650_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_650_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_650_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2017bbDeepJetle1b700':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_700_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_700_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_700_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_700_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_700_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2017bbDeepJetle1b748':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_748_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_748_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_748_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_748_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_748_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2017bbDeepJetle1b800':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_800_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_800_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_800_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_800_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_800_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2017bbDeepJetle1b850':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_850_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_850_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_850_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_850_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_850_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2017bbDeepJetle1b883':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_883_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_883_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_883_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_883_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_883_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2017bbDeepJetle1b900':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_900_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_900_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_900_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_900_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_900_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2017bbDeepJetle1b969':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_969_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_969_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_969_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_969_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_969_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2016bbDeepJetNon100':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_Non/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_100_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_Non/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_100_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_up_Non/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_100_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_down_Non/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_100_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_Non/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_100_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2016bbDeepJetle1b61':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_61_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_61_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_61_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_61_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_61_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2016bbDeepJetle1b100':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_100_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_100_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_100_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_100_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_100_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2016bbDeepJetle1b150':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_150_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_150_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_150_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_150_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_150_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2016bbDeepJetle1b200':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_200_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_200_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_200_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_200_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_200_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2016bbDeepJetle1b221':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_221_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_221_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_221_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_221_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_221_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2016bbDeepJetle1b250':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_250_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_250_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_250_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_250_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_250_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2016bbDeepJetle1b309':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_309_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_309_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_309_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_309_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_309_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2016bbDeepJetle1b350':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_350_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_350_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_350_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_350_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_350_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2016bbDeepJetle1b400':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_400_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_400_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_400_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_400_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_400_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2016bbDeepJetle1b450':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_450_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_450_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_450_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_450_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_450_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2016bbDeepJetle1b500':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_500_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_500_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_500_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_500_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_500_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2016bbDeepJetle1b542':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_542_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_542_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_542_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_542_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_542_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2016bbDeepJetle1b600':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_600_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_600_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_600_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_600_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_600_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2016bbDeepJetle1b632':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_632_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_632_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_632_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_632_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_632_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2016bbDeepJetle1b722':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_722_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_722_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_722_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_722_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_722_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2016bbDeepJetle1b800':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_800_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_800_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_800_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_800_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_800_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2016bbDeepJetle1b848':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_848_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_848_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_848_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_848_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_848_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2016bbDeepJetle1b895':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_895_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_895_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_895_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_895_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_895_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2016bbDeepJetle1b953':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_953_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_953_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_953_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_953_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_953_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2016bbDeepJetNon100':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_Non/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_100_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_Non/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_100_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_up_Non/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_100_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_down_Non/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_100_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_Non/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_100_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2016bbDeepJetle1b61':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_61_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_61_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_61_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_61_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_61_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2016bbDeepJetle1b100':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_100_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_100_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_100_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_100_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_100_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2016bbDeepJetle1b150':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_150_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_150_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_150_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_150_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_150_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2016bbDeepJetle1b200':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_200_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_200_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_200_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_200_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_200_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2016bbDeepJetle1b221':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_221_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_221_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_221_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_221_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_221_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2016bbDeepJetle1b250':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_250_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_250_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_250_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_250_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_250_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2016bbDeepJetle1b309':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_309_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_309_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_309_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_309_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_309_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2016bbDeepJetle1b350':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_350_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_350_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_350_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_350_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_350_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2016bbDeepJetle1b400':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_400_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_400_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_400_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_400_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_400_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2016bbDeepJetle1b450':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_450_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_450_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_450_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_450_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_450_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2016bbDeepJetle1b500':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_500_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_500_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_500_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_500_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_500_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2016bbDeepJetle1b542':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_542_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_542_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_542_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_542_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_542_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2016bbDeepJetle1b600':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_600_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_600_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_600_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_600_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_600_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2016bbDeepJetle1b632':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_632_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_632_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_632_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_632_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_632_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2016bbDeepJetle1b722':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_722_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_722_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_722_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_722_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_722_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2016bbDeepJetle1b800':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_800_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_800_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_800_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_800_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_800_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2016bbDeepJetle1b848':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_848_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_848_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_848_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_848_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_848_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2016bbDeepJetle1b895':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_895_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_895_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_895_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_895_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_895_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2016bbDeepJetle1b953':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_953_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_953_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_953_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_953_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_953_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2018bbDeepJetNon124':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_Non/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_124_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_Non/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_124_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_up_Non/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_124_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_down_Non/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_124_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_Non/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_124_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2018bbDeepJetle1b49':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_49_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_49_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_49_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_49_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_49_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2018bbDeepJetle1b124':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_124_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_124_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_124_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_124_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_124_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2018bbDeepJetle1b200':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_200_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_200_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_200_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_200_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_200_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2018bbDeepJetle1b277':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_277_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_277_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_277_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_277_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_277_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2018bbDeepJetle1b350':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_350_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_350_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_350_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_350_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_350_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2018bbDeepJetle1b418':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_418_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_418_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_418_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_418_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_418_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2018bbDeepJetle1b450':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_450_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_450_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_450_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_450_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_450_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2018bbDeepJetle1b500':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_500_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_500_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_500_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_500_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_500_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2018bbDeepJetle1b550':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_550_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_550_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_550_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_550_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_550_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2018bbDeepJetle1b600':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_600_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_600_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_600_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_600_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_600_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2018bbDeepJetle1b650':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_650_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_650_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_650_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_650_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_650_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2018bbDeepJetle1b700':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_700_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_700_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_700_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_700_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_700_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2018bbDeepJetle1b726':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_726_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_726_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_726_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_726_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_726_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2018bbDeepJetle1b752':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_752_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_752_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_752_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_752_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_752_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2018bbDeepJetle1b800':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_800_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_800_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_800_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_800_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_800_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2018bbDeepJetle1b850':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_850_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_850_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_850_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_850_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_850_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2018bbDeepJetle1b900':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_900_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_900_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_900_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_900_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_900_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p25Dijet2018bbDeepJetle1b950':
                 signalSys += ' --jesUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_950_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_950_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_950_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_950_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_950_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2018bbDeepJetNon124':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_Non/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_124_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_Non/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_124_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_up_Non/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_124_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_down_Non/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_124_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_Non/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_124_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2018bbDeepJetle1b49':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_49_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_49_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_49_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_49_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_49_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2018bbDeepJetle1b124':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_124_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_124_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_124_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_124_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_124_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2018bbDeepJetle1b200':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_200_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_200_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_200_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_200_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_200_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2018bbDeepJetle1b277':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_277_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_277_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_277_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_277_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_277_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2018bbDeepJetle1b350':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_350_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_350_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_350_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_350_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_350_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2018bbDeepJetle1b418':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_418_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_418_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_418_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_418_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_418_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2018bbDeepJetle1b450':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_450_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_450_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_450_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_450_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_450_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2018bbDeepJetle1b500':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_500_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_500_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_500_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_500_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_500_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2018bbDeepJetle1b550':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_550_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_550_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_550_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_550_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_550_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2018bbDeepJetle1b600':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_600_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_600_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_600_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_600_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_600_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2018bbDeepJetle1b650':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_650_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_650_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_650_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_650_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_650_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2018bbDeepJetle1b700':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_700_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_700_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_700_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_700_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_700_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2018bbDeepJetle1b726':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_726_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_726_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_726_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_726_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_726_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2018bbDeepJetle1b752':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_752_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_752_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_752_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_752_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_752_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2018bbDeepJetle1b800':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_800_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_800_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_800_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_800_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_800_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2018bbDeepJetle1b850':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_850_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_850_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_850_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_850_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_850_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2018bbDeepJetle1b900':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_900_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_900_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_900_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_900_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_900_JER_Interpolation_rescale.root'

            elif box=='PFNo70DMgq0p2Dijet2018bbDeepJetle1b950':
                 signalSys += ' --jesUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_950_JESUP_Interpolation_rescale.root --jesDown signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_950_JESDOWN_Interpolation_rescale.root'
                 signalSys += ' --btagUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_up_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_950_Nominal_Interpolation_rescale.root --btagDown signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_down_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_950_Nominal_Interpolation_rescale.root'
                 signalSys += ' --jerUp signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_950_JER_Interpolation_rescale.root'

#EDITJEU


        penaltyString = ''
        if options.penalty:
            penaltyString = '--penalty'
        elif options.noSys:
            penaltyString = '--fixed'

        xsecString = '--xsec %f'%(options.xsec)


        if box=='CaloDijet2015' or box=='CaloDijet20152016':
            signalDsName = 'inputs/ResonanceShapes_%s_13TeV_CaloScouting_Spring15.root'%model
        elif box=='CaloDijet2016':
            signalDsName = 'inputs/ResonanceShapes_%s_13TeV_CaloScouting_Spring16.root'%model
        elif box=='PFDijet2016':
            signalDsName = 'inputs/ResonanceShapes_%s_13TeV_Spring16.root'%model
	elif 'PFDijetbg20161tt' == box:
	    	signalDsName = 'inputs/Inter_U/ResonanceShapes_qg_bg_13TeV_Spring16_Interpolation_Norminal_rescale.root'
	elif 'PFDijetbb20162ttQI' == box:
	    	signalDsName = 'inputs/Newbb/ResonanceShapes_qq_bb_13TeV_Spring16_Inter_Interpolation_rescale.root'
	elif 'PFDijetbb20162tt' == box:
	    	signalDsName = 'signalHistos_bb_t/ResonanceShapes_qq_bb_13TeV_Spring16_tight_Interpolation_rescale.root'
        elif 'PFDijetbb20162mm2' == box:
            signalDsName = 'inputs/Med_Inter_U/ResonanceShapes_qq_bb_13TeV_Spring16_Norminal_Inter_Interpolation.root'
        elif 'PFDijetbb20162mm' == box:
            signalDsName = 'inputs/bTag_uncertainty/ResonanceShapes_qq_bb_13TeV_Spring16_central_Norminal_Inter_Interpolation_rescale.root'
        elif 'PFDijetbb20162mmU'==box:
            signalDsName = 'inputs/bTag_uncertainty/ResonanceShapes_qq_bb_13TeV_Spring16_UP_Norminal_Inter_Interpolation_rescale.root'
        elif 'PFDijetbb20162mmD'==box:
            signalDsName = 'inputs/bTag_uncertainty/ResonanceShapes_qq_bb_13TeV_Spring16_DOWN_Norminal_Inter_Interpolation_rescale.root'
        elif 'PFDijetbb20162mm9'==box:
            signalDsName = 'inputs/Inter_09/ResonanceShapes_qq_bb_13TeV_Spring16_Norminal_Inter_Interpolation_rescale.root'
	elif 'PFDijetbg20161ttC'==box:
	    	signalDsName = 'inputs/bTag_uncertainty_bg/ResonanceShapes_qg_bb_13TeV_Spring16_central_Norminal_Inter_Interpolation_rescale.root'
        elif 'PFDijetbg20161ttU'==box:
            signalDsName = 'inputs/bTag_uncertainty_bg/ResonanceShapes_qg_bb_13TeV_Spring16_UP_Norminal_Inter_Interpolation_rescale.root'
        elif 'PFDijetbg20161ttD'==box:
            signalDsName = 'inputs/bTag_uncertainty_bg/ResonanceShapes_qg_bb_13TeV_Spring16_DOWN_Norminal_Inter_Interpolation_rescale.root'
        elif 'PFDijetbg20161ttG'==box:
            signalDsName = 'inputs/Gaus/ResonanceShapes_gaus10_13TeV_Spring16_rescale.root'
	elif 'PFDijetbb20161mm1btag'==box:
		    signalDsName = 'inputs/1btag_mm_coloron_Uncertainty/ResonanceShapes_qq_bb_13TeV_Spring16_Norminal_Inter_Interpolation_rescale.root'
        elif 'PFDijetbb20161tt1btag'==box:
		    signalDsName = 'inputs/1btag_tt_coloron_Uncertainty/ResonanceShapes_qq_bb_13TeV_Spring16_Norminal_Inter_Interpolation_rescale.root'
	elif 'PFDijetbb20161mm1btag2'==box:
	   	 	signalDsName = 'inputs/Coloron_bb_tight_Uncertainty/ResonanceShapes_qq_bb_13TeV_Spring16_Norminal_Inter_Interpolation_rescale.root'
	elif 'PFDijetbb20161mmle1'==box:
	  	  signalDsName = 'inputs/1btag_mm_coloron_Uncertainty_le1/ResonanceShapes_qq_bb_13TeV_Spring16_Norminal_Inter_Interpolation_rescale.root'
	elif 'PFDijetbb20161tt'==box:
	 	   signalDsName = 'inputs/1ttColoron_Uncertainty/ResonanceShapes_qq_bb_13TeV_Spring16_Norminal_Inter_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2017bbDeepJetNon100':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_Non/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_100_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2017bbDeepJetle1b52':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_52_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2017bbDeepJetle1b100':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_100_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2017bbDeepJetle1b152':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_152_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2017bbDeepJetle1b200':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_200_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2017bbDeepJetle1b250':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_250_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2017bbDeepJetle1b303':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_303_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2017bbDeepJetle1b350':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_350_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2017bbDeepJetle1b400':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_400_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2017bbDeepJetle1b450':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_450_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2017bbDeepJetle1b494':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_494_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2017bbDeepJetle1b550':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_550_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2017bbDeepJetle1b580':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_580_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2017bbDeepJetle1b600':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_600_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2017bbDeepJetle1b650':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_650_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2017bbDeepJetle1b700':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_700_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2017bbDeepJetle1b748':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_748_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2017bbDeepJetle1b800':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_800_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2017bbDeepJetle1b850':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_850_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2017bbDeepJetle1b883':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_883_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2017bbDeepJetle1b900':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_900_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2017bbDeepJetle1b969':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_969_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2017bbDeepJetNon100':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_Non/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_100_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2017bbDeepJetle1b52':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_52_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2017bbDeepJetle1b100':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_100_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2017bbDeepJetle1b152':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_152_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2017bbDeepJetle1b200':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_200_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2017bbDeepJetle1b250':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_250_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2017bbDeepJetle1b303':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_303_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2017bbDeepJetle1b350':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_350_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2017bbDeepJetle1b400':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_400_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2017bbDeepJetle1b450':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_450_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2017bbDeepJetle1b494':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_494_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2017bbDeepJetle1b550':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_550_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2017bbDeepJetle1b580':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_580_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2017bbDeepJetle1b600':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_600_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2017bbDeepJetle1b650':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_650_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2017bbDeepJetle1b700':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_700_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2017bbDeepJetle1b748':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_748_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2017bbDeepJetle1b800':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_800_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2017bbDeepJetle1b850':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_850_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2017bbDeepJetle1b883':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_883_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2017bbDeepJetle1b900':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_900_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2017bbDeepJetle1b969':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_969_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2016bbDeepJetNon100':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_Non/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_100_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2016bbDeepJetle1b61':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_61_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2016bbDeepJetle1b100':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_100_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2016bbDeepJetle1b150':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_150_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2016bbDeepJetle1b200':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_200_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2016bbDeepJetle1b221':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_221_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2016bbDeepJetle1b250':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_250_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2016bbDeepJetle1b309':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_309_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2016bbDeepJetle1b350':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_350_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2016bbDeepJetle1b400':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_400_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2016bbDeepJetle1b450':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_450_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2016bbDeepJetle1b500':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_500_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2016bbDeepJetle1b542':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_542_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2016bbDeepJetle1b600':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_600_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2016bbDeepJetle1b632':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_632_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2016bbDeepJetle1b722':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_722_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2016bbDeepJetle1b800':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_800_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2016bbDeepJetle1b848':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_848_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2016bbDeepJetle1b895':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_895_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2016bbDeepJetle1b953':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_953_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2016bbDeepJetNon100':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_Non/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_100_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2016bbDeepJetle1b61':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_61_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2016bbDeepJetle1b100':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_100_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2016bbDeepJetle1b150':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_150_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2016bbDeepJetle1b200':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_200_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2016bbDeepJetle1b221':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_221_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2016bbDeepJetle1b250':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_250_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2016bbDeepJetle1b309':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_309_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2016bbDeepJetle1b350':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_350_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2016bbDeepJetle1b400':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_400_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2016bbDeepJetle1b450':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_450_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2016bbDeepJetle1b500':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_500_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2016bbDeepJetle1b542':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_542_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2016bbDeepJetle1b600':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_600_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2016bbDeepJetle1b632':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_632_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2016bbDeepJetle1b722':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_722_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2016bbDeepJetle1b800':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_800_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2016bbDeepJetle1b848':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_848_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2016bbDeepJetle1b895':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_895_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2016bbDeepJetle1b953':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_953_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2018bbDeepJetNon124':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_Non/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_124_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2018bbDeepJetle1b49':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_49_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2018bbDeepJetle1b124':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_124_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2018bbDeepJetle1b200':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_200_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2018bbDeepJetle1b277':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_277_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2018bbDeepJetle1b350':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_350_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2018bbDeepJetle1b418':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_418_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2018bbDeepJetle1b450':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_450_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2018bbDeepJetle1b500':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_500_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2018bbDeepJetle1b550':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_550_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2018bbDeepJetle1b600':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_600_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2018bbDeepJetle1b650':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_650_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2018bbDeepJetle1b700':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_700_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2018bbDeepJetle1b726':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_726_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2018bbDeepJetle1b752':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_752_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2018bbDeepJetle1b800':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_800_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2018bbDeepJetle1b850':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_850_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2018bbDeepJetle1b900':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_900_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p25Dijet2018bbDeepJetle1b950':
                signalDsName = 'signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p25_bb_13TeV_Spring16_950_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2018bbDeepJetNon124':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_Non/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_124_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2018bbDeepJetle1b49':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_49_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2018bbDeepJetle1b124':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_124_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2018bbDeepJetle1b200':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_200_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2018bbDeepJetle1b277':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_277_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2018bbDeepJetle1b350':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_350_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2018bbDeepJetle1b418':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_418_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2018bbDeepJetle1b450':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_450_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2018bbDeepJetle1b500':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_500_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2018bbDeepJetle1b550':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_550_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2018bbDeepJetle1b600':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_600_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2018bbDeepJetle1b650':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_650_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2018bbDeepJetle1b700':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_700_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2018bbDeepJetle1b726':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_726_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2018bbDeepJetle1b752':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_752_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2018bbDeepJetle1b800':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_800_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2018bbDeepJetle1b850':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_850_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2018bbDeepJetle1b900':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_900_Nominal_Interpolation_rescale.root'

        elif box=='PFNo70DMgq0p2Dijet2018bbDeepJetle1b950':
                signalDsName = 'signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet_central_le1b/ResonanceShapes_DMgq0p2_bb_13TeV_Spring16_950_Nominal_Interpolation_rescale.root'

#EDITSI

        backgroundDsName = {'CaloDijet2015':'inputs/data_CaloScoutingHT_Run2015D_BiasCorrected_CaloDijet2015.root',
                            #'CaloDijet2016':'inputs/data_CaloScoutingHT_Run2016BCD_NewBiasCorrectedFlat_Golden12910pb_CaloDijet2016.root',
                            'CaloDijet2016':'inputs/data_CaloScoutingHT_Run2016BCDEFG_BiasCorrected_Mjj300_Golden27637pb_CaloDijet2016.root',
                            #'PFDijet2016':'inputs/data_PFRECOHT_Run2016BCD_Golden12910pb_PFDijet2016.root',
                            'CaloDijet20152016':'inputs/data_CaloScoutingHT_Run2015D2016B_CaloDijet20152016.root',
                            'PFDijet2016':'inputs/JetHT_run2016_moriond17_red_cert_v2.root',
                            'PFDijetbb20160mt':'inputs/JetHT_run2016_moriond17_red_cert_v2.root',
			    'PF1103Dijet2017bb':'inputs/JetHT_run2017_red_cert_scan.root',
                            'PFDijetbb20161mt':'inputs/JetHT_run2016_moriond17_red_cert_v2.root',
                            'PFDijetbb20162mt':'inputs/JetHT_run2016_moriond17_red_cert_v2.root',
                            'PFDijetbb20160mm':'inputs/JetHT_run2016_moriond17_red_cert_v2.root',
                            'PFDijetbb20161mm':'inputs/JetHT_run2016_moriond17_red_cert_v2.root',
                            'PFDijetbb20162mm':'inputs/JetHT_run2016_moriond17_red_cert_v2.root',
			    'PFDijetbb20162mm2':'inputs/JetHT_run2016_moriond17_red_cert_v2.root',
			    'PFDijetbg20161tt':'inputs/JetHT_run2016_moriond17_red_cert_v2.root',
			    'PFDijetbg20161ttwithW':'inputs/JetHT_run2016_moriond17_red_cert_v2.root',
			    'PFDijetbg20161ttwithoutW':'inputs/JetHT_run2016_moriond17_red_cert_v2.root',
			    'PFDijetbb20162tt':'inputs/JetHT_run2016_moriond17_red_cert_v2.root',
			    'PFDijetbb20162ttQI':'inputs/JetHT_run2016_moriond17_red_cert_v2.root',
                            'PFDijetbg20161ttD':'inputs/JetHT_run2016_moriond17_red_cert_v2_le1.root',
                            'PFDijetbg20161ttG':'inputs/JetHT_run2016_moriond17_red_cert_v2_le1.root',
			    'PFDijetbb20162mmC':'inputs/JetHT_run2016_moriond17_red_cert_v2.root',
                            'PFNo70DMgq0p25Dijet2017bbDeepJetNon100':'inputs/JetHT_run2017_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2017bbDeepJetle1b52':'inputs/JetHT_run2017_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2017bbDeepJetle1b100':'inputs/JetHT_run2017_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2017bbDeepJetle1b152':'inputs/JetHT_run2017_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2017bbDeepJetle1b200':'inputs/JetHT_run2017_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2017bbDeepJetle1b250':'inputs/JetHT_run2017_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2017bbDeepJetle1b303':'inputs/JetHT_run2017_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2017bbDeepJetle1b350':'inputs/JetHT_run2017_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2017bbDeepJetle1b400':'inputs/JetHT_run2017_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2017bbDeepJetle1b450':'inputs/JetHT_run2017_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2017bbDeepJetle1b494':'inputs/JetHT_run2017_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2017bbDeepJetle1b550':'inputs/JetHT_run2017_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2017bbDeepJetle1b580':'inputs/JetHT_run2017_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2017bbDeepJetle1b600':'inputs/JetHT_run2017_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2017bbDeepJetle1b650':'inputs/JetHT_run2017_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2017bbDeepJetle1b700':'inputs/JetHT_run2017_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2017bbDeepJetle1b748':'inputs/JetHT_run2017_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2017bbDeepJetle1b800':'inputs/JetHT_run2017_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2017bbDeepJetle1b850':'inputs/JetHT_run2017_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2017bbDeepJetle1b883':'inputs/JetHT_run2017_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2017bbDeepJetle1b900':'inputs/JetHT_run2017_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2017bbDeepJetle1b969':'inputs/JetHT_run2017_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2017bbDeepJetNon100':'inputs/JetHT_run2017_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2017bbDeepJetle1b52':'inputs/JetHT_run2017_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2017bbDeepJetle1b100':'inputs/JetHT_run2017_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2017bbDeepJetle1b152':'inputs/JetHT_run2017_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2017bbDeepJetle1b200':'inputs/JetHT_run2017_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2017bbDeepJetle1b250':'inputs/JetHT_run2017_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2017bbDeepJetle1b303':'inputs/JetHT_run2017_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2017bbDeepJetle1b350':'inputs/JetHT_run2017_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2017bbDeepJetle1b400':'inputs/JetHT_run2017_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2017bbDeepJetle1b450':'inputs/JetHT_run2017_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2017bbDeepJetle1b494':'inputs/JetHT_run2017_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2017bbDeepJetle1b550':'inputs/JetHT_run2017_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2017bbDeepJetle1b580':'inputs/JetHT_run2017_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2017bbDeepJetle1b600':'inputs/JetHT_run2017_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2017bbDeepJetle1b650':'inputs/JetHT_run2017_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2017bbDeepJetle1b700':'inputs/JetHT_run2017_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2017bbDeepJetle1b748':'inputs/JetHT_run2017_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2017bbDeepJetle1b800':'inputs/JetHT_run2017_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2017bbDeepJetle1b850':'inputs/JetHT_run2017_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2017bbDeepJetle1b883':'inputs/JetHT_run2017_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2017bbDeepJetle1b900':'inputs/JetHT_run2017_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2017bbDeepJetle1b969':'inputs/JetHT_run2017_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2016bbDeepJetNon100':'inputs/JetHT_run2016_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2016bbDeepJetle1b61':'inputs/JetHT_run2016_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2016bbDeepJetle1b100':'inputs/JetHT_run2016_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2016bbDeepJetle1b150':'inputs/JetHT_run2016_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2016bbDeepJetle1b200':'inputs/JetHT_run2016_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2016bbDeepJetle1b221':'inputs/JetHT_run2016_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2016bbDeepJetle1b250':'inputs/JetHT_run2016_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2016bbDeepJetle1b309':'inputs/JetHT_run2016_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2016bbDeepJetle1b350':'inputs/JetHT_run2016_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2016bbDeepJetle1b400':'inputs/JetHT_run2016_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2016bbDeepJetle1b450':'inputs/JetHT_run2016_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2016bbDeepJetle1b500':'inputs/JetHT_run2016_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2016bbDeepJetle1b542':'inputs/JetHT_run2016_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2016bbDeepJetle1b600':'inputs/JetHT_run2016_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2016bbDeepJetle1b632':'inputs/JetHT_run2016_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2016bbDeepJetle1b722':'inputs/JetHT_run2016_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2016bbDeepJetle1b800':'inputs/JetHT_run2016_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2016bbDeepJetle1b848':'inputs/JetHT_run2016_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2016bbDeepJetle1b895':'inputs/JetHT_run2016_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2016bbDeepJetle1b953':'inputs/JetHT_run2016_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2016bbDeepJetNon100':'inputs/JetHT_run2016_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2016bbDeepJetle1b61':'inputs/JetHT_run2016_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2016bbDeepJetle1b100':'inputs/JetHT_run2016_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2016bbDeepJetle1b150':'inputs/JetHT_run2016_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2016bbDeepJetle1b200':'inputs/JetHT_run2016_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2016bbDeepJetle1b221':'inputs/JetHT_run2016_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2016bbDeepJetle1b250':'inputs/JetHT_run2016_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2016bbDeepJetle1b309':'inputs/JetHT_run2016_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2016bbDeepJetle1b350':'inputs/JetHT_run2016_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2016bbDeepJetle1b400':'inputs/JetHT_run2016_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2016bbDeepJetle1b450':'inputs/JetHT_run2016_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2016bbDeepJetle1b500':'inputs/JetHT_run2016_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2016bbDeepJetle1b542':'inputs/JetHT_run2016_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2016bbDeepJetle1b600':'inputs/JetHT_run2016_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2016bbDeepJetle1b632':'inputs/JetHT_run2016_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2016bbDeepJetle1b722':'inputs/JetHT_run2016_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2016bbDeepJetle1b800':'inputs/JetHT_run2016_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2016bbDeepJetle1b848':'inputs/JetHT_run2016_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2016bbDeepJetle1b895':'inputs/JetHT_run2016_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2016bbDeepJetle1b953':'inputs/JetHT_run2016_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2018bbDeepJetNon124':'inputs/JetHT_run2018_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2018bbDeepJetle1b49':'inputs/JetHT_run2018_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2018bbDeepJetle1b124':'inputs/JetHT_run2018_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2018bbDeepJetle1b200':'inputs/JetHT_run2018_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2018bbDeepJetle1b277':'inputs/JetHT_run2018_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2018bbDeepJetle1b350':'inputs/JetHT_run2018_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2018bbDeepJetle1b418':'inputs/JetHT_run2018_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2018bbDeepJetle1b450':'inputs/JetHT_run2018_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2018bbDeepJetle1b500':'inputs/JetHT_run2018_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2018bbDeepJetle1b550':'inputs/JetHT_run2018_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2018bbDeepJetle1b600':'inputs/JetHT_run2018_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2018bbDeepJetle1b650':'inputs/JetHT_run2018_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2018bbDeepJetle1b700':'inputs/JetHT_run2018_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2018bbDeepJetle1b726':'inputs/JetHT_run2018_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2018bbDeepJetle1b752':'inputs/JetHT_run2018_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2018bbDeepJetle1b800':'inputs/JetHT_run2018_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2018bbDeepJetle1b850':'inputs/JetHT_run2018_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2018bbDeepJetle1b900':'inputs/JetHT_run2018_red_cert_scan.root',

                            'PFNo70DMgq0p25Dijet2018bbDeepJetle1b950':'inputs/JetHT_run2018_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2018bbDeepJetNon124':'inputs/JetHT_run2018_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2018bbDeepJetle1b49':'inputs/JetHT_run2018_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2018bbDeepJetle1b124':'inputs/JetHT_run2018_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2018bbDeepJetle1b200':'inputs/JetHT_run2018_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2018bbDeepJetle1b277':'inputs/JetHT_run2018_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2018bbDeepJetle1b350':'inputs/JetHT_run2018_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2018bbDeepJetle1b418':'inputs/JetHT_run2018_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2018bbDeepJetle1b450':'inputs/JetHT_run2018_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2018bbDeepJetle1b500':'inputs/JetHT_run2018_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2018bbDeepJetle1b550':'inputs/JetHT_run2018_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2018bbDeepJetle1b600':'inputs/JetHT_run2018_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2018bbDeepJetle1b650':'inputs/JetHT_run2018_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2018bbDeepJetle1b700':'inputs/JetHT_run2018_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2018bbDeepJetle1b726':'inputs/JetHT_run2018_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2018bbDeepJetle1b752':'inputs/JetHT_run2018_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2018bbDeepJetle1b800':'inputs/JetHT_run2018_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2018bbDeepJetle1b850':'inputs/JetHT_run2018_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2018bbDeepJetle1b900':'inputs/JetHT_run2018_red_cert_scan.root',

                            'PFNo70DMgq0p2Dijet2018bbDeepJetle1b950':'inputs/JetHT_run2018_red_cert_scan.root',

#EDITBG
                            }





        blindString = ''
        if options.blind:
            blindString = '--noFitAsimov --run expected'

        sysString = ''
        if options.noSys and options.deco:
            sysString = '-S 0 --freezeNuisances=shapeBkg_%s_bkg_deco_%s__norm,deco_%s_eig1,deco_%s_eig2,deco_%s_eig3,jes,jer,lumi'%(box,box,box,box,box)
        elif options.noSys:
            sysString = '-S 0 --freezeNuisances=shapeBkg_%s_bkg_%s__norm,p1_%s,p2_%s,p3_%s,jes,jer,lumi'%(box,box,box,box,box)
        elif options.multi and options.fitPdf!='all':
            sysString = '--setPhysicsModelParameters pdf_index=%i --freezeNuisances pdf_index'%(pdfIndexMap[options.fitPdf])
            if options.fitPdf != 'fiveparam':
                sysString += ',p51_CaloDijet2016,p52_CaloDijet2016,p53_CaloDijet2016,p54_CaloDijet2016'
            if options.fitPdf != 'modexp':
                sysString += ',pm1_CaloDijet2016,pm2_CaloDijet2016,pm3_CaloDijet2016,pm4_CaloDijet2016'
            if options.fitPdf != 'atlas':
                sysString += ',pa1_CaloDijet2016,pa2_CaloDijet2016,pa3_CaloDijet2016,pa4_CaloDijet2016'

        sysStringList.append(sysString)

        decoString = ''
        if options.deco:
            decoString  ='--deco'

        multiString = ''
        if options.multi:
            decoString  ='--multi'

        for massPoint in massIterable(options.mass):
            exec_me('python python/WriteDataCard_btag_22018.py -m %s --mass %s -i %s -l %f -c %s -b %s -d %s %s %s %s %s %s %s %s'%(model, massPoint, options.inputFitFile,1000*lumi,options.config,box,options.outDir,signalDsName,backgroundDsName[box],penaltyString,signalSys,xsecString,decoString,multiString),options.dryRun)
            if options.bayes:
                rRangeString =  '--setPhysicsModelParameterRanges '
                if options.deco:
                    rRangeString += 'shapeBkg_%s_bkg_deco_%s__norm=%f,%f'%(box,box,1-NSIGMA*paramDict['Ntot_bkg_%s'%box][1]/paramDict['Ntot_bkg_%s'%box][0],1+NSIGMA*paramDict['Ntot_bkg_%s'%box][1]/paramDict['Ntot_bkg_%s'%box][0])
                    rRangeString += ':deco_%s_eig1=%f,%f'%(box,-1.0*NSIGMA,NSIGMA)
                    rRangeString += ':deco_%s_eig2=%f,%f'%(box,-1.0*NSIGMA,NSIGMA)
                    rRangeString += ':deco_%s_eig3=%f,%f'%(box,-1.0*NSIGMA,NSIGMA)
                else:
                    rRangeString += 'shapeBkg_%s_bkg_%s__norm=%f,%f'%(box,box,1-NSIGMA*paramDict['Ntot_bkg_%s'%box][1]/paramDict['Ntot_bkg_%s'%box][0],1+NSIGMA*paramDict['Ntot_bkg_%s'%box][1]/paramDict['Ntot_bkg_%s'%box][0])
                    rRangeString += ':p1_%s=%f,%f'%(box,paramDict['p1_%s'%box][0]-NSIGMA*paramDict['p1_%s'%box][1],paramDict['p1_%s'%box][0]+NSIGMA*paramDict['p1_%s'%box][1])
                    rRangeString += ':p2_%s=%f,%f'%(box,paramDict['p2_%s'%box][0]-NSIGMA*paramDict['p2_%s'%box][1],paramDict['p2_%s'%box][0]+NSIGMA*paramDict['p2_%s'%box][1])
                    rRangeString += ':p3_%s=%f,%f'%(box,paramDict['p3_%s'%box][0]-NSIGMA*paramDict['p3_%s'%box][1],paramDict['p3_%s'%box][0]+NSIGMA*paramDict['p3_%s'%box][1])
                if options.rMax>-1:
                    rRangeString += ':r=0,%f'%(options.rMax)
                rRangeStringList.append(rRangeString)
                toyString = ''
                if options.toys>-1:
                    toyString = '-t %i -s -1'%options.toys
                if len(boxes)==1:
  		  
                   exec_me('combine -M MarkovChainMC -H Asymptotic %s/dijet_combine_%s_%s_lumi-%.3f_%s.txt -n %s_%s_lumi-%.3f_%s --tries 20 --proposal ortho --burnInSteps 200 --iteration 30000 --propHelperWidthRangeDivisor 10 %s %s %s %s'%(options.outDir,model,massPoint,lumi,box,model,massPoint,lumi,box,rRangeString,blindString,sysString,toyString),options.dryRun)
                   exec_me('mv higgsCombine%s_%s_lumi-%.3f_%s.MarkovChainMC.mH120*root %s/'%(model,massPoint,lumi,box,options.outDir),options.dryRun)
            else:
                if signif:
                    rRangeString = ''
                    if options.rMax>-1:
                        rRangeString = '--setPhysicsModelParameterRanges r=0,%f'%(options.rMax)
                        rRangeStringList.append(rRangeString)
                    if len(boxes)==1:
                        exec_me('combine -M ProfileLikelihood --signif %s/dijet_combine_%s_%s_lumi-%.3f_%s.txt -n %s_%s_lumi-%.3f_%s %s %s'%(options.outDir,model,massPoint,lumi,box,model,massPoint,lumi,box,rRangeString,sysString),options.dryRun)
                        exec_me('mv higgsCombine%s_%s_lumi-%.3f_%s.ProfileLikelihood.mH120.root %s/'%(model,massPoint,lumi,box,options.outDir),options.dryRun)
                else:
                    rRangeString = ''
                    if options.rMax>-1:
                        rRangeString =  '--setPhysicsModelParameterRanges r=0,%f'%(options.rMax)
                        rRangeStringList.append(rRangeString)
                    if len(boxes)==1:
			print('combine -M Asymptotic -H ProfileLikelihood %s/dijet_combine_%s_%s_lumi-%.3f_%s.txt -n %s_%s_lumi-%.3f_%s --minimizerTolerance %f --minimizerStrategy %i %s --saveWorkspace %s %s'%(options.outDir,model,massPoint,lumi,box,model,massPoint,lumi,box,options.min_tol,options.min_strat,rRangeString,blindString,sysString),options.dryRun)
                        exec_me('combine -M Asymptotic -H ProfileLikelihood %s/dijet_combine_%s_%s_lumi-%.3f_%s.txt -n %s_%s_lumi-%.3f_%s --minimizerTolerance %f --minimizerStrategy %i %s --saveWorkspace %s %s'%(options.outDir,model,massPoint,lumi,box,model,massPoint,lumi,box,options.min_tol,options.min_strat,rRangeString,blindString,sysString),options.dryRun)
                        exec_me('mv higgsCombine%s_%s_lumi-%.3f_%s.Asymptotic.mH120.root %s/'%(model,massPoint,lumi,box,options.outDir),options.dryRun)
    if len(boxes)>1:
        lumiTotal = sum(lumiFloat)
        for box,lumi in zip(boxes,lumiFloat): exec_me('cp %s/dijet_combine_%s_%s_lumi-%.3f_%s.txt .'%(options.outDir,model,massPoint,lumi,box),options.dryRun)
        cmds = ['%s=dijet_combine_%s_%s_lumi-%.3f_%s.txt'%(box,model,massPoint,lumi,box) for box,lumi in zip(boxes,lumiFloat)]
        exec_me('combineCards.py %s > %s/dijet_combine_%s_%s_lumi-%.3f_%s.txt'%(' '.join(cmds),options.outDir,model,massPoint,lumiTotal,options.box),options.dryRun)
        exec_me('cat %s/dijet_combine_%s_%s_lumi-%.3f_%s.txt'%(options.outDir,model,massPoint,lumiTotal,options.box),options.dryRun)
        if options.bayes:
            rRangeStringListMod = [rRangeString.replace('--setPhysicsModelParameterRanges ','') for rRangeString in rRangeStringList ]
            paramRangeList = []
            for listMod in rRangeStringListMod:
                paramRangeList.extend(listMod.split(':'))
            paramRangeList = list(set(paramRangeList))
            rRangeStringTotal = ''
            if options.deco or rMax>=-1:
                rRangeStringTotal = '--setPhysicsModelParameterRanges ' + ','.join(paramRangeList)

            sysStringListMod = [sysString.replace('-S 0 --freezeNuisances=','') for sysString in sysStringList ]
            paramFreezeList = []
            for listMod in sysStringListMod:
                paramFreezeList.extend(listMod.split(','))
            paramFreezeList = list(set(paramFreezeList))
            sysStringTotal = ''
            if options.noSys:
                sysStringTotal = '-S 0 --freezeNuisances=' + ','.join(paramFreezeList)
            exec_me('combine -M MarkovChainMC -H Asymptotic %s/dijet_combine_%s_%s_lumi-%.3f_%s.txt -n %s_%s_lumi-%.3f_%s --tries 30 --proposal ortho --burnInSteps 1000 --iteration 40000 --propHelperWidthRangeDivisor 10 %s %s %s %s'%(options.outDir,model,massPoint,lumiTotal,options.box,model,massPoint,lumiTotal,options.box,rRangeStringTotal,blindString,sysStringTotal,toyString),options.dryRun)
            exec_me('mv higgsCombine%s_%s_lumi-%.3f_%s.MarkovChainMC.mH120*root %s/'%(model,massPoint,lumiTotal,options.box,options.outDir),options.dryRun)
        else:
            if signif:
                rRangeString = ''
                if options.rMax>-1:
                    rRangeString = '--setPhysicsModelParameterRanges r=0,%f'%(options.rMax)
                exec_me('combine -M ProfileLikelihood --signif %s/dijet_combine_%s_%s_lumi-%.3f_%s.txt -n %s_%s_lumi-%.3f_%s %s %s'%(options.outDir,model,massPoint,lumiTotal,options.box,model,massPoint,lumiTotal,options.box,rRangeString,sysString),options.dryRun)
                exec_me('mv higgsCombine%s_%s_lumi-%.3f_%s.ProfileLikelihood.mH120.root %s/'%(model,massPoint,lumiTotal,options.box,options.outDir),options.dryRun)
            else:
                rRangeString = ''
                if options.rMax>-1:
                    rRangeString =  '--setPhysicsModelParameterRanges r=0,%f'%(options.rMax)
                exec_me('combine -M Asymptotic -H ProfileLikelihood %s/dijet_combine_%s_%s_lumi-%.3f_%s.txt -n %s_%s_lumi-%.3f_%s --minimizerTolerance %f --minimizerStrategy %i %s --saveWorkspace %s %s'%(options.outDir,model,massPoint,lumiTotal,options.box,model,massPoint,lumiTotal,options.box,options.min_tol,options.min_strat,rRangeString,blindString,sysString),options.dryRun)
                exec_me('mv higgsCombine%s_%s_lumi-%.3f_%s.Asymptotic.mH120.root %s/'%(model,massPoint,lumiTotal,options.box,options.outDir),options.dryRun)
            for box,lumi in zip(boxes,lumiFloat): exec_me('rm dijet_combine_%s_%s_lumi-%.3f_%s.txt'%(model,massPoint,lumi,box),options.dryRun)

if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option('-c','--config',dest="config",type="string",default="config/run2.config",
                  help="Name of the config file to use")
    parser.add_option('-b','--box',dest="box", default="CaloDijet",type="string",
                  help="box name")
    parser.add_option('-m','--model',dest="model", default="gg",type="string",
                  help="signal model name")
    parser.add_option('--mass',dest="mass", default='750',type="string",
                  help="mass of resonance")
    parser.add_option('-l','--lumi',dest="lumi", default="1.918",type="string",
                  help="lumi in fb^-1, possibly for different channels e.g.: 1.918_2.590")
    parser.add_option('--signif',dest="signif",default=False,action='store_true',
                  help="calculate significance instead of limit")
    parser.add_option('-d','--dir',dest="outDir",default="./",type="string",
                  help="Output directory to store cards")
    parser.add_option('--min-tol',dest="min_tol",default=0.001,type="float",
                  help="minimizer tolerance (default = 0.001)")
    parser.add_option('--min-strat',dest="min_strat",default=2,type="int",
                  help="minimizer strategy (default = 2)")
    parser.add_option('--dry-run',dest="dryRun",default=False,action='store_true',
                  help="Just print out commands to run")
    parser.add_option('--penalty',dest="penalty",default=False,action='store_true',
                  help="penalty terms on background parameters")
    parser.add_option('-i','--input-fit-file',dest="inputFitFile", default='FitResults/BinnedFitResults.root',type="string",
                  help="input fit file")
    parser.add_option('--no-signal-sys',dest="noSignalSys",default=False,action='store_true',
                  help="do not create signal shape systematic histograms / uncertainties")
    parser.add_option('--no-sys',dest="noSys",default=False,action='store_true',
                  help="no systematic uncertainties when running combine")
    parser.add_option('--blind',dest="blind",default=False,action='store_true',
                  help="run only blinded expected limits")
    parser.add_option('--rMax',dest="rMax",default=-1,type="float",
                  help="maximum r value (for better precision)")
    parser.add_option('--xsec',dest="xsec",default=1,type="float",
                  help="xsec for signal in pb (r = 1)")
    parser.add_option('-j','--jobs',dest="jobs",default=0,type="int",
                  help="number of jobs to submit when running toys for each mass point (just set to 1 for observed limits)")
    parser.add_option('--bayes',dest="bayes",default=False,action='store_true',
                  help="bayesian limits")
    parser.add_option('--deco',dest="deco",default=False,action='store_true',
                  help="decorrelate shape parameters")
    parser.add_option('--tag',dest="tag", default='master',type="string",
                  help="tag for repository")
    parser.add_option('-q','--queue',dest="queue",default="1nh",type="string",
                  help="queue: 1nh, 8nh, 1nd, etc.")
    parser.add_option('-t','--toys',dest="toys",default=-1,type="int",
                  help="number of toys per job(for bayesian expected limits)")
    parser.add_option('--multi',dest="multi",default=False,action='store_true',
                  help="using RooMultiPdf for total background")
    parser.add_option('--fit-pdf',dest="fitPdf", default="all", choices=['all','modexp','fiveparam','atlas'],
                  help="pdf for fitting")


    (options,args) = parser.parse_args()


    if options.jobs:
        submit_jobs(options,args)
    else:
        main(options,args)
