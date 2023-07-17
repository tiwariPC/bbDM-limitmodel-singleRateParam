import os
import glob

path_2016='datacards/datacard_bbDM2016_C'
path_2017='datacards/datacard_bbDM2017_C'
path_2018='datacards/datacard_bbDM2018_C'
cards_2016 = glob.glob(path_2016+'/*.txt')
cards_2017 = glob.glob(path_2017+'/*.txt')
cards_2018 = glob.glob(path_2018+'/*.txt')

Outputpath='datacards/datacard_bbDMrun2_C'
os.system('rm -rf datacards/datacard_bbDMrun2_C/*')
if not os.path.exists('datacards/datacard_bbDMrun2_C'):
    os.mkdir('datacards/datacard_bbDMrun2_C')

def mergeYearCards(cards_2016,cards_2017,cards_2018):
    for ii, infile1 in  enumerate(cards_2016):
        for jj, infile2 in enumerate(cards_2017):
            for kk, infile3 in enumerate(cards_2018):
                if infile1.split('/')[-1].replace('_2016_','_2017_')==infile2.split('/')[-1] and infile1.split('/')[-1].replace('_2016_','_2018_')==infile3.split('/')[-1]:
                #if os.path.isfile(files_B[ij]):#.exists():
                    outputile = infile1.split('/')[-1].replace("_2016_","_run2_")
                    os.system('combineCards.py  '+"d2016="+infile1+"   "+"d2017="+infile2+"   "+"d2018="+infile3+"     >"+Outputpath+"/"+outputile)

mergeYearCards(cards_2016,cards_2017,cards_2018)

os.system("sed -i'.bak' 's|"+path_2016+"/|"+''+ "|g' "+Outputpath+"/*")
os.system("sed -i'.bak' 's|"+path_2017+"/|"+''+ "|g' "+Outputpath+"/*")
os.system("sed -i'.bak' 's|"+path_2018+"/|"+''+ "|g' "+Outputpath+"/*")

os.system("rm -rf "+Outputpath+"/*bak")
