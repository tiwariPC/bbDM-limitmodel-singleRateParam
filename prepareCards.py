import os
import yaml
import numpy as np
from collections import OrderedDict
import pandas as pd
import sys, optparse,argparse

## ----- command line argument
usage = "python -y 2017 -c 2b -reg ['SR']"
parser = argparse.ArgumentParser(description=usage)
parser.add_argument("-y", "--year", dest="year", default="2017")
parser.add_argument("-m", "--model", dest="model", default="THDMa")
parser.add_argument("-c", "--category",  dest="category",default="B")
parser.add_argument("-f", "--inputfilename",  dest="inputfilename",default="")
# parser.add_argument("-r", "--region", dest="region", default=['SR'])
parser.add_argument("-reg", nargs="+", default=["a", "b"])
args = parser.parse_args()

year     = args.year
category = args.category
regions  = args.reg
modelName = args.model
rootfilename = args.inputfilename

print (year, category, regions)
f  = open('datacard_templates/datacard_template_'+category+'.yaml')
doc = yaml.safe_load(f)

signalFile = open('datacard_templates/datacard_template_signal.yaml','r')
signalDoc  = yaml.safe_load(signalFile)

outdir2 = 'datacards/datacard_bbDM'+year+'_'+category
os.system('mkdir '+ outdir2)
os.system('mkdir datacards/temp_cards')
os.system('rm -rf  datacards/temp_cards/*  '+ outdir2+'/*')
top_ = '''
imax *  number of channels
jmax *  number of backgrounds

kmax *  number of nuisance parameters (sources of systematical uncertainties)
'''

def getUpperPart2(reg,cat):
   top_= 'shapes * '+reg+' AllMETHistos.root  bbDM'+year+'_'+cat+'_'+reg+'_$PROCESS bbDM'+year+'_'+cat+'_'+reg+'_$PROCESS_$SYSTEMATIC'
   return top_

# def getUpperPart2(reg,cat):
#    top_= 'shapes * '+reg+' AllMETHistos.root  bbDM2017_'+cat+'_'+reg+'_bdtscore'+'_$PROCESS bbDM2017_'+cat+'_'+reg+'_bdtscore'+'_$PROCESS_$SYSTEMATIC'
#    return top_

def getUpperPart3(reg):
   top_ = 'bin '+reg
   # observation -1
   return top_

def getDic(dics,name):
   values=''
   itm=dics[name]
   # print name ,itm[0].split()
   values = itm[0].split()
   # for key, value in dics:
   #    if key==name:
   #       itm=np.array(value[0].split())
   return values

def getSyst(lists):
   syst=OrderedDict()
   # print getDic(lists,'bin')
   reg     = getDic(lists,'bin')[0].split(':')[0]
   length  = int(getDic(lists,'bin')[0].split(':')[1])
   nuis    = getDic(lists,'Nuisances')
   unc     = getDic(lists,'SystUnclnN')
   for n, u in zip(nuis,unc):
      # print 'testing ', n , u
      syst[str(n)]=[u] * length

   return syst


def getProcSyst(lists):
   nuisancesForCard=OrderedDict()
   # print 'testing ', lists
   NuisForProc = lists['NuisForProc']
   uncertainties  = lists['UnclnN']
   procs   = getDic(lists,'Process')

   # print 'NuisForProc',NuisForProc
   for ij, istring in enumerate(uncertainties):
      nuis = istring.split()[0]
      syst = istring.split()[1]
      # print 'nuis, syst',nuis, syst
      values=[]
      if syst=='shape':values.append('shape')
      else:values.append('lnN')

      for proc in procs:
         # print nuis,NuisForProc[ij]

         if proc in  (NuisForProc[ij])[nuis]:
            if syst=='shape':
               values.append(1)
            else:
               values.append(syst)
         else:values.append('-')
      nuisancesForCard[nuis]=values

   # print ('nuisancesForCard', nuisancesForCard)
   return nuisancesForCard


def getbinProcRate(lists):
   binProcRate = OrderedDict()
   reg     = getDic(lists,'bin')[0].split(':')[0]
   length  = int(getDic(lists,'bin')[0].split(':')[1])
   procs   = getDic(lists,'Process')
   procs1  = getDic(lists,'process1')

   rates   = [getDic(lists,'rate')[0].split(':')[0]] * length

   binProcRate['bin']      =  [reg] * length
   binProcRate['process']  =  procs
   binProcRate['process1'] =  procs1
   binProcRate['rate']     = rates
   # print 'binProcRate', binProcRate

   # print (lists['rateTest'])

   return binProcRate

def getProcRate(lists):
   binProcRate = OrderedDict()
   reg     = getDic(lists,'bin')[0].split(':')[0]
   length  = int(getDic(lists,'bin')[0].split(':')[1])
   procs   = getDic(lists,'Process')
   procs1  = getDic(lists,'process1')

   rates   = [getDic(lists,'rate')[0].split(':')[0]] * length

   # binProcRate['bin']      =  [reg] * length
   # binProcRate['process']  =  procs
   binProcRate['process'] =  procs1
   binProcRate['rate']     = rates
   # print 'binProcRate', binProcRate

   # print (lists['rateTest'])

   return binProcRate


