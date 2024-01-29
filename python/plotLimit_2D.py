#!/usr/bin/env python

import ROOT
from array import array
import numpy as np
import argparse
from scipy.stats import norm

parser = argparse.ArgumentParser(description='')
parser.add_argument('--signame','-s',default="grav",type=str,help='grav or heavyhiggs')
parser.add_argument('--inputDir','-i',default="./ParallelForLimits/2024-01-11_heavyhiggs",type=str,help='input directory')
parser.add_argument('--outputDir','-o',default="./output/plots/2Dplot",type=str,help='output directory')
args = parser.parse_args()

def z_value_from_p_value(p_value, two_tailed=False):
    alpha = p_value / 2 if two_tailed else p_value
    z_value = norm.ppf(1 - alpha)
    return z_value

def redrawBorder():
    # code from -> https://root-forum.cern.ch/t/how-to-redraw-axis-and-plot-borders/28252
    ROOT.gPad.Update();
    ROOT.gPad.RedrawAxis();

def lumi(year):
    if (year=="2016"): return 35.9
    elif (year=="2017"): return 41.5
    elif (year=="2018"): return 59.7
    elif (year=="fullRun2"): return 138
    else: return 0

def Acceptance(year, coupling, mass):
    if (args.signame == "grav"): Acceptance_file = "/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/SignalNorm_Splines_full_multiWidth.txt"
    elif (args.signame == "heavyhiggs"): Acceptance_file = "/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/SignalNorm_Splines_genFiducial_multiWidth.txt"
    with open(Acceptance_file) as infile:
        Lines = infile.readlines()
    totalNorm=0
    for line in Lines:
        y, c, m, cat, norm = line.split()
        if (year=="fullRun2" and c==coupling and m==mass and cat=='All'):
                totalNorm += float(norm)
        elif (y==year and c==coupling and m==mass and cat=='All'):
            totalNorm = float(norm)
            break
    totalNorm = float(totalNorm)/float(lumi(year))
    if (year!="fullRun2"): totalNorm = 0.85
    return totalNorm


