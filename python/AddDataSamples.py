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

    for f in args:
        title =  f.split('.root')[0].split('/')[-1].split('_')[0]    
        year = f.split('.root')[0].split('_')[-1]
        print(title,year)
        tfileIn = rt.TFile.Open(f)
        
        h_mgg_1GeVbin = rt.TH1D('h_mgg_1GeVbin','h_mgg_1GeVbin',14000,0,14000)
        #h_mgg_5GeVbin = rt.TH1D('h_mgg_5GeVbin','h_mgg_5GeVbin',2800,0,14000)
        thetree=tfileIn.Get("HighMassDiphoton")

        project(thetree,h_mgg_1GeVbin, "mgg", 'eventClass==%d'%(cat) )
        
        #h = tfileIn.Get('h_mjj_ratio_%s'%options.type)
        h_mgg_1GeVbin.SetName('h_%s'%(title))
        h_mgg_1GeVbin.SetTitle('h_%s'%(title))
        h_mgg_1GeVbin.SetDirectory(0)
        histos.append(h_mgg_1GeVbin)

    
    if options.type=='nom':
        tfileOut = rt.TFile.Open('%s/InputShapes_%s_%s_%s.root'%(options.outDir,title,options.cat,year),'recreate')
    #else:
        #tfileOut = rt.TFile.Open('%s/InputShapes_%s_%s_%s.root'%(options.outDir,title,year,TYPE),'recreate')
    tfileOut.cd()
    for h in histos:
        h.Write()
    tfileOut.Close()
        
        
