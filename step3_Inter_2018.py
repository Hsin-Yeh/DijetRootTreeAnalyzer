import os

<<<<<<< HEAD
tag = 'PFNo70modelDijetYearflavorAlgo'

#L = ['signalHistos_bg_JunInter_For2018Scan_DeepJet','Gaussian_bg_JunInter_For2018Scan_DeepJet','signalHistos_bg_JunInter_For2017Scan_DeepJet','Gaussian_bg_JunInter_For2017Scan_DeepJet','signalHistos_bg_JunInter_For2016Scan_DeepJet','Gaussian_bg_JunInter_For2016Scan_DeepJet'] 

L=['signalHistos_DMgq0p25_bb_NovInter_For2017Scan_DeepJet','signalHistos_DMgq0p2_bb_NovInter_For2017Scan_DeepJet','signalHistos_DMgq0p25_bb_NovInter_For2016Scan_DeepJet','signalHistos_DMgq0p2_bb_NovInter_For2016Scan_DeepJet','signalHistos_DMgq0p25_bb_NovInter_For2018Scan_DeepJet','signalHistos_DMgq0p2_bb_NovInter_For2018Scan_DeepJet']
#['signalHistos_bg_JunInter_For2016Scan_DeepJet','signalHistos_bb_JunInter_For2016Scan_DeepJet','signalHistos_bg_JunInter_For2018Scan_DeepJet','signalHistos_bb_JunInter_For2018Scan_DeepJet','signalHistos_bb_JunInter_For2017Scan_DeepJet','signalHistos_bg_JunInter_For2017Scan_DeepJet'] 
=======
tag = 'PFNo64DijetYearflavorAlgo'

#L = ['signalHistos_bg_JunInter_For2018Scan_DeepJet','Gaussian_bg_JunInter_For2018Scan_DeepJet','signalHistos_bg_JunInter_For2017Scan_DeepJet','Gaussian_bg_JunInter_For2017Scan_DeepJet','signalHistos_bg_JunInter_For2016Scan_DeepJet','Gaussian_bg_JunInter_For2016Scan_DeepJet'] 

L = ['signalHistos_bg_JunInter_For2016Scan_DeepJet','signalHistos_bb_JunInter_For2016Scan_DeepJet','signalHistos_bg_JunInter_For2018Scan_DeepJet','signalHistos_bb_JunInter_For2018Scan_DeepJet','signalHistos_bb_JunInter_For2017Scan_DeepJet','signalHistos_bg_JunInter_For2017Scan_DeepJet'] 
>>>>>>> fefdb2e706949d9e1c73a96989ee3c57a3f88afa

ns = ''#'ns'
nobtag= ''#'nobtag'

cata=[]
Com_list=[]
Comi=''
index = 0
Total=''

for i in L:
<<<<<<< HEAD
  if 'DMgq0p25' in i:
    flavor = 'bb'
    model = 'DMgq0p25'
    cata = ['Non','le1b']
  elif 'DMgq0p2' in i:
    flavor = 'bb'
    model = 'DMgq0p2'
    cata = ['Non','le1b']
  elif 'bg' in i:
=======
  if 'bg' in i:
>>>>>>> fefdb2e706949d9e1c73a96989ee3c57a3f88afa
    flavor = 'bg'
    model = 'qg'
    cata = ['Non','1b','le1b']
    if 'Gaussian' in i:
      cata = ['le1b']
<<<<<<< HEAD
  elif 'bb' in i:
=======

  if 'bb' in i:
>>>>>>> fefdb2e706949d9e1c73a96989ee3c57a3f88afa
    model = 'qq'
    flavor='bb'
    cata = ['Non','le1b','2b']
    if 'Gaussian' in i:
      cata = ['le1b']

  if 'CSVv2' in i:
    Algo = 'CSVv2'
  if 'DeepCSV' in i:
    Algo = 'DeepCSV'
  if 'DeepJet' in i:
    Algo = 'DeepJet'

  if '2016' in i:
    Year = '2016'
  elif '2018' in i:
    Year = '2018'
  else:
    Year = '2017'
  
  for j in cata:
    NewTag = tag.replace('flavor',flavor).replace('model',model).replace('Algo',Algo).replace('Year',Year)
    if 'Gaussian' in i:
      NewTag = NewTag.replace('PF','PFGaus')
    comm1 = 'python python/bTag_ForScan_Inter'+nobtag+'.py -f '+i+'_central_'+j+' -t '+NewTag+' -m '+model+' -c '+j
<<<<<<< HEAD
    comm2 = 'python python/excute2_2018_Inter'+ns+'.py -t '+NewTag+j+' -m '+model+' -p exp -F '+i+'_central_'+j
    Total+=comm1+'\n\n'
    Comi += comm2+'\n\n'
    if index%1 ==0:
=======
    if Year == '2018':
      comm2 = 'python python/excute2_2018_Inter'+ns+'.py -t '+NewTag+j+' -m '+model+' -p exp -F '+i+'_central_'+j
    if Year == '2017':
      comm2 = 'python python/excute2_2017_Inter'+ns+'.py -t '+NewTag+j+' -m '+model+' -p exp -F '+i+'_central_'+j 
    if Year == '2016':
      comm2 = 'python python/excute2_2016_Inter'+ns+'.py -t '+NewTag+j+' -m '+model+' -p exp -F '+i+'_central_'+j 
    Total+=comm1+'\n\n'
    Comi += comm2+'\n\n'
    if index%3 ==0:
>>>>>>> fefdb2e706949d9e1c73a96989ee3c57a3f88afa
       Com_list.append(Comi)
       Comi = ''
    index = index +1
Com_list.append(Comi)
if '' in Com_list:
  Com_list.remove('')
index = 0
for i in Com_list:
   index+=1
   a = open('aloha_Inter2018_'+nobtag+ns+str(index)+'.sh','w+')
   a.write('#!/bin/bash\n\n'+i)
   a.close()
   os.system('chmod 751 aloha_Inter2018_'+nobtag+ns+str(index)+'.sh')
a= open('aloha_Inter2018_'+nobtag+ns+'0.sh','w+')
a.write('#!/bin/bash\n\n'+Total)
a.close()
os.system('chmod 751 aloha_Inter2018_'+nobtag+ns+'0.sh')
