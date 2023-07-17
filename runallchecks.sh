for year in "2016" "2017" "2018" "run2"
do
   for catg in "C" "2b" "1b"
   do
      source /afs/cern.ch/work/p/ptiwari/cmsCombineTool/CMSSW_11_3_4/src/limitmodels/bb+DM_analysis/bbDMlimitmodelrateParam_oneRP/runPulls_perbin.sh "pullsNimpacts"${year} "datacards/datacard_bbDM"${year}"_"${catg}"/bbDM_datacard_"${year}"_THDMa_${catg}_allregion_2HDMa_Ma150_MChi1_MA600_tb35_st_0p7.txt" ${year} ${catg}
   # done
   # for catg in "C" "2b" "1b"
   # do
      source /afs/cern.ch/work/p/ptiwari/cmsCombineTool/CMSSW_11_3_4/src/limitmodels/bb+DM_analysis/bbDMlimitmodelrateParam_oneRP/runImpacts.sh "pullsNimpacts"${year} "datacards/datacard_bbDM"${year}"_"${catg}"/bbDM_datacard_"${year}"_THDMa_${catg}_allregion_2HDMa_Ma150_MChi1_MA600_tb35_st_0p7.txt" ${year} ${catg}
   done
done
