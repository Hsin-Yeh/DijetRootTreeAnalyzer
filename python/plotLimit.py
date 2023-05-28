#!/usr/bin/env python

import ROOT
from array import array
import argparse

parser = argparse.ArgumentParser(description='')
parser.add_argument('--year','-y',default="2016",type=str,help='year')
parser.add_argument('--coupling','-c',default="kMpl001",type=str,help='coupling')
parser.add_argument('--signame','-s',default="grav",type=str,help='grav or heavyhiggs')
parser.add_argument('--outputDir','-o',default="./",type=str,help='output directory')
parser.add_argument('--debug','-d',action="store_true",help='debug mode')
parser.add_argument('--unblind',action="store_true",help='debug mode')
args = parser.parse_args()

if __name__ == "__main__":
    # mass = [750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750, 3000, 3250, 3500, 4000, 5000]
    # crossSection = [4.850e-02, 1.133e-02, 3.428e-03, 1.234e-03, 4.981e-04, 2.201e-04, 1.036e-04, 5.074e-05, 2.613e-05, 1.384e-05, 7.548e-06, 4.226e-06, 1.439e-06, 2.150e-07]
    # mass = [750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 3000, 3500, 4000, 4250, 4500, 4750, 5000, 5250, 5500, 5750, 6000, 6500, 7000, 8000]
    # crossSection = [4.870e+00, 1.120e+00, 3.413e-01, 1.224e-01, 4.940e-02, 2.180e-02, 1.025e-02, 5.051e-03, 1.373e-03, 4.229e-04, 1.435e-04, 8.663e-05, 5.367e-05, 3.368e-05, 2.163e-05, 1.398e-05, 9.145e-06, 6.022e-06, 3.967e-06, 1.742e-06, 7.583e-07, 1.269e-07]
    # mass = [750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 3000, 3500, 4000, 4500, 4750, 5000, 5250, 5500, 5750, 6000, 6500, 7000, 8000]
    # crossSection = [1.905e+01, 4.403e+00, 1.328e+00, 4.750e-01, 1.919e-01, 8.481e-02, 3.981e-02, 1.967e-02, 5.410e-03, 1.669e-03, 5.707e-04, 2.157e-04, 1.364e-04, 8.732e-05, 5.709e-05, 3.748e-05, 2.479e-05, 1.652e-05, 7.426e-06, 3.360e-06, 6.570e-07]

    in_filename = "finalResults_" + args.year + "_" + args.signame + "_" + args.coupling;
    mass_array, obs_array, exp_array, expP1s_array, expP2s_array, expM1s_array, expM2s_array = array('d'), array('d'), array('d'), array('d'), array('d'), array('d'), array('d');
    with open (in_filename,'r') as infile:
        Lines = infile.readlines()
    for line in Lines:
        mass, obs, exp, expP1s, expP2s, expM1s, expM2s = line.split()
        print (mass, obs, exp, expP1s, expP2s, expM1s, expM2s)
        mass_array.append(float(mass))
        obs_array.append(float(obs))
        exp_array.append(float(exp))
        expP1s_array.append(float(expP1s))
        expP2s_array.append(float(expP2s))
        expM1s_array.append(float(expM1s))
        expM2s_array.append(float(expM2s))


    m_gStyle = ROOT.TStyle();
    m_gStyle.SetOptFit(0);

    expGraph_init      = ROOT.TGraphErrors(len(mass_array),mass_array,exp_array);
    exp1SGraph_init    = ROOT.TGraphErrors(len(mass_array),mass_array,expM1s_array);
    exp2SGraph_init    = ROOT.TGraphErrors(len(mass_array),mass_array,expM2s_array);
    obsGraph_init      = ROOT.TGraphErrors(len(mass_array),mass_array,obs_array);

    # Add P1s to M1s graph
    for ipoint in range(1, len(mass_array)+1):
        exp1SGraph_init.SetPoint(len(mass_array)+ipoint,mass_array[-ipoint],expP1s_array[-ipoint]);
        exp2SGraph_init.SetPoint(len(mass_array)+ipoint,mass_array[-ipoint],expP2s_array[-ipoint]);

    expGraph = expGraph_init.Clone();
    exp1SGraph = exp1SGraph_init.Clone();
    exp2SGraph = exp2SGraph_init.Clone();
    obsGraph = obsGraph_init.Clone();

    canv = ROOT.TCanvas("canv","Title",800,600);
    canv.SetLogy();
    canv.SetLogx();
    canv.SetRightMargin(0.08);
    canv.SetLeftMargin(0.15);

    exp1SGraph.SetFillColor(3);
    exp2SGraph.SetFillColor(5);
    exp2SGraph.GetXaxis().SetTitleSize(0.045);
    exp2SGraph.GetYaxis().SetTitleSize(0.045);

    exp2SGraph.GetYaxis().SetRangeUser(0.005,20);
    exp2SGraph.GetYaxis().SetTitle("95% CL limit #sigma(pp#rightarrowG#rightarrow#gamma#gamma) (fb)" if args.signame == "grav" else "95% CL limit #sigma(pp#rightarrowS#rightarrow#gamma#gamma) (fb)" );
    exp2SGraph.GetXaxis().SetTitle("m_{G} (GeV)" if args.signame == "grav" else "m_{S} (GeV)");
    exp2SGraph.GetXaxis().SetMoreLogLabels();
    exp2SGraph.GetXaxis().SetRangeUser(600,8000);

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
    if (args.unblind): obsGraph.Draw("PL");
    # if (unblind) obsGraph.Draw("L");
    # obsGraph.Draw("LC");


    # grxs[coupling].SetLineWidth(3);
    # grxs[coupling].SetLineColor(kRed);
    # grxs[coupling].SetLineStyle(9);
    # grxs[coupling].SetMarkerStyle(20);
    # grxs[coupling].Draw("Lsame");

    gr_2016  = ROOT.TGraph();
    if (args.coupling=="kMpl001"): gr_2016.SetPoint(0,2300, 0.125977);
    if (args.coupling=="kMpl01"): gr_2016.SetPoint(0,4100, 0.0983398);
    if (args.coupling=="kMpl02"): gr_2016.SetPoint(0,4700, 0.1014);
    gr_2016.SetMarkerStyle(30);
    gr_2016.SetMarkerSize(4);
    gr_2016.SetMarkerColor(9);
    gr_2016.Draw("Psame");

    leg = ROOT.TLegend(0.55,0.6,0.75,0.85,"brNDC");
    leg.SetBorderSize(1);
    leg.SetTextFont(62);
    leg.SetLineColor(0);
    leg.SetLineStyle(1);
    leg.SetLineWidth(1);
    leg.SetFillColor(0);
    leg.SetFillStyle(1001);
    leg.SetTextSize(0.033);

    if ( args.coupling == "kMpl001" ): plabel = "#tilde{k}=0.01,J=2"
    elif ( args.coupling == "kMpl01" ): plabel = "#tilde{k}=0.1,J=2"
    elif ( args.coupling == "kMpl02" ): plabel = "#tilde{k}=0.2,J=2"
    elif ( args.coupling == "0p014"): plabel = "#frac{#Gamma}{m} = 1.4 #times 10^{-4},J=0"
    elif ( args.coupling == "1p4"): plabel = "#frac{#Gamma}{m} = 1.4 #times 10^{-2},J=0"
    elif ( args.coupling == "5p6"): plabel = "#frac{#Gamma}{m} = 5.6 #times 10^{-2},J=0"

    leg.SetHeader(plabel,"C");
    if ( args.signame == "grav" ):
        # leg.AddEntry(grxs[coupling],"G_{RS}#rightarrow#gamma#gamma (LO)","l");
        leg.AddEntry(gr_2016,"Published 2016 Mass Limit","P");
        leg.AddEntry(expGraph,"expected Limit","L"); #L_{int}=36.4/pb
        leg.AddEntry(exp1SGraph,"#pm1#sigma","F");
        leg.AddEntry(exp2SGraph,"#pm2#sigma","F");
        # leg.AddEntry(obsGraph,"observed Limit (Asymptotic)","L");
    leg.Draw();

    cmsText=ROOT.TLatex(0.17,0.90, "CMS");
    cmsText.SetNDC(1);
    cmsText.SetTextFont(61);
    cmsText.SetLineColor(0);
    cmsText.SetLineStyle(1);
    cmsText.SetLineWidth(1);
    cmsText.SetTextSize(0.035);
    cmsText.Draw();

    extraText=ROOT.TLatex(0.23,0.90, "Preliminary");
    extraText.SetNDC(1);
    extraText.SetTextFont(52);
    extraText.SetLineColor(0);
    extraText.SetLineStyle(1);
    extraText.SetLineWidth(1);
    extraText.SetTextSize(0.035);
    extraText.Draw();

    thelumi = {};
    thelumi["2016"]=35.9;
    thelumi["2017"]=41.5;
    thelumi["2018"]=59.7;
    thelumi["fullRun2"]=137.1;
    lumiText=ROOT.TLatex(0.70,0.90, "%d fb^{-1} (13 TeV)"%(thelumi[args.year]) );
    lumiText.SetNDC(1);
    lumiText.SetTextFont(42);
    lumiText.SetLineColor(0);
    lumiText.SetLineStyle(1);
    lumiText.SetLineWidth(1);
    lumiText.SetTextSize(0.035);
    lumiText.Draw();

    canv.SaveAs( "./limitplot_%s_%s_%s.png"% (args.signame, args.coupling, args.year) );

    outfile = ROOT.TFile( "./limitplot_%s_%s_%s.root"% (args.signame.c_str(), args.coupling, args.year) , "RECREATE");
    canv.Write();
    expGraph.SetName("expGraph");
    obsGraph.SetName("obsGraph");
    exp1SGraph.SetName("exp1SGraph");
    exp2SGraph.SetName("exp2SGraph");
    expGraph.Write();
    obsGraph.Write();
    exp1SGraph.Write();
    exp2SGraph.Write();

    outfile.Write();
    outfile.Close();
