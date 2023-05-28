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

    c1 = ROOT.TCanvas()
    pad1 = ROOT.TPad("pad1","",0.05,0.40,0.95,0.95)
    pad2 = ROOT.TPad("pad2","",0.05,0.05,0.95,0.35)
    pad1.cd()
    l = ROOT.TLegend(0.6, 0.55, 0.8, 0.7)
    luminosity = {"2016":35.9, "2017":41.5, "2018":59.7}
    color=[[1,2,4], [5,6,8]]
    linestyle=[1,1,10]
    markerstyle=[24,26,28]

    g_EBEB, g_EBEE, g_All = {},{},{}
    EBEBnorms, EBEEnorms, Allnorms, masses = {}, {}, {}, {}
    for ifile, in_filename in enumerate(args.in_filenames):
        EBEBnorm, EBEEnorm, Allnorm, mass =  array('d'), array('d') , array('d'), array('d')
        with open (in_filename,'r') as infile:
            Lines = infile.readlines()
        for line in Lines:
            if (line.split()[0]==args.year and line.split()[1]==args.coupling and float(line.split()[2])%100!=0 ):
                if (line.find("EBEB")!=-1): EBEBnorm.append(float(line.split(" ")[4])/luminosity[args.year])
                elif (line.find("EBEE")!=-1): EBEEnorm.append(float(line.split(" ")[4])/luminosity[args.year])
                elif (line.find("All")!=-1):
                    Allnorm.append(float(line.split(" ")[4])/luminosity[args.year])
                    mass.append(float(line.split(" ")[2]))
        EBEBnorms[ifile] = EBEBnorm
        EBEEnorms[ifile] = EBEEnorm
        Allnorms[ifile] = Allnorm
        g_EBEB[ifile] = ROOT.TGraph(len(mass), mass, EBEBnorm)
        g_EBEE[ifile] = ROOT.TGraph(len(mass), mass, EBEEnorm)
        g_All[ifile] = ROOT.TGraph(len(mass), mass, Allnorm)

        g_All[ifile].SetTitle("")
        g_All[ifile].GetXaxis().SetTitle("Mass_{X} [GeV]")
        g_All[ifile].GetYaxis().SetTitle("Normalization")
        g_All[ifile].SetMarkerColor(color[0][ifile])
        g_All[ifile].SetMarkerSize(1)
        g_All[ifile].SetLineColor(color[0][ifile])
        g_All[ifile].SetLineWidth(1)
        g_All[ifile].SetLineStyle(linestyle[ifile])
        g_All[ifile].SetMarkerStyle(markerstyle[ifile])
        if (ifile==0): g_All[ifile].Draw("AL")
        else: g_All[ifile].Draw("LSame")
        g_All[ifile].GetYaxis().SetRangeUser(0,1)
        g_EBEB[ifile].SetMarkerColor(color[1][ifile])
        g_EBEB[ifile].SetMarkerSize(1)
        g_EBEB[ifile].SetLineColor(color[1][ifile])
        g_EBEB[ifile].SetLineWidth(1)
        g_EBEB[ifile].SetLineStyle(linestyle[ifile])
        g_All[ifile].SetMarkerStyle(markerstyle[ifile])
        g_EBEB[ifile].Draw("LSame")
        g_EBEE[ifile].SetMarkerColor(color[2][ifile])
        g_EBEE[ifile].SetMarkerSize(1)
        g_EBEE[ifile].SetLineColor(color[2][ifile])
        g_EBEE[ifile].SetLineWidth(1)
        g_EBEE[ifile].SetLineStyle(linestyle[ifile])
        g_EBEE[ifile].Draw("LSame");
        g_All[ifile].SetMarkerStyle(markerstyle[ifile])

        # l.AddEntry(g_FC, "FC", "P")
        # l.AddEntry(g_ZFC, "ZFC", "P")
        # l.Draw("same")

    pad2.cd()
    EBEBnorm_diff, EBEEnorm_diff, All_diff= array('d'), array('d'), array('d')
    EBEBnorm_diff=EBEBnorm[0]/EBEBnorm[1]
    EBEEnorm_diff=EBEEnorm[0]/EBEEnorm[1]
    Allnorm_diff=Allnorm[0]/Allnorm[1]
    g_diff_EBEB = ROOT.TGraph(len(masses[0]), masses[0], EBEBnorm_diff)
    g_diff_EBEE = ROOT.TGraph(len(masses[0]), masses[0], EBEEnorm_diff)
    g_diff_All = ROOT.TGraph(len(masses[0]), masses[0], Allnorm_diff)
    g_diff_EBEB.Draw("AL")
    g_diff_EBEE.Draw("LSame")
    g_diff_All.Draw("LSame")

    c1.SaveAs("test.png")
