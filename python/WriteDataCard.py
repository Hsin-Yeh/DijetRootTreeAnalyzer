from optparse import OptionParser
import ROOT as rt
import rootTools
from framework import Config
from array import *
import os
import sys
import pandas as pd

def getNormalization():    
    norm = pd.read_csv('/afs/cern.ch/work/a/apsallid/CMS/Hgg/exodiphotons/seconditeration/CMSSW_10_2_13/src/diphoton-analysis/SignalNorm.txt', sep=" ", header=None)
    norm.columns = ["Year", "Coupling", "MassPoint", "Category", "Norm"]
    norm.Year = norm.Year.astype(str)
    norm.Coupling = norm.Coupling.astype(str)
    norm.MassPoint = norm.MassPoint.astype(int)
    norm.Category = norm.Category.astype(str)
    norm.Norm = norm.Norm.astype(float)

    print(norm)

    return norm

def luminosityErrorFrac(year):

    lumierror = {}
    
    lumierror["2015"] =  0.023
    lumierror["2016"] =  0.025
    lumierror["2017"] =  0.023
    lumierror["2018"] =  0.025
    lumierror["2018_newjson"] =  0.025
    lumierror["2018ABC_prompt"] =  0.025
    lumierror["2018ABC_rereco"] =  0.025
    lumierror["2018AB"] =  0.025
    lumierror["2018ABC"] =  0.025
    lumierror["2018CD"] =  0.025
    lumierror["2018D"] =  0.025

    return 1. + lumierror[year]

def getDownFromUpNom(hUp,hNom):

    hDown = hUp.Clone(hUp.GetName().replace('Up','Down'))    
    for i in range(1,hDown.GetNbinsX()+1):
        nom = hNom.GetBinContent(i)
        up = hUp.GetBinContent(i)
        if up > 0:
            down = nom*nom / up 
            hDown.SetBinContent(i, down)
        else:
            hDown.SetBinContent(i, 0)

    return hDown

    

def fixPars(w, label, doFix=True, setVal=None):
    parSet = w.allVars()
    for par in rootTools.RootIterator.RootIterator(parSet):
        if label in par.GetName():
            par.setConstant(doFix)
            if setVal is not None: par.setVal(setVal)

