#!/usr/bin/env python
#
# for year in {"2016","2017","2018"}; do for coup in {"kMpl01","kMpl02","kMpl001"}; do python python/plotNorm.py ../../SignalNorm_Splines_full.txt ../../SignalNorm_Splines_genFiducial.txt -y ${year} -c ${coup}; done; done
#
import ROOT
from array import array
import numpy as np
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

    ROOT.gROOT.LoadMacro("~/rootlogon.C")

    c1 = ROOT.TCanvas("c1","c1", 700, 600)
    l = ROOT.TLegend(0.4, 0.25, 0.88, 0.45)
    l.SetNColumns(2);
    if (args.coupling=="kMpl001"):
        l.SetHeader("#tilde{k}=0.01              #frac{#Gamma_{X}}{m_{X}} = 1.4 #times 10^{-4}","C")
        hh_coupling="0p014"
    elif (args.coupling=="kMpl01"):
        l.SetHeader("#tilde{k}=0.1               #frac{#Gamma_{X}}{m_{X}} = 1.4 #times 10^{-2}","C")
        hh_coupling="1p4"
    elif (args.coupling=="kMpl02"):
        l.SetHeader("#tilde{k}=0.2               #frac{#Gamma_{X}}{m_{X}} = 5.6 #times 10^{-2}","C")
        hh_coupling="5p6"

    l.SetBorderSize(0);
    l.SetFillStyle(0);
    luminosity = {"2016":35.9, "2017":41.5, "2018":59.7}
    color=[[0,2,4], [0,2,4]]
    linestyle=[1,1,10]
    markerstyle=[24,26,28]

    EBEBnorm_1, EBEEnorm_1, Allnorm_1, mass_1 =  array('d'), array('d') , array('d'), array('d')
    EBEBnorm_2, EBEEnorm_2, Allnorm_2, mass_2 =  array('d'), array('d') , array('d'), array('d')
    with open (args.in_filenames[0],'r') as infile:
        Lines = infile.readlines()
    for line in Lines:
        if (line.split()[0]==args.year and line.split()[1]==args.coupling and float(line.split()[2])%100==0):
            if (line.find("EBEB")!=-1): EBEBnorm_1.append(float(line.split(" ")[4])/luminosity[args.year])
            elif (line.find("EBEE")!=-1): EBEEnorm_1.append(float(line.split(" ")[4])/luminosity[args.year])
            elif (line.find("All")!=-1):
                Allnorm_1.append(float(line.split(" ")[4])/luminosity[args.year])
                mass_1.append(float(line.split(" ")[2]))
    with open (args.in_filenames[1],'r') as infile:
        Lines = infile.readlines()
    for line in Lines:
        if (line.split()[0]==args.year and line.split()[1]==hh_coupling and float(line.split()[2])%10==0):
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
    g_All_1.GetYaxis().SetTitle("#varepsilon #times A")
    g_All_1.GetXaxis().SetTitle("m_{X} (GeV)")
    # g_All_1.GetXaxis().CenterTitle(1)
    # g_All_1.GetYaxis().CenterTitle(1)
    g_All_1.SetLineColor(1)
    g_All_1.SetLineWidth(2)
    g_All_1.SetLineStyle(7)
    g_All_1.Draw("AL")
    g_All_1.GetYaxis().SetRangeUser(0,1.15)
    g_EBEB_1.SetLineColor(2)
    g_EBEB_1.SetLineWidth(2)
    g_EBEB_1.SetLineStyle(7)
    g_EBEB_1.Draw("LSame")
    g_EBEE_1.SetLineColor(4)
    g_EBEE_1.SetLineWidth(2)
    g_EBEE_1.SetLineStyle(7)
    g_EBEE_1.Draw("LSame");
    g_All_2.SetLineColor(1)
    g_All_2.SetLineWidth(3)
    g_All_2.Draw("LSame")
    g_EBEB_2.SetLineColor(2)
    g_EBEB_2.SetLineWidth(3)
    g_EBEB_2.Draw("LSame")
    g_EBEE_2.SetLineColor(4)
    g_EBEE_2.SetLineWidth(3)
    g_EBEE_2.Draw("LSame");

    l.AddEntry(g_All_1, "Total J=2", "l")
    l.AddEntry(g_All_2, "Total J=0", "l")
    l.AddEntry(g_EBEB_1, "EBEB J=2", "l")
    l.AddEntry(g_EBEB_2, "EBEB J=0", "l")
    l.AddEntry(g_EBEE_1, "EBEE J=2", "l")
    l.AddEntry(g_EBEE_2, "EBEE J=0", "l")
    l.Draw("same")

    cmsText=ROOT.TLatex(0.17,0.83, "CMS");
    cmsText.SetNDC(1);
    cmsText.SetTextFont(61);
    cmsText.SetLineColor(0);
    cmsText.SetLineStyle(1);
    cmsText.SetLineWidth(1);
    cmsText.SetTextSize(0.04);
    cmsText.Draw();

    extraText=ROOT.TLatex(0.24,0.83, "Simulation");
    extraText.SetNDC(1);
    extraText.SetTextFont(52);
    extraText.SetLineColor(0);
    extraText.SetLineStyle(1);
    extraText.SetLineWidth(1);
    extraText.SetTextSize(0.04);
    extraText.Draw();

    yearText=ROOT.TLatex(0.39,0.90, args.year);
    yearText.SetNDC(1);
    yearText.SetTextFont(52);
    yearText.SetLineColor(0);
    yearText.SetLineStyle(1);
    yearText.SetLineWidth(1);
    yearText.SetTextSize(0.04);
    # yearText.Draw();

    lumiText=ROOT.TLatex(0.8,0.90, "13 TeV");
    lumiText.SetNDC(1);
    lumiText.SetTextFont(42);
    lumiText.SetLineColor(0);
    lumiText.SetLineStyle(1);
    lumiText.SetLineWidth(1);
    lumiText.SetTextSize(0.04);
    lumiText.Draw();

    c1.SaveAs("%s/SignalNorm_%s_%s.png"%(args.outputDir,args.coupling,args.year))
    c1.SaveAs("%s/SignalNorm_%s_%s.pdf"%(args.outputDir,args.coupling,args.year))