def getSignalHists(doc,model):
   parameters = doc[model]
   # print ("parameters   :  %s"%parameters)
   samples  = []
   if model=="THDMa":
      ma_list  = parameters[2]['ma']
      mA_list  = parameters[3]['mA']

      for mA in mA_list:
         for ma in ma_list:
            if int(mA)!=600:continue
            samp = "2HDMa_Ma"+str(ma)+"_MChi1_MA"+str(mA)+"_tb35_st_0p7"
            samples.append(samp)
   print ("samples  ",samples)
   print ("total samples   ",len(samples))
   return samples
'''
=======================
START WRITING DATACARDS
=======================
'''
for reg in regions:
   # print getSyst(doc.items())
   # print (doc[reg])
   if reg=='SR':

      for sigHist in getSignalHists(signalDoc,modelName):

         outputfile = 'bbDM_datacard_'+year+'_'+reg+'_'+category+'_'+sigHist+'.txt'
         outdir     = 'datacards/temp_cards'
         df0 = pd.DataFrame(getbinProcRate(doc[reg]))
         # df1 = pd.DataFrame(getProcRate(doc[reg]))
         df0['process'] = df0['process'].replace(['signal'],sigHist)
         # sigHist_bb     = sigHist.replace('ggF','bbF')
         # df0['process'] = df0['process'].replace(['signal2'],sigHist_bb)

         # df =  pd.DataFrame(getSyst(doc))
         df =  pd.DataFrame(getProcSyst(doc[reg]))
         # df = pd.merge(df0,df1)

         fout = open(outdir+'/'+outputfile,'w')
         p0 = df0.T.to_string(justify='right',index=True, header=False)
         # p1 = df1.T.to_string(justify='right',index=True, header=False)
         p = df.T.to_string(justify='right',index=True,header=False)

         part1 = top_
         part2 = getUpperPart2(reg,category)
         part3 = getUpperPart3(reg)

         fout.write(part1+'\n')
         fout.write('------------'+'\n')
         fout.write(part2+'\n')
         fout.write('------------'+'\n')
         fout.write(part3+'\n')
         fout.write('observation -1'+'\n')
         fout.write('------------'+'\n')
         fout.write(p0+'\n')
         # fout.write(p1+'\n')
         fout.write('------------'+'\n')
         fout.write(p+'\n')
         fout.close()

   else:
      outputfile = 'bbDM_datacard_'+year+'_'+reg+'_'+category+'.txt'
      outdir     = 'datacards/temp_cards'
      # print(doc[reg])
      df0 = pd.DataFrame(getbinProcRate(doc[reg]))
      # df1 = pd.DataFrame(getProcRate(doc[reg]))
      df0['process'] = df0['process'].replace(['signal'],sigHist)



      # df =  pd.DataFrame(getSyst(doc))
      df =  pd.DataFrame(getProcSyst(doc[reg]))
      # df = pd.merge(df0,df1)

      fout = open(outdir+'/'+outputfile,'w')
      p0 = df0.T.to_string(justify='right',index=True, header=False)
      # p1 = df1.T.to_string(justify='right',index=True, header=False)
      p = df.T.to_string(justify='right',index=True,header=False)

      part1 = top_
      part2 = getUpperPart2(reg,category)
      part3 = getUpperPart3(reg)

      fout.write(part1+'\n')
      fout.write('------------'+'\n')
      fout.write(part2+'\n')
      fout.write('------------'+'\n')
      fout.write(part3+'\n')
      fout.write('observation -1'+'\n')
      fout.write('------------'+'\n')
      fout.write(p0+'\n')
      # fout.write(p1+'\n')
      fout.write('------------'+'\n')
      fout.write(p+'\n')
      fout.close()

'''
============================
replace process1 with process
============================
'''
os.system("sed -i'.bak' 's/process1/process /g' datacards/temp_cards/*")
os.system("sed -i'.bak' 's/YEAR/"+year+"/g' datacards/temp_cards/*")
os.system("rm -rf datacards/temp_cards/*bak")



modelRename =''

if modelName == 'THDMa' :
   modelRename = 'THDMa'

bbDM_file='datacardslist/bbDM'+year+'_datacardslist_'+category+'_'+'allregion_'+modelRename+'_all.txt'
bbDM_file_SR='datacardslist/bbDM'+year+'_datacardslist_'+category+'_'+'SR_'+modelRename+'_all.txt'


