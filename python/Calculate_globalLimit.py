#!/usr/bin/env python

import ROOT
from array import array
import numpy as np
import argparse
from scipy.stats import norm

parser = argparse.ArgumentParser(description='')
parser.add_argument('--signame','-s',default="grav",type=str,help='grav or heavyhiggs')
parser.add_argument('--coupling','-c',default=14,type=int,help='coupling to calculate global significance')
parser.add_argument('--mass','-m',default=1300,type=int,help='mass to calculate global significance')
parser.add_argument('--outputDir','-o',default="./output/plots/2Dplot",type=str,help='output directory')
args = parser.parse_args()

def globalLimit():
    ROOT.gROOT.LoadMacro("~/rootlogon.C")

    m_gStyle = ROOT.TStyle();
    m_gStyle.SetOptFit(0);
    m_gStyle.SetPalette(55);

    masses=array('d')
    for mass in range(600,3010,10):
        masses.append(mass)
    couplings = array('d',[0.014, 0.361, 0.707, 1.054, 1.4, 2.450, 3.500, 4.550, 5.600])
    coupnames = array('i',[14, 361, 707, 1054, 1400, 2450, 3500, 4550, 5600])

    for icoup, coupling in enumerate(couplings):
        coupname = str(coupnames[icoup])
        zvalues, counts={}, {}
        # Record observed zvalues
        for mass in masses:
            in_filename = "ParallelForLimits/2023-11-03/finalResults_" + args.signame + "_" + coupname + "_" + str(int(mass)) + ".txt";
            with open (in_filename,'r') as infile:
                Lines = infile.readlines()
                if (Lines==0 or len(Lines[1].split())==1):
                    print("No limits for %f %f"%(coupling,mass))
                else:
                    zvalue=Lines[2].split()[1]
                    zvalues[mass]=zvalue

        # Switch to Toy significance to calculate global significance
        for itoy in range(100):
            toy_zvalues=[]
            for mass in masses:
                in_filename = "ParallelForLimits/2023-11-03/finalResults_" + args.signame + "_" + coupname + "_" + str(int(mass)) + ".txt";
                with open (in_filename,'r') as infile:
                    Lines = infile.readlines()
                    if (Lines==0 or len(Lines[1].split())==1):
                        print("No limits for %f %f"%(coupling,mass))
                    else:
                        toy_zvalue = Lines[3].split()[itoy]
                        toy_zvalues.append(toy_zvalue)
            sigma_max = max(toy_zvalues)
            for mass, zvalue in zvalues.items():
                if (sigma_max > zvalue): counts[mass] = counts[mass]+1


if __name__ == "__main__":
    globalLimit()
