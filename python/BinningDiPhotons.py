from optparse import OptionParser
import ROOT as rt
import rootTools
from framework import Config
from array import *
import os
import sys

def sigma_function(category, width, value):
    fun = 0.
    if category == "EBEB": 
        if width == "kMpl001":
             fun =  0.484 + 0.012 * value
        elif width == "kMpl01":
             fun =  0.823 + 0.017 * value
        elif width == "kMpl02":
             fun =  3.180 + 0.040 * value
    if category == "EBEE": 
        if width == "kMpl001":
             fun =  -0.259 + 0.021 * value
        elif width == "kMpl01":
             fun =  -0.065 + 0.025 * value
        elif width == "kMpl02":
             fun =  2.892 + 0.044 * value

    return fun

if __name__ == '__main__':
    
    parser = OptionParser()
    parser.add_option('-m','--initmass',dest="initmass",default="500",type="string",
                  help="Initial mass")
    (options,args) = parser.parse_args()

    cats = ["EBEB","EBEE"]
    widthscenarios = ["kMpl001","kMpl01","kMpl02"]
    
    for cat in cats:
        print(40*"=")
        print(cat)
        for width in widthscenarios:
            print(width)
            bins = []
            mass = float(options.initmass)
            bins.append(int(mass))
            while ( mass < 14000.):
                binwidth = sigma_function(cat,width,mass)
                mass += binwidth
                bins.append(int(mass))
            print(bins)

    
