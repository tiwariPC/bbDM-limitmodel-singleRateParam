import os
import sys, optparse,argparse
from glob import glob
sys.path.append('configs')

from LimitHelper import RunLimits

## ----- command line argument
usage = "python ---- "
parser = argparse.ArgumentParser(description=usage)
parser.add_argument("-i", "--inputdatacard",  dest="inputdatacard",default="datacard.txt")
parser.add_argument("-c", "--category",  dest="category",default="R")
parser.add_argument("-y", "--year",  dest="year",default="2017")
parser.add_argument("-cards", "--inputdatacardpath",  dest="inputdatacardpath",default=".")
parser.add_argument("-merge", "--mergecard", action="store_true",  dest="mergecard")
parser.add_argument("-LP", "--LPcardpath",  dest="LPcardpath",default=".")
parser.add_argument("-HP", "--HPcardpath",  dest="HPcardpath",default=".")
parser.add_argument("-o", "--outputdir",  dest="outputdir",default=".")
parser.add_argument("-tag", "--tagname",  dest="tagname",default="test")
parser.add_argument("-f", "--freezepar", action="store_true",  dest="freezepar")
parser.add_argument("-runlimit", "--runlimit", action="store_true",  dest="runlimit")
parser.add_argument("-fixpar", "--fixedparameters",  dest="fixedparameters",default="[ma=150,tb=1p0,st=0p35]")
parser.add_argument("-scan", "--scanDimension",  dest="scanDimension",default="1d")
parser.add_argument("-par", "--scanpar",  dest="scanpar",default="mA")
parser.add_argument("-model", "--model",  dest="model",default="2HDMa")
# parser.add_argument("-scan", "--paramscan",  dest="paramscan",default="mA")

args = parser.parse_args()
YEAR = args.year
pref =''
if args.freezepar:
    pref = '--freezeParameters allConstrainedNuisances'
files = []
if args.inputdatacard:
    files = [args.inputdatacard]

cat = args.category

def comp(o):
    return int(o.split('_')[-6].strip('Ma'))
if args.inputdatacardpath:
    files = glob(args.inputdatacardpath+'/*txt')
    files.sort(key=comp)

fixed_ = args.fixedparameters

fixed_ = args.fixedparameters
scanparam =args.scanpar
scan = args.scanDimension
model = args.model

print ("scan  ", scan)
print ("model  ",model)
print ('fixed_  ',fixed_)
# os.system('mkdir bin logs')
#os.system('rm -rf bin/*  logs/*')
tag=args.tagname#'oldlimitfile'
if not os.path.exists('bin/'+tag):
    os.makedirs('bin/'+tag)
# os.system('rm -rf bin/'+tag+'/*')


RunLimits=RunLimits('datacardtemplatename', '2017', 'bbDM', 'dummy', tag, model)
ifiles = ['bbDM_datacard_2017_SR_R_ggF_sp_0p35_tb_1p0_mXd_10_mA_400_ma_150.txt','bbDM_datacard_2017_SR_R_ggF_sp_0p35_tb_1p0_mXd_10_mA_600_ma_150.txt',
	'bbDM_datacard_2017_SR_R_ggF_sp_0p35_tb_1p0_mXd_10_mA_1000_ma_150.txt','bbDM_datacard_2017_SR_R_ggF_sp_0p35_tb_1p0_mXd_10_mA_1200_ma_150.txt',
	'bbDM_datacard_2017_SR_R_ggF_sp_0p35_tb_1p0_mXd_10_mA_1600_ma_150.txt']

# parameters = {"mA":[400,600,1000,1200,1600],"tb":['0p5','1p0','1p5','4p0','8p0','20p0','50p0'],"st":['0p1','0p2','0p3','0p4','0p5','0p6','0p7']}


def getParameters(model):
    dic = {}
    if model=="THDMa":
        dic = {"mA":[200,400,600,800,1000,1200,1600],"tb":['0p5','1p0','1p5','4p0','8p0','20p0','50p0'],"st":['0p1','0p2','0p3','0p4','0p5','0p6','0p7'],"ma":[10,50,100,150,200,250,300,350,400,450,500]}
    if model=="ZpB":
        dic = {"mZp":[100,200,300,350,500,650,800,1000,1500,2000,2500,3000,3500],"mchi":[1,50,100,150,200,400,600,800]}
    if model=="ZpTHDM":
        dic = {"mZp":[1000,1200,1400,1700,2000,2500],"mA0":[300,400,500,600,700,800,900,1000,1200,1600]}

    return dic