def initializeWorkspace(w,cfg,box,scaleFactor=1.,penalty=False,multi=False,x=None,emptyHist1D=None):
    
    if x is None:
        x = array('d', cfg.getBinning(box)[0]) # mjj binning
    nBins = len(x)-1
    maxBins = nBins
    
    variables = cfg.getVariablesRange(box, "variables",w)
    print(variables)
    w.var('th1x').setBins(maxBins)
    parameters = cfg.getVariables(box, "combine_parameters")
    paramNames = []
    for parameter in parameters:
        if penalty and '_norm' in parameter:
            continue
        w.factory(parameter)
        
    #constPars = ['sqrts','p0_%s'%box, 'sqrts5', 'p50_%s'%box, 'sqrtsm', 'pm0_%s'%box, 'sqrtsa', 'pa0_%s'%box]
    constPars = ['sqrts', 'sqrts5', 'p50_%s'%box, 'sqrtsm', 'pm0_%s'%box, 'sqrtsa', 'pa0_%s'%box]
    if w.var('meff_%s'%box).getVal()<0 and w.var('seff_%s'%box).getVal()<0:
        constPars.extend(['meff_%s'%box,'seff_%s'%box])
    if  w.var('pa4_%s'%box)!=None and w.var('pa4_%s'%box).getVal()==0:
        constPars.extend(['pa4_%s'%box])
    if  w.var('pm3_%s'%box)!=None and w.var('pm3_%s'%box).getVal()==0:
        constPars.extend(['pm3_%s'%box])
    if  w.var('pm4_%s'%box)!=None and w.var('pm4_%s'%box).getVal()==0:
        constPars.extend(['pm4_%s'%box])
        
        
    for parameter in parameters:
        paramName = parameter.split('[')[0]
        if paramName not in constPars:
            paramNames.append(paramName)
            w.var(paramName).setConstant(False)
            
        
        # float normalization parameters
        fixPars(w,"Ntot",False)
        
        # fix Gaussian constraint parameters
        fixPars(w,"In")
        fixPars(w,"Mean")
        fixPars(w,"Sigma")

        # fix center of mass energy, trigger turn-on, and p0                                                                                   
        for myvar in constPars:
            fixPars(w,myvar)

        
        
    if emptyHist1D==None:
        emptyHist1D = rt.TH1D("emptyHist1D","emptyHist1D",len(x)-1,x)
        iBinX = -1
        for ix in range(1,len(x)):
            iBinX+=1
            emptyHist1D.SetBinContent(ix,1)
            emptyHist1D.SetBinError(ix,0)
        
    
    commands = cfg.getVariables(box, "combine_pdfs")
    bkgs = []
    for command in commands:
        lower = command.lower()
        if lower.find('sum::')!=-1 or lower.find('prod::')!=-1 or lower.find('expr::')!=-1 or lower.find('roogaussian::')!=-1 or lower.find('rooefficiency:')!=-1:
            w.factory(command)
            #w.Print()
        else:
            myclass = command.split('::')[0]
            remaining = command.split('::')[1]
            name = remaining.split('(')[0]
            altname = '_'.join(reversed(name.split('_')))
            mytuple = remaining.replace(name,'').replace('(','').replace(')','')
            mylist = mytuple.split(',')
            arglist = [name, name]
            for myvar in mylist:
                if w.var(myvar)!=None:
                    arglist.append(w.var(myvar))
                elif w.function(myvar)!=None:
                    arglist.append(w.function(myvar))  
                elif 'eff_' in myvar:
                        parlist = rt.RooArgList(myvar)
                        listdef = ''
                        prodlist = rt.RooArgList('g')
                        for iBinX in range(0,maxBins):
                            if w.function('eff_bin%02d'%(iBinX))!=None:
                                parlist.add(w.function('eff_bin%02d'%(iBinX)))
                            elif w.var('eff_bin%02d'%(iBinX))!=None:
                                parlist.add(w.var('eff_bin%02d'%(iBinX)))
                            else:
                                w.factory("eff_bin%02d[1]"%(iBinX))
                                w.factory("eff_bin%02d_Mean[1]"%(iBinX))
                                w.factory("eff_bin%02d_SigmaL[1e-5]"%(iBinX))
                                w.factory("eff_bin%02d_SigmaR[1e-5]"%(iBinX))
                                w.var("eff_bin%02d_Mean"%(iBinX)).setConstant(True)
                                w.var("eff_bin%02d_SigmaL"%(iBinX)).setConstant(True)
                                w.var("eff_bin%02d_SigmaR"%(iBinX)).setConstant(True)
                                if iBinX<7:
                                    w.var("eff_bin%02d"%(iBinX)).setConstant(False)
                                    w.factory("RooBifurGauss::g_eff_bin%02d(eff_bin%02d,eff_bin%02d_Mean,eff_bin%02d_SigmaL,eff_bin%02d_SigmaR)"%((iBinX,iBinX,iBinX,iBinX,iBinX)))
                                    prodlist.add(w.pdf('g_eff_bin%02d'%iBinX))
                                else:
                                    w.var("eff_bin%02d"%(iBinX)).setConstant(True)
                                parlist.add(w.var('eff_bin%02d'%(iBinX)))
                        rootTools.Utils.importToWS(w,parlist)
                        rootTools.Utils.importToWS(w,prodlist)
                        prod = rt.RooProdPdf('g_eff','g_eff',prodlist)
                        rootTools.Utils.importToWS(w,prod)                        
                        arglist.append(parlist)                        
            if myclass == 'RooMultiPdf':
                arglist = arglist[0:2]
                arglist.append(w.cat(mylist[0]))
                mypdfs = rt.RooArgList('pdf_list')
                [mypdfs.add(w.pdf(myvar)) for myvar in mylist[1:]]
                rootTools.Utils.importToWS(w,mypdfs)
                arglist.append(mypdfs)                
                        
            args = tuple(arglist)
            pdf = getattr(rt,myclass)(*args)
            if hasattr(pdf,'setTH1Binning'):
                pdf.setTH1Binning(emptyHist1D)
            rootTools.Utils.importToWS(w,pdf)
            bkg = name.split("_")
            print(bkg)
            if box in bkg: bkg.remove(box)
            bkgs.append("_".join(bkg))
            print(bkg)
            print("_".join(bkg))

    
    w.Print('v')
    if multi:
        #print(pdf_index)
        paramNames.append('pdf_index')
        bkgs = ['multi']
    return paramNames, bkgs


