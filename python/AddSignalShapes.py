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
 
    (options,args) = parser.parse_args()
    if options.type=='nom':
        TYPE = ''
    else:
        TYPE = options.type.upper()

    histos = []
    year = ''

    cat = -1
    if options.cat == "EBEB" : cat = 0
    elif options.cat == "EBEE" : cat = 1

    syslist = {"energyScaleStatUp"   : "ph1energyScaleStatUp*ph2energyScaleStatUp",
               "energyScaleSystUp"   : "ph1energyScaleSystUp*ph2energyScaleSystUp",
               "energyScaleGainUp"   : "ph1energyScaleGainUp*ph2energyScaleGainUp",
               "energySigmaUp"       : "ph1energySigmaUp*ph2energySigmaUp",

               "energyScaleStatDown"   : "ph1energyScaleStatDown*ph2energyScaleStatDown",
               "energyScaleSystDown"   : "ph1energyScaleSystDown*ph2energyScaleSystDown",
               "energyScaleGainDown"   : "ph1energyScaleGainDown*ph2energyScaleGainDown",
               "energySigmaDown"       : "ph1energySigmaDown*ph2energySigmaDown" }
 
    for f in args:
        year = f.split('.root')[0].split('_')[-1]
        if year != "2016":
            mass = int(f.split('_M_')[1].split('_TuneCP2')[0])
            title =  f.split('_M_')[0].split('/')[-1]        
        else:
            mass = int(f.split('_M-')[1].split('_TuneCP2')[0])
            title =  f.split('_M-')[0].split('/')[-1]        

        print(title,year,mass)
        tfileIn = rt.TFile.Open(f)
        
        #h_mgg_1GeVbin = rt.TH1D('h_mgg_1GeVbin','h_mgg_1GeVbin',14000,0,14000)
        #h_mgg_5GeVbin = rt.TH1D('h_mgg_5GeVbin','h_mgg_5GeVbin',2800,0,14000)
        h_mgg_ratio = rt.TH1D('h_mgg_ratio','h_mgg_ratio',1000,0.,2.)
        thetree=tfileIn.Get("HighMassDiphoton")

        if options.type=='nom':
            project(thetree,h_mgg_ratio, "mgg/%f"%(float(mass)), 'eventClass==%d'%(cat) )
        else: 
            project(thetree,h_mgg_ratio, "mgg*%s/%f"%(syslist[options.sys],float(mass)), 'eventClass==%d'%(cat) )

        #h = tfileIn.Get('h_mjj_ratio_%s'%options.type)
        h_mgg_ratio.SetName('h_%s_M%i_%s'%(title,mass,year))
        h_mgg_ratio.SetTitle('h_%s_M%i_%s'%(title,mass,year))
        h_mgg_ratio.SetDirectory(0)
        histos.append(h_mgg_ratio)

    
    if options.type=='nom':
        tfileOut = rt.TFile.Open('%s/InputShapes_%s_%s_%s.root'%(options.outDir,title,options.cat,year),'recreate')
    else:
        tfileOut = rt.TFile.Open('%s/InputShapes_%s_%s_%s_%s.root'%(options.outDir,title,options.cat,year,options.sys),'recreate')
    tfileOut.cd()
    for h in histos:
        h.Write()
    tfileOut.Close()
        
        
