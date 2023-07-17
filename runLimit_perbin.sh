for year in "run2" #"2018" "2016" "2017"
do
   for cat in  "C" #"2b" "1b"
   do
      python runLimit.py -runlimit -cards /afs/cern.ch/work/p/ptiwari/cmsCombineTool/CMSSW_11_3_4/src/limitmodels/bb+DM_analysis/bbDMlimitmodelrateParam_oneRP/datacards/datacard_bbDM${year}_${cat} -tag Apr23_${year}_${cat} -scan 1d -par ma -fixpar "[mA=600,tb=35,st=0p7]" -model THDMa -c ${cat} -y ${year}
   done
done
