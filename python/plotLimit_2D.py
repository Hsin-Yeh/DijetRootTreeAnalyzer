#!/usr/bin/env python

import ROOT
from array import array
import numpy as np
import argparse
from scipy.stats import norm

parser = argparse.ArgumentParser(description='')
parser.add_argument('--year','-y',default="2016",type=str,help='year')
parser.add_argument('--signame','-s',default="grav",type=str,help='grav or heavyhiggs')
parser.add_argument('--outputDir','-o',default="./",type=str,help='output directory')
args = parser.parse_args()

def z_value_from_p_value(p_value, two_tailed=False):
    alpha = p_value / 2 if two_tailed else p_value
    z_value = norm.ppf(1 - alpha)
    return z_value

def pvalue2D():
    ROOT.gROOT.LoadMacro("~/rootlogon.C")

    m_gStyle = ROOT.TStyle();
    m_gStyle.SetOptFit(0);
    m_gStyle.SetPalette(55);

    masses=array('d')
    for mass in range(600,5010,10):
        masses.append(mass)
    couplings = array('d',[0.014, 0.361, 0.707, 1.054, 1.4, 2.450, 3.500, 4.550, 5.600])
    coupnames = array('i',[14, 361, 707, 1054, 1400, 2450, 3500, 4550, 5600])
    h_zvalue = ROOT.TH2F("h_zvalue","zvalue",len(masses)-1,masses,len(couplings)-1,couplings)
    h_pvalue = ROOT.TH2F("h_pvalue","pvalue",len(masses)-1,masses,len(couplings)-1,couplings)
    h_obslimit = ROOT.TH2F("h_obslimit","observed limit",len(masses)-1,masses,len(couplings)-1,couplings)
    h_explimit = ROOT.TH2F("h_explimit","expected limit",len(masses)-1,masses,len(couplings)-1,couplings)

    for icoup, coupling in enumerate(couplings):
        coupname = str(coupnames[icoup])
        for mass in masses:
            in_filename = "ParallelForLimits/2023-10-25/results/grav/" + coupname + "/finalResults_" + args.signame + "_" + coupname + "_" + str(int(mass)) + ".txt";
            binx = h_zvalue.GetXaxis().FindBin(mass)
            biny = h_zvalue.GetYaxis().FindBin(coupling)
            binxy = h_zvalue.GetBin(binx,biny,0)
            with open (in_filename,'r') as infile:
                Lines = infile.readlines()
                if (Lines==0 or len(Lines[1].split())==1):
                    print("No limits for %f %f"%(coupling,mass))
                else:
                    mass, obs, expP2s, expP1s, exp, expM1s, expM2s = Lines[0].split()
                    pvalue=Lines[1].split()[1]
                    zvalue = z_value_from_p_value(float(pvalue))
                    h_obslimit.SetBinContent(binxy,float(obs))
                    h_explimit.SetBinContent(binxy,float(exp))
                    h_pvalue.SetBinContent(binxy,float(pvalue))
                    h_zvalue.SetBinContent(binxy,float(zvalue))

    cmsText=ROOT.TLatex(0.14,0.90, "CMS");
    cmsText.SetNDC(1);
    cmsText.SetTextFont(61);
    cmsText.SetLineColor(0);
    cmsText.SetLineStyle(1);
    cmsText.SetLineWidth(1);
    cmsText.SetTextSize(0.04);

    extraText=ROOT.TLatex(0.23,0.90, "Preliminary");
    extraText.SetNDC(1);
    extraText.SetTextFont(52);
    extraText.SetLineColor(0);
    extraText.SetLineStyle(1);
    extraText.SetLineWidth(1);
    extraText.SetTextSize(0.04);

    lumiText=ROOT.TLatex(0.54,0.90, "138 fb^{-1} (13 TeV)");
    lumiText.SetNDC(1);
    lumiText.SetTextFont(42);
    lumiText.SetLineColor(0);
    lumiText.SetLineStyle(1);
    lumiText.SetLineWidth(1);
    lumiText.SetTextSize(0.04);

    c1 = ROOT.TCanvas("c1","c1",600,600)
    c1.SetRightMargin(0.2)
    h_pvalue.SetTitle("")
    h_pvalue.GetXaxis().SetTitle("M_{X} [GeV]")
    h_pvalue.GetXaxis().SetTitleSize(0.05)
    h_pvalue.GetYaxis().SetTitle("#Gamma_{X}/M_{X} [%]")
    h_pvalue.GetYaxis().SetTitleSize(0.05)
    h_pvalue.GetZaxis().SetTitle("p value")
    h_pvalue.GetZaxis().SetTitleOffset(0.9)
    h_pvalue.GetZaxis().SetTitleSize(0.05)
    h_pvalue.Draw("colz")
    cmsText.Draw();
    extraText.Draw();
    lumiText.Draw();
    c1.SaveAs("%s/pvalue.png"%(args.outputDir))

    h_zvalue.SetTitle("")
    h_zvalue.GetXaxis().SetTitle("M_{X} [GeV]")
    h_zvalue.GetXaxis().SetTitleSize(0.05)
    h_zvalue.GetYaxis().SetTitle("#Gamma_{X}/M_{X} [%]")
    h_zvalue.GetYaxis().SetTitleSize(0.05)
    h_zvalue.GetZaxis().SetTitle("Z value (#sigma)")
    h_zvalue.GetZaxis().SetTitleOffset(0.9)
    h_zvalue.GetZaxis().SetTitleSize(0.05)
    h_zvalue.SetMinimum(-0.01)
    h_zvalue.Draw("colz")
    cmsText.Draw();
    extraText.Draw();
    lumiText.Draw();
    c1.SaveAs("%s/zvalue.png"%(args.outputDir))

    h_obslimit.SetTitle("")
    h_obslimit.GetXaxis().SetTitle("M_{X} [GeV]")
    h_obslimit.GetXaxis().SetTitleSize(0.05)
    h_obslimit.GetYaxis().SetTitle("#Gamma_{X}/M_{X} [%]")
    h_obslimit.GetYaxis().SetTitleSize(0.05)
    h_obslimit.GetZaxis().SetTitle("#sigmaB(X#rightarrow#gamma#gamma)_{95%CL} (fb)")
    h_obslimit.GetZaxis().SetTitleOffset(1.1)
    h_obslimit.GetZaxis().SetTitleSize(0.05)
    h_obslimit.Draw("colz")
    cmsText.Draw();
    extraText.Draw();
    lumiText.Draw();
    c1.SaveAs("%s/observedlimit.png"%(args.outputDir))

    h_explimit.SetTitle("")
    h_explimit.GetXaxis().SetTitle("M_{X} [GeV]")
    h_explimit.GetXaxis().SetTitleSize(0.05)
    h_explimit.GetYaxis().SetTitle("#Gamma_{X}/M_{X} [%]")
    h_explimit.GetYaxis().SetTitleSize(0.05)
    h_explimit.GetZaxis().SetTitle("#sigmaB(X#rightarrow#gamma#gamma)_{95%CL} (fb)")
    h_explimit.GetZaxis().SetTitleOffset(1.1)
    h_explimit.GetZaxis().SetTitleSize(0.05)
    h_explimit.Draw("colz")
    cmsText.Draw();
    extraText.Draw();
    lumiText.Draw();
    c1.SaveAs("%s/expectedlimit.png"%(args.outputDir))

    ########## Set Range 600-2500GeV
    h_pvalue.SetTitle("")
    h_pvalue.GetXaxis().SetTitle("M_{X} [GeV]")
    h_pvalue.GetXaxis().SetTitleSize(0.05)
    h_pvalue.GetXaxis().SetRangeUser(600,2500)
    h_pvalue.GetYaxis().SetTitle("#Gamma_{X}/M_{X} [%]")
    h_pvalue.GetYaxis().SetTitleSize(0.05)
    h_pvalue.GetZaxis().SetTitle("p value")
    h_pvalue.GetZaxis().SetTitleOffset(0.9)
    h_pvalue.GetZaxis().SetTitleSize(0.05)
    h_pvalue.Draw("colz")
    cmsText.Draw();
    extraText.Draw();
    lumiText.Draw();
    c1.SaveAs("%s/pvalue_zoomin.png"%(args.outputDir))

    h_zvalue.SetTitle("")
    h_zvalue.GetXaxis().SetTitle("M_{X} [GeV]")
    h_zvalue.GetXaxis().SetTitleSize(0.05)
    h_zvalue.GetXaxis().SetRangeUser(600,2500)
    h_zvalue.GetYaxis().SetTitle("#Gamma_{X}/M_{X} [%]")
    h_zvalue.GetYaxis().SetTitleSize(0.05)
    h_zvalue.GetZaxis().SetTitle("Z value (#sigma)")
    h_zvalue.GetZaxis().SetTitleOffset(0.9)
    h_zvalue.GetZaxis().SetTitleSize(0.05)
    h_zvalue.SetMinimum(-0.01)
    h_zvalue.Draw("colz")
    cmsText.Draw();
    extraText.Draw();
    lumiText.Draw();
    c1.SaveAs("%s/zvalue_zoomin.png"%(args.outputDir))

    h_obslimit.SetTitle("")
    h_obslimit.GetXaxis().SetTitle("M_{X} [GeV]")
    h_obslimit.GetXaxis().SetTitleSize(0.05)
    h_obslimit.GetXaxis().SetRangeUser(600,2500)
    h_obslimit.GetYaxis().SetTitle("#Gamma_{X}/M_{X} [%]")
    h_obslimit.GetYaxis().SetTitleSize(0.05)
    h_obslimit.GetZaxis().SetTitle("#sigmaB(X#rightarrow#gamma#gamma)_{95%CL} (fb)")
    h_obslimit.GetZaxis().SetTitleOffset(1.1)
    h_obslimit.GetZaxis().SetTitleSize(0.05)
    h_obslimit.Draw("colz")
    cmsText.Draw();
    extraText.Draw();
    lumiText.Draw();
    c1.SaveAs("%s/observedlimit_zoomin.png"%(args.outputDir))

    h_explimit.SetTitle("")
    h_explimit.GetXaxis().SetTitle("M_{X} [GeV]")
    h_explimit.GetXaxis().SetTitleSize(0.05)
    h_explimit.GetXaxis().SetRangeUser(600,2500)
    h_explimit.GetYaxis().SetTitle("#Gamma_{X}/M_{X} [%]")
    h_explimit.GetYaxis().SetTitleSize(0.05)
    h_explimit.GetZaxis().SetTitle("#sigmaB(X#rightarrow#gamma#gamma)_{95%CL} (fb)")
    h_explimit.GetZaxis().SetTitleOffset(1.1)
    h_explimit.GetZaxis().SetTitleSize(0.05)
    h_explimit.Draw("colz")
    cmsText.Draw();
    extraText.Draw();
    lumiText.Draw();
    c1.SaveAs("%s/expectedlimit_zoomin.png"%(args.outputDir))


if __name__ == "__main__":
    pvalue2D()
