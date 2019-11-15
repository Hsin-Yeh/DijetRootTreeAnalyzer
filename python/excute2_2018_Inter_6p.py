
import os,sys
from optparse import OptionParser

if __name__=='__main__':

  parser = OptionParser()

  parser.add_option('-t','--tag',dest='tag',type='string',default='none',help='')
  parser.add_option('-m','--model',dest='model',type='string',default='none',help='')
  parser.add_option('-p','--point',dest='point',type='string',default='none',help='expected or observed')
  parser.add_option('-F','--folder',dest='Folder',type='string',default='none',help='') 

  (options,args) = parser.parse_args()

  

  if 'Non' in options.tag :
    CSV_Value = [0.1]
  elif '2018' in options.tag:
#    CSV_Value = [0.2770]
    CSV_Value = [0.0494, 0.1241, 0.2, 0.2770,0.35, 0.4184,0.45,0.5,0.55,0.6,0.65,0.7, 0.7264, 0.7527,0.8,0.85,0.9,0.95]
  elif '2017' in options.tag:
    CSV_Value = [0.0521,0.1,0.1522,0.2,0.25,0.3033,0.35,0.4,0.45,0.4941,0.55,0.5803,0.6,0.65,0.7,0.7489,0.8001,0.85,0.8838,0.9,0.9693] 
  elif '2016' in options.tag:
    CSV_Value = [0.0614,0.1,0.15,0.2, 0.2217,0.25, 0.3093,0.35,0.4,0.45,0.5, 0.5426,0.6, 0.6321, 0.7221,0.8, 0.8484, 0.8953, 0.9535] 

  if 'Non' in options.tag and '2018' in options.tag:
    CSV_Value = [0.1241]

  tag = options.tag
  model = options.model
  point = options.point 
  Folder = options.Folder
  
  if model == 'qq':
    flavor = 'bb'
  elif model == 'qg':
    flavor = 'bg'
  for i in CSV_Value:
    print('\n\n\npython python/Working2_2018.py -b '+tag+str(int(i*1000))+'6p -f '+tag+str(int(i*1000))+'6pScan -o cards_'+tag+str(int(i*1000))+'6p_scan -s '+Folder+'/ResonanceShapes_'+model+'_'+flavor+'_13TeV_Spring16_'+str(int(i*1000))+'_Nominal_Interpolation_rescale.root -m '+model+' -p ' + point+'\n\n\n')
    os.system('python python/Working2_2018.py -b '+tag+str(int(i*1000))+'6p -f '+tag+str(int(i*1000))+'6pScan -o cards_'+tag+str(int(i*1000))+'6p_scan -s '+Folder+'/ResonanceShapes_'+model+'_'+flavor+'_13TeV_Spring16_'+str(int(i*1000))+'_Nominal_Interpolation_rescale.root -m '+model+' -p ' + point)
