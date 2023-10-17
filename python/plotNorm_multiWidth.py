#!/usr/bin/env python

import ROOT
import pandas as pd
from array import array
import argparse

parser = argparse.ArgumentParser(description='')
parser.add_argument('--inputfile','-i',default="test.txt",type=str,help='input file')
args = parser.parse_args()

def lumi(year):
    if (year==2016): return 35.9
    elif (year==2017): return 41.5
    elif (year==2018): return 59.7
    elif (year==fullRun2): return 138
    else: return 0

def Read_SignalNorm():
    # Provide the file path
    file_path = args.inputfile
    # Define column names
    columns = ["year", "coup", "mass", "cat", "norm"]
    # Read the data from the file into a DataFrame
    df = pd.read_csv(file_path, sep=" ", header=None, names=columns)
    # Print the resulting DataFrame
    print(df)
    return df

def get_norm(year, coup, cat, df):
    norms, masses = array('d'), array('d')
    for mass in range (500, 5000, 10):
        condition = (df["year"] == year) & (df["coup"] == coup) & (df["mass"] == mass) & (df["cat"] == cat)

        # Use loc to filter the DataFrame based on the condition and retrieve the "norm" value
        norm = df.loc[condition, "norm"].values[0] if any(condition) else None
        norms.append(float(norm)/lumi(year))
        masses.append(float(mass))
    return masses, norms

def color(i):
    colorwheel = [416, 600, 800, 632, 880, 432, 616, 860, 820, 900, 420, 620, 820, 652, 1000, 452, 636, 842, 863, 823]
    # colorindex = int(i/11) + int(i%11)
    return colorwheel[i]


def plotNorm():
    df = Read_SignalNorm()
    widths = [14, 707, 1400, 3500, 5600]
    cats = ["EBEB","EBEE","All"]
    graphs = {}
    c1 = ROOT.TCanvas("c1","c1", 700, 600)
    l = ROOT.TLegend(0.6, 0.25, 0.88, 0.45)
    for icat, cat in enumerate(cats):
        for iwidth, width in enumerate(widths):
            key = icat*len(widths) + iwidth
            masses, norms = get_norm(2016, width, cat, df)
            graphs[key] = ROOT.TGraph(len(masses),masses,norms)
            graphs[key].SetLineColor(color(iwidth))
            if (icat==0): l.AddEntry(graphs[iwidth],f"{width/100}%","l")
            if (key==0): graphs[key].Draw("AL")
            else: graphs[key].Draw("Lsame")
    l.Draw()
    graphs[0].GetYaxis().SetRangeUser(0,0.8)
    graphs[0].SetTitle("2016")
    c1.SaveAs("test.png")

if __name__ == "__main__":
    plotNorm()
