#!/usr/bin/env python
# python python/plotNLL.py signal_bias/higgsCombine2017_DiPhotons_kMpl001_EBEB_fixed_pdf_*mH${mass}.root signal_bias/higgsCombine2017_DiPhotons_kMpl001_EBEB_Envelope.MultiDimFit.mH${mass}.root --mass ${mass}

import ROOT
import root_numpy
import argparse
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import math

parser = argparse.ArgumentParser(description='')
parser.add_argument('in_filenames',nargs="+",help='input filenames')
parser.add_argument('--outputDir','-d',default="output/plots/sysplots",type=str,help='output plot directory')
parser.add_argument('--xMax',default=2,type=float,help='plot x max')
parser.add_argument('--xMin',default=-2,type=float,help='plot x min')
parser.add_argument('--yMax',default=-1,type=float,help='plot y max')
parser.add_argument('--yMin',default=-1,type=float,help='plot y min')
parser.add_argument('--year',default=2016,type=int,help='plot name year')
parser.add_argument('--coup',default="kMpl001",type=str,help='plot name coup')
parser.add_argument('--cat',default="EBEB",type=str,help='plot name cat')
parser.add_argument('--mass',default=750,type=int,help='plot name mass')

args = parser.parse_args()

def average_array(array):
    count=0
    average_total=0
    for num in array:
        if math.isnan(num) != True and num < 1e7:
            count+=1
            average_total+=num
    return average_total/count

if __name__ == "__main__":

    # Define a list of colors
    color_template = ['blue', 'green', 'red', 'purple', 'orange', 'yellow']
    # Create a figure and axes object
    fig, ax = plt.subplots()

    average_total = 0
    for ifile,in_filename in enumerate(args.in_filenames):
        tfileIn = ROOT.TFile.Open(in_filename)
        linestyle='solid'
        if (in_filename.find("Envelope") != -1):
            name="Envelope"
            linestyle='dashed'
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
        average_total = average_array(total)
        print(average_total)
        ax.scatter(r,total,color=color_template[ifile],linestyle=linestyle,label=name)

    ax.legend()
    ax.set_xlim([args.xMin,args.xMax])
    average_total = average_total/len(args.in_filenames)
    ax.set_ylim(average_total-2,average_total+5)
    if (args.yMax != -1 ): ax.set_ylim([args.yMin,args.yMax])
    ax.set_xlabel("r")
    ax.set_ylabel("2*(deltaNLL+nll+nll0)")
    plt.savefig("discrete_profiling_%s_%s_%s_%s.png"%(args.year, args.coup, args.cat, args.mass))
