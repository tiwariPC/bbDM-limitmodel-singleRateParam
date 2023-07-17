for algorithm in "saturated" "KS" "AD"
do
   for year in "2016" "2017" "2018"
   do
      for catg in "1b" "2b" "C"
      do
         for mode in "_result_bonly_CRonly"
         do
            datacard=datacards/datacard_bbDM"${year}"_"${catg}"/bbDM_datacard_"${year}"_THDMa_${catg}_allregion_2HDMa_Ma150_MChi1_MA600_tb35_st_0p7.txt

            text2workspace.py $datacard --channel-masks
            datacardws=`echo $datacard | sed  's|.txt|.root|g'`

            echo $datacardws

            combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode} --setParametersForFit mask_sr=1,mask_cat_1b_sr=1,mask_cat_2b_sr=1 --setParametersForEval mask_sr=0,mask_cat_1b_sr=0,mask_cat_2b_sr=0 --freezeParameters r --setParameters r=0

            combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParametersForFit mask_sr=1,mask_cat_1b_sr=1,mask_cat_2b_sr=1 --setParametersForEval mask_sr=0,mask_cat_1b_sr=0,mask_cat_2b_sr=0 --freezeParameters r --setParameters r=0,mask_sr=1,mask_cat_1b_sr=1,mask_cat_2b_sr=1 -t 1 --toysFrequentist -s 12431 &

            wait

            hadd higgsCombine${mode}_toy.GoodnessOfFit.mH120.Merged.root higgsCombine${mode}_toy.GoodnessOfFit.mH120.*.root

            ## plotting
            combineTool.py -M CollectGoodnessOfFit --input higgsCombine${mode}.GoodnessOfFit.mH120.root higgsCombine${mode}_toy.GoodnessOfFit.mH120.Merged.root -m 120.0 -o gof${mode}_${catg}_${year}.json
            plotGof.py gof${mode}_${catg}_${year}.json --statistic ${algorithm} --mass 120.0 -o gof${mode}_${catg}_${year} --title-right="B-only hypothesis"

            for f in *gof${mode}_${catg}_${year}*; do mv -v -f -- "$f" ./gofplots_${algorithm} ; done

            rm -rf higgsCombine${mode}*.root
         done
      done
   done
done