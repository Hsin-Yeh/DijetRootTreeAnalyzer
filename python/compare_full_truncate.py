#!/usr/bin/env python
import ROOT
import argparse
from array import array

parser = argparse.ArgumentParser(description='')
parser.add_argument('--fileDir',
                    '-d',
                    default="/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/FinalResults/Limits",
                    type=str,
                    help='fileDir')
parser.add_argument('--model','-m',default="heavyhiggs",type=str,help='model')
parser.add_argument('--coup','-c',default="0p014",type=str,help='coupling')
parser.add_argument('--year','-y',default="2016",type=str,help='year')

args = parser.parse_args()

if __name__ == "__main__":

    fullName = args.fileDir+"/full/expOnly/limitplot_"+args.model+"_"+args.coup+"_"+args.year+".root"
    truncateName = args.fileDir+"/truncate/expOnly/limitplot_"+args.model+"_"+args.coup+"_"+args.year+".root"
    tfileFull = ROOT.TFile.Open(fullName)
    tfileTruncate = ROOT.TFile.Open(truncateName)

    gFull = tfileFull.Get("expGraph")
    gTruncate = tfileTruncate.Get("expGraph")

    mass, diff = array( 'd' ), array( 'd' )
    for i in range(gFull.GetN()):
        mass.append(gFull.GetX[i])
        diff.append(abs(gFull.GetY[i]-gTruncate.GetY[i])/gFull.GetY[i])

    gdiff=ROOT.TGraph(gFull.GetN(), mass, diff)

    c1 = ROOT.TCanvas()
    pad1 = ROOT.TPad("pad1","pad1",0,0.3,1,1);
    pad1.SetBottomMargin(0.01);
    pad1.Draw();
    pad1.cd();
    pad.SetLogy()
    gFull.Draw("AL")
    gTruncate.Draw("same")
    gFull.GetXaxis().SetRangeUser(500,5500)
    gFull.GetYaxis().SetRangeUser(0.02,20)

    pad2 = ROOT.TPad("pad2","pad2",0,0,1,0.28)
    gdiff.Draw()
    c1.SaveAs("test.png")

    tfileFull.Close()
    tfileTruncate.Close()
