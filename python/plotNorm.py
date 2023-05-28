#!/usr/bin/env python

import ROOT
from array import array
import argparse

parser = argparse.ArgumentParser(description='')
parser.add_argument('in_filenames',nargs="+",help='input filenames')
parser.add_argument('--outputDir','-o',default="./",type=str,help='output directory')
parser.add_argument('--report','-r',default=10000,type=int,help='report every x events')
parser.add_argument('--debug','-d',action="store_true",help='debug mode')
parser.add_argument('--year','-y',default="2016",type=str,help='year')
parser.add_argument('--coupling','-c',default="kMpl001",type=str,help='coupling')
args = parser.parse_args()


if __name__ == "__main__":

    for ifile, in_filename in enumerate(args.in_filenames):
        EBEBnorm, EBEEnorm, Allnorm =  array('d'), array('d') , array('d')
        with open (in_filename,'r') as infile:
            Lines = infile.readlines()
        for line in Lines:
            if (line.find(args.year)!=-1 and line.find(args.coupling)!=-1):
                if (line.find("EBEB")!=-1): EBEBnorm.append(float(line.split(" ")[4]))
                elif (line.find("EBEE")!=-1): EBEEnorm.append(float(line.split(" ")[4]))
                elif (line.find("All")!=-1):
                    Allnorm.append(line.split(" ")[4])
                    mass.append(line.split(" ")[3])
        c1 = ROOT.TCanvas()
        l = ROOT.TLegend(0.6, 0.55, 0.8, 0.7)
        g_EBEB = ROOT.TGraph(len(mass), mass, EBEBnorm)
        g_EBEE = ROOT.TGraph(len(mass), mass, EBEEnorm)
        g_All = ROOT.TGraph(len(mass), mass, Allnorm)

        g_EBEB.SetTitle("")
        g_EBEB.GetXaxis().SetTitle("Mass_{X} [GeV]")
        g_EBEB.GetYaxis().SetTitle("Normalization")
        g_EBEB.SetMarkerColor(2)
        g_EBEB.SetMarkerSize(2)
        # g_EBEB.SetLineStyle(10)
        g_EBEB.Draw("AP");
        # g_FC.SetMarkerStyle(24)

        # l.AddEntry(g_FC, "FC", "P")
        # l.AddEntry(g_ZFC, "ZFC", "P")
        # l.Draw("same")

    c1.SaveAs("test.png")