def writeDataCard(box,model,txtfileName,bkgs,paramNames,w,penalty,fixed,year,shapes=[],multi=False):
        obsRate = w.data("data_obs").sumEntries()
        nBkgd = len(bkgs)
        rootFileName = txtfileName.replace('.txt','.root')
        signals = len(model.split('p'))
        if signals>1:
                rates = [w.data("%s_%s"%(box,sig)).sumEntries() for sig in model.split('p')]
                processes = ["%s_%s"%(box,sig) for sig in model.split('p')]
                if '2015' in box:
                        lumiErrs = [1.027 for sig in model.split('p')]
                elif '2016' in box:
                        lumiErrs = [1.062 for sig in model.split('p')]                  
                elif 'DiPhotons' in box:
                        lumiErrs = [luminosityErrorFrac(year) for sig in model.split('p')]
                        pdfsErrs = [1.06 for sig in model.split('p')]
                        effErrs = [1.06 for sig in model.split('p')]
        else:
                rates = [w.data("%s_%s"%(box,model)).sumEntries()]
                processes = ["%s_%s"%(box,model)]
                if '2015' in box:
                        lumiErrs = [1.027]
                elif '2016' in box:
                        lumiErrs = [1.062]            
                elif 'DiPhotons' in box:
                        lumiErrs = [luminosityErrorFrac(year)]
                        pdfsErrs = [1.06]
                        effErrs = [1.06]
        for bkg in bkgs: print(bkg)             
        #rates.extend([w.var('Ntot_%s_%s'%(bkg,box)).getVal() for bkg in bkgs])
        #rates.extend([w.var('Ntot_%s_%s'%(box,bkg)).getVal() for bkg in bkgs])
        rates.extend([w.var('Ntot_%s'%(bkg)).getVal() for bkg in bkgs])
        #processes.extend(["%s_%s"%(box,bkg) for bkg in bkgs])
        processes.extend(["%s"%(bkg) for bkg in bkgs])
        lumiErrs.extend([1.00 for bkg in bkgs])
        pdfsErrs.extend([1.00 for bkg in bkgs])
        effErrs.extend([1.00 for bkg in bkgs])
        #lumiErrs.extend([1.00])
        divider = "------------------------------------------------------------\n"
        datacard = "imax 1 number of channels\n" + \
                   "jmax %i number of processes minus 1\n"%(nBkgd+signals-1) + \
                   "kmax * number of nuisance parameters\n" + \
                   divider + \
                   "observation	%.3f\n"%obsRate + \
                   divider + \
                   "shapes * * %s w%s:$PROCESS w%s:$PROCESS_$SYSTEMATIC\n"%(rootFileName,box,box) + \
                   divider
        binString = "bin"
        processString = "process"
        processNumberString = "process"
        rateString = "rate"
        lumiString = "lumi\tlnN"
        effString="eff\tlnN"
        pdfsString = "PDFs\tlnN"
        for i in range(0,len(bkgs)+signals):
            binString +="\t%s"%box
            processString += "\t%s"%processes[i]
            processNumberString += "\t%i"%(i-signals+1)
            rateString += "\t%.3f" %rates[i]
            lumiString += "\t%.3f"%lumiErrs[i]
            effString += "\t%.3f"%effErrs[i]
            pdfsString += "\t%.3f"%pdfsErrs[i]
        binString+="\n"; processString+="\n"; processNumberString+="\n"; rateString +="\n"; lumiString+="\n"; effString+="\n"; pdfsString+="\n";
        datacard+=binString+processString+processNumberString+rateString+divider
        # now nuisances
        datacard+=lumiString+effString+pdfsString
        for shape in shapes:
            shapeString = '%s\tshape\t'%shape
            for sig in range(0,signals):
                shapeString += '\t1.0'
            for i in range(0,len(bkgs)):
                shapeString += '\t-'
            shapeString += '\n'
            datacard+=shapeString
        for paramName in paramNames:
            if fixed:
                fixPars(w,paramName)    
            elif 'Mean' in paramName or 'Sigma' in paramName:
                fixPars(w,paramName)           
            elif penalty:                    
                mean = w.var(paramName).getVal()
                sigma = w.var(paramName).getError()                
                if "Ntot" in paramName:                    
                    effectString = ''
                    for sig in range(0,signals):
                        effectString += "\t1.0"           
                    for bkg in bkgs:
                        if bkg in paramName:
                            effectString += "\t%.3f"%(1.0+sigma/mean)                            
                        else:
                            effectString += "\t1.0"                    
                    datacard += "%s\tlnN%s\n"%(paramName.replace("Ntot","Norm"),effectString)
                else:
                    datacard += "%s\tparam\t%e\t%e\n"%(paramName,mean,sigma)
                         
            else:
                if "Ntot" in paramName:
                    continue
                
                elif paramName=='pdf_index':                            
                    datacard += "%s\tdiscrete\n"%(paramName)
                elif paramName in ["meff","seff"]:
                    datacard += "%s\tparam\t%e\t%e\n"%(paramName,w.var(paramName+"_Mean").getVal(),w.var(paramName+"_Sigma").getVal())
                else:
                    if multi:
                        if ('_norm' in paramName and 'multi' not in paramName):
                            continue
                    datacard += "%s\tflatParam\n"%(paramName)
            
        txtfile = open(txtfileName,"w")
        txtfile.write(datacard)
        txtfile.close()
        
