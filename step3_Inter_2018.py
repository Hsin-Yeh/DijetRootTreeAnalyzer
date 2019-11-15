import os

tag = 'PFNo64DijetYearflavorAlgo'

#L = ['signalHistos_bg_JunInter_For2018Scan_DeepJet','Gaussian_bg_JunInter_For2018Scan_DeepJet','signalHistos_bg_JunInter_For2017Scan_DeepJet','Gaussian_bg_JunInter_For2017Scan_DeepJet','signalHistos_bg_JunInter_For2016Scan_DeepJet','Gaussian_bg_JunInter_For2016Scan_DeepJet'] 

L = ['signalHistos_bg_JunInter_For2016Scan_DeepJet','signalHistos_bb_JunInter_For2016Scan_DeepJet','signalHistos_bg_JunInter_For2018Scan_DeepJet','signalHistos_bb_JunInter_For2018Scan_DeepJet','signalHistos_bb_JunInter_For2017Scan_DeepJet','signalHistos_bg_JunInter_For2017Scan_DeepJet'] 

ns = ''#'ns'
nobtag= ''#'nobtag'

cata=[]
Com_list=[]
Comi=''
index = 0
Total=''

for i in L:
  if 'bg' in i:
    flavor = 'bg'
    model = 'qg'
    cata = ['Non','1b','le1b']
    if 'Gaussian' in i:
      cata = ['le1b']

  if 'bb' in i:
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
    if Year == '2018':
      comm2 = 'python python/excute2_2018_Inter'+ns+'.py -t '+NewTag+j+' -m '+model+' -p exp -F '+i+'_central_'+j
    if Year == '2017':
      comm2 = 'python python/excute2_2017_Inter'+ns+'.py -t '+NewTag+j+' -m '+model+' -p exp -F '+i+'_central_'+j 
    if Year == '2016':
      comm2 = 'python python/excute2_2016_Inter'+ns+'.py -t '+NewTag+j+' -m '+model+' -p exp -F '+i+'_central_'+j 
    Total+=comm1+'\n\n'
    Comi += comm2+'\n\n'
    if index%3 ==0:
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
