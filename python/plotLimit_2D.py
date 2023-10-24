#!/usr/bin/env python

import ROOT
from array import array
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='')
parser.add_argument('--year','-y',default="2016",type=str,help='year')
parser.add_argument('--coupling','-c',default="kMpl001",type=str,help='coupling')
parser.add_argument('--signame','-s',default="grav",type=str,help='grav or heavyhiggs')
parser.add_argument('--outputDir','-o',default="./",type=str,help='output directory')
parser.add_argument('--debug','-d',action="store_true",help='debug mode')
parser.add_argument('--unblind',action="store_true",help='debug mode')
args = parser.parse_args()

def pvalue2D():
    ROOT.gROOT.LoadMacro("~/rootlogon.C")

    m_gStyle = ROOT.TStyle();
    m_gStyle.SetOptFit(0);

    masses=array('d')
    for mass in range(600,5010,10):
        masses.append(mass)
    couplings = array('d',[14, 361, 707, 1054, 1400, 2450, 3500, 4550, 5600])
    h_pvalue = ROOT.TH2F("h_pvalue","h_pvalue",len(masses)-1,masses,len(couplings)-1,couplings)

    for coupling in couplings:
        for mass in masses:
            in_filename = "ParallelForLimits/2023-10-23/results/grav/coupling/finalResults_" + args.signame + "_" + str(coupling) + "_" + str(mass) + ".txt";
            binx = h_pvalue.GetXaxis().FindBin(mass)
            biny = h_pvalue.GetYaxis().FindBin(coupling)
            binxy = h_pvalue.GetBin(binx,biny,0)
            with open (in_filename,'r') as infile:
                Lines = infile.readlines()
                mass, pvalue = Lines[1].split()
                h_pvalue.SetBinContent(binxy,pvalue)
    c1 = ROOT.TCanvas()
    h_pvalue.Draw("colz")
    c1.SaveAs("test.png")

if __name__ == "__main__":
    pvalue2D()
