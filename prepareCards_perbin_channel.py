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
f  = open('datacard_templates/datacard_template_'+category+'_perBin_asChanel_addProcs.yaml')
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
   if 'SR' in reg:
      for sigHist in getSignalHists(signalDoc,modelName):
         outputfile = 'bbDM_datacard_'+year+'_'+reg+'_'+category+'_'+sigHist+'.txt'
         outdir     = 'datacards/temp_cards'
         df0 = pd.DataFrame(getbinProcRate(doc[reg]))
         # df1 = pd.DataFrame(getProcRate(doc[reg]))
         # df0['process'] = df0['process'].replace(['signal'],sigHist)
         df0['process'] = [ele.replace('signal',sigHist) for ele in df0['process']]
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
   srfile = ['bbDM_datacard_'+year+'_SR_bin'+str(ibin)+'_'+category+'_'+sigHist+'.txt' for ibin in range(1,5)]
   outfile= 'bbDM_datacard_'+year+'_'+modelRename+'_'+category+'_allregion_'+sigHist+'.txt'
   if category=='1b':
      os.system('combineCards.py sr_bin1='+outdir+'/'+srfile[0]+' sr_bin2='+outdir+'/'+srfile[1]+' sr_bin3='+outdir+'/'+srfile[2]+' sr_bin4='+outdir+'/'+srfile[3]+' zll_bin1='+outdir+'/bbDM_datacard_'+year+'_ZLL_bin1_'+category+'.txt zll_bin2='+outdir+'/bbDM_datacard_'+year+'_ZLL_bin2_'+category+'.txt zll_bin3='+outdir+'/bbDM_datacard_'+year+'_ZLL_bin3_'+category+'.txt zll_bin4='+outdir+'/bbDM_datacard_'+year+'_ZLL_bin4_'+category+'.txt wl_bin1='+outdir+'/bbDM_datacard_'+year+'_WL_bin1_'+category+'.txt wl_bin2='+outdir+'/bbDM_datacard_'+year+'_WL_bin2_'+category+'.txt wl_bin3='+outdir+'/bbDM_datacard_'+year+'_WL_bin3_'+category+'.txt wl_bin4='+outdir+'/bbDM_datacard_'+year+'_WL_bin4_'+category+'.txt >'+outdir2+'/'+outfile)
      ftmp = open(outdir2+'/'+outfile,'a')
      ftmp.write('\n')
      for ibin in ['bin1','bin2','bin3','bin4']:
         ftmp.write("ratewjets_"+category+"_"+year+"_"+ibin+"        rateParam wl_"+ibin+" wjets 1. [0.5,1.5]"+"\n")
         ftmp.write("ratewjets_"+category+"_"+year+"_"+ibin+"        rateParam sr_"+ibin+" wjets 1. [0.5,1.5]"+"\n")
         ftmp.write("ratezjets_"+category+"_"+year+"_"+ibin+"     rateParam zll_"+ibin+" dyjets 1. [0.5,1.5]"+"\n")
         ftmp.write("ratezjets_"+category+"_"+year+"_"+ibin+"     rateParam sr_"+ibin+" zjets 1. [0.5,1.5]"+"\n")
         ftmp.write("sr_"+ibin+" autoMCStats 90 0 1"+"\n")
         ftmp.write("wl_"+ibin+" autoMCStats 90 0 1"+"\n")
         ftmp.write("zll_"+ibin+" autoMCStats 90 0 1"+"\n")
      ftmp.close()
      ftxt.write(outdir+'/'+outfile+' \n')
      ftxt_SR.write(outfile_SR+'\n')
   elif category=='2b':
      os.system('combineCards.py sr_bin1='+outdir+'/'+srfile[0]+' sr_bin2='+outdir+'/'+srfile[1]+' sr_bin3='+outdir+'/'+srfile[2]+' sr_bin4='+outdir+'/'+srfile[3]+' zll_bin1='+outdir+'/bbDM_datacard_'+year+'_ZLL_bin1_'+category+'.txt zll_bin2='+outdir+'/bbDM_datacard_'+year+'_ZLL_bin2_'+category+'.txt zll_bin3='+outdir+'/bbDM_datacard_'+year+'_ZLL_bin3_'+category+'.txt zll_bin4='+outdir+'/bbDM_datacard_'+year+'_ZLL_bin4_'+category+'.txt topl_bin1='+outdir+'/bbDM_datacard_'+year+'_TOPL_bin1_'+category+'.txt topl_bin2='+outdir+'/bbDM_datacard_'+year+'_TOPL_bin2_'+category+'.txt topl_bin3='+outdir+'/bbDM_datacard_'+year+'_TOPL_bin3_'+category+'.txt topl_bin4='+outdir+'/bbDM_datacard_'+year+'_TOPL_bin4_'+category+'.txt >'+outdir2+'/'+outfile)
      ftmp = open(outdir2+'/'+outfile,'a')
      ftmp.write('\n')
      for ibin in ['bin1','bin2','bin3','bin4']:
         ftmp.write("ratett_"+category+"_"+year+"_"+ibin+"        rateParam topl_"+ibin+" tt  1. [0.5,1.5]"+"\n")
         ftmp.write("ratett_"+category+"_"+year+"_"+ibin+"        rateParam sr_"+ibin+" tt  1. [0.5,1.5]"+"\n")
         ftmp.write("ratezjets_"+category+"_"+year+"_"+ibin+"     rateParam zll_"+ibin+" dyjets 1. [0.5,1.5]"+"\n")
         ftmp.write("ratezjets_"+category+"_"+year+"_"+ibin+"     rateParam sr_"+ibin+" zjets  1. [0.5,1.5]"+"\n")
         ftmp.write("sr_"+ibin+" autoMCStats 90 0 1"+"\n")
         ftmp.write("topl_"+ibin+" autoMCStats 90 0 1"+"\n")
         ftmp.write("zll_"+ibin+" autoMCStats 90 0 1"+"\n")
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