def limit_1D(mass_array, exp_array, expM1s_array, expM2s_array, expP1s_array, expP2s_array, obs_array, coupling):
    expGraph_init      = ROOT.TGraphErrors(len(mass_array),mass_array,exp_array);
    exp1SGraph_init    = ROOT.TGraphErrors(len(mass_array),mass_array,expM1s_array);
    exp2SGraph_init    = ROOT.TGraphErrors(len(mass_array),mass_array,expM2s_array);
    obsGraph_init      = ROOT.TGraphErrors(len(mass_array),mass_array,obs_array);

    # Add P1s to M1s graph
    for ipoint in range(1, len(mass_array)+1):
        exp1SGraph_init.SetPoint(len(mass_array)+ipoint-1,mass_array[-ipoint],expP1s_array[-ipoint]);
        exp2SGraph_init.SetPoint(len(mass_array)+ipoint-1,mass_array[-ipoint],expP2s_array[-ipoint]);

    expGraph = expGraph_init.Clone();
    exp1SGraph = exp1SGraph_init.Clone();
    exp2SGraph = exp2SGraph_init.Clone();
    obsGraph = obsGraph_init.Clone();

    canv = ROOT.TCanvas("canv","Title",800,600);
    canv.SetLogy();
    # canv.SetLogx();
    canv.SetRightMargin(0.08);
    canv.SetLeftMargin(0.15);

    exp1SGraph.SetFillColor(3);
    exp2SGraph.SetFillColor(5);
    exp2SGraph.GetXaxis().SetTitleSize(0.045);
    exp2SGraph.GetYaxis().SetTitleSize(0.045);

    # exp2SGraph.GetYaxis().SetRangeUser(0.9,200);
    exp2SGraph.GetYaxis().SetTitle("95% CL limit #sigma(pp#rightarrowG#rightarrow#gamma#gamma) (fb)" if args.signame == "grav" else "95% CL limit #sigma(pp#rightarrowS#rightarrow#gamma#gamma) (fb)" );
    exp2SGraph.GetXaxis().SetTitle("m_{G} (GeV)" if args.signame == "grav" else "m_{S} (GeV)");
    exp2SGraph.GetXaxis().SetTitleOffset(1.3);
    exp2SGraph.GetXaxis().SetMoreLogLabels();
    exp2SGraph.GetXaxis().SetRangeUser(600,5000)
    exp2SGraph.SetTitle("")

    exp2SGraph.Draw("AF");
    exp1SGraph.Draw("F");
    expGraph.SetLineColor(4);
    expGraph.SetLineStyle(7);
    expGraph.SetLineWidth(3);
    expGraph.Draw("CL");

    obsGraph.SetMarkerColor(1);
    obsGraph.SetMarkerStyle(20);
    obsGraph.SetMarkerSize(0.5);
    obsGraph.SetLineWidth(2);
    obsGraph.SetLineColor(1);
    obsGraph.SetLineStyle(1);
    obsGraph.Draw("PL");

    if (args.signame == "grav"):
        g_xs_TuneCP2.SetLineWidth(3);
        g_xs_TuneCP2.SetLineColor(2);
        g_xs_TuneCP2.SetLineStyle(9);
        g_xs_TuneCP2.SetMarkerStyle(20);
        g_xs_TuneCP2.Draw("Lsame");

        # g_xs_TuneCUEP8M1.SetLineWidth(3);
        # g_xs_TuneCUEP8M1.SetLineColor(8);
        # g_xs_TuneCUEP8M1.SetLineStyle(9);
        # g_xs_TuneCUEP8M1.SetMarkerStyle(20);
        # g_xs_TuneCUEP8M1.Draw("Lsame");

    # gr_2016  = ROOT.TGraph();
    # if (args.coupling=="kMpl001"): gr_2016.SetPoint(0,2245, 0.1175);
    # if (args.coupling=="kMpl01"): gr_2016.SetPoint(0,4100, 0.0924);
    # if (args.coupling=="kMpl02"): gr_2016.SetPoint(0,4700, 0.0924);
    # gr_2016.SetMarkerStyle(30);
    # gr_2016.SetMarkerSize(4);
    # gr_2016.SetMarkerColor(9);
    # gr_2016.Draw("Psame");

    leg = ROOT.TLegend(0.55,0.5,0.85,0.87,"brNDC");
    leg.SetBorderSize(1);
    leg.SetTextFont(62);
    leg.SetLineColor(0);
    leg.SetLineStyle(1);
    leg.SetLineWidth(2);
    leg.SetFillColor(0);
    leg.SetFillStyle(1001);
    leg.SetTextSize(0.04);

    # if ( args.coupling == "kMpl001" ): plabel = "#tilde{k}=0.01,  J=2"
    # elif ( args.coupling == "kMpl01" ): plabel = "#tilde{k}=0.1,  J=2"
    # elif ( args.coupling == "kMpl02" ): plabel = "#tilde{k}=0.2,  J=2"
    # elif ( args.coupling == "0p014"): plabel = "#frac{#Gamma}{m} = 1.4 #times 10^{-4}, J=0"
    # elif ( args.coupling == "1p4"): plabel = "#frac{#Gamma}{m} = 1.4 #times 10^{-2}, J=0"
    # elif ( args.coupling == "5p6"): plabel = "#frac{#Gamma}{m} = 5.6 #times 10^{-2}, J=0"

    plabel=coupling
    leg.SetHeader(plabel,"C");
    if ( args.signame == "grav" ):
        leg.AddEntry(g_xs_TuneCP2,"G_{RS}#rightarrow#gamma#gamma (LO)","l");
        # leg.AddEntry(g_xs_TuneCUEP8M1,"G_{RS}#rightarrow#gamma#gamma (LO) CUEP8M1","l");
        # leg.AddEntry(gr_2016,"Published 2016 Mass Limit","P");
    leg.AddEntry(expGraph,"expected Limit","L"); #L_{int}=36.4/pb
    leg.AddEntry(exp1SGraph,"#pm1#sigma","F");
    leg.AddEntry(exp2SGraph,"#pm2#sigma","F");
    leg.AddEntry(obsGraph,"observed Limit","L");
    leg.Draw();

    cmsText=ROOT.TLatex(0.17,0.90, "CMS");
    cmsText.SetNDC(1);
    cmsText.SetTextFont(61);
    cmsText.SetLineColor(0);
    cmsText.SetLineStyle(1);
    cmsText.SetLineWidth(1);
    cmsText.SetTextSize(0.04);
    cmsText.Draw();

    # extraText=ROOT.TLatex(0.23,0.90, "Preliminary");
    # extraText.SetNDC(1);
    # extraText.SetTextFont(52);
    # extraText.SetLineColor(0);
    # extraText.SetLineStyle(1);
    # extraText.SetLineWidth(1);
    # extraText.SetTextSize(0.04);
    # extraText.Draw();

    # lumiText=ROOT.TLatex(0.72,0.90, "%d fb^{-1} (13 TeV)"%(lumi(year)) );
    # # lumiText=ROOT.TLatex(0.70,0.90, "%d fb^{-1} (13 TeV)"%(138));
    # lumiText.SetNDC(1);
    # lumiText.SetTextFont(42);
    # lumiText.SetLineColor(0);
    # lumiText.SetLineStyle(1);
    # lumiText.SetLineWidth(1);
    # lumiText.SetTextSize(0.04);
    # lumiText.Draw();

    # redrawBorder()

    canv.SaveAs("test_%s.png"%coupling)
    # canv.SaveAs( "./limitplot_%s_%s_%s_unblind.pdf"% (signame, coupling, args.year) );



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
        mass_array, obs_array, exp_array, expP1s_array, expP2s_array, expM1s_array, expM2s_array, exp1s_array, exp2s_array, mass_long_array = array('d'), array('d'), array('d'), array('d'), array('d'), array('d'), array('d'), array('d'), array('d'), array('d');
        coupname = str(coupnames[icoup])
        print(coupname)
        for mass in masses:
            in_filename = args.inputDir + "/results/finalResults_" + args.signame + "_" + coupname + "_" + str(int(mass)) + ".txt";
            norm = Acceptance("fullRun2", str(coupname), str(int(mass)))
            binx = h_zvalue.GetXaxis().FindBin(mass)
            biny = h_zvalue.GetYaxis().FindBin(coupling)
            binxy = h_zvalue.GetBin(binx,biny,0)
            try:
                with open (in_filename,'r') as infile:
                    Lines = infile.readlines()
                    if (Lines==0 or len(Lines[1].split())==1):
                        print("No limits for %f %f"%(coupling,mass))
                    else:
                        mass, obs, expP2s, expP1s, exp, expM1s, expM2s = Lines[0].split()
                        pvalue=Lines[1].split()[1]
                        # zvalue=Lines[2].split()[1]
                        zvalue = z_value_from_p_value(float(pvalue))
                        h_obslimit.SetBinContent(binxy,float(obs)/norm)
                        h_explimit.SetBinContent(binxy,float(exp)/norm)
                        h_pvalue.SetBinContent(binxy,float(pvalue))
                        h_zvalue.SetBinContent(binxy,float(zvalue))
                        mass_array.append(float(mass))
                        obs_array.append(float(obs)/norm)
                        exp_array.append(float(exp)/norm)
                        expP1s_array.append(float(expP1s)/norm)
                        expP2s_array.append(float(expP2s)/norm)
                        expM1s_array.append(float(expM1s)/norm)
                        expM2s_array.append(float(expM2s)/norm)
            except IOError:
                print("%s not found"%(in_filename))
        # limit_1D(mass_array, exp_array, expM1s_array, expM2s_array, expP1s_array, expP2s_array, obs_array, coupname)


    cmsText=ROOT.TLatex(0.14,0.90, "CMS");
    cmsText.SetNDC(1);
    cmsText.SetTextFont(61);
    cmsText.SetLineColor(0);
    cmsText.SetLineStyle(1);
    cmsText.SetLineWidth(1);
    cmsText.SetTextSize(0.04);

    # extraText=ROOT.TLatex(0.23,0.90, "Preliminary");
    # extraText.SetNDC(1);
    # extraText.SetTextFont(52);
    # extraText.SetLineColor(0);
    # extraText.SetLineStyle(1);
    # extraText.SetLineWidth(1);
    # extraText.SetTextSize(0.04);

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
    # extraText.Draw();
    lumiText.Draw();
    c1.SaveAs("%s/pvalue_%s.pdf"%(args.outputDir,args.signame))

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
    # extraText.Draw();
    lumiText.Draw();
    c1.SaveAs("%s/zvalue_%s.pdf"%(args.outputDir,args.signame))

    h_obslimit.SetTitle("")
    h_obslimit.GetXaxis().SetTitle("m_{G} (GeV)" if args.signame == "grav" else "m_{S} (GeV)");
    h_obslimit.GetXaxis().SetTitleSize(0.05)
    h_obslimit.GetYaxis().SetTitle("#Gamma_{G}/M_{G} (%)" if args.signame == "grav" else "#Gamma_{S}/M_{S} (%)");
    h_obslimit.GetYaxis().SetTitleSize(0.05)
    h_obslimit.GetYaxis().SetTitle("95% CL limit #sigma(pp#rightarrowG#rightarrow#gamma#gamma) (fb)" if args.signame == "grav" else "95% CL limit #sigma(pp#rightarrowS#rightarrow#gamma#gamma) (fb)" );
    h_obslimit.GetZaxis().SetTitleOffset(1.1)
    h_obslimit.GetZaxis().SetTitleSize(0.05)
    h_obslimit.Draw("colz")
    cmsText.Draw();
    # extraText.Draw();
    lumiText.Draw();
    c1.SaveAs("%s/observedlimit_%s.pdf"%(args.outputDir,args.signame))

    h_explimit.SetTitle("")
    h_explimit.GetXaxis().SetTitle("m_{G} (GeV)" if args.signame == "grav" else "m_{S} (GeV)");
    h_explimit.GetXaxis().SetTitleSize(0.05)
    h_explimit.GetYaxis().SetTitle("#Gamma_{G}/M_{G} (%)" if args.signame == "grav" else "#Gamma_{S}/M_{S} (%)");
    h_explimit.GetYaxis().SetTitleSize(0.05)
    h_explimit.GetYaxis().SetTitle("95% CL limit #sigma(pp#rightarrowG#rightarrow#gamma#gamma) (fb)" if args.signame == "grav" else "95% CL limit #sigma(pp#rightarrowS#rightarrow#gamma#gamma) (fb)" );
    h_explimit.GetZaxis().SetTitleOffset(1.1)
    h_explimit.GetZaxis().SetTitleSize(0.05)
    h_explimit.Draw("colz")
    cmsText.Draw();
    # extraText.Draw();
    lumiText.Draw();
    c1.SaveAs("%s/expectedlimit_%s.pdf"%(args.outputDir,args.signame))

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
    # extraText.Draw();
    lumiText.Draw();
    c1.SaveAs("%s/pvalue_zoomin_%s.pdf"%(args.outputDir,args.signame))

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
    # extraText.Draw();
    lumiText.Draw();
    c1.SaveAs("%s/zvalue_zoomin_%s.pdf"%(args.outputDir,args.signame))

    h_obslimit.SetTitle("")
    h_obslimit.GetXaxis().SetTitle("m_{G} (GeV)" if args.signame == "grav" else "m_{S} (GeV)");
    h_obslimit.GetXaxis().SetTitleSize(0.05)
    h_obslimit.GetXaxis().SetRangeUser(600,2500)
    h_obslimit.GetYaxis().SetTitle("#Gamma_{G}/M_{G} (%)" if args.signame == "grav" else "#Gamma_{S}/M_{S} (%)");
    h_obslimit.GetYaxis().SetTitleSize(0.05)
    h_obslimit.GetYaxis().SetTitle("95% CL limit #sigma(pp#rightarrowG#rightarrow#gamma#gamma) (fb)" if args.signame == "grav" else "95% CL limit #sigma(pp#rightarrowS#rightarrow#gamma#gamma) (fb)" );
    h_obslimit.GetZaxis().SetTitleOffset(1.1)
    h_obslimit.GetZaxis().SetTitleSize(0.05)
    h_obslimit.Draw("colz")
    cmsText.Draw();
    # extraText.Draw();
    lumiText.Draw();
    c1.SaveAs("%s/observedlimit_zoomin_%s.pdf"%(args.outputDir,args.signame))

    h_explimit.SetTitle("")
    h_explimit.GetXaxis().SetTitle("m_{G} (GeV)" if args.signame == "grav" else "m_{S} (GeV)");
    h_explimit.GetXaxis().SetTitleSize(0.05)
    h_explimit.GetXaxis().SetRangeUser(600,2500)
    h_explimit.GetYaxis().SetTitle("#Gamma_{G}/M_{G} (%)" if args.signame == "grav" else "#Gamma_{S}/M_{S} (%)");
    h_explimit.GetYaxis().SetTitleSize(0.05)
    h_explimit.GetYaxis().SetTitle("95% CL limit #sigma(pp#rightarrowG#rightarrow#gamma#gamma) (fb)" if args.signame == "grav" else "95% CL limit #sigma(pp#rightarrowS#rightarrow#gamma#gamma) (fb)" );
    h_explimit.GetZaxis().SetTitleOffset(1.1)
    h_explimit.GetZaxis().SetTitleSize(0.05)
    h_explimit.Draw("colz")
    cmsText.Draw();
    # extraText.Draw();
    lumiText.Draw();
    c1.SaveAs("%s/expectedlimit_zoomin_%s.pdf"%(args.outputDir,args.signame))


if __name__ == "__main__":
    pvalue2D()
