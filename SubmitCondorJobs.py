from ROOT import *
from optparse import OptionParser
import os,sys
import datetime


if __name__=='__main__':

  current_time = datetime.datetime.now()

  parser = OptionParser()
  parser.add_option('-l','--list',dest="li",type="string",default="none",help='root list input')
  parser.add_option('-c','--cutFile',dest='cut',type="string",default="none",help='cutfile from config/')
  parser.add_option('-s','--split',dest='split',type="int",default=5,help='number of jobs')
  parser.add_option('-d','--outputdir',dest='Odir',type="string",default="none",help='output directory')
  parser.add_option('-f','--outputfile',dest='Ofile',type="string",default="none",help='output file name')
  parser.add_option('-t','--tag',dest='tag',type='string',default='none',help='tag')
  (options,args) = parser.parse_args()
 
  tag = options.tag
  Flist = options.li
  cutFile = options.cut
  split = options.split
  OutputDir = options.Odir
  OutputFile= options.Ofile

  FolderName = 'batch/CondorSubmittion_%s_%04d%02d%02d_%02d%02d%02d' % (tag,current_time.year,current_time.month,current_time.day,current_time.hour,current_time.minute,current_time.second)

  os.system('mkdir %s'%FolderName)
  os.system('mkdir %s'%FolderName+'/error')
  os.system('mkdir %s'%FolderName+'/log')
  os.system('mkdir %s'%FolderName+'/output')
  txtfile = open(Flist)
  content = {}
  contentFull = {}
  for i in range(split):
    content[i]= ''
    contentFull[i] = ''
  for index,line in enumerate(txtfile.readlines()):
    content[index%split] += line.split('/')[-1]
    contentFull[index%split] += line

  for i in range(split):
 
    tmp = open('%s/FileList_%d.txt'%(FolderName,i+1),'w+')
    tmp.write(contentFull[i])
    tmp.close()

    ExcuteFile=open('%s/CondorJob_%d.sh'%(FolderName,i+1),'w+')
    ExcuteFile.write('#!/bin/bash\n\n')

    ExcuteFile.write('''
cd /afs/cern.ch/work/z/zhixing/private/CMSSW_9_4_0/src/CMSDIJET/DijetRootTreeAnalyzer2018/

eval `scramv1 runtime -sh`

'''+'\n\n')

    ExcuteFile.write('./main %s %s dijets/events /tmp/%s /tmp/%s'%('%s/FileList_%d.txt'%(FolderName,i+1),cutFile,OutputFile+'_'+str(i),OutputFile+'_'+str(i))+'\n\n')
    ExcuteFile.write('mv /tmp/%s*.root %s/'%(OutputFile+'_'+str(i),OutputDir))
    ExcuteFile.close()

    os.system('chmod 751 %s/CondorJob_%d.sh'%(FolderName,i+1))

  for i in range(split):
    SubCont = '''+JobFlavour= "testmatch"
executable = %s
output     = %s/output/$(ClusterId).$(ProcId).out
error      = %s/error/$(ClusterId).$(ProcId).err
log        = %s/log/$(ClusterId).$(ProcId).log

queue'''%('%s/CondorJob_%d.sh'%(FolderName,i+1),FolderName,FolderName,FolderName)

    submition = open('%s/Sub_%d.sub'%(FolderName,i+1),'w+')
    submition.write(SubCont)
    submition.close()

  for i in range(split):
    print 'condor_submit %s/Sub_%d.sub'%(FolderName,i+1)
    os.system('condor_submit %s/Sub_%d.sub'%(FolderName,i+1))
