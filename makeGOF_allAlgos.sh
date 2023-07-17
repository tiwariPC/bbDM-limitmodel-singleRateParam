maskParams="mask_sr=1,mask_cat_1b_sr=1,mask_cat_2b_sr=1,mask_d2016_cat_1b_sr=1,mask_d2016_cat_2b_sr=1,mask_d2017_cat_1b_sr=1,mask_d2017_cat_2b_sr=1,mask_d2018_cat_1b_sr=1,mask_d2018_cat_2b_sr=1"
unmaskParams="mask_sr=0,mask_cat_1b_sr=0,mask_cat_2b_sr=0,mask_d2016_cat_1b_sr=0,mask_d2016_cat_2b_sr=0,mask_d2017_cat_1b_sr=0,mask_d2017_cat_2b_sr=0,mask_d2018_cat_1b_sr=0,mask_d2018_cat_2b_sr=0"

for year in "2016" "2017" "2018"
do
   for catg in "1b" "2b" "C"
   do
      datacard=datacards/datacard_bbDM"${year}"_"${catg}"/bbDM_datacard_"${year}"_THDMa_${catg}_allregion_2HDMa_Ma150_MChi1_MA600_tb35_st_0p7.txt
      text2workspace.py $datacard --channel-masks
      datacardws=`echo $datacard | sed  's|.txt|.root|g'`
      echo $datacardws
      for mode in "_result_bonly_CRonly"
      do
         for algorithm in "saturated" #"KS" "AD"
         do
            combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode} --setParametersForFit ${maskParams} --setParametersForEval ${unmaskParams} --freezeParameters r --setParameters r=0

            combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParametersForFit ${maskParams} --setParametersForEval ${unmaskParams} --freezeParameters r --setParameters r=0,${maskParams} -t 100 --toysFrequentist -s 12431 &
            combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParametersForFit ${maskParams} --setParametersForEval ${unmaskParams} --freezeParameters r --setParameters r=0,${maskParams} -t 100 --toysFrequentist -s 12432 &
            combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParametersForFit ${maskParams} --setParametersForEval ${unmaskParams} --freezeParameters r --setParameters r=0,${maskParams} -t 100 --toysFrequentist -s 12433 &
            combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParametersForFit ${maskParams} --setParametersForEval ${unmaskParams} --freezeParameters r --setParameters r=0,${maskParams} -t 100 --toysFrequentist -s 12434 &
            combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParametersForFit ${maskParams} --setParametersForEval ${unmaskParams} --freezeParameters r --setParameters r=0,${maskParams} -t 100 --toysFrequentist -s 12435 &
            combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParametersForFit ${maskParams} --setParametersForEval ${unmaskParams} --freezeParameters r --setParameters r=0,${maskParams} -t 100 --toysFrequentist -s 12436 &
            combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParametersForFit ${maskParams} --setParametersForEval ${unmaskParams} --freezeParameters r --setParameters r=0,${maskParams} -t 100 --toysFrequentist -s 12437 &
            combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParametersForFit ${maskParams} --setParametersForEval ${unmaskParams} --freezeParameters r --setParameters r=0,${maskParams} -t 100 --toysFrequentist -s 12438 &
            combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParametersForFit ${maskParams} --setParametersForEval ${unmaskParams} --freezeParameters r --setParameters r=0,${maskParams} -t 100 --toysFrequentist -s 12439 &
            combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParametersForFit ${maskParams} --setParametersForEval ${unmaskParams} --freezeParameters r --setParameters r=0,${maskParams} -t 100 --toysFrequentist -s 12430 &
            combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParametersForFit ${maskParams} --setParametersForEval ${unmaskParams} --freezeParameters r --setParameters r=0,${maskParams} -t 100 --toysFrequentist -s 124311 &
            combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParametersForFit ${maskParams} --setParametersForEval ${unmaskParams} --freezeParameters r --setParameters r=0,${maskParams} -t 100 --toysFrequentist -s 124312 &
            combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParametersForFit ${maskParams} --setParametersForEval ${unmaskParams} --freezeParameters r --setParameters r=0,${maskParams} -t 100 --toysFrequentist -s 124313 &
            combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParametersForFit ${maskParams} --setParametersForEval ${unmaskParams} --freezeParameters r --setParameters r=0,${maskParams} -t 100 --toysFrequentist -s 124314 &
            combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParametersForFit ${maskParams} --setParametersForEval ${unmaskParams} --freezeParameters r --setParameters r=0,${maskParams} -t 100 --toysFrequentist -s 124315 &
            combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParametersForFit ${maskParams} --setParametersForEval ${unmaskParams} --freezeParameters r --setParameters r=0,${maskParams} -t 100 --toysFrequentist -s 124316 &
            combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParametersForFit ${maskParams} --setParametersForEval ${unmaskParams} --freezeParameters r --setParameters r=0,${maskParams} -t 100 --toysFrequentist -s 124317 &
            combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParametersForFit ${maskParams} --setParametersForEval ${unmaskParams} --freezeParameters r --setParameters r=0,${maskParams} -t 100 --toysFrequentist -s 124318 &
            combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParametersForFit ${maskParams} --setParametersForEval ${unmaskParams} --freezeParameters r --setParameters r=0,${maskParams} -t 100 --toysFrequentist -s 124319 &
            combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParametersForFit ${maskParams} --setParametersForEval ${unmaskParams} --freezeParameters r --setParameters r=0,${maskParams} -t 100 --toysFrequentist -s 124320 &

            wait
            # ${mode}
            hadd higgsCombine${mode}_toy.GoodnessOfFit.mH120.Merged.root higgsCombine${mode}_toy.GoodnessOfFit.mH120.*.root

            ## plotting
            combineTool.py -M CollectGoodnessOfFit --input higgsCombine${mode}.GoodnessOfFit.mH120.root higgsCombine${mode}_toy.GoodnessOfFit.mH120.Merged.root -m 120.0 -o gof${mode}_${catg}_${year}.json
            plotGof.py gof${mode}_${catg}_${year}.json --statistic ${algorithm} --mass 120.0 -o gof${mode}_${catg}_${year} --title-right="B-only hypothesis("${catg}" "${year}")"

            for f in *gof${mode}_${catg}_${year}*; do mv -v -f -- "$f" ./gofplots_${algorithm} ; done

            rm -rf higgsCombine${mode}*.root
         done
      done
   done
done