def stringToDic(fixed_):
    dic = {}
    items = fixed_.replace(']','').replace('[','').split(',')
    print ("items",items)
    for item in items:
        key = item.split('=')[0]
        value = item.split('=')[1]
        dic[key] = [value]

    return dic
def getParametersDic():
    allparameters = {}
    if scan=="1d":
        parameters=getParameters(model)
        fixedparam = stringToDic(fixed_)
        allparameters = fixedparam
        allparameters[scanparam]=parameters[scanparam]

    if scan=="2d":
        parameters=getParameters(model)
        allparameters = {}
        if model =="THDMa":
            fixedparam = stringToDic(fixed_)
            allparameters = fixedparam
        items = scanparam.replace(']','').replace('[','').split(',')
        for key in items:
            allparameters[key]=parameters[key]

    return allparameters


def prepareDatacardsList():
    parameters=getParametersDic()
    print ('parameters  ',parameters)
    datacards =[]
    if model =="ZpB":
        mZp_list = parameters['mZp']
        mchi_list= parameters['mchi']
        for mzp in mZp_list:
            for mchi in mchi_list:
                isfill = False
                if  (int(mzp)==100 and (int(mchi)==1 or int(mchi)==50)):isfill=True
                if  (int(mzp)==200 and (int(mchi)==1 or int(mchi)==50 or int(mchi)==100 or int(mchi)==150)):isfill=True
                if  (int(mzp)==300 and int(mchi)==150):isfill=True
                if  (int(mzp)==350 and int(mchi)==50):isfill=True
                if  (int(mzp)==500 and (int(mchi)==1 or int(mchi)==100 or int(mchi)==200 or int(mchi)==400)):isfill=True
                if  (int(mzp)==650 and int(mchi)==50):isfill=True
                if  (int(mzp)==800 and int(mchi)==50):isfill=True
                if  (int(mzp)==1000 and (int(mchi)==1 or int(mchi)==100 or int(mchi)==200 or int(mchi)==400 or int(mchi)==600 or int(mchi)==800)):isfill=True
                if  (int(mzp)==1500 and (int(mchi)==1 or int(mchi)==100 or int(mchi)==200 or int(mchi)==400 or int(mchi)==600 or int(mchi)==800)):isfill=True
                if  (int(mzp)==2000 and (int(mchi)==1 or int(mchi)==100 or int(mchi)==200 or int(mchi)==400 or int(mchi)==600 or int(mchi)==800)):isfill=True
                if  (int(mzp)==2500 and (int(mchi)==1 or int(mchi)==100 or int(mchi)==200 or int(mchi)==400 or int(mchi)==600 or int(mchi)==800)):isfill=True
                if  (int(mzp)==3000 and (int(mchi)==1 or int(mchi)==100 or int(mchi)==200 )):isfill=True
                if  (int(mzp)==3500 and (int(mchi)==1 or int(mchi)==100)):isfill=True
                if isfill:
                    card = 'bbDM_datacard_2017_SR_R_MZp_'+str(mzp)+'_Mchi_'+str(mchi)+'.txt'
                    datacards.append(card)
        # datacards = ['bbDM_datacard_2017_SR_R_MZp_100_Mchi_1.txt','bbDM_datacard_2017_SR_R_MZp_200_Mchi_1.txt','bbDM_datacard_2017_SR_R_MZp_500_Mchi_1.txt','bbDM_datacard_2017_SR_R_MZp_1000_Mchi_1.txt','bbDM_datacard_2017_SR_R_MZp_1500_Mchi_1.txt','bbDM_datacard_2017_SR_R_MZp_2000_Mchi_1.txt','bbDM_datacard_2017_SR_R_MZp_2500_Mchi_1.txt','bbDM_datacard_2017_SR_R_MZp_3000_Mchi_1.txt','bbDM_datacard_2017_SR_R_MZp_3500_Mchi_1.txt']
    if model=="ZpTHDM":
        mZp_list = parameters['mZp']
        mA0_list = parameters['mA0']
        for mzp in mZp_list:
            for mA in mA0_list:
                print (mzp,mA)
                isfill=False
                if  (int(mzp)==1000 and (int(mA)==300 or int(mA)==800)):isfill=True
                if (int(mzp)==1200 and (int(mA)==300 or int(mA)==500 or int(mA)==900 or int(mA)==1000)):isfill=True
                if (int(mzp)==1400 and (int(mA)==300 or int(mA)==400 or int(mA)==500 or int(mA)==600 or int(mA)==800 or int(mA)==900 or int(mA)==1000 or int(mA)==1200)) :isfill=True
                if (int(mzp)==1700 and (int(mA)==300 or int(mA)==400 or int(mA)==500 or int(mA)==600 or int(mA)==700 or int(mA)==800 or int(mA)==900 or int(mA)==1000 or int(mA)==1200 or int(mA)==1400)) :isfill=True
                if (int(mzp)==2000 and (int(mA)==300 or int(mA)==700 or int(mA)==1000 or int(mA)==1200 or int(mA)==1400 or int(mA)==1600)):isfill=True
                if (int(mzp)==2500 and (int(mA)==300 or int(mA)==400 or int(mA)==500 or int(mA)==600 or int(mA)==700 or int(mA)==1000 or int(mA)==1200 or int(mA)==1600)):isfill=True
                if isfill:
                    card = 'bbDM_datacard_2017_SR_R_MZp'+str(mzp)+'_MA0'+str(mA)+'.txt'
                    datacards.append(card)
        # datacards = ['bbDM_datacard_2017_SR_R_MZp1000_MA0300.txt','bbDM_datacard_2017_SR_R_MZp1200_MA0300.txt','bbDM_datacard_2017_SR_R_MZp1400_MA0300.txt','bbDM_datacard_2017_SR_R_MZp1700_MA0300.txt','bbDM_datacard_2017_SR_R_MZp2000_MA0300.txt','bbDM_datacard_2017_SR_R_MZp2500_MA0300.txt']
    if model=="THDMa":
        mA_list = parameters['mA']
        ma_list = parameters['ma']
        st_list = parameters['st']
        tb_list  = parameters['tb']
        print (mA_list,ma_list,st_list,tb_list)
        for tb in tb_list:
            for st in st_list:
                for ma in ma_list:
                    for mA in mA_list:
                        if int(ma)==350 and int(mA)==400:continue
                        if (int(ma)==250 or int(ma)==350) and int(mA)==200:continue
                        if len(st_list)>1 and int(ma)!=200:continue
                        if (len(tb_list)>1 and int(ma)==350):continue
                        card = 'bbDM_datacard_2017_SR_'+cat+'_ggF_sp_'+str(st)+'_tb_'+str(tb)+'_mXd_10_mA_'+str(mA)+'_ma_'+str(ma)+'.txt'
                        datacards.append(card)

    return datacards



