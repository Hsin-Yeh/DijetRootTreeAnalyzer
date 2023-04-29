#!/usr/bin/env python

import ROOT
from array import array

import argparse
parser = argparse.ArgumentParser(description='Compute histogram bin width with signal resolution')
parser.add_argument('in_filenames',nargs="+",help='input filenames')
args = parser.parse_args()


for infile in args.in_filenames:
    with open (infile) as f:
        Lines = f.readlines()

        for Line in Lines:
            cat, coup, p0, p0err, p1, p1err, chi2 = Line.split()

            binEdges=[500]
            check = True

            while ( binEdges[-1] <= 8000 ):
                binWidth = float(p0) + float(p1)*binEdges[-1]
                binEdges.append(binEdges[-1]+int(binWidth))
                # if (binEdges[-1]>8000 and check):
                #     check = False
                #     print(binEdges[-1], len(binEdges))

            print (cat, coup, len(binEdges)-1)
            print (binEdges)
