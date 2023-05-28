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

    luminosity = {"2016":35.9, "2017":41.5, "2018":59.7}
    color={"All":1,"EBEB":2,"EBEE":4}
    linestyle=[1,9,10]
    for ifile, in_filename in enumerate(args.in_filenames):
        EBEBnorm, EBEEnorm, Allnorm, mass =  array('d'), array('d') , array('d'), array('d')
        with open (in_filename,'r') as infile:
            Lines = infile.readlines()
        for line in Lines:
            if (line.find(args.year)!=-1 and line.find(args.coupling)!=-1):
                if (line.find("EBEB")!=-1): EBEBnorm.append(float(line.split(" ")[4])/luminosity[args.year])
                elif (line.find("EBEE")!=-1): EBEEnorm.append(float(line.split(" ")[4])/luminosity[args.year])
                elif (line.find("All")!=-1):
                    Allnorm.append(float(line.split(" ")[4])/luminosity[args.year])
                    mass.append(float(line.split(" ")[2]))
        c1 = ROOT.TCanvas()
        l = ROOT.TLegend(0.6, 0.55, 0.8, 0.7)
        g_EBEB = ROOT.TGraph(len(mass), mass, EBEBnorm)
        g_EBEE = ROOT.TGraph(len(mass), mass, EBEEnorm)
        g_All = ROOT.TGraph(len(mass), mass, Allnorm)

        g_All.SetTitle("")
        g_All.GetXaxis().SetTitle("Mass_{X} [GeV]")
        g_All.GetYaxis().SetTitle("Normalization")
        g_All.SetMarkerColor(color["All"])
        g_All.SetMarkerSize(1)
        g_All.SetLineColor(color["All"])
        g_All.SetLineWidth(2)
        g_All.SetLineStyle(linestyle[ifile])
        if (ifile==0): g_All.Draw("AL")
        else: g_All.Draw("LSame")
        g_All.GetYaxis().SetRangeUser(0,1)
        g_EBEB.SetMarkerColor(color["EBEB"])
        g_EBEB.SetMarkerSize(1)
        g_EBEB.SetLineColor(color["EBEB"])
        g_EBEB.SetLineWidth(2)
        g_EBEB.SetLineStyle(linestyle[ifile])
        g_EBEB.Draw("LSame")
        g_EBEE.SetMarkerColor(color["EBEE"])
        g_EBEE.SetMarkerSize(1)
        g_EBEE.SetLineColor(color["EBEE"])
        g_EBEE.SetLineWidth(2)
        g_EBEE.SetLineStyle(linestyle[ifile])
        g_EBEE.Draw("LSame");

        # g_FC.SetMarkerStyle(24)

        # l.AddEntry(g_FC, "FC", "P")
        # l.AddEntry(g_ZFC, "ZFC", "P")
        # l.Draw("same")

    c1.SaveAs("test.png")
