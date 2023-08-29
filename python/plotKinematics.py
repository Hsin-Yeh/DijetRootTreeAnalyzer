#!/usr/bin/env python3

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

        h_mgg      = rt.TH1D('h_mgg     ','h_mgg     ',100,200,8500)
        h_qt       = rt.TH1D('h_qt      ','h_qt      ',100,0,1000)
        h_deltaR   = rt.TH1D('h_deltaR  ','h_deltaR  ',20,0,10)
        h_deltaEta = rt.TH1D('h_deltaEta','h_deltaEta',20,0,6)
        h_deltaPhi = rt.TH1D('h_deltaPhi','h_deltaPhi',20,0,3.14)
        h_ph1pt    = rt.TH1D('h_ph1pt   ','h_ph1pt   ',50,125,1000)
        h_ph1scEta = rt.TH1D('h_ph1scEta','h_ph1scEta',20,-2.5,2.5)
        h_ph2pt    = rt.TH1D('h_ph2pt'   ,'h_ph2pt',50,125,1000)
        h_ph2scEta = rt.TH1D('h_ph2scEta','h_ph2scEta',20,-2.5,2.5)

        thetree=tfileIn.Get("HighMassDiphoton")

        project(thetree,h_mgg      , "mgg"      , 'eventClass==%d && mgg > 500'%(cat))
        project(thetree,h_qt       , "qt"       , 'eventClass==%d && mgg > 500'%(cat))
        project(thetree,h_deltaR   , "deltaR"   , 'eventClass==%d && mgg > 500'%(cat))
        project(thetree,h_deltaEta , "deltaEta" , 'eventClass==%d && mgg > 500'%(cat))
        project(thetree,h_deltaPhi , "deltaPhi" , 'eventClass==%d && mgg > 500'%(cat))
        project(thetree,h_ph1pt    , "ph1pt"    , 'eventClass==%d && mgg > 500'%(cat))
        project(thetree,h_ph1scEta , "ph1scEta" , 'eventClass==%d && mgg > 500'%(cat))
        project(thetree,h_ph2pt    , "ph2pt"    , 'eventClass==%d && mgg > 500'%(cat))
        project(thetree,h_ph2scEta , "ph2scEta" , 'eventClass==%d && mgg > 500'%(cat))

        h_mgg.SetDirectory(0)
        h_qt.SetDirectory(0)
        h_deltaR.SetDirectory(0)
        h_deltaEta.SetDirectory(0)
        h_deltaPhi.SetDirectory(0)
        h_ph1pt.SetDirectory(0)
        h_ph1scEta.SetDirectory(0)
        h_ph2pt.SetDirectory(0)
        h_ph2scEta.SetDirectory(0)

        histos.append(h_mgg)
        histos.append(h_qt)
        histos.append(h_deltaR)
        histos.append(h_deltaEta)
        histos.append(h_deltaPhi)
        histos.append(h_ph1pt)
        histos.append(h_ph1scEta)
        histos.append(h_ph2pt)
        histos.append(h_ph2scEta)

        # for i in range(1,80):
        #     print("%d, %d-%dGeV, %d"%(i, 500+100*(i-1), 500+100*i, h_mgg_100GeVbin.GetBinContent(i)))

    if options.type=='nom':
        tfileOut = rt.TFile.Open('%s/Kinematics_%s_%s_%s.root'%(options.outDir,title,options.cat,year),'recreate')
    #else:
        #tfileOut = rt.TFile.Open('%s/InputShapes_%s_%s_%s.root'%(options.outDir,title,year,TYPE),'recreate')
    tfileOut.cd()
    for h in histos:
        h.Write()
    tfileOut.Close()
