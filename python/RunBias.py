from optparse import OptionParser
import ROOT as rt
import rootTools
from framework import Config
from array import *
import os
import sys
from RunCombine import massIterable
import glob
        
def exec_me(command,dryRun=True):
    print command
    if not dryRun: os.system(command)

if __name__ == '__main__':
    
    parser = OptionParser()
    parser.add_option('-c','--config',dest="config",type="string",default="config/dijet_bias.config",
                  help="Name of the config file to use")
    parser.add_option('-b','--box',dest="box", default="CaloDijet2016",type="string",
                  help="box name")
    parser.add_option('-m','--model',dest="model", default="qq",type="string",
                  help="signal model name")
    parser.add_option('--mass',dest="mass", default='750',type="string",
                  help="mass of resonance")
    parser.add_option('-l','--lumi',dest="lumi", default="12.910",type="string",
                  help="lumi in fb^-1, e.g.: 12.910")
    parser.add_option('--dry-run',dest="dryRun",default=False,action='store_true',
                  help="Just print out commands to run")
    parser.add_option('--rMax',dest="rMax",default=20,type="float",
                  help="maximum r value (for better precision)")
    parser.add_option('-r',dest="r",default=1,type="float",
                  help="expect signal r value")
    parser.add_option('--rMin',dest="rMin",default=-20,type="float",
                  help="minimum r value (for better precision)")
    parser.add_option('--xsec',dest="xsec",default=10,type="float",
                  help="xsec for signal in pb (r = 1)")
    parser.add_option('-i','--input-fit-file',dest="inputFitFile", default='inputs/DijetFitResults.root',type="string",
                  help="input fit file")
    parser.add_option('-d','--dir',dest="outDir",default="./",type="string",
                  help="Output directory to store everything")
    parser.add_option('-t','--toys',dest="toys",default=1000,type="int",
                  help="number of toys")    
    parser.add_option('--gen-pdf',dest="genPdf", default="expow1", choices=['dijet','expow1','invpow1','invpowlin1','moddijet1'],
                  help="pdf for generating")
    parser.add_option('--fit-pdf',dest="fitPdf", default="dijet", choices=['dijet','expow1','invpow1','invpowlin1','moddijet1'],
                  help="pdf for fitting")
    parser.add_option('--asymptotic-file',dest="asymptoticFile",default=None,type="string",
                  help="load asymptotic cross section results file")
    parser.add_option('--year',dest="year",default="2017",type="string",
                  help="year")
    
    (options,args) = parser.parse_args()

    pdfIndexMap = {'dijet': 0,
                   'expow1': 1,
                   'invpow1': 2,
                   'invpowlin1': 3
                   #'moddijet1': 4,
                   }

    box = options.box
    lumi = float(options.lumi)
    model = options.model
    
    backgroundDsName = {'DiPhotons_kMpl001_EBEB': 'output/InputShapes_data_EBEB_%s.root' % options.year,
                        'DiPhotons_kMpl001_EBEE': 'output/InputShapes_data_EBEE_%s.root' % options.year,
                        'DiPhotons_kMpl01_EBEB': 'output/InputShapes_data_EBEB_%s.root' % options.year,
                        'DiPhotons_kMpl01_EBEE': 'output/InputShapes_data_EBEE_%s.root' % options.year,
                        'DiPhotons_kMpl02_EBEB': 'output/InputShapes_data_EBEB_%s.root' % options.year,
                        'DiPhotons_kMpl02_EBEE': 'output/InputShapes_data_EBEE_%s.root' % options.year,                       
                        'DiPhotons_0p014_EBEB': 'output/InputShapes_data_EBEB_%s.root' % options.year,
                        'DiPhotons_0p014_EBEE': 'output/InputShapes_data_EBEE_%s.root' % options.year,
                        'DiPhotons_1p4_EBEB': 'output/InputShapes_data_EBEB_%s.root' % options.year,
                        'DiPhotons_1p4_EBEE': 'output/InputShapes_data_EBEE_%s.root' % options.year,
                        'DiPhotons_5p6_EBEB': 'output/InputShapes_data_EBEB_%s.root' % options.year,
                        'DiPhotons_5p6_EBEE': 'output/InputShapes_data_EBEE_%s.root' % options.year
                        }
    
    signalDsName = ''
    if 'DiPhotons' in box:
        if 'kMpl' in box: 
            signalDsName = '/afs/cern.ch/work/a/apsallid/CMS/Hgg/exodiphotons/seconditeration/CMSSW_10_2_13/src/diphoton-analysis/DijetShapeInterpolator/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_%s_%s_%s.root'% (box.split("_")[-2], box.split("_")[-1], options.year)
        else: 
            signalDsName = '/afs/cern.ch/work/a/apsallid/CMS/Hgg/exodiphotons/seconditeration/CMSSW_10_2_13/src/diphoton-analysis/DijetShapeInterpolator/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_%s_%s_%s.root'% (box.split("_")[-2], box.split("_")[-1], options.year)

            
    signalSys = ''    
    '''
    if box=='CaloDijet2016':
        signalSys  =   '--jesUp inputs/ResonanceShapes_%s_13TeV_CaloScouting_Spring16_JESUP.root --jesDown inputs/ResonanceShapes_%s_13TeV_CaloScouting_Spring16_JESDOWN.root'%(model,model)
        signalSys += ' --jerUp inputs/ResonanceShapes_%s_13TeV_CaloScouting_Spring16_JERUP.root --jerDown inputs/ResonanceShapes_%s_13TeV_CaloScouting_Spring16_JERDOWN.root'%(model,model)
    elif box=='PFDijet2016':
        signalSys  =   '--jesUp inputs/ResonanceShapes_%s_13TeV_Spring16_JESUP.root --jesDown inputs/ResonanceShapes_%s_13TeV_Spring16_JESDOWN.root'%(model,model)
        signalSys += ' --jerUp inputs/ResonanceShapes_%s_13TeV_Spring16_JERUP.root'%(model)
    '''
    if 'DiPhotons' in box:
        if 'kMpl' in box: 
            signalSys  =   '--eneScStatUp /afs/cern.ch/work/a/apsallid/CMS/Hgg/exodiphotons/seconditeration/CMSSW_10_2_13/src/diphoton-analysis/DijetShapeInterpolator/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_%s_%s_%s_energyScaleStatUp.root --eneScStatDown /afs/cern.ch/work/a/apsallid/CMS/Hgg/exodiphotons/seconditeration/CMSSW_10_2_13/src/diphoton-analysis/DijetShapeInterpolator/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_%s_%s_%s_energyScaleStatDown.root'% (box.split("_")[-2], box.split("_")[-1], options.year, box.split("_")[-2], box.split("_")[-1], options.year) 
            signalSys  +=   ' --eneScSystUp /afs/cern.ch/work/a/apsallid/CMS/Hgg/exodiphotons/seconditeration/CMSSW_10_2_13/src/diphoton-analysis/DijetShapeInterpolator/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_%s_%s_%s_energyScaleSystUp.root --eneScSystDown /afs/cern.ch/work/a/apsallid/CMS/Hgg/exodiphotons/seconditeration/CMSSW_10_2_13/src/diphoton-analysis/DijetShapeInterpolator/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_%s_%s_%s_energyScaleSystDown.root'% (box.split("_")[-2], box.split("_")[-1], options.year, box.split("_")[-2], box.split("_")[-1], options.year) 
            signalSys  +=   ' --eneScGainUp /afs/cern.ch/work/a/apsallid/CMS/Hgg/exodiphotons/seconditeration/CMSSW_10_2_13/src/diphoton-analysis/DijetShapeInterpolator/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_%s_%s_%s_energyScaleGainUp.root --eneScGainDown /afs/cern.ch/work/a/apsallid/CMS/Hgg/exodiphotons/seconditeration/CMSSW_10_2_13/src/diphoton-analysis/DijetShapeInterpolator/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_%s_%s_%s_energyScaleGainDown.root'% (box.split("_")[-2], box.split("_")[-1], options.year, box.split("_")[-2], box.split("_")[-1], options.year) 
            signalSys  +=   ' --eneScSigmaUp /afs/cern.ch/work/a/apsallid/CMS/Hgg/exodiphotons/seconditeration/CMSSW_10_2_13/src/diphoton-analysis/DijetShapeInterpolator/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_%s_%s_%s_energySigmaUp.root --eneScSigmaDown /afs/cern.ch/work/a/apsallid/CMS/Hgg/exodiphotons/seconditeration/CMSSW_10_2_13/src/diphoton-analysis/DijetShapeInterpolator/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_%s_%s_%s_energySigmaDown.root'% (box.split("_")[-2], box.split("_")[-1], options.year, box.split("_")[-2], box.split("_")[-1], options.year) 
        else: 
            signalSys  =   '--eneScStatUp /afs/cern.ch/work/a/apsallid/CMS/Hgg/exodiphotons/seconditeration/CMSSW_10_2_13/src/diphoton-analysis/DijetShapeInterpolator/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_%s_%s_%s_energyScaleStatUp.root --eneScStatDown /afs/cern.ch/work/a/apsallid/CMS/Hgg/exodiphotons/seconditeration/CMSSW_10_2_13/src/diphoton-analysis/DijetShapeInterpolator/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_%s_%s_%s_energyScaleStatDown.root'% (box.split("_")[-2], box.split("_")[-1], options.year, box.split("_")[-2], box.split("_")[-1], options.year) 
            signalSys  +=   ' --eneScSystUp /afs/cern.ch/work/a/apsallid/CMS/Hgg/exodiphotons/seconditeration/CMSSW_10_2_13/src/diphoton-analysis/DijetShapeInterpolator/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_%s_%s_%s_energyScaleSystUp.root --eneScSystDown /afs/cern.ch/work/a/apsallid/CMS/Hgg/exodiphotons/seconditeration/CMSSW_10_2_13/src/diphoton-analysis/DijetShapeInterpolator/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_%s_%s_%s_energyScaleSystDown.root'% (box.split("_")[-2], box.split("_")[-1], options.year, box.split("_")[-2], box.split("_")[-1], options.year) 
            signalSys  +=   ' --eneScGainUp /afs/cern.ch/work/a/apsallid/CMS/Hgg/exodiphotons/seconditeration/CMSSW_10_2_13/src/diphoton-analysis/DijetShapeInterpolator/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_%s_%s_%s_energyScaleGainUp.root --eneScGainDown /afs/cern.ch/work/a/apsallid/CMS/Hgg/exodiphotons/seconditeration/CMSSW_10_2_13/src/diphoton-analysis/DijetShapeInterpolator/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_%s_%s_%s_energyScaleGainDown.root'% (box.split("_")[-2], box.split("_")[-1], options.year, box.split("_")[-2], box.split("_")[-1], options.year) 
            signalSys  +=   ' --eneScSigmaUp /afs/cern.ch/work/a/apsallid/CMS/Hgg/exodiphotons/seconditeration/CMSSW_10_2_13/src/diphoton-analysis/DijetShapeInterpolator/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_%s_%s_%s_energySigmaUp.root --eneScSigmaDown /afs/cern.ch/work/a/apsallid/CMS/Hgg/exodiphotons/seconditeration/CMSSW_10_2_13/src/diphoton-analysis/DijetShapeInterpolator/ResonanceShapes_InputShapes_GluGluSpin0ToGammaGamma_W_%s_%s_%s_energySigmaDown.root'% (box.split("_")[-2], box.split("_")[-1], options.year, box.split("_")[-2], box.split("_")[-1], options.year) 

    xsecTree = None
    rDict = {}
    if options.asymptoticFile is not None:
        print "INFO: Input ref xsec file!"
        asymptoticRootFile = rt.TFile.Open(options.asymptoticFile,"READ")
        xsecTree = asymptoticRootFile.Get("xsecTree")        
        xsecTree.Draw('>>elist','','entrylist')
        elist = rt.gDirectory.Get('elist')
        entry = -1
        while True:
            entry = elist.Next()
            if entry == -1: break
            xsecTree.GetEntry(entry)
            rDict[int(eval('xsecTree.mass'))] = eval('xsecTree.xsecULExp_%s'%box)/options.xsec
    else:        
        for massPoint in massIterable(options.mass):   
            rDict[int(massPoint)] = options.r
    print rDict
        
    #xsecString = '--xsec %f'%options.xsec
    rRangeString =  '--setParameterRanges r=%.3f,%.3f'%(options.rMin,options.rMax)

    fixStringGen = '--setParameters pdf_index=%i'%(pdfIndexMap[options.genPdf])
    freezeStringGen = '--freezeParameters pdf_index'
    
    #if options.genPdf != 'dijet':
    #    freezeStringGen += ',p1_%s,p2_%s' % (box,box)
    #if options.genPdf != 'expow1':
    #    freezeStringGen += ',pex1_1_%s,pex1_2_%s' % (box,box)
    #if options.genPdf != 'invpow1':
    #    freezeStringGen += ',pip1_1_%s,pip1_2_%s' % (box,box)
    #if options.genPdf != 'invpowlin1':
    #    freezeStringGen += ',pil1_1_%s,pil1_2_%s,pil1_3_%s' % (box,box,box)
    #if options.genPdf != 'moddijet1':
    #    freezeStringGen += ',pmd1_1_%s,pmd1_2_%s,pmd1_3_%s,pmd1_4_%s' % (box,box,box,box)
    if options.genPdf == 'dijet':
        freezeStringGen += ',p1_%s,p2_%s' % (box,box)
    if options.genPdf == 'expow1':
        freezeStringGen += ',pex1_1_%s,pex1_2_%s' % (box,box)
    if options.genPdf == 'invpow1':
        freezeStringGen += ',pip1_1_%s,pip1_2_%s' % (box,box)
    if options.genPdf == 'invpowlin1':
        freezeStringGen += ',pil1_1_%s,pil1_2_%s,pil1_3_%s' % (box,box,box)
    #if options.genPdf == 'moddijet1':
    #    freezeStringGen += ',pmd1_1_%s,pmd1_2_%s,pmd1_3_%s,pmd1_4_%s' % (box,box,box,box)
    
        
    fixStringFit = '--setParameters pdf_index=%i'%(pdfIndexMap[options.fitPdf])
    freezeStringFit = '--freezeParameters pdf_index'
    if options.fitPdf != 'dijet':
        freezeStringFit += ',p1_%s,p2_%s' % (box,box)
    if options.fitPdf != 'expow1':
        freezeStringFit += ',pex1_1_%s,pex1_2_%s' % (box,box)
    if options.fitPdf != 'invpow1':
        freezeStringFit += ',pip1_1_%s,pip1_2_%s' % (box,box)
    if options.fitPdf != 'invpowlin1':
        freezeStringFit += ',pil1_1_%s,pil1_2_%s,pil1_3_%s' % (box,box,box)
    #if options.fitPdf != 'moddijet1':
    #    freezeStringFit += ',pmd1_1_%s,pmd1_2_%s,pmd1_3_%s,pmd1_4_%s' % (box,box,box,box)
    
    for massPoint in massIterable(options.mass):        
        exec_me('python python/WriteDataCard.py -m %s --year %s --mass %s %s -i %s -l %f -c %s -b %s -d %s %s %s --multi'%(model, options.year, massPoint,backgroundDsName[box], options.inputFitFile,1000*lumi,options.config,box,options.outDir, signalDsName,signalSys),options.dryRun)
        exec_me('combine -M GenerateOnly %s/diphoton_combine_%i_%s_%s.txt -n %s_r-%.3f_%s_%s_%s_%s %s %s %s --bypassFrequentistFit --seed -1 --saveToys --expectSignal %.3f -t %i'%(options.outDir,int(massPoint),box,options.year,int(massPoint),rDict[int(massPoint)],box,options.genPdf,options.fitPdf,options.year,rRangeString,fixStringGen,freezeStringGen,rDict[int(massPoint)],options.toys),options.dryRun)

        toysfile = glob.glob('./higgsCombine%s_r-%.3f_%s_%s_%s_%s.GenerateOnly.mH*.root' %(int(massPoint),rDict[int(massPoint)],box,options.genPdf,options.fitPdf,options.year))

        exec_me('combine -M FitDiagnostics --robustFit=1 %s/diphoton_combine_%i_%s_%s.txt -n %s_r-%.3f_%s_%s_%s_%s --toysFile %s -t %i %s %s %s --cminDefaultMinimizerStrategy=2 --saveWorkspace -v -1'%(
            options.outDir,int(massPoint),box,options.year,
            int(massPoint),rDict[int(massPoint)],box,options.genPdf,options.fitPdf,options.year,
            toysfile[0],
            options.toys,
            rRangeString,fixStringFit,freezeStringFit),
                options.dryRun)

        exec_me('mv %s %s/.'%(toysfile[0],options.outDir),options.dryRun)
       #Test one by one. See if the above work and then uncomment
         #exec_me('mv higgsCombine%s_%s_lumi-%.3f_r-%.3f_%s_%s_%s.MaxLikelihoodFit.mH120.123456.root %s/'%(model,massPoint,lumi,rDict[int(massPoint)],box,options.genPdf,options.fitPdf,options.outDir),options.dryRun)
        #exec_me('mv mlfit%s_%s_lumi-%.3f_r-%.3f_%s_%s_%s.root %s/'%(model,massPoint,lumi,rDict[int(massPoint)],box,options.genPdf,options.fitPdf,options.outDir),options.dryRun)

#toysfile=`ls |grep GenerateOnly`


#mv fitDiagnostics_${THEINSIGNAME}_mu${THEMUIN}_${THECOUP}_${THEMODEL}_${THEMASS}.root fitDiagnostics_${THEINSIGNAME}_mu${THEMUIN}_${THECOUP}_${THEMODEL}_${THEMASS}_${CURRENTTOY}.root

#cp fitDiagnostics_${THEINSIGNAME}_mu${THEMUIN}_${THECOUP}_${THEMODEL}_${THEMASS}_${CURRENTTOY}.root ${THEINOUTPATH}/${THECOUP}/mu${THEMUIN}/${THEMODEL}/mass${THEMASS}/.
