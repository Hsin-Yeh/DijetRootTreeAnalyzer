#!/usr/bin/env python3

import ROOT
import argparse

parser = argparse.ArgumentParser(description='')
parser.add_argument('in_filenames',nargs="+",help='input filenames')
args = parser.parse_args()

def color(i):
    colorwheel = [416, 600, 800, 632, 880, 432, 616, 860, 820, 900, 420, 620, 820, 652, 1000, 452, 636, 842, 863, 823]
    # colorindex = int(i/11) + int(i%11)
    return colorwheel[i]

def plot_Shapes(in_filename):
    histos = {}
    c1 = ROOT.TCanvas()
    leg = ROOT.TLegend(0.6,0.6,0.88,0.8)
    f = ROOT.TFile(in_filename)
    mass = int(in_filename.split("GeV")[0].split("_")[-1])
    nEntries = f.GetListOfKeys().GetEntries()

    # loop over histograms in the input ROOT file
    for h in range(0, nEntries):
        hName = f.GetListOfKeys()[h].GetName()
        width = float(hName.split('_')[2])
        print (f"Extracting shapes for width = {width} GeV")
        histos[h] = f.Get(hName)
        histos[h].SetLineColor(color(h))
        histos[h].SetLineWidth(2)
        leg.AddEntry(histos[h],f"{width/100}%","l")
        if(h==0): histos[h].Draw("HIST")
        else: histos[h].Draw("HISTSame")
    histos[0].GetXaxis().SetRangeUser(mass*0.5,mass*1.5)
    histos[0].GetYaxis().SetRangeUser(1e-4,5e-1)
    histos[0].SetTitle(f"2016 Mass={mass}GeV")
    leg.Draw()
    c1.SetLogy()
    c1.SaveAs(f"test_{mass}.png")

if __name__ == "__main__":
    plot_Shapes(args.in_filenames[0])
