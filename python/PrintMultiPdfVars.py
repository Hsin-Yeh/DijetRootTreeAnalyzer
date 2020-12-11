from optparse import OptionParser
import ROOT as rt
import rootTools
from framework import Config
from array import *
import os
import sys
from RunCombine import massIterable

if __name__ == '__main__':
    
    parser = OptionParser()
    parser.add_option('-b','--box',dest="box", default="CaloDijet2016",type="string",
                  help="box name")
    parser.add_option('-m','--model',dest="model", default="gg",type="string",
                  help="bkg model")

    (options,args) = parser.parse_args()

    box = options.box
    model = options.model	

    for f in args:
        if f.lower().endswith('.root'):
            rootFile = rt.TFile(f)
            #rootFile.ls() 

    #print("w"+box)	
    wIn = rootFile.Get("w"+box)
    #wIn.Print()
    fitres = wIn.obj("nll_extDijetPdf_%s_%s_data_obs"%(box.split("_")[-2],box.split("_")[-1]))
    #print(fitres.floatParsFinal().getSize())
    forthemultival = 0. 
    for i in range(0,fitres.floatParsFinal().getSize()): 
         curvar = fitres.floatParsFinal()[i].GetName()
         if model == "dijet" and curvar == "Ntot_%s_bkg"%(box):
             forthemultival = fitres.floatParsFinal()[i].getVal()
	 if model =="expow1": 
             curvar = curvar.replace("p1_Di","pex1_1_Di").replace("p2_Di","pex1_2_Di").replace("Ntot_%s_bkg"%(box),"Ntot_%s_bkg%s"%(box,model))        
         if model =="invpow1":
             curvar = curvar.replace("p1_Di","pip1_1_Di").replace("p2_Di","pip1_2_Di").replace("Ntot_%s_bkg"%(box),"Ntot_%s_bkg%s"%(box,model))
         if model =="invpowlin1":
             curvar = curvar.replace("p1_Di","pil1_1_Di").replace("p2_Di","pil1_2_Di").replace("p3_Di","pil1_3_Di").replace("Ntot_%s_bkg"%(box),"Ntot_%s_bkg%s"%(box,model))

         print("'%s[%.5f]',"%(curvar.replace("dijet",""),fitres.floatParsFinal()[i].getVal())) 
         #print(fitres.floatParsFinal()[i].getVal())
         #print(fitres.floatParsFinal()[i].GetName())
    if model != "invpowlin": print(("'%s_bkg%s_norm[1]',"%(box,model)).replace("dijet","")) 
    else: print("'%s_bkg%s_norm[1]'"%(box,model))
    if model == "dijet":
	print("'Ntot_%s_multi[%.5f]',"%(box,forthemultival))


