#!/usr/bin/env python3

from optparse import OptionParser
import ROOT

from ROOT import TCanvas, TColor, TGaxis, TH1F, TPad
from ROOT import kBlack, kBlue, kRed


def createCanvasPads():
    ROOT.gStyle.SetOptStat(0)
    c = TCanvas("c", "canvas", 800, 800)
    # Upper histogram plot is pad1
    pad1 = TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
    pad1.SetBottomMargin(0)  # joins upper and lower plot
    # pad1.SetGridx()
    pad1.SetLogy()
    pad1.Draw()
    # Lower ratio plot is pad2
    c.cd()  # returns to main canvas before defining pad2
    pad2 = TPad("pad2", "pad2", 0, 0, 1, 0.3)
    pad2.SetTopMargin(0)  # joins upper and lower plot
    pad2.SetBottomMargin(0.35)
    pad2.SetGridy()
    pad2.Draw()

    return c, pad1, pad2

def createRatio(h1, h2):
    h3 = h1.Clone("h3")
    h3.SetLineColor(kRed)
    h3.SetLineWidth(2)
    h3.SetMarkerStyle(21)
    h3.SetTitle("")
    h3.SetMinimum(0)
    h3.SetMaximum(2)
    # Set up plot for markers and errors
    h3.Sumw2()
    h3.SetStats(0)
    h3.Divide(h2)

    # Adjust y-axis settings
    y = h3.GetYaxis()
    y.SetTitle("Extrapolate / MC")
    y.SetNdivisions(505)
    y.SetTitleSize(25)
    y.SetTitleFont(43)
    y.SetTitleOffset(1.55)
    y.SetLabelFont(43)
    y.SetLabelSize(20)

    # Adjust x-axis settings
    x = h3.GetXaxis()
    x.SetTitle("M_{#gamma#gamma} [GeV]")
    x.SetTitleSize(35)
    x.SetTitleFont(43)
    x.SetTitleOffset(0.9)
    x.SetLabelFont(43)
    x.SetLabelSize(20)

    return h3

def main():
    plotxmin=500
    plotxmax=800

    f_ext = ROOT.TFile("ResonanceShapes_GluGluSpin0ToGammaGamma_W_0p014_EBEB_2017_finebinned.root")
    f_gen = ROOT.TFile("InputShapes_GluGluSpin0ToGammaGamma_W_0p014_EBEB_2017.root")

    h_ext = f_ext.Get("h_gg_650")
    h_gen = f_gen.Get("h_GluGluSpin0ToGammaGamma_W_0p014_M650_2017_8Gev")

    factor=1
    h_ext.Scale(factor/h_ext.Integral());
    h_gen.Scale(factor/h_gen.Integral());
    h_compare = createRatio(h_ext, h_gen)

    c, pad1, pad2 = createCanvasPads()
    pad1.cd()
    h_gen.Draw("HIST")
    h_gen.GetXaxis().SetRangeUser(plotxmin,plotxmax)
    h_gen.GetXaxis().SetTitle("M_{#gamma#gamma} [GeV]")
    h_gen.GetXaxis().SetTitleSize(0.07)
    h_gen.GetXaxis().SetTitleOffset(0.8)
    h_gen.GetYaxis().SetTitle("a.u.")
    h_gen.GetYaxis().SetTitleSize(0.07)
    h_gen.GetYaxis().SetTitleOffset(0.8)
    h_gen.SetLineColor(2)
    h_gen.SetLineWidth(2)
    h_gen.SetTitle("ggH 650GeV 0.014% 2017")
    h_ext.Draw("HISTSame")
    h_ext.SetLineWidth(2)
    leg = ROOT.TLegend(0.6,0.7,0.9,0.88)
    leg.AddEntry(h_gen,"MC Generated (UL)","l")
    leg.AddEntry(h_ext,"Extrapolation (ReReco)","l")
    leg.Draw()
    axis = TGaxis(-5, 20, -5, 220, 20, 220, 510, "")
    axis.SetLabelFont(43)
    axis.SetLabelSize(15)
    axis.Draw()
    pad2.cd()
    h_compare.Draw("HIST")
    h_compare.GetXaxis().SetRangeUser(plotxmin,plotxmax)
    h_compare.GetXaxis().SetTitle("M_{#gamma#gamma} [GeV]")

    c.SaveAs("test.png")

if __name__ == '__main__':
    main()