def runLimit(datacards):
    print("datacards[0]", datacards[0])
    YEAR = datacards[0].split('/')[-1].split('bbDM_datacard_')[-1].split('_')[0]
    for datacard in datacards:
        if not model in datacard.split('/')[-1]:continue
        print "Running :  ",datacard
        print ("skipParam[0] ",skipParam[0].replace("=","_"),skipParam[1].replace("=","_"),skipParam[2].replace("=","_"))
        if model=="THDMa":
            print(skipParam[0].replace("=","").replace('mA','MA'), skipParam[1].replace("=",""), skipParam[2].replace("=","_"))
            if not skipParam[0].replace("=","").replace('mA','MA') in datacard and model=="THDMa":continue
            if not skipParam[1].replace("=","") in datacard and model=="THDMa":continue
            if not skipParam[2].replace("=","_") in datacard and model=="THDMa":continue
        print ("skipParam ",skipParam)
        if scan=="1d" and model=="ZpB":
            if not skipParam[0].replace("=","_")+'.' in datacard and model=="ZpB":continue
        if model=="ZpTHDM":
	    if not skipParam[0].replace("=","") in datacard:continue
        # YEAR = datacard.split('bbDM_datacard_')[-1].split('_')[0]
        datacard = datacard

        if not os.path.exists('logs'): os.mkdir('logs')
        # command = 'combine -M AsymptoticLimits '+datacard+'  '+pref+'   >  logs/'+datacard.split('/')[-1].replace('.txt','')+'_logfile.txt'
        command = 'combine -M AsymptoticLimits '+datacard+' >  logs/'+datacard.split('/')[-1].replace('.txt','')+'_logfile.txt'
        print ("command",command)
        os.system(command)

        RunLimits.LogToLimitList('logs/'+datacard.split('/')[-1].replace('.txt','')+'_logfile.txt',scan=scan,paramscan=scanparam, category=cat,model=model,year=YEAR)

    if scan=='1d':
        if not os.path.exists('bin'+'/'+str(tag)): os.mkdir('bin'+'/'+str(tag))
        limitrootfile = RunLimits.TextFileToRootGraphs('bin'+'/'+str(tag)+'/'+'limits_bbDM_'+cat+'_'+YEAR+'.txt')
        RunLimits.SaveLimitPdf1D(limitrootfile)
    #if scan=='2d' and model=="ZpB":

