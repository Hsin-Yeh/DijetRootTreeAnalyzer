from optparse import OptionParser
import ROOT as rt
import rootTools
from framework import Config
from array import *
import os
import sys

def project(tree, h, var, cut):
    print 'projecting var: %s, cut: %s from tree: %s into hist: %s'%(var, cut, tree.GetName(), h.GetName())
    tree.Project(h.GetName(),var,cut)

if __name__ == '__main__':
    
    parser = OptionParser()
    parser.add_option('-t','--type',dest="type",default="nom",type="string",
                  help="type of result")
    parser.add_option('-m','--model',dest="model",default="gg",type="string",
                  help="model")
    parser.add_option('-c','--cat',dest="cat",default="EBEB",type="string",
                  help="category")
    parser.add_option('-d','--outdir',dest="outDir",default="./",type="string",
                  help="Output directory to store output histograms")
    parser.add_option('-s','--sys',dest="sys",default="energyScaleStat",type="string",
                  help="Systematics")
    parser.add_option("-e", "--method",dest="method",default="full",type="string",
                  help="Choose full range or truncate with the fwhm mass range")

    (options,args) = parser.parse_args()
    if options.type=='nom':
        TYPE = ''
    else:
        TYPE = options.type.upper()

    histos = []
    year = ''

    energySyslist = {"energyScaleStatUp"   : "ph1energyScaleStatUp*ph2energyScaleStatUp",
                     "energyScaleSystUp"   : "ph1energyScaleSystUp*ph2energyScaleSystUp",
                     "energyScaleGainUp"   : "ph1energyScaleGainUp*ph2energyScaleGainUp",
                     "energySigmaUp"       : "ph1energySigmaUp*ph2energySigmaUp",

                     "energyScaleStatDown"   : "ph1energyScaleStatDown*ph2energyScaleStatDown",
                     "energyScaleSystDown"   : "ph1energyScaleSystDown*ph2energyScaleSystDown",
                     "energyScaleGainDown"   : "ph1energyScaleGainDown*ph2energyScaleGainDown",
                     "energySigmaDown"       : "ph1energySigmaDown*ph2energySigmaDown" }

    SFSyslist     = {"nom" : "ph1SF*ph2SF",
                     "SFUp" : "ph1SFUp*ph2SFUp",
                     "SFDown" : "ph1SFDown*ph2SFDown"}

    EEPFSyslist   = {"nom" : "ph1EEPF*ph2EEPF",
                     "EEPFUp" : "ph1EEPFUp*ph2EEPFUp",
                     "EEPFDown" : "ph1EEPFDown*ph2EEPFDown"}

    PuSyslist   = {"nom" : "weightPuManual",
                   "PuUp" : "weightPuManualUp",
                   "PuDown" : "weightPuManualDown"}

    acc={}
    eff={}
    acc["EBEB"] = "(mgg > 500 && deltaR > 0.45 && ph1pt>125 && ph2pt>125 && isEBEB)"
    acc["EBEE"] = "(mgg > 500 && deltaR > 0.45 && ph1pt>125 && ph2pt>125 && (isEBEE || isEEEB))"
    eff["2016"] = "isGood*(HLT_DoublePhoton60 || HLT_ECALHT800)"
    eff["2017"] = "isGood*(HLT_DoublePhoton70 || HLT_ECALHT800)"
    eff["2018"] = "isGood*(HLT_DoublePhoton70 || HLT_ECALHT800)"

    for f in args:
        year = f.split('.root')[0].split('_')[-1]
        if year != "2016":
            mass = int(f.split('_M_')[1].split('_TuneCP2')[0])
            title =  f.split('_M_')[0].split('/')[-1]
        else:
            mass = int(f.split('_M_')[1].split('_TuneCP2')[0])
            title =  f.split('_M_')[0].split('/')[-1]

        print(title,year,mass)
        tfileIn = rt.TFile.Open(f)
        thetree=tfileIn.Get("HighMassDiphoton")

        # Find mean and fwhm
        massMin=0.8*mass;
        massMax=1.2*mass;
        h_mgg = rt.TH1D('h_mgg','h_mgg',1000,massMin,massMax)
        project(thetree,h_mgg,"mgg","1")
        bin1 = h_mgg.FindFirstBinAbove(h_mgg.GetMaximum()/2)
        bin2 = h_mgg.FindLastBinAbove(h_mgg.GetMaximum()/2)
        mean = h_mgg.GetBinCenter(h_mgg.GetMaximumBin())
        fwhm = h_mgg.GetBinCenter(bin2) - h_mgg.GetBinCenter(bin1);
        massMin=mean-2*fwhm
        massMax=mean+2*fwhm
        print(mean,fwhm,massMin,massMax)

        # h_mgg_1GeVbin = rt.TH1D('h_mgg_1GeVbin','h_mgg_1GeVbin',14000,0,14000)
        #h_mgg_5GeVbin = rt.TH1D('h_mgg_5GeVbin','h_mgg_5GeVbin',2800,0,14000)
        h_mgg_8GeVbin = rt.TH1D('h_mgg_8GeVbin','h_mgg_8GeVbin',1750, 0, 14000)
        h_mgg_ratio = rt.TH1D('h_mgg_ratio','h_mgg_ratio',1000,0,2.0)

        if options.sys.find("Up")!=-1: numSigma = 1
        elif options.sys.find("Down")!=-1: numSigma = -1
        else: numSigma = 0

        nomCut = '(' + acc[options.cat] + ')*(' + eff[year] + ')*(' + SFSyslist["nom"] + ')*(' + EEPFSyslist["nom"] + ')*(' + PuSyslist["nom"] + ')*(weightAll)'
        fwhmCut = 'mgg>%f && mgg<%f'%(massMin,massMax)
        genMassCut = 'mggGen>%f && mggGen<%f'%(mass*0.8, mass*1.2)


        if options.method=="full":          allCuts = nomCut
        elif options.method=="truncate":    allCuts = '(' + nomCut + ')*(' + fwhmCut + ')'
        elif options.method=="genFiducial": allCuts = '(' + nomCut + ')*(' + genMassCut + ')'

        if options.type=='nom':
            project(thetree,h_mgg_ratio, "mgg/%f"%(float(mass)), allCuts )
            project(thetree,h_mgg_8GeVbin, "mgg"%(float(mass)), allCuts )
        elif options.sys in energySyslist:
            project(thetree,h_mgg_ratio, "mgg*%s/%f"%(energySyslist[options.sys],float(mass)), allCuts )

        elif options.sys in SFSyslist:
            allCuts = '(' + acc[options.cat] + ')*(' + eff[year] + ')*(' + SFSyslist[options.sys] + ')*(' + EEPFSyslist["nom"] + ")*(" + PuSyslist["nom"] + ")*(weightAll)"
            project(thetree,h_mgg_ratio, "mgg/%f"%(float(mass)), allCuts )

        elif options.sys in PuSyslist:
            allCuts = '(' + acc[options.cat] + ')*(' + eff[year] + ')*(' + SFSyslist["nom"] + ')*(' + EEPFSyslist["nom"] + ")*(" + PuSyslist[options.sys] + ")*(weightAll)"
            project(thetree,h_mgg_ratio, "mgg/%f"%(float(mass)), allCuts )

        elif options.sys in EEPFSyslist:
            allCuts = '(' + acc[options.cat] + ')*(' + eff[year] + ')*(' + SFSyslist["nom"] + ')*(' + EEPFSyslist[options.sys] + ")*(" + PuSyslist["nom"] + ")*(weightAll)"
            project(thetree,h_mgg_ratio, "mgg/%f"%(float(mass)), allCuts )

        #h = tfileIn.Get('h_mjj_ratio_%s'%options.type)
        h_mgg_ratio.SetName('h_%s_M%i_%s'%(title,mass,year))
        h_mgg_ratio.SetTitle('h_%s_M%i_%s'%(title,mass,year))
        h_mgg_ratio.SetDirectory(0)
        histos.append(h_mgg_ratio)
        h_mgg_8GeVbin.SetName('h_%s_M%i_%s_8Gev'%(title,mass,year))
        h_mgg_8GeVbin.SetTitle('h_%s_M%i_%s_8GeV'%(title,mass,year))
        h_mgg_8GeVbin.SetDirectory(0)
        histos.append(h_mgg_8GeVbin)



    if options.type=='nom':
        tfileOut = rt.TFile.Open('%s/InputShapes_%s_%s_%s.root'%(options.outDir,title,options.cat,year),'recreate')
    else:
        tfileOut = rt.TFile.Open('%s/InputShapes_%s_%s_%s_%s.root'%(options.outDir,title,options.cat,year,options.sys),'recreate')
    tfileOut.cd()
    for h in histos:
        h.Write()
    tfileOut.Close()
