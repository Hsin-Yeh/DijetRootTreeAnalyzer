#!/usr/bin/env python

import ROOT
import argparse

parser = argparse.ArgumentParser(description='')
parser.add_argument('in_filenames',nargs="+",help='input filenames')
args = parser.parse_args()

def project(tree, h, var, cut):
    print 'projecting var: %s, cut: %s from tree: %s into hist: %s'%(var, cut, tree.GetName(), h.GetName())
    tree.Project(h.GetName(),var,cut)


if __name__ == "__main__":


    for in_filename in args.in_filenames:
        tfileIn = ROOT.TFile.Open(in_filename)
        thetree=tfileIn.Get("HighMassDiphoton")
        basename=in_filename.rsplit("/",1)[1].split(".root")[0]

        h_original = ROOT.TH1D("h_original",basename,200, 0, 2000)
        h_METFilters = ROOT.TH1D("h_METFilters",basename,200, 0, 2000)

        project(thetree, h_original, "mgg", "")
        if "2016" in in_filename:
            project(thetree, h_METFilters, "mgg", "passgoodVertices && passglobalSuperTightHalo2016Filter && passHBHENoiseFilter && passHBHENoiseIsoFilter && passEcalDeadCellTriggerPrimitiveFilter && passBadPFMuonFilter && passeeBadScFilter")
        elif "2017" in in_filename:
            project(thetree, h_METFilters, "mgg", "passgoodVertices && passglobalSuperTightHalo2016Filter && passHBHENoiseFilter && passHBHENoiseIsoFilter && passEcalDeadCellTriggerPrimitiveFilter && passBadPFMuonFilter && passeeBadScFilter && passecalBadCalibFilterUpdate")
        elif "2018" in in_filename:
            project(thetree, h_METFilters, "mgg", "passgoodVertices && passglobalSuperTightHalo2016Filter && passHBHENoiseFilter && passHBHENoiseIsoFilter && passEcalDeadCellTriggerPrimitiveFilter && passBadPFMuonFilter && passeeBadScFilter && passecalBadCalibFilterUpdate")

        n_original = h_original.GetEntries()
        n_METFilters = h_METFilters.GetEntries()
        n_diff = (n_original-n_METFilters)/n_original

        ROOT.gStyle.SetOptStat(0)
        c1 = ROOT.TCanvas()
        c1.SetLogy()
        h_METFilters.SetLineColor(4)
        h_METFilters.SetLineWidth(2)
        h_METFilters.GetXaxis().SetTitle("M_{#gamma#gamma}[GeV]")
        h_METFilters.GetYaxis().SetTitle("Events")
        h_METFilters.Draw("HIST");
        h_original.SetLineColor(2)
        h_original.SetLineWidth(2)
        h_original.Draw("HISTSame");

        # pad2 = ROOT.TPad("pad2","pad2",0,0,1,0.28)
        # h_METFilters.Add(h_original,-1)
        # h_METFilters.Divide(h_original)
        # h_METFilters.Draw()

        leg = ROOT.TLegend(0.35,0.7,0.88,0.88)
        leg.SetTextSize(0.03)
        leg.AddEntry(h_original,"without METFilters, Passed Events: {}".format(n_original),"l")
        leg.AddEntry(h_METFilters,"with METFilters, Passed Events: {}".format(n_METFilters),"l")
        leg.AddEntry(0,"Difference = {:.2f}%".format(n_diff*100),"")
        leg.Draw("same")

        c1.Update()
        c1.SaveAs("output/plots/METFilters_Study/compareMETFilters_{}.png".format(basename))
