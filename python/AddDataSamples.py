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

    acc={}
    eff={}
    acc["EBEB"] = "(mgg > 500 && deltaR > 0.45 && ph1pt>125 && ph2pt>125 && isEBEB)"
    acc["EBEE"] = "(mgg > 500 && deltaR > 0.45 && ph1pt>125 && ph2pt>125 && (isEBEE || isEEEB))"
    eff["2016"] = "isGood*(HLT_DoublePhoton60 || HLT_ECALHT800)"
    eff["2017"] = "isGood*(HLT_DoublePhoton70 || HLT_ECALHT800)"
    eff["2018"] = "isGood*(HLT_DoublePhoton70 || HLT_ECALHT800)"

    for f in args:
        title =  f.split('.root')[0].split('/')[-1].split('_')[0]    
        year = f.split('.root')[0].split('_')[-1]
        print(title,year)
        tfileIn = rt.TFile.Open(f)

        h_mgg_1GeVbin = rt.TH1D('h_mgg_1GeVbin','h_mgg_1GeVbin',14000,0,14000)
        # h_mgg_50GeVbin = rt.TH1D('h_mgg_50GeVbin','h_mgg_50GeVbin',160,500,8500)
        # h_mgg_100GeVbin = rt.TH1D('h_mgg_100GeVbin','h_mgg_100GeVbin',80,500,8500)
        thetree=tfileIn.Get("HighMassDiphoton")

        nomCut = '(' + acc[options.cat] + ')*(' + eff[year] + ')'
        project(thetree,h_mgg_1GeVbin, "mgg", nomCut)
        # project(thetree,h_mgg_1GeVbin, "mgg", 'eventClass==%d && mgg > 500'%(cat))
        # project(thetree,h_mgg_50GeVbin, "mgg", 'eventClass==%d && mgg > 500'%(cat))
        # project(thetree,h_mgg_100GeVbin, "mgg", 'eventClass==%d && mgg > 500'%(cat))
      
        #h = tfileIn.Get('h_mjj_ratio_%s'%options.type)
        h_mgg_1GeVbin.SetName('h_%s'%(title))
        h_mgg_1GeVbin.SetTitle('h_%s'%(title))
        h_mgg_1GeVbin.SetDirectory(0)
        # h_mgg_50GeVbin.SetDirectory(0)
        # h_mgg_100GeVbin.SetDirectory(0)
        histos.append(h_mgg_1GeVbin)
        # histos.append(h_mgg_50GeVbin)
        # histos.append(h_mgg_100GeVbin)

        # for i in range(1,80):
        #     print("%d, %d-%dGeV, %d"%(i, 500+100*(i-1), 500+100*i, h_mgg_100GeVbin.GetBinContent(i)))


    if options.type=='nom':
        tfileOut = rt.TFile.Open('%s/InputShapes_%s_%s_%s.root'%(options.outDir,title,options.cat,year),'recreate')
    #else:
        #tfileOut = rt.TFile.Open('%s/InputShapes_%s_%s_%s.root'%(options.outDir,title,year,TYPE),'recreate')
    tfileOut.cd()
    for h in histos:
        h.Write()
    tfileOut.Close()
        
        
