#!/usr/bin/env python

import argparse
import ROOT

parser = argparse.ArgumentParser(description='')
parser.add_argument('in_filenames',nargs="+",help='input filenames')
parser.add_argument('--outputDir','-o',default="./output",type=str,help='output directory')
parser.add_argument('--report','-r',default=10000,type=int,help='report every x events')
parser.add_argument('--debug','-d',action="store_true",help='debug mode')
args = parser.parse_args()

coup="kMpl01"
mass="3000"
year="2017"
c1 = ROOT.TCanvas()
color_template = [1, 2, 4]
h={}
for ifile, in_filename in enumerate(args.in_filenames):
    print(in_filename)
    infile = ROOT.TFile.Open(in_filename)
    infile.cd()
    h[ifile] = infile.Get("h_RSGravitonToGammaGamma_%s_M%s_%s"%(coup, mass, year))
    h[ifile].SetLineColor(color_template[ifile])
    if( ifile == 0 ):
        h[ifile].Draw("HIST")
    else:
        h[ifile].Draw("HISTSame")

h[0].GetXaxis().SetRangeUser(0.7,1.3)
c1.SetLogy()
c1.SaveAs("test.png")
