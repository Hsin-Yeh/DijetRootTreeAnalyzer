#!/usr/bin/env python

import ROOT
import argparse
import pandas as pd
import numpy as np

parser = argparse.ArgumentParser(description='')
parser.add_argument('in_filenames',nargs="+",help='input filenames')
args = parser.parse_args()

def getNormalization():
    norm = pd.read_csv(args.in_filenames[0], sep=" ", header=None)
    norm.columns = ["Year", "Coupling", "MassPoint", "Category", "Norm"]
    norm.Year = norm.Year.astype(str)
    norm.Coupling = norm.Coupling.astype(str)
    norm.MassPoint = norm.MassPoint.astype(int)
    norm.Category = norm.Category.astype(str)
    norm.Norm = norm.Norm.astype(float)

    # print(norm)

    return norm

if __name__ == '__main__':

    norm = getNormalization()
    years = ["2016", "2017", "2018"]
    coups = ["kMpl001","kMpl01","kMpl02","0p014","1p4","5p6"]
    cats = ["EBEB","EBEE","All"]

    for cat in cats:
        for coup in coups:
            if coup == "kMpl01" or coup == "kMpl02":
                masses = np.arange(500, 7000, 50)
            else:
                masses = np.arange(500, 5000, 50)
            for mass in masses:
                for year in years:
                    thenorm = norm[ (norm["Year"] == year) & (norm["Coupling"] == coup) & (norm["Category"] == cat) & ( norm["MassPoint"] == mass ) ]
                    thenormvalue = thenorm['Norm'].values[0]
                    averageNorm += thenormvalue
                averageNorm / 3
