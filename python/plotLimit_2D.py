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
    couplings = array('d',[14, 361, 707, 1054, 1400, 2450, 3500, 4550, 5600])
    h_sigma = ROOT.TH2F("h_sigma","h_sigma",len(masses)-1,masses,len(couplings)-1,couplings)

    for coupling in couplings:
        for mass in masses:
            print(coupling,mass)
            in_filename = "ParallelForLimits/2023-10-23/results/grav/" + str(int(coupling)) + "/finalResults_" + args.signame + "_" + str(int(coupling)) + "_" + str(int(mass)) + ".txt";
            binx = h_sigma.GetXaxis().FindBin(mass)
            biny = h_sigma.GetYaxis().FindBin(coupling)
            binxy = h_sigma.GetBin(binx,biny,0)
            with open (in_filename,'r') as infile:
                Lines = infile.readlines()
                if (len(Lines)>0 and len(Lines[1].split())>1):
                    pvalue=Lines[1].split()[1]
                    sigma = z_value_from_p_value(float(pvalue))
                    h_sigma.SetBinContent(binxy,sigma)
    c1 = ROOT.TCanvas()
    h_sigma.Draw("colz")
    c1.SaveAs("test.png")

if __name__ == "__main__":
    pvalue2D()
