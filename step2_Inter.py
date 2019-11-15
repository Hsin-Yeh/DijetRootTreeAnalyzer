import os

FolderName = 'signalHistos_model_flavor_NovInter_ForYearScan_Algo'
cata = []

TComm = []
for a in ['DMgq0p25','DMgq0p2']:
  for b in ['2018','2016','2017']:
#    for c in ['CSVv2','DeepCSV','DeepJet']:
     for c in ['DeepJet']:
#     for c in ['DeepCSV','CSVv2','DeepJet']:
       if a == 'qg':
	 d = 'bg'
       else:
	 d = 'bb'
       folder = FolderName.replace('model',a).replace('Year',b).replace('Algo',c).replace('flavor',d)
       name=[]
       for i in ['_up','_central','_down']:
         if 'bg' in folder:
           cata = ['le1b','1b','Non']
         if 'bb' in folder:
           cata = ['Non','2b','le1b']
         for j in cata:
           print('cp -r '+folder+i+' '+folder+i+'_'+j)
#           os.system('cp -r '+folder+i+' '+folder+i+'_'+j)
           name.append(folder+i+'_'+j)
       
       for i in name:
	 comm = ''
         if '2016' in i:
            py = 'python/bTag_extractShapes_Interpolater_scan_2016_Inter_CEN.py'
            py2 = 'python/ReScaleInterpolation_2016_Inter_CEN.py '
       
         elif '2017' in i:
            py = 'python/bTag_extractShapes_Interpolater_scan_2017_Inter_CEN.py'
            py2 = 'python/ReScaleInterpolation_2017_Inter_CEN.py '
       
	 elif '2018' in i:
            py = 'python/bTag_extractShapes_Interpolater_scan_2018_Inter_CEN.py'
            py2 = 'python/ReScaleInterpolation_2018_Inter_CEN.py '

         for j in ['up','central','down']:
           if j in i:
             py = py.replace('CEN',j)
       
         if 'bb' in i:
           add1 = ' qq '
         if 'bg' in i:
           add1 = ' qg '
	 if 'DMgq0p25' in i:
           add1 = ' DMgq0p25 '
         if 'DMgq0p2' in i:     
	   add1 = ' DMgq0p2 '

	 print i
 
	 if 'central' in i:
	   py2= py2.replace('_CEN','')
	 else:
	   py2 = py2.replace('CEN','UD')

	 print py2
 
	 comm += 'python '+py+' -m '+add1+'-e '+i+' -c '+i.split('_')[-1] + '\n'
         comm += 'python python/extract.py -m '+add1+' -i '+i + '\n'
         comm += 'python '+py2+' -m '+add1+' -F '+i+' -c '+i.split('_')[-1] + '\n\n'
	 TComm.append(comm)

         #print('python '+py+' -m '+add1+'-e '+i+' -c '+i.split('_')[-1])
         #os.system('python '+py+' -m '+add1+'-e '+i+' -c '+i.split('_')[-1])
       
         #print('python python/extract.py -m '+add1+' -i '+i)
         #os.system('python python/extract.py -m '+add1+' -i '+i)
       
         #print('python '+py2+' -m '+add1+' -F '+i+' -c '+i.split('_')[-1])
         #os.system('python '+py2+' -m '+add1+' -F '+i+' -c '+i.split('_')[-1])

excution = 6
command = {}
for i in range(excution):
  command[i] = '#!/bin/bash\n\n'
for i,j in enumerate(TComm):
  command[i%excution] += j

for i in range(excution):
  cc = open('step2_Inter_%d.sh'%(i+1),'w+')
  cc.write(command[i])
  cc.close()
  os.system('chmod 751 step2_Inter_%d.sh'%(i+1))