def writeDataCardMC(box,model,txtfileName,bkgs,paramNames,w):
        obsRate = w.data("data_obs").sumEntries()
        nBkgd = len(bkgs)
        rootFileName = txtfileName.replace('.txt','.root')
        signals = len(model.split('p'))
        if signals>1:
                rates = [w.data("%s_%s"%(box,sig)).sumEntries() for sig in model.split('p')]
                processes = ["%s_%s"%(box,sig) for sig in model.split('p')]
                if '2015' in box:
                        lumiErrs = [1.027 for sig in model.split('p')]
                elif '2016' in box:
                        lumiErrs = [1.062 for sig in model.split('p')]                  
        else:
                rates = [w.data("%s_%s"%(box,model)).sumEntries()]
                processes = ["%s_%s"%(box,model)]
                if '2015' in box:
                        lumiErrs = [1.027]
                elif '2016' in box:
                        lumiErrs = [1.062]            
        rates.extend([w.var('Ntot_%s_%s'%(bkg,box)).getVal() for bkg in bkgs])
        processes.extend(["%s_%s"%(box,bkg) for bkg in bkgs])
        if '2015' in box:
                lumiErrs.extend([1.027 for bkg in bkgs])
        elif '2016' in box:
                lumiErrs.extend([1.062 for bkg in bkgs])
        divider = "------------------------------------------------------------\n"
        datacard = "imax 1 number of channels\n" + \
                   "jmax %i number of processes minus 1\n"%(nBkgd+signals-1) + \
                   "kmax * number of nuisance parameters\n" + \
                   divider + \
                   "observation	%.3f\n"%obsRate + \
                   divider + \
                   "shapes * * %s w%s:$PROCESS w%s:$PROCESS_$SYSTEMATIC\n"%(rootFileName,box,box) + \
                   divider
        binString = "bin"
        processString = "process"
        processNumberString = "process"
        rateString = "rate"
        lumiString = "lumi\tlnN"
        for i in range(0,len(bkgs)+signals):
            binString +="\t%s"%box
            processString += "\t%s"%processes[i]
            processNumberString += "\t%i"%(i-signals+1)
            rateString += "\t%.3f" %rates[i]
            lumiString += "\t%.3f"%lumiErrs[i]
        binString+="\n"; processString+="\n"; processNumberString+="\n"; rateString +="\n"; lumiString+="\n"
        datacard+=binString+processString+processNumberString+rateString+divider
        # now nuisances
        datacard+=lumiString
        for shape in shapes:
            shapeString = '%s\tshape\t'%shape
            for sig in range(0,signals):
                shapeString += '\t1.0'
            for i in range(0,len(bkgs)):
                shapeString += '\t-'
            shapeString += '\n'
            datacard+=shapeString
        txtfile = open(txtfileName,"w")
        txtfile.write(datacard)
        txtfile.close()

def convertToTh1xHist(hist):
    
    hist_th1x = rt.TH1D(hist.GetName()+'_th1x',hist.GetName()+'_th1x',hist.GetNbinsX(),0,hist.GetNbinsX())
    for i in range(1,hist.GetNbinsX()+1):
        hist_th1x.SetBinContent(i,hist.GetBinContent(i))
        hist_th1x.SetBinError(i,hist.GetBinError(i))

    return hist_th1x

def convertToMjjHist(hist_th1x,x):
    
    hist = rt.TH1D(hist_th1x.GetName()+'_mjj',hist_th1x.GetName()+'_mjj',len(x)-1,x)
    for i in range(1,hist_th1x.GetNbinsX()+1):
        hist.SetBinContent(i,hist_th1x.GetBinContent(i)/(x[i]-x[i-1]))
        hist.SetBinError(i,hist_th1x.GetBinError(i)/(x[i]-x[i-1]))

    return hist

def applyTurnonFunc(hist,effFr,w):

    hist_turnon = hist.Clone(hist.GetName()+"_turnon")
    for p in rootTools.RootIterator.RootIterator(effFr.floatParsFinal()):
        w.var(p.GetName()).setVal(p.getVal())
        w.var(p.GetName()).setError(p.getError())

    for i in range(1,hist.GetNbinsX()+1):
        w.var('mjj').setVal(hist.GetXaxis().GetBinCenter(i))
        #print 'mjj = %f, eff = %f'%(hist.GetXaxis().GetBinCenter(i), w.function('effFunc').getVal(rt.RooArgSet(w.var('mjj'))))
        hist_turnon.SetBinContent(i,hist.GetBinContent(i)*w.function('effFunc').getVal(rt.RooArgSet(w.var('mjj'))))
        
    return hist_turnon

def applyTurnonGraph(hist,effGraph):

    hist_turnon = hist.Clone(hist.GetName()+"_turnon")

    for i in range(1,hist.GetNbinsX()+1):
        eff = effGraph.GetY()[i-1]
        effUp = effGraph.GetEYhigh()[i-1]
        effDown = effGraph.GetEYlow()[i-1]
        hist_turnon.SetBinContent(i,hist.GetBinContent(i)*eff)
        
    return hist_turnon
        
    
    


