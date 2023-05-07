#!/usr/bin/env python

import ROOT
import argparse
import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser(description='')
parser.add_argument('in_filenames',nargs="+",help='input filenames')
parser.add_argument('--outputDir','-d',default="output/plots/sysplots",type=str,help='output plot directory')
args = parser.parse_args()

if __name__ == "__main__":

    for in_filename in args.in_filenames:
        tfileIn = ROOT.TFile.Open(in_filename)
        tree=tfileIn.Get("limit")
        r = tree.AsMatrix(["r"])
        nll = tree.AsMatrix(["nll"])
        nll0 = tree.AsMatrix(["nll0"])
        deltaNLL = tree.AsMatrix("deltaNLL")
        total = 2*(deltaNLL+nll+nll0)
        import matplotlib.pyplot as plt
        plt.scatter(r,total)
        plt.savefig("test.png")
