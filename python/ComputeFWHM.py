#!/usr/bin/env python

import ROOT as rt
import rootTools
from array import array

import argparse
parser = argparse.ArgumentParser(description='Compute histogram bin width with signal resolution')
parser.add_argument('in_filenames',nargs="+",help='input filenames')
args = parser.parse_args()

for infile in args.in_filenames:
    year = infile.split('.root')[0].split('_')[-1]
    mass = int(infile.split('_M_')[1].split('_TuneCP2')[0])
    title =  infile.split('_M_')[0].split('/')[-1]
    print(title,year,mass)
    tfileIn = rt.TFile.Open(infile)

    massMin=0.8*mass;
    massMax=1.2*mass;
    h_mgg = rt.TH1D('h_mgg','h_mgg',1000,massMin,massMax)
    thetree=tfileIn.Get("HighMassDiphoton")
    project(thetree,h_mgg_1GeVbin,"mgg")

    bin1 = h_mgg.FindFirstBinAbove(h_mgg.GetMaximum()/2)
    bin1 = h_mgg.FindLastBinAbove(h_mgg.GetMaximum()/2)
    mean = h_mgg.GetBinCenter(h->GetMaximumBin())
    fwhm = h_mgg.GetBinCenter(bin2) - hist.GetBinCenter(bin1);
