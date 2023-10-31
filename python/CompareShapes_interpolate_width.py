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
    y.SetTitle("Interpolate / MC")
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
    plotxmin=600
    plotxmax=1500

    f_gen = ROOT.TFile("ResonanceShapes_InputShapes_RSGravitonToGammaGamma_kMpl01_EBEB_2016_fineBinning.root")
    f_int = ROOT.TFile("width_InputShapes_RSGravitonToGammaGamma_EBEB_2016_1000GeV.root")

    h_int = f_int.Get("h_gg_1400")
    h_gen = f_gen.Get("h_gg_1000")

    factor=1
    h_int.Scale(factor/h_int.Integral());
    h_gen.Scale(factor/h_gen.Integral());
    h_compare = createRatio(h_int, h_gen)

    c, pad1, pad2 = createCanvasPads()
    pad1.cd()
    h_gen.Draw("HIST")
    h_gen.GetXaxis().SetRangeUser(plotxmin,plotxmax)
    h_gen.SetMinimum(1e-5)
    h_gen.GetXaxis().SetTitle("M_{#gamma#gamma} [GeV]")
    h_gen.GetXaxis().SetTitleSize(0.07)
    h_gen.GetXaxis().SetTitleOffset(0.8)
    h_gen.GetYaxis().SetTitle("Probability")
    h_gen.GetYaxis().SetTitleSize(0.07)
    h_gen.GetYaxis().SetTitleOffset(0.8)
    h_gen.SetLineColor(2)
    h_gen.SetLineWidth(2)
    h_gen.SetTitle("RSG 1000GeV #Gamma_{G}/m_{G}=1.4%")
    h_int.Draw("HISTSame")
    h_int.SetLineWidth(2)
    leg = ROOT.TLegend(0.6,0.7,0.9,0.88)
    leg.AddEntry(h_gen,"MC Generated","l")
    leg.AddEntry(h_int,"Interpolation","l")
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
