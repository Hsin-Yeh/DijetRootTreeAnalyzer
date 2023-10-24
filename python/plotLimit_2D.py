#!/usr/bin/env python

import ROOT
from array import array
import numpy as np
import argparse
from scipy.stats import norm

parser = argparse.ArgumentParser(description='')
parser.add_argument('--year','-y',default="2016",type=str,help='year')
parser.add_argument('--coupling','-c',default="kMpl001",type=str,help='coupling')
parser.add_argument('--signame','-s',default="grav",type=str,help='grav or heavyhiggs')
parser.add_argument('--outputDir','-o',default="./",type=str,help='output directory')
parser.add_argument('--debug','-d',action="store_true",help='debug mode')
parser.add_argument('--unblind',action="store_true",help='debug mode')
args = parser.parse_args()

def z_value_from_p_value(p_value, two_tailed=True):
    alpha = p_value / 2 if two_tailed else p_value
    z_value = norm.ppf(1 - alpha)
    return z_value

def pvalue2D():
    ROOT.gROOT.LoadMacro("~/rootlogon.C")

    m_gStyle = ROOT.TStyle();
    m_gStyle.SetOptFit(0);
    m_gStyle.SetPalette(55);

    masses=array('d')
    for mass in range(600,5010,10):
        masses.append(mass)
    couplings = array('d',[0.00014, 0.00361, 0.00707, 0.01054, 0.014, 0.02450, 0.03500, 0.04550, 0.05600])
    coupnames = array('s',[14, 361, 707, 1054, 1400, 2450, 3500, 4550, 5600])
    h_zvalue = ROOT.TH2F("h_zvalue","zvalue",len(masses)-1,masses,len(couplings)-1,couplings)
    h_pvalue = ROOT.TH2F("h_pvalue","pvalue",len(masses)-1,masses,len(couplings)-1,couplings)

    for icoup, coupling in enumerate(couplings):
        coupname = coupnames[icoup]
        for mass in masses:
            in_filename = "ParallelForLimits/2023-10-23/results/grav/" + coupname + "/finalResults_" + args.signame + "_" + coupname + "_" + str(int(mass)) + ".txt";
            binx = h_zvalue.GetXaxis().FindBin(mass)
            biny = h_zvalue.GetYaxis().FindBin(coupling)
            binxy = h_zvalue.GetBin(binx,biny,0)
            with open (in_filename,'r') as infile:
                Lines = infile.readlines()
                if (len(Lines)>0 and len(Lines[1].split())>1):
                    pvalue=Lines[1].split()[1]
                    h_pvalue.SetBinContent(binxy,float(pvalue))
                    zvalue = z_value_from_p_value(float(pvalue))
                    h_zvalue.SetBinContent(binxy,zvalue)
    c1 = ROOT.TCanvas()
    h_pvalue.Draw("colz")
    c1.SaveAs("pvalue.png")
    h_zvalue.Draw("colz")
    c1.SaveAs("zvalue.png")


if __name__ == "__main__":
    pvalue2D()
