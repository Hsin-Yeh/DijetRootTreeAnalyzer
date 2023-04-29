#!/usr/bin/env python
import ROOT
import argparse

parser = argparse.ArgumentParser(description='')
parser.add_argument('--old','-o',defalut="",type=str,help='previous 2016 analysis')
parser.add_argument('--new','-n',defalut="",type=str,help='Current full Run2 analysis')
args = parser.parse_args()

if __name__ == "__main__":
    f_old = ROOT.TFile.Open(args.old)
    f_new = ROOT.TFile.Open(args.new)
