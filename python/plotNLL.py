#!/usr/bin/env python

import ROOT
import root_numpy
import argparse
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser(description='')
parser.add_argument('in_filenames',nargs="+",help='input filenames')
parser.add_argument('--outputDir','-d',default="output/plots/sysplots",type=str,help='output plot directory')
args = parser.parse_args()

if __name__ == "__main__":

    # Define a list of colors
    color_template = ['blue', 'green', 'red', 'purple', 'orange', 'yellow']
    # Create a figure and axes object
    fig, ax = plt.subplots()

    for ifile,in_filename in enumerate(args.in_filenames):
        tfileIn = ROOT.TFile.Open(in_filename)
        if (in_filename.find("Envelope") != -1): name="Envelope"
        elif (in_filename.find("pdf_0") != -1): name="dijet"
        elif (in_filename.find("pdf_1") != -1): name="expow1"
        elif (in_filename.find("pdf_2") != -1): name="invpow1"
        elif (in_filename.find("pdf_3") != -1): name="invpowlin1"
        tree=tfileIn.Get("limit")
        r = root_numpy.tree2array(tree,'r')
        nll= root_numpy.tree2array(tree,'nll')
        nll0 = root_numpy.tree2array(tree,'nll0')
        deltaNLL = root_numpy.tree2array(tree,'deltaNLL')
        total = 2*(deltaNLL+nll+nll0)
        print(r, nll, nll0, deltaNLL, total)
        ax.scatter(r,total,color=color_template[ifile],label=name)

    ax.legend()
    # ax.set_xlim([-1,0])
    plt.savefig("test.png")
