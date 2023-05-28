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
    # pad2 = ROOT.TPad("pad2","",0.05,0.05,0.95,0.35)
    # pad1.cd()
    l = ROOT.TLegend(0.6, 0.55, 0.8, 0.7)
    luminosity = {"2016":35.9, "2017":41.5, "2018":59.7}
    color=[[1,2,4], [5,6,8]]
    linestyle=[1,1,10]
    markerstyle=[24,26,28]

    EBEBnorm_1, EBEEnorm_1, Allnorm_1, mass_1 =  array('d'), array('d') , array('d'), array('d')
    EBEBnorm_2, EBEEnorm_2, Allnorm_2, mass_2 =  array('d'), array('d') , array('d'), array('d')
    with open (args.in_filenames[0],'r') as infile:
        Lines = infile.readlines()
    for line in Lines:
        if (line.split()[0]==args.year and line.split()[1]==args.coupling):
            if (line.find("EBEB")!=-1): EBEBnorm_1.append(float(line.split(" ")[4])/luminosity[args.year])
            elif (line.find("EBEE")!=-1): EBEEnorm_1.append(float(line.split(" ")[4])/luminosity[args.year])
            elif (line.find("All")!=-1):
                Allnorm_1.append(float(line.split(" ")[4])/luminosity[args.year])
                mass_1.append(float(line.split(" ")[2]))
    with open (args.in_filenames[1],'r') as infile:
        Lines = infile.readlines()
    for line in Lines:
        if (line.split()[0]==args.year and line.split()[1]==args.coupling):
            if (line.find("EBEB")!=-1): EBEBnorm_2.append(float(line.split(" ")[4])/luminosity[args.year])
            elif (line.find("EBEE")!=-1): EBEEnorm_2.append(float(line.split(" ")[4])/luminosity[args.year])
            elif (line.find("All")!=-1):
                Allnorm_2.append(float(line.split(" ")[4])/luminosity[args.year])
                mass_2.append(float(line.split(" ")[2]))

    g_EBEB_1 = ROOT.TGraph(len(mass_1), mass_1, EBEBnorm_1)
    g_EBEE_1 = ROOT.TGraph(len(mass_1), mass_1, EBEEnorm_1)
    g_All_1 = ROOT.TGraph(len(mass_1), mass_1, Allnorm_1)
    g_EBEB_2 = ROOT.TGraph(len(mass_2), mass_2, EBEBnorm_2)
    g_EBEE_2 = ROOT.TGraph(len(mass_2), mass_2, EBEEnorm_2)
    g_All_2 = ROOT.TGraph(len(mass_2), mass_2, Allnorm_2)

    g_All_1.SetTitle("")
    g_All_1.GetXaxis().SetTitle("Mass_{X} [GeV]")
    g_All_1.GetYaxis().SetTitle("Normalization")
    g_All_1.SetLineColor(1)
    g_All_1.SetLineWidth(1)
    g_All_1.Draw("AL")
    g_All_1.GetYaxis().SetRangeUser(0,1)
    g_EBEB_1.SetLineColor(2)
    g_EBEB_1.SetLineWidth(1)
    g_EBEB_1.Draw("LSame")
    g_EBEE_1.SetLineColor(4)
    g_EBEE_1.SetLineWidth(1)
    g_EBEE_1.Draw("LSame");
    # g_All_2.SetLineColor(5)
    # g_All_2.SetLineWidth(1)
    # g_All_2.Draw("LSame")
    # g_EBEB_2.SetLineColor(6)
    # g_EBEB_2.SetLineWidth(1)
    # g_EBEB_2.Draw("LSame")
    # g_EBEE_2.SetLineColor(8)
    # g_EBEE_2.SetLineWidth(1)
    # g_EBEE_2.Draw("LSame");

    # l.AddEntry(g_FC, "FC", "P")
    # l.AddEntry(g_ZFC, "ZFC", "P")
    # l.Draw("same")

# pad2.cd()
# EBEBnorm_diff, EBEEnorm_diff, All_diff= array('d'), array('d'), array('d')
# EBEBnorm_diff=EBEBnorm[0]/EBEBnorm[1]
# EBEEnorm_diff=EBEEnorm[0]/EBEEnorm[1]
# Allnorm_diff=Allnorm[0]/Allnorm[1]
# g_diff_EBEB = ROOT.TGraph(len(masses[0]), masses[0], EBEBnorm_diff)
# g_diff_EBEE = ROOT.TGraph(len(masses[0]), masses[0], EBEEnorm_diff)
# g_diff_All = ROOT.TGraph(len(masses[0]), masses[0], Allnorm_diff)
# g_diff_EBEB.Draw("AL")
# g_diff_EBEE.Draw("LSame")
# g_diff_All.Draw("LSame")

    c1.SaveAs("test.png")
