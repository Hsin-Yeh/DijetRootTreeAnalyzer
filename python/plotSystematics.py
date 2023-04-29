#!/usr/bin/env python

import ROOT
import argparse
import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser(description='')
parser.add_argument('in_filenames',nargs="+",help='input filenames')
parser.add_argument('--outputDir','-d',default="output/plots/sysplots",type=str,help='output plot directory')
args = parser.parse_args()

def project(tree, h, var, cut):
    print 'projecting var: %s, cut: %s from tree: %s into hist: %s'%(var, cut, tree.GetName(), h.GetName())
    tree.Project(h.GetName(),var,cut)


if __name__ == "__main__":

    year = args.in_filenames[0].rsplit("/",1)[1].split(".root")[0].split("pythia8_")[1]
    if (args.in_filenames[0].find("RSG")):
        coup = args.in_filenames[0].rsplit("/",1)[1].split("_M_")[0].split("GammaGamma_")[1]
    elif (args.in_filenames[0].find("GluGlu")):
        coup = args.in_filenames[0].rsplit("/",1)[1].split("_M_")[0].split("_W_")[1]
    energySyslist_Up = {"energyScaleGain"   : "ph1energyScaleGainUp*ph2energyScaleGainUp",
                        "energyScaleStat"   : "ph1energyScaleStatUp*ph2energyScaleStatUp",
                        "energyScaleSyst"   : "ph1energyScaleSystUp*ph2energyScaleSystUp",
                        "energySigma"       : "ph1energySigmaUp*ph2energySigmaUp"}

    energySyslist_Down = {"energyScaleStat"   : "ph1energyScaleStatDown*ph2energyScaleStatDown",
                          "energyScaleSyst"   : "ph1energyScaleSystDown*ph2energyScaleSystDown",
                          "energyScaleGain"   : "ph1energyScaleGainDown*ph2energyScaleGainDown",
                          "energySigma"       : "ph1energySigmaDown*ph2energySigmaDown"}
    cats=["EBEB","EBEE"]

    sysvalues_Up={}
    sysvalues_Down={}
    syserrors_Up={}
    syserrors_Down={}
    c1 = ROOT.TCanvas()
    for cat in cats:
        if cat == "EBEB" : catID = 0
        elif cat == "EBEE" : catID = 1
        for energySys in energySyslist_Up:
            sysvalues_Up.clear()
            sysvalues_Up.clear()
            sysvalues_Down.clear()
            syserrors_Up.clear()
            syserrors_Down.clear()

            for in_filename in args.in_filenames:
                tfileIn = ROOT.TFile.Open(in_filename)
                thetree=tfileIn.Get("HighMassDiphoton")
                mass=in_filename.rsplit("/",1)[1].split("_M_")[1].split("_TuneCP2_")[0]
                catCut = 'eventClass==%d'%(catID)
                # allCut=""
                genMassCut = 'mggGen>%f && mggGen<%f'%(float(mass)*0.8, float(mass)*1.2)
                allCut = '(' + catCut + ')*(' + genMassCut + ')'
                # histonames
                h_sysName_Up="h_sysUp_" + energySys + "M_" + mass + "_" + coup + "_" + cat + "_" + year
                h_sysName_Down="h_sysDown_" + energySys + "M_" + mass + "_" + coup + "_" + cat + "_" + year
                h_mggName_Up="h_mggUp_" + energySys + "M_" + mass + "_" + coup + "_" + cat + "_" + year
                h_mggName_Down="h_mggDown_" + energySys + "M_" + mass + "_" + coup + "_" + cat + "_" + year
                # Define histos
                h_energySys_Up = ROOT.TH1D(h_sysName_Up,h_sysName_Up,20, 0.9, 1.1)
                h_energySys_Down = ROOT.TH1D(h_sysName_Down,h_sysName_Down,20, 0.9, 1.1)
                h_mgg_Up = ROOT.TH1D(h_mggName_Up,h_mggName_Up,1000, 0, 1.5)
                h_mgg_Down = ROOT.TH1D(h_mggName_Down,h_mggName_Down,1000, 0, 1.5)
                # Project histos
                project(thetree, h_energySys_Up, energySyslist_Up[energySys], allCut)
                project(thetree, h_energySys_Down, energySyslist_Down[energySys], allCut)
                project(thetree,h_mgg_Up, "mgg*%s/%f"%(energySyslist_Up[energySys],float(mass)), allCut)
                project(thetree,h_mgg_Down, "mgg*%s/%f"%(energySyslist_Down[energySys],float(mass)), allCut)
                # Draw histos
                if (energySys=="energyScaleGain"):
                    h_energySys_Up.SetLineColor(2)
                    h_energySys_Down.SetLineColor(4)
                    h_energySys_Up.Draw("HIST")
                    h_energySys_Down.Draw("HISTsame")
                    leg = ROOT.TLegend(0.2,0.65,0.6,0.8)
                    leg.AddEntry(h_energySys_Up,"+1#sigma","l")
                    leg.AddEntry(h_energySys_Down,"-1#sigma","l")
                    leg.Draw("same")
                    c1.SaveAs("%s/%s.png"%(args.outputDir, h_sysName_Up))
                    h_mgg_Up.SetLineColor(2)
                    h_mgg_Down.SetLineColor(4)
                    h_mgg_Up.Draw("HIST")
                    h_mgg_Down.Draw("HISTsame")
                    leg.Draw("same")
                    c1.SaveAs("%s/%s.png"%(args.outputDir, h_mggName_Up))
                # Record the mean and errors
                sysvalues_Up[float(mass)] = h_energySys_Up.GetMean()
                sysvalues_Down[float(mass)] = h_energySys_Down.GetMean()
                syserrors_Up[float(mass)] = h_energySys_Up.GetStdDev()
                syserrors_Down[float(mass)] = h_energySys_Up.GetStdDev()

                tfileIn.Close()

            sorted_masses = [x[0] for x in sorted(sysvalues_Up.items())]
            sorted_masses.insert(0,0)
            sorted_sysvalues_Up = [x[1] for x in sorted(sysvalues_Up.items())]
            sorted_sysvalues_Down = [x[1] for x in sorted(sysvalues_Down.items())]
            sorted_syserrors_Up = [x[1] for x in sorted(syserrors_Up.items())]
            sorted_syserrors_Down = [x[1] for x in sorted(syserrors_Down.items())]
            print(sorted_sysvalues_Up)
            print(sorted_syserrors_Up)

            # Create a histogram and fill it with the data
            h_Up = ROOT.TH1F("h_Up","",len(sorted_masses)-1,np.array(sorted_masses))
            h_Down = ROOT.TH1F("h_Down","",len(sorted_masses)-1,np.array(sorted_masses))
            for i in range(len(sorted_masses)-1):
                h_Up.SetBinContent(i+1, sorted_sysvalues_Up[i])
                h_Down.SetBinContent(i+1, sorted_sysvalues_Down[i])
                h_Up.SetBinError(i+1, sorted_syserrors_Up[i])
                h_Down.SetBinError(i+1, sorted_syserrors_Down[i])

            plotTitle=energySys+"_"+coup+"_"+cat+"_"+year
            h_Up.SetTitle(plotTitle)
            h_Up.SetLineColor(2)
            h_Up.SetLineWidth(4)
            h_Up.GetXaxis().SetTitle("Mass_{X} [GeV]")
            h_Up.Draw("HIST")
            h_Up.GetYaxis().SetRangeUser(h_Down.GetMinimum()*0.99,h_Up.GetMaximum()*1.01)
            # h_Up.GetXaxis().SetRangeUser(1800,sorted_masses[-1])
            h_Down.SetLineColor(4)
            h_Down.SetLineWidth(4)
            h_Down.Draw("HISTsame")
            h_Up.SetStats(False)
            leg = ROOT.TLegend(0.16,0.75,0.45,0.85)
            leg.AddEntry(h_Up,"+1#sigma","l")
            leg.AddEntry(h_Down,"-1#sigma","l")
            leg.SetFillStyle(0)
            leg.SetBorderSize(0)
            leg.Draw("same")
            c1.SaveAs("%s/%s_%s_%s_%s.png"%(args.outputDir, energySys, coup, cat, year))