def plotLimit(tag):
        limitrootfile = RunLimits.TextFileToRootGraphs('bin'+'/'+str(tag)+'/'+'limits_bbDM_'+cat+'_'+YEAR+'.txt')
        # limitrootfile = 'bin'+'/'+str(tag)+'/'+'limits_bbDM_'+cat+'_'+YEAR+'.root'
        if scan=='1d':RunLimits.SaveLimitPdf1D(limitrootfile)

# def combineCards(LP,HP,outdir):
#     for datacard in datacards:
#         LPCard = LP+'/'+datacard
#         HPCard = HP+'/'+datacard
#         subcommand = "LP="+LPCard+"  "+"HP="+HPCard+"  >> "+outdir+"/"+datacard
#         os.system('combineCards.py  '+subcommand)

def combineCards(indir,outdir):
    for datacard in datacards:
        if 'bbDM_datacard_2017_SR_R_ggF' in datacard:
            SRCard    = indir+'/'+datacard
            TopECard  = indir+'/bbDM_datacard_2017_TOPE_R.txt'
            TopMuCard = indir+'/bbDM_datacard_2017_TOPMU_R.txt'
            ZEECard   = indir+'/bbDM_datacard_2017_ZEE_R.txt'
            ZMUMUCard = indir+'/bbDM_datacard_2017_ZMUMU_R.txt'

            subcommand = "SR="+SRCard+"  "+"TOPE="+TopECard+"  "+"TOPMU="+TopMuCard+"   "+"ZEE="+ZEECard+"   "+"ZMUMU="+ZMUMUCard+"  >> "+outdir+"/"+datacard
            print subcommand
            os.system('combineCards.py  '+subcommand)
            f_temp = open(outdir+"/"+datacard,'a')

            f_temp.write('ratezll rateParam ZEE dyjets 1.0 [0,2.5]'+'\n')
            f_temp.write('ratezll rateParam ZMUMU dyjets 1.0 [0,2.5]'+'\n')
            f_temp.write('ratezll rateParam SR zjets 1.0 [0,2.5]'+'\n')
            f_temp.write('ratett rateParam TOPE tt 1.0 [0,2.5]'+'\n')
            f_temp.write('ratett rateParam TOPMU tt 1.0 [0,2.5]'+'\n')
            f_temp.write('ratett rateParam SR tt 1.0 [0,2.5]'+'\n')
            f_temp.close()

skipParam = fixed_.replace(']','').replace('[','').split(',') #stringToDic(fixed_)

print ("skipParam ",skipParam,skipParam[0])
datacards = files #prepareDatacardsList()
print (datacards)

if args.runlimit:
    # try:
    #     runLimit(datacards)
    # except:
    #     pass
    plotLimit(tag)

if args.mergecard:
    # combineCards(args.LPcardpath,args.HPcardpath,args.outputdir)
    combineCards(args.inputdatacardpath,args.outputdir)
