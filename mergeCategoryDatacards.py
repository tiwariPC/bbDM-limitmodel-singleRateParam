import os
from glob import glob

import sys, optparse,argparse
## ----- command line argument
usage = "python DataframeToHist.py -F -inDir directoryName -D outputDir "
parser = argparse.ArgumentParser(description=usage)
parser.add_argument("-O", "--onebcards",  dest="onebcards",default=".")
parser.add_argument("-T", "--twobcards",  dest="twobcards",default=".")
parser.add_argument("-D", "--outputdir", dest="outputdir",default=".")

args = parser.parse_args()

path_oneb = args.onebcards
path_twob = args.twobcards

Outputpath = args.outputdir

files_oneb = glob(path_oneb+"/*txt")
files_twob = glob(path_twob+"/*txt")
if os.path.isdir(Outputpath):
	os.system("rm -rf "+Outputpath+"/*")
else:os.system("mkdir "+Outputpath)

for ii, infile in  enumerate(files_twob):
	#print infile
	for jj, infile2 in enumerate(files_oneb):
	   if infile.split('/')[-1].replace('_2b_','_1b_')==infile2.split('/')[-1]:
	   #if os.path.isfile(files_oneb[ij]):#.exists():
		outputile = infile.split('/')[-1].replace("_2b_","_C_")
		os.system('combineCards.py  '+"cat_1b="+infile2+"   "+"cat_2b="+infile+"     >"+Outputpath+"/"+outputile)


os.system("sed -i'.bak' 's|"+path_oneb+"/|"+''+ "|g' "+Outputpath+"/*")
os.system("sed -i'.bak' 's|"+path_twob+"/|"+''+ "|g' "+Outputpath+"/*")

# os.system("sed -i'.bak' 's|cat_1b=|cat_1b="+path_oneb+"/|g'")
# os.system("sed -i'.bak' 's|cat_2b=|cat_2b="+path_twob+"/|g'")

os.system("rm -rf "+Outputpath+"/*bak")