if __name__ == '__main__':
    import BinnedFit
    parser = OptionParser()
    parser.add_option('-c','--config',dest="config",type="string",default="config/run2.config",
                  help="Name of the config file to use")
    parser.add_option('-d','--dir',dest="outDir",default="./",type="string",
                  help="Output directory to store cards")
    parser.add_option('-l','--lumi',dest="lumi", default=1.,type="float",
                  help="integrated luminosity in pb^-1")
    parser.add_option('--jesUp',dest="jesUpFile", default=None,type="string",
                  help="jes Up file")
    parser.add_option('--jerUp',dest="jerUpFile", default=None,type="string",
                  help="jer Up file")
    parser.add_option('--eneScStatUp',dest="eneScStatUpFile", default=None,type="string",
                  help="eneScStat Up file")
    parser.add_option('--eneScSystUp',dest="eneScSystUpFile", default=None,type="string",
                  help="eneScSyst Up file")
    parser.add_option('--eneScGainUp',dest="eneScGainUpFile", default=None,type="string",
                  help="eneScGain Up file")
    parser.add_option('--eneScSigmaUp',dest="eneScSigmaUpFile", default=None,type="string",
                  help="eneScSigma Up file")
    parser.add_option('--jesDown',dest="jesDownFile", default=None,type="string",
                  help="jes Down file")
    parser.add_option('--jerDown',dest="jerDownFile", default=None,type="string",
                  help="jer Down file")
    parser.add_option('--eneScStatDown',dest="eneScStatDownFile", default=None,type="string",
                  help="eneScStat Down file")
    parser.add_option('--eneScSystDown',dest="eneScSystDownFile", default=None,type="string",
                  help="eneScSyst Down file")
    parser.add_option('--eneScGainDown',dest="eneScGainDownFile", default=None,type="string",
                  help="eneScGain Down file")
    parser.add_option('--eneScSigmaDown',dest="eneScSigmaDownFile", default=None,type="string",
                  help="eneScSigma Down file")
    parser.add_option('-b','--box',dest="box", default="CaloDijet",type="string",
                  help="box name")
    parser.add_option('--asimov',dest="asimov",default=False,action='store_true',
                  help="replace real data with asimov dataset from input fit result")
    parser.add_option('--penalty',dest="penalty",default=False,action='store_true',
                  help="penalty terms on background shape + norm parameters from input fit result")
    parser.add_option('--fixed',dest="fixed",default=False,action='store_true',
                  help="fixed background shape + norm parameters")
    parser.add_option('-i','--input-fit-file',dest="inputFitFile", default=None,type="string",
                  help="input fit file")
    parser.add_option('-m','--model',dest="model", default="gg",type="string",
                  help="signal model name")
    parser.add_option('--mass',dest="mass", default=750,type="float",
                  help="mass of resonance")
    parser.add_option('--xsec',dest="xsec", default=1,type="float",
                  help="xsec of resonance")
    parser.add_option('--no-signal-sys',dest="noSignalSys",default=False,action='store_true',
                  help="no signal shape systematic uncertainties")
    parser.add_option('--trigger',dest="trigger",default=False,action='store_true',
                  help="apply trigger turn on systematics to signal")
    parser.add_option('--deco',dest="deco",default=False,action='store_true',
                  help="decorrelate parameters")
    parser.add_option('--refit',dest="refit",default=False,action='store_true',
                  help="refit for S+B")
    parser.add_option('--multi',dest="multi",default=False,action='store_true',
                  help="using RooMultiPdf for total background")
    parser.add_option('--mc',dest="mcFile", default=None,type="string",
                  help="file containing MC-based background prediciton inputs")
    parser.add_option('--year',dest="year",default="2017",type="string",
                  help="year")

    (options,args) = parser.parse_args()
    
    cfg = Config.Config(options.config)

    box = options.box
    lumi = options.lumi
    
    signalXsec = options.xsec

    signalFileName = ''
    model = options.model
    massPoint = options.mass
    histoName = cfg.getVariables(box, "histoName")

    myTH1 = None
    for f in args:
        if f.lower().endswith('.root'):
            if f.lower().find('resonanceshapes')!=-1:
                signalFileName = f
            else:
                rootFile = rt.TFile(f)                
                names = [k.GetName() for k in rootFile.GetListOfKeys()]
                if histoName in names:
                    myTH1 = rootFile.Get(histoName)
                    myTH1.Print('v')

    w = rt.RooWorkspace("w"+box)
    
    paramNames, bkgs = initializeWorkspace(w,cfg,box,scaleFactor=1,penalty=options.penalty,multi=options.multi)
    
    
    th1x = w.var('th1x')
    
    if myTH1 is None:
        print "give a background root file as input"        
    
    x = array('d', cfg.getBinning(box)[0]) # mjj binning
        
    myTH1.Rebin(len(x)-1,'data_obs_rebin',x)
    myRebinnedTH1 = rt.gDirectory.Get('data_obs_rebin')
    myRebinnedTH1.SetDirectory(0)

    myRealTH1 = convertToTh1xHist(myRebinnedTH1)
    
    dataHist = None
    if options.asimov:
        asimov = w.pdf('extDijetPdf').generateBinned(rt.RooArgSet(th1x),rt.RooFit.Asimov())
        asimov.SetName('data_obs')
        asimov.SetTitle('data_obs')
        dataHist = asimov
    else:
        dataHist = rt.RooDataHist("data_obs", "data_obs", rt.RooArgList(th1x), rt.RooFit.Import(myRealTH1))
        #triggerData = wIn.data("triggerData")
        #rootTools.Utils.importToWS(w,triggerData)
        
    rootTools.Utils.importToWS(w,dataHist)

    #the normalization dataframe
    norm = getNormalization()
    
    # import signal pdfs
    signalHistosOriginal = []
    signalHistosRebin = []
    signalHistos = []
    signalFile = rt.TFile.Open(signalFileName)
    names = [k.GetName() for k in signalFile.GetListOfKeys()]
    for name in names:
        d = signalFile.Get(name)
        if isinstance(d, rt.TH1):
            #d.SetDirectory(rt.gROOT)
            if name=='h_%s_%i'%(model,massPoint):
                #Remember that in the preparation of the trees we have 
                #used the weightAll cut to normalize the signal samples to 1000/pb luminosity.
                #Then in the normalzation based on eff x acc we multiplied by the luminosity.
                #So, here we will scale by the normalization of the file read above. 
                #print "====>>> Before: ", signalXsec,lumi,d.Integral()
                #d.Scale(signalXsec*lumi)
                print "====>>> Before: ", lumi,d.Integral()
                print(options.year, box.split("_")[1], box.split("_")[2], massPoint)
                thenorm = norm[ (norm["Year"] == options.year) & (norm["Coupling"] == box.split("_")[1]) & (norm["Category"] == box.split("_")[2]) & ( norm["MassPoint"] == int(massPoint)) ]
                thenormvalue = thenorm['Norm'].values[0]
                print(thenormvalue)
                d.Scale(thenormvalue)
                print "====>>> After: ", lumi,d.Integral()
                if options.trigger:
                    d_turnon = applyTurnonFunc(d,effFrIn,w)
                    name+='_turnon'
                    d = d_turnon
                d.Rebin(len(x)-1,name+'_rebin',x)
                d_rebin = rt.gDirectory.Get(name+'_rebin')
                d_rebin.SetDirectory(0)

                signalHistosOriginal.append(d)
                signalHistosRebin.append(d_rebin)

                d_th1x = convertToTh1xHist(d_rebin)
                print(d_th1x.Integral())
                signalHistos.append(d_th1x)
                
                sigDataHist = rt.RooDataHist('%s_%s'%(box,model),'%s_%s'%(box,model), rt.RooArgList(th1x), rt.RooFit.Import(d_th1x))
                print(sigDataHist.sumEntries())
                sigDataHist_mgg = rt.RooDataHist('%s_%s_mgg'%(box,model),'%s_%s_mgg'%(box,model), rt.RooArgList(w.var('mgg')), rt.RooFit.Import(d))
                sigPdf_mgg = rt.RooHistPdf('pdf_%s_%s_mgg'%(box,model),'pdf_%s_%s_mgg'%(box,model), rt.RooArgSet(w.var('mgg')), sigDataHist_mgg)
                rootTools.Utils.importToWS(w,sigDataHist)
                rootTools.Utils.importToWS(w,sigDataHist_mgg)

    # initialize fit parameters (b-only fit)
    if options.inputFitFile is not None:
        inputRootFile = rt.TFile.Open(options.inputFitFile,"r")
        wIn = inputRootFile.Get("w"+box).Clone("wIn"+box)            
        if wIn.obj("fitresult_extDijetPdf_data_obs") != None: 
            frIn = wIn.obj("fitresult_extDijetPdf_data_obs")
        elif wIn.obj("nll_extDijetPdf_%s_data_obs"% box.split("DiPhotons_")[1] ) != None:
            frIn = wIn.obj("nll_extDijetPdf_%s_data_obs"% box.split("DiPhotons_")[1])
        elif wIn.obj("fitresult_extDijetPdf_data_obs_with_constr") != None:
            fr = wIn.obj("fitresult_extDijetPdf_data_obs_with_constr")
        elif wIn.obj("nll_extDijetPdf_data_obs_with_constr") != None:
            frIn = wIn.obj("nll_extDijetPdf_data_obs_with_constr")
        elif wIn.obj("simNll") != None:
            frIn = wIn.obj("simNll")
        print "restoring parameters from fit"
        if options.trigger:
            effFrIn = wIn.obj("nll_effPdf_triggerData")
            
        frIn.Print("V")
        
        for p in rootTools.RootIterator.RootIterator(frIn.floatParsFinal()):
            if w.var(p.GetName()) != None:
                w.var(p.GetName()).setVal(p.getVal())
                w.var(p.GetName()).setError(p.getError())
            if "Ntot" in p.GetName():
                if options.deco:
                    w.factory('Ntot_bkg_deco_%s[%f]'%(box,p.getVal()))
                    w.var('Ntot_bkg_deco_%s'%(box)).setError(p.getError())
                if options.multi:
                    w.var('Ntot_%s_multi'%(box)).setVal(p.getVal())
                    w.var('Ntot_%s_multi'%(box)).setError(p.getError())
                    
                    
        for p in rootTools.RootIterator.RootIterator(frIn.constPars()):
            if w.var(p.GetName()) != None:
                w.var(p.GetName()).setVal(p.getVal())
                w.var(p.GetName()).setError(p.getError())
        
        if options.deco or options.refit:
            sigDataHist = w.data('%s_%s'%(box,model))
            sigPdf = rt.RooHistPdf('%s_sig'%box,'%s_sig'%box,rt.RooArgSet(th1x), sigDataHist)
            rootTools.Utils.importToWS(w,sigPdf)
            w.factory('mu[1]')
            w.var('mu').setConstant(False)
            w.var('mu').setMin(0)
            w.var('mu').setVal(0.2) # initial value close to zero
            w.factory('Ntot_sig_%s_In[%f]'%(box,sigDataHist.sumEntries()))
            w.factory('expr::Ntot_sig_%s("mu*Ntot_sig_%s_In",mu,Ntot_sig_%s_In)'%(box,box,box))
            w.factory('SUM::extSpBPdf(Ntot_sig_%s*%s_sig,Ntot_bkg_%s*%s_bkg)'%(box,box,box,box))
            w.factory('SUM::extSigPdf(Ntot_sig_%s*%s_sig)'%(box,box))
            frSpB = BinnedFit.binnedFit(w.pdf('extSpBPdf'), w.data('data_obs'))
            paramsToDecoNames = []
            for p in rootTools.RootIterator.RootIterator(frSpB.floatParsFinal()):
                paramsToDecoNames.append(p.GetName)                
            paramsToDeco = rt.RooArgList()
            if 'Ntot_bkg_%s'%box in paramsToDecoNames:
                paramsToDeco.add(w.var('Ntot_bkg_%s'%box))
            if 'p1_%s'%box in paramsToDecoNames:
                paramsToDeco.add(w.var('p1_%s'%box))
            if 'p2_%s'%box in paramsToDecoNames:
                paramsToDeco.add(w.var('p2_%s'%box))
            if 'p3_%s'%box in paramsToDecoNames:
                paramsToDeco.add(w.var('p3_%s'%box))
            if 'p4_%s'%box in paramsToDecoNames:
                paramsToDeco.add(w.var('p4_%s'%box))                    
            condCovMatrix = frSpB.conditionalCovarianceMatrix(paramsToDeco)
            w.var('mu').setConstant(True)
            frSpB_muFixed = BinnedFit.binnedFit(w.pdf('extSpBPdf'), w.data('data_obs'))
            covMatrix = frSpB_muFixed.covarianceMatrix()
            condCovMatrix.Print("V")
            covMatrix.Print("V")
            frIn.Print('V')
            frSpB.Print('v')
            frSpB_muFixed.Print('v')
        if options.deco:
            deco = rt.PdfDiagonalizer("deco_%s"%box,w,frSpB_muFixed)
            bkgs_deco = []
            for bkg in bkgs:
                pdf_deco = deco.diagonalize(w.pdf('%s_%s'%(box,bkg)))
                pdf_deco.SetName('%s_%s_deco'%(box,bkg))
                rootTools.Utils.importToWS(w,pdf_deco,rt.RooFit.RecycleConflictNodes())
                bkgs_deco.append(bkg+'_deco')
                w.var('deco_%s_eig0'%box).setConstant(True)
                if '%s_%s_norm'%(box,bkg) in paramNames:
                    loc = paramNames.index('%s_%s_norm'%(box,bkg))
                    paramNames[loc] = '%s_%s_deco_norm'%(box,bkg)
                    w.factory('%s_%s_deco_norm[1]'%(box,bkg))
                    w.var('%s_%s_deco_norm'%(box,bkg)).setConstant(False)
                if 'p1_%s'%box in paramNames:
                    loc = paramNames.index('p1_%s'%box)
                    paramNames[loc] = 'deco_%s_eig1'%box
                if 'p2_%s'%box in paramNames:
                    loc = paramNames.index('p2_%s'%box)
                    paramNames[loc] = 'deco_%s_eig2'%box
                if 'p3_%s'%box in paramNames:
                    loc = paramNames.index('p3_%s'%box)
                    paramNames[loc] = 'deco_%s_eig3'%box
                if 'p4_%s'%box in paramNames:
                    loc = paramNames.index('p4_%s'%box)
                    paramNames[loc] = 'deco_%s_eig4'%box
                    
            bkgs = bkgs_deco
            
        for p in rootTools.RootIterator.RootIterator(frIn.floatParsFinal()):
            if "Ntot" in p.GetName():
                if options.deco:
                    w.factory('Ntot_bkg_deco_%s[%f]'%(box,p.getVal()))
                    w.var('Ntot_bkg_deco_%s'%(box)).setError(p.getError())
                
                
    if options.noSignalSys:
        shapes = []
        shapeFiles = {}
    else:
        shapes = []
        shapeFiles = {}
        if options.jesUpFile is not None or options.jesDownFile is not None:
            shapes.append('jes')
            shapeFiles['jesUp'] = options.jesUpFile
            shapeFiles['jesDown'] = options.jesDownFile
        if options.jerUpFile is not None or options.jerDownFile is not None:
            shapes.append('jer')
            shapeFiles['jerUp'] = options.jerUpFile
            shapeFiles['jerDown'] = options.jerDownFile
        if options.eneScStatUpFile is not None or options.eneScStatDownFile is not None:
            shapes.append('eneScStat')
            shapeFiles['eneScStatUp'] = options.eneScStatUpFile
            shapeFiles['eneScStatDown'] = options.eneScStatDownFile
        if options.eneScSystUpFile is not None or options.eneScSystDownFile is not None:
            shapes.append('eneScSyst')
            shapeFiles['eneScSystUp'] = options.eneScSystUpFile
            shapeFiles['eneScSystDown'] = options.eneScSystDownFile
        if options.eneScGainUpFile is not None or options.eneScGainDownFile is not None:
            shapes.append('eneScGain')
            shapeFiles['eneScGainUp'] = options.eneScGainUpFile
            shapeFiles['eneScGainDown'] = options.eneScGainDownFile
        if options.eneScSigmaUpFile is not None or options.eneScSigmaDownFile is not None:
            shapes.append('eneScSigma')
            shapeFiles['eneScSigmaUp'] = options.eneScSigmaUpFile
            shapeFiles['eneScSigmaDown'] = options.eneScSigmaDownFile

    # JES and JER uncertainties
    hSigTh1x = signalHistos[0]
    hUpTh1x = None
    hDownTh1x = None
    for shape in shapes:
        if shapeFiles[shape+'Up'] is not None:
            fUp = rt.TFile.Open(shapeFiles[shape+'Up'])
            if options.trigger:
                hUp = applyTurnonFunc(fUp.Get('h_%s_%i'%(model,massPoint)),effFrIn,w)
            else:
                hUp = fUp.Get('h_%s_%i'%(model,massPoint))
            hUp.SetName('h_%s_%i_%sUp'%(model,massPoint,shape))
            hUp.SetDirectory(0)
            hUp.Rebin(len(x)-1,hUp.GetName()+'_rebin',x)
            hUpRebin = rt.gDirectory.Get(hUp.GetName()+'_rebin')
            hUpRebin.SetDirectory(0)        
            hUpTh1x = convertToTh1xHist(hUpRebin)            
            hUpTh1x.Scale(hSigTh1x.Integral()/hUpTh1x.Integral())
            
            hUp_DataHist = rt.RooDataHist('%s_%s_%sUp'%(box,model,shape),'%s_%s_%sUp'%(box,model,shape),rt.RooArgList(th1x),hUpTh1x)
        
            rootTools.Utils.importToWS(w,hUp_DataHist)
            
        if shapeFiles[shape+'Down'] is not None: 
            fDown = rt.TFile.Open(shapeFiles[shape+'Down'])
            if options.trigger:
                hDown = applyTurnonFunc(fDown.Get('h_%s_%i'%(model,massPoint)),effFrIn,w)
            else:
                hDown = fDown.Get('h_%s_%i'%(model,massPoint))
            hDown.SetName('h_%s_%i_%sDown'%(model,massPoint,shape))
            hDown.SetDirectory(0)
        
            hDown.Rebin(len(x)-1,hDown.GetName()+'_rebin',x)
            hDownRebin = rt.gDirectory.Get(hDown.GetName()+'_rebin')
            hDownRebin.SetDirectory(0)        
            hDownTh1x = convertToTh1xHist(hDownRebin)
            hDownTh1x.Scale(hSigTh1x.Integral()/hDownTh1x.Integral())
        
            hDown_DataHist = rt.RooDataHist('%s_%s_%sDown'%(box,model,shape),'%s_%s_%sDown'%(box,model,shape),rt.RooArgList(th1x),hDownTh1x)
        
            rootTools.Utils.importToWS(w,hDown_DataHist)
        else:
            hDownTh1x = getDownFromUpNom(hUpTh1x,hSigTh1x)
            hDownTh1x.Scale(hSigTh1x.Integral()/hDownTh1x.Integral())
        
            hDown_DataHist = rt.RooDataHist('%s_%s_%sDown'%(box,model,shape),'%s_%s_%sDown'%(box,model,shape),rt.RooArgList(th1x),hDownTh1x)
        
            rootTools.Utils.importToWS(w,hDown_DataHist)

    if options.mcFile is not None:
        bkgs = ['bkg']
        mcFile = rt.TFile.Open(options.mcFile,'read')        
        mcName = cfg.getVariables(box, "mcName")
        mcHist = mcFile.Get(mcName)        
        mcHist.Rebin(len(x)-1,'mc_rebin',x)
        mcHist_rebin = rt.gDirectory.Get('mc_rebin')
        mcHist_th1x = convertToTh1xHist(mcHist_rebin)
        mcDataHist = rt.RooDataHist('%s_%s'%(box,'bkg'),'%s_%s'%(box,'bkg'), rt.RooArgList(th1x), rt.RooFit.Import(mcHist_th1x))
        mcDataHist_mgg = rt.RooDataHist('%s_%s_mgg'%(box,'bkg'),'%s_%s_mgg'%(box,'bkg'), rt.RooArgList(w.var('mgg')), rt.RooFit.Import(mcHist))
        rootTools.Utils.importToWS(w,mcDataHist)
        rootTools.Utils.importToWS(w,mcDataHist_mgg)

 
    outFile = 'diphoton_combine_%i_%s_%s.root'%(massPoint,box,options.year)
    outputFile = rt.TFile.Open(options.outDir+"/"+outFile,"recreate")
    if options.mcFile is not None:
        writeDataCardMC(box,model,options.outDir+"/"+outFile.replace(".root",".txt"),bkgs,paramNames,w)
    else:
        writeDataCard(box,model,options.outDir+"/"+outFile.replace(".root",".txt"),bkgs,paramNames,w,options.penalty,options.fixed,options.year,shapes=shapes,multi=options.multi)
    w.Write()
    w.Print('v')
    del w
    os.system("cat %s"%options.outDir+"/"+outFile.replace(".root",".txt"))
