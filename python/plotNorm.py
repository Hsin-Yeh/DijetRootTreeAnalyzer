#!/usr/bin/env python

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

    c1 = ROOT.TCanvas()
    pad1 = ROOT.TPad("pad1","",0,0.30,1,1)
    pad1.SetBottomMargin(0);
    pad1.SetGridx();
    pad1.Draw()
    pad1.cd()
    l = ROOT.TLegend(0.15, 0.65, 0.85, 0.85)
    l.SetNColumns(2);
    l.SetHeader("%s %s"%(args.year, args.coupling),"C")
    l.SetFillStyle(0);
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
    g_All_1.GetYaxis().SetTitle("Normalization")
    g_All_1.SetLineColor(3)
    g_All_1.SetLineWidth(1)
    g_All_1.Draw("AL")
    g_All_1.GetYaxis().SetRangeUser(0,1)
    g_EBEB_1.SetLineColor(6)
    g_EBEB_1.SetLineWidth(1)
    g_EBEB_1.Draw("LSame")
    g_EBEE_1.SetLineColor(8)
    g_EBEE_1.SetLineWidth(1)
    g_EBEE_1.Draw("LSame");
    g_All_2.SetLineColor(1)
    g_All_2.SetLineWidth(1)
    g_All_2.Draw("LSame")
    g_EBEB_2.SetLineColor(2)
    g_EBEB_2.SetLineWidth(1)
    g_EBEB_2.Draw("LSame")
    g_EBEE_2.SetLineColor(4)
    g_EBEE_2.SetLineWidth(1)
    g_EBEE_2.Draw("LSame");

    l.AddEntry(g_All_1, "Total w/o Prefire reweight", "l")
    l.AddEntry(g_All_2, "Total with Prefire reweight", "l")
    l.AddEntry(g_EBEB_1, "EBEB w/o Prefire reweight", "l")
    l.AddEntry(g_EBEB_2, "EBEB with Prefire reweight", "l")
    l.AddEntry(g_EBEE_1, "EBEE w/o Prefire reweight", "l")
    l.AddEntry(g_EBEE_2, "EBEE with Prefire reweight", "l")
    l.Draw("same")

    c1.cd()
    pad2 = ROOT.TPad("pad2","",0,0.05,1,0.3)
    pad2.SetTopMargin(0);
    pad2.SetBottomMargin(0.2);
    pad2.SetGridx();
    pad2.Draw()
    pad2.cd()
    EBEBnorm_diff, EBEEnorm_diff, All_diff= array('d'), array('d'), array('d')
    EBEBnorm_diff=np.divide(EBEBnorm_1,EBEBnorm_2)
    EBEEnorm_diff=np.divide(EBEEnorm_1,EBEEnorm_2)
    Allnorm_diff=np.divide(Allnorm_1,Allnorm_2)
    g_diff_EBEB = ROOT.TGraph(len(mass_1), mass_1, EBEBnorm_diff)
    g_diff_EBEE = ROOT.TGraph(len(mass_1), mass_1, EBEEnorm_diff)
    g_diff_All = ROOT.TGraph(len(mass_1), mass_1, Allnorm_diff)

    g_diff_All.SetTitle("")
    g_diff_All.GetXaxis().SetTitle("Mass_{X} [GeV]")
    g_diff_All.GetYaxis().SetTitle("new/old")
    g_diff_All.SetLineColor(1)
    g_diff_All.GetYaxis().SetTitleSize(20);
    g_diff_All.GetYaxis().SetTitleFont(43);
    g_diff_All.GetYaxis().SetTitleOffset(1.55);
    g_diff_All.GetYaxis().SetLabelFont(43);
    g_diff_All.GetYaxis().SetLabelSize(15);
    g_diff_All.GetXaxis().SetTitleSize(20);
    g_diff_All.GetXaxis().SetTitleFont(43);
    g_diff_All.GetXaxis().SetTitleOffset(2.5);
    g_diff_All.GetXaxis().SetLabelFont(43);
    g_diff_All.GetXaxis().SetLabelSize(15);
    g_diff_All.Draw("AL")
    g_diff_All.GetYaxis().SetRangeUser(0.97,1.15)
    g_diff_EBEB.SetLineColor(2)
    g_diff_EBEB.Draw("LSame")
    g_diff_EBEE.SetLineColor(4)
    g_diff_EBEE.Draw("LSame")

    l_diff = ROOT.TLegend(0.5,0.7,0.85,0.85)
    l_diff.SetNColumns(3)
    l_diff.SetTextSize(0.1)
    l_diff.SetFillStyle(0);
    l_diff.SetBorderSize(0)
    l_diff.AddEntry(g_diff_All,"All","l")
    l_diff.AddEntry(g_diff_EBEB,"EBEB","l")
    l_diff.AddEntry(g_diff_EBEE,"EBEE","l")
    l_diff.Draw()

    c1.SaveAs("%s/SignalNorm_prefiring_%s_%s.png"%(args.outputDir,args.coupling,args.year))
