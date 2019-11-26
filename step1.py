import sys
 
command = '' 
for n in ['DeepJet']:
# for m in ['2017','2016']:
 for m in ['2016','2017','2018']:
<<<<<<< HEAD
  for i in ['DMgq0p25']:
   for j in ['up','central','down']:
=======
  for i in ['DMgq0p2','DMgq0p25']:#['qq','qg']
>>>>>>> fefdb2e706949d9e1c73a96989ee3c57a3f88afa
    if i == 'qq' or i == 'DMgq0p2' or i =='DMgq0p25': 
     flavor = 'bb'
    if i == 'qg': 
     flavor = 'bg'
<<<<<<< HEAD
    command += 'python python/bTag_signalStudies_scanInter_'+n+'_'+m+'.py -f %s -m %s -s %s'%(flavor,i,j)+'\n'
=======
    command += 'python python/bTag_signalStudies_scanInter_'+n+'_'+m+'.py -f %s -m %s'%(flavor,i)+'\n'
>>>>>>> fefdb2e706949d9e1c73a96989ee3c57a3f88afa
#    if i =='qq':
#        cate = ['le1b','2b','Non']
#    elif i =='qg':
#        cate = ['le1b','1b','Non']
#    for k in cate:
#        command  += 'cp -r signalHistos_%s_Dec_ForScan_'%flavor+n+' signalHistos_%s_Dec_ForScan_'%flavor+n+'_'+k+'\n'

print command
 
