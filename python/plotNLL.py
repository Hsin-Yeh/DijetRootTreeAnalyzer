#!/usr/bin/env python

import ROOT
import root_numpy
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
        r = root_numpy.tree2array(tree,'r')
        nll= root_numpy.tree2array(tree,'nll')
        nll0 = root_numpy.tree2array(tree,'nll0')
        deltaNLL = root_numpy.tree2array(tree,'deltaNLL')
        total = 2*(deltaNLL+nll+nll0)
        print(r, nll, nll0, deltaNLL, total)
        plt.scatter(r,total)
        plt.savefig("test.png")
