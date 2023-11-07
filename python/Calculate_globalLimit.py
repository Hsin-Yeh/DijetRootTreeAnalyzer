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
parser.add_argument('--inputDir','-i',default="./ParallelForLimits/2023-11-06/",type=str,help='input directory')
parser.add_argument('--out_filename','-o',default="./global_significance.txt",type=str,help='output filename')
args = parser.parse_args()

def z_value_from_p_value(p_value, two_tailed=False):
    alpha = p_value / 2 if two_tailed else p_value
    z_value = norm.ppf(1 - alpha)
    return z_value

def globalLimit():
    numtoys=1000
    f = open(args.out_filename, "w")
    f.close()

    ROOT.gROOT.LoadMacro("~/rootlogon.C")
    m_gStyle = ROOT.TStyle();
    m_gStyle.SetOptFit(0);
    m_gStyle.SetPalette(55);

    masses=array('d')
    for mass in range(600,2010,10):
        masses.append(mass)
    coupnames = array('i',[14, 1400, 5600])

    for coupname in coupnames:
        zvalues, counts={}, {}
        # Record observed zvalues
        for mass in masses:
            counts[mass]=0

            in_filename = args.inputDir + "/finalResults_" + args.signame + "_" + str(coupname) + "_" + str(int(mass)) + ".txt";
            try:
                with open (in_filename,'r') as infile:
                    Lines = infile.readlines()
                    if (Lines==0 or len(Lines[1].split())==1):
                        print("No limits for %i %i"%(coupname,mass))
                    else:
                        zvalue=Lines[2].split()[1]
                        zvalues[mass]=zvalue
            except IOError:
                print("No limits for %i %i"%(coupname,mass))

        # Switch to Toy significance to calculate global significance
        for itoy in range(numtoys):
            toy_zvalues=[]
            for mass in masses:
                in_filename = args.inputDir + "/finalResults_" + args.signame + "_" + str(coupname) + "_" + str(int(mass)) + ".txt";
                try:
                    with open (in_filename,'r') as infile:
                        Lines = infile.readlines()
                        if (len(Lines)==4 and len(Lines[1].split())==2):
                            toy_zvalue = Lines[3].split()[itoy]
                            toy_zvalues.append(toy_zvalue)
                except IOError:
                    print("No limits for %i %i"%(coupname,mass))

            sigma_max = max(toy_zvalues)
            # print(coupname, len(toy_zvalues), masses[toy_zvalues.index(max(toy_zvalues))], sigma_max)
            for mass, zvalue in zvalues.items():
                if (sigma_max > zvalue):
                    counts[mass] = counts[mass]+1

        with open (args.out_filename,'a') as outfile:
            for mass in masses:
                global_p_value = float(float(counts[mass])/numtoys)
                global_z_value = z_value_from_p_value(global_p_value)
                outfile.write('%s, %i, %f, %f, %f\n'%(coupname, mass, float(zvalues[mass]), global_p_value, global_z_value))

if __name__ == "__main__":
    globalLimit()
