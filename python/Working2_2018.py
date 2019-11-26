import sys,os
from optparse import OptionParser
from ROOT import *

if __name__=='__main__':
  parser = OptionParser()

  parser.add_option('-b','--box',dest="box",default="./",type="string",help="box name")
  parser.add_option('-f','--fit_dir',dest="fit_dir", default="",type="string", help="Folder which stores Fit Result")
  parser.add_option('-m','--model',dest="model", default="",type="string", help="model")
  parser.add_option('-o','--out_dir',dest="out_dir", default="",type="string", help="Folder which stores limit")
  parser.add_option('-s','--signal',dest="signal", default="",type="string", help="Nominal root file place")
  parser.add_option('-p','--printout',dest="printout", default="",type="string", help="expected or observed")
  
  (options,args) = parser.parse_args()

  signal=options.signal
  model = options.model
  out_dir=options.out_dir+''
  fit_dir=options.fit_dir+''
  box=options.box
  Print = options.printout
 
  os.system('mkdir fits_2019_09')
  os.system('mkdir fits_2019_09/'+fit_dir)
  os.system('mkdir '+out_dir)

  content = '#!/bin/bash\n\n'
 
  con = 'dijet.config'
  if '5p' in box:
     con  ='dijet_5param.config'
  elif '6p' in box:
     con = 'dijet_6param.config'

  lumi = 59750
  year = '2018'
  if '2017' in box:
    lumi = 41800
    year = '2017'
  elif '2016' in box:
    lumi = 37600 
    year = '2016'

  content += 'python python/BinnedFit.py -c config/'+con+' -l '+str(lumi)+' -m '+model+' -s '+signal+' inputs/JetHT_run'+year+'_red_cert_scan.root -b '+box+' -d fits_2019_09/'+fit_dir+' --fit-spectrum\n\n'
  content += 'python python/RunCombine_I_btag2018.py -m '+model+' -d '+out_dir+' --mass range\(1600,7000,100\) -c config/'+con+' -i fits_2019_09/'+fit_dir+'/DijetFitResults_'+box+'.root -b '+box+' --rMax 20 --xsec 1e-3 -l '+str(float(lumi)/1000.0)+'00\n\n'
  content += 'python python/GetCombine.py -d '+out_dir+'/ -m '+model+' --mass range\(1600,7000,100\) -b '+box+' --xsec 1e-3 -l '+str(float(lumi)/1000.0)+'\n\n'
  content += 'python python/Plot1DLimit_1718.py -o '+Print+' -d '+out_dir+'/ -m '+model+' -b '+box+' -l '+str(float(lumi)/1000.0)+' --massMin 1000 --massMax 8000 --xsecMin 1e-4 --xsecMax 1e2\n\n'


  print('python python/BinnedFit.py -c config/'+con+' -l '+str(lumi)+' -m '+model+' -s '+signal+' inputs/JetHT_run'+year+'_red_cert_scan.root -b '+box+' -d fits_2019_09/'+fit_dir+' --fit-spectrum\n\n')
  os.system('python python/BinnedFit.py -c config/'+con+' -l '+str(lumi)+' -m '+model+' -s '+signal+' inputs/JetHT_run'+year+'_red_cert_scan.root -b '+box+' -d fits_2019_09/'+fit_dir+' --fit-spectrum\n\n')

  print('python python/RunCombine_I_btag2018.py -m '+model+' -d '+out_dir+' --mass range\(1600,7000,100\) -c config/'+con+' -i fits_2019_09/'+fit_dir+'/DijetFitResults_'+box+'.root -b '+box+' --rMax 20 --xsec 1e-3 -l '+str(float(lumi)/1000.0)+'0\n\n')
  os.system('python python/RunCombine_I_btag2018.py -m '+model+' -d '+out_dir+' --mass range\(1600,7000,100\) -c config/'+con+' -i fits_2019_09/'+fit_dir+'/DijetFitResults_'+box+'.root -b '+box+' --rMax 20 --xsec 1e-3 -l '+str(float(lumi)/1000.0)+'0\n\n')

  print('python python/GetCombine.py -d '+out_dir+'/ -m '+model+' --mass range\(1600,7000,100\) -b '+box+' --xsec 1e-3 -l '+str(float(lumi)/1000.0)+'\n\n')
#  os.system('python python/GetCombine.py -d '+out_dir+'/ -m '+model+' --mass range\(1600,7000,100\) -b '+box+' --xsec 1e-3 -l '+str(float(lumi)/1000.0)+'\n\n')

  print('python python/Plot1DLimit_1718.py -o '+Print+' -d '+out_dir+'/ -m '+model+' -b '+box+' -l '+str(float(lumi)/1000.0)+' --massMin 1000 --massMax 8000 --xsecMin 1e-4 --xsecMax 1e2\n\n')
#  os.system('python python/Plot1DLimit_1718.py -o '+Print+' -d '+out_dir+'/ -m '+model+' -b '+box+' -l '+str(float(lumi)/1000.0)+' --massMin 1000 --massMax 8000 --xsecMin 1e-4 --xsecMax 1e2\n\n')

  excute_out = open(box+'.sh','w+')
  excute_out.write(content)
  excute_out.close()

  os.system('chmod 751 '+box+'.sh')
  os.system('mv '+box+'.sh /afs/cern.ch/work/z/zhixing/private/CMSSW_7_4_14/src/CMSDIJET/DijetRootTreeAnalyzer/ExucteCommandBox')