ftxt = open(bbDM_file,'w')
ftxt_SR= open(bbDM_file_SR,'w')
for sigHist in getSignalHists(signalDoc,modelName):
   outfile_SR = 'bbDM'+year+'_'+category+'_SR_'+sigHist
   srfile = 'bbDM_datacard_'+year+'_SR_'+category+'_'+sigHist+'.txt'
   outfile= 'bbDM_datacard_'+year+'_'+modelRename+'_'+category+'_allregion_'+sigHist+'.txt'
   if category=='1b':
      os.system('combineCards.py sr='+outdir+'/'+srfile+' zee='+outdir+'/bbDM_datacard_'+year+'_ZEE_'+category+'.txt  zmumu='+outdir+'/bbDM_datacard_'+year+'_ZMUMU_'+category+'.txt wmu='+outdir+'/bbDM_datacard_'+year+'_WMU_'+category+'.txt we='+outdir+'/bbDM_datacard_'+year+'_WE_'+category+'.txt >'+outdir2+'/'+outfile)
      ftmp = open(outdir2+'/'+outfile,'a')
      ftmp.write('\n')
      ftmp.write("ratewjets_"+category+"        rateParam we wjets 1. [0.5,1.5]"+"\n")
      ftmp.write("ratewjets_"+category+"        rateParam wmu wjets 1. [0.5,1.5]"+"\n")
      ftmp.write("ratewjets_"+category+"        rateParam sr wjets 1. [0.5,1.5]"+"\n")
      #ftmp.write("ratewjets_m        rateParam sr wjets 1. [0.5,1.5]"+"\n")
      ftmp.write("ratezjets_"+category+"     rateParam zee dyjets 1. [0.5,1.5]"+"\n")
      ftmp.write("ratezjets_"+category+"     rateParam zmumu dyjets 1. [0.5,1.5]"+"\n")
      ftmp.write("ratezjets_"+category+"     rateParam sr zjets 1. [0.5,1.5]"+"\n")
      #ftmp.write("ratezjets_m     rateParam sr zjets 1. [0.5,1.5]"+"\n")
      ftmp.write("sr autoMCStats 10 0 1"+"\n")
      ftmp.write("we autoMCStats 10 0 1"+"\n")
      ftmp.write("wmu autoMCStats 10 0 1"+"\n")
      ftmp.write("zee autoMCStats 10 0 1"+"\n")
      ftmp.write("zmumu autoMCStats 10 0 1"+"\n")
      ftmp.close()
      ftxt.write(outdir+'/'+outfile+' \n')
      ftxt_SR.write(outfile_SR+'\n')
   elif category=='2b':
      os.system('combineCards.py sr='+outdir+'/'+srfile+' zee='+outdir+'/bbDM_datacard_'+year+'_ZEE_'+category+'.txt  zmumu='+outdir+'/bbDM_datacard_'+year+'_ZMUMU_'+category+'.txt topmu='+outdir+'/bbDM_datacard_'+year+'_TOPMU_'+category+'.txt tope='+outdir+'/bbDM_datacard_'+year+'_TOPE_'+category+'.txt >'+outdir2+'/'+outfile)
      ftmp = open(outdir2+'/'+outfile,'a')
      ftmp.write('\n')
      ftmp.write("ratett_"+category+"        rateParam tope tt 1. [0.5,1.5]"+"\n")
      ftmp.write("ratett_"+category+"        rateParam topmu tt 1. [0.5,1.5]"+"\n")
      ftmp.write("ratett_"+category+"        rateParam sr tt 1. [0.5,1.5]"+"\n")
      #ftmp.write("ratett_m        rateParam sr tt 1. [0.5,1.5]"+"\n")
      ftmp.write("ratezjets_"+category+"     rateParam zee dyjets 1. [0.5,1.5]"+"\n")
      ftmp.write("ratezjets_"+category+"     rateParam zmumu dyjets 1. [0.5,1.5]"+"\n")
      ftmp.write("ratezjets_"+category+"     rateParam sr zjets 1. [0.5,1.5]"+"\n")
      #ftmp.write("ratezjets_m     rateParam sr zjets 1. [0.5,1.5]"+"\n")
      ftmp.write("sr autoMCStats 10 0 1"+"\n")
      ftmp.write("tope autoMCStats 10 0 1"+"\n")
      ftmp.write("topmu autoMCStats 10 0 1"+"\n")
      ftmp.write("zee autoMCStats 10 0 1"+"\n")
      ftmp.write("zmumu autoMCStats 10 0 1"+"\n")
      ftmp.close()
      ftxt.write(outdir+'/'+outfile+' \n')
      ftxt_SR.write(outfile_SR+'\n')
ftxt.close()
ftxt_SR.close()

# os.system("sed -i'.bak' 's|datacards/temp_cards/|"+''+ "|g' "+outdir2+"/*")
os.system("rm -rf "+outdir2+"/*bak")
if rootfilename:
   os.system("sed -i'.bak' 's|datacards/temp_cards/AllMETHistos.root|"+rootfilename+ "|g' "+outdir2+"/*")
   os.system("rm -rf "+outdir2+"/*bak")
