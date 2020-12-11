from optparse import OptionParser
import ROOT as rt
import rootTools
from framework import Config
from array import *
import os
import sys

def getThyXsecDict(year):    
    thyXsecDict = {}
    xsecFiles = {}
    #2017
    xsecFiles = { "2017" : ['/afs/cern.ch/work/a/apsallid/CMS/Hgg/exodiphotons/seconditeration/CMSSW_10_2_13/src/diphoton-analysis/output/2017/signalNorm/XS_kMpl001.txt',
                            '/afs/cern.ch/work/a/apsallid/CMS/Hgg/exodiphotons/seconditeration/CMSSW_10_2_13/src/diphoton-analysis/output/2017/signalNorm/XS_kMpl01.txt',
                            '/afs/cern.ch/work/a/apsallid/CMS/Hgg/exodiphotons/seconditeration/CMSSW_10_2_13/src/diphoton-analysis/output/2017/signalNorm/XS_kMpl02.txt',
                            '/afs/cern.ch/work/a/apsallid/CMS/Hgg/exodiphotons/seconditeration/CMSSW_10_2_13/src/diphoton-analysis/output/2017/signalNorm/XS_0p014.txt',
                            '/afs/cern.ch/work/a/apsallid/CMS/Hgg/exodiphotons/seconditeration/CMSSW_10_2_13/src/diphoton-analysis/output/2017/signalNorm/XS_1p4.txt',
                            '/afs/cern.ch/work/a/apsallid/CMS/Hgg/exodiphotons/seconditeration/CMSSW_10_2_13/src/diphoton-analysis/output/2017/signalNorm/XS_5p6.txt'],
                  
                  "2018" : ['/afs/cern.ch/work/a/apsallid/CMS/Hgg/exodiphotons/seconditeration/CMSSW_10_2_13/src/diphoton-analysis/output/2018/signalNorm/XS_kMpl001.txt',
                            '/afs/cern.ch/work/a/apsallid/CMS/Hgg/exodiphotons/seconditeration/CMSSW_10_2_13/src/diphoton-analysis/output/2018/signalNorm/XS_kMpl01.txt',
                            '/afs/cern.ch/work/a/apsallid/CMS/Hgg/exodiphotons/seconditeration/CMSSW_10_2_13/src/diphoton-analysis/output/2018/signalNorm/XS_kMpl02.txt',
                            '/afs/cern.ch/work/a/apsallid/CMS/Hgg/exodiphotons/seconditeration/CMSSW_10_2_13/src/diphoton-analysis/output/2018/signalNorm/XS_0p014.txt',
                            '/afs/cern.ch/work/a/apsallid/CMS/Hgg/exodiphotons/seconditeration/CMSSW_10_2_13/src/diphoton-analysis/output/2018/signalNorm/XS_1p4.txt',
                            '/afs/cern.ch/work/a/apsallid/CMS/Hgg/exodiphotons/seconditeration/CMSSW_10_2_13/src/diphoton-analysis/output/2018/signalNorm/XS_5p6.txt']
    }
    
    print xsecFiles
    for xsecFile in xsecFiles[year]:
        moreThyModels = []
        f = open(xsecFile)
        coup = xsecFile.split("/")[-1].split("_")[-1].split(".")[0]
        thyXsecDict[coup] = {}
        for i,line in enumerate(f.readlines()):

            #print(i,line)
            if line[0]=='#': continue
            line = line.replace('\n','')
            line = line.replace('\t','')
            line = line.replace('\r','')
            lineList = [l for l in line.split(" ") if l!='']

            #print(lineList)
            thyXsecDict[coup][int(float(lineList[0]))] = float(lineList[1])
            
        f.close()

    return thyXsecDict

def project(tree, h, var, cut):
    print 'projecting var: %s, cut: %s from tree: %s into hist: %s'%(var, cut, tree.GetName(), h.GetName())
    tree.Project(h.GetName(),var,cut)

if __name__ == '__main__':
    
    parser = OptionParser()
    parser.add_option('-t','--type',dest="type",default="nom",type="string",
                  help="type of result")
    parser.add_option('-d','--outdir',dest="outDir",default="./",type="string",
                  help="Output directory to store output histograms")
    parser.add_option('--year',dest="year",default="2017",type="string",
                  help="year")
 
    (options,args) = parser.parse_args()
    if options.type=='nom':
        TYPE = ''
    else:
        TYPE = options.type.upper()

    year = ''

    thyXsecDict = getThyXsecDict(options.year) 
    thyModels = thyXsecDict.keys()

    sig_xsec = {}
    for model in thyModels:
        sig_xsec[model] = array('d')
        print(model)
        for mg in sorted(thyXsecDict[model].keys()):
            print mg, thyXsecDict[model][mg]
        
    cats = ["EBEB", "EBEE"]

    #Save signal normalization
    outFile = open("SignalNorm.txt","a+")

    for f in args:
        for thecat in cats:
            if thecat == "EBEB" : cat = 0
            elif thecat == "EBEE" : cat = 1
            title =  f.split('_M_')[0].split('/')[-1]        
            year = f.split('.root')[0].split('_')[-1]
            mass = int(f.split('_M_')[1].split('_TuneCP2')[0])
            print(title,year,mass)
            tfileIn = rt.TFile.Open(f)
            
            #h_mgg_1GeVbin = rt.TH1D('h_mgg_1GeVbin','h_mgg_1GeVbin',14000,0,14000)
            h_mgg_5GeVbin = rt.TH1D('h_mgg_5GeVbin','h_mgg_5GeVbin',2800,0,14000)
            thetree=tfileIn.Get("HighMassDiphoton")
            
            project(thetree,h_mgg_5GeVbin, "mgg", 'eventClass==%d'%(cat) )

            #h = tfileIn.Get('h_mjj_ratio_%s'%options.type)
            h_mgg_5GeVbin.SetName('h_%s_M%i_%s'%(title,mass,year))
            h_mgg_5GeVbin.SetTitle('h_%s_M%i_%s'%(title,mass,year))
            h_mgg_5GeVbin.SetDirectory(0)

            print(title,mass,year)

            #Will write to file the following info
            #Signal Year Type Coupling MassPoint Category Integral Xsec
            if "RSG" in title:
                outFile.write( "%s %s %s %s %i %s %f %.5e \n" %(title.split("_")[0],year,options.type,title.split("_")[1],mass, thecat, h_mgg_5GeVbin.Integral(), thyXsecDict[title.split("_")[1]][mass] ) )
            else:
                outFile.write( "%s %s %s %s %i %s %f %.5e \n" %(title.split("_")[0],year,options.type,title.split("_")[2],mass, thecat, h_mgg_5GeVbin.Integral(), thyXsecDict[title.split("_")[2]][mass] ) )
   
    
    outFile.close()   
