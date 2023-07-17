maskParams="mask_sr_bin1=1,mask_sr_bin2=1,mask_sr_bin3=1,mask_sr_bin4=1,mask_cat_1b_sr_bin1=1,mask_cat_1b_sr_bin2=1,mask_cat_1b_sr_bin3=1,mask_cat_1b_sr_bin4=1,mask_cat_2b_sr_bin1=1,mask_cat_2b_sr_bin2=1,mask_cat_2b_sr_bin3=1,mask_cat_2b_sr_bin4=1,mask_d2016_cat_1b_sr_bin1=1,mask_d2016_cat_1b_sr_bin2=1,mask_d2016_cat_1b_sr_bin3=1,mask_d2016_cat_1b_sr_bin4=1,mask_d2016_cat_2b_sr_bin1=1,mask_d2016_cat_2b_sr_bin2=1,mask_d2016_cat_2b_sr_bin3=1,mask_d2016_cat_2b_sr_bin4=1,mask_d2017_cat_1b_sr_bin1=1,mask_d2017_cat_1b_sr_bin2=1,mask_d2017_cat_1b_sr_bin3=1,mask_d2017_cat_1b_sr_bin4=1,mask_d2017_cat_2b_sr_bin1=1,mask_d2017_cat_2b_sr_bin2=1,mask_d2017_cat_2b_sr_bin3=1,mask_d2017_cat_2b_sr_bin4=1,mask_d2018_cat_1b_sr_bin1=1,mask_d2018_cat_1b_sr_bin2=1,mask_d2018_cat_1b_sr_bin3=1,mask_d2018_cat_1b_sr_bin4=1,mask_d2018_cat_2b_sr_bin1=1,mask_d2018_cat_2b_sr_bin2=1,mask_d2018_cat_2b_sr_bin3=1,mask_d2018_cat_2b_sr_bin4=1"
unmaskParams="mask_sr_bin1=0,mask_sr_bin2=0,mask_sr_bin3=0,mask_sr_bin4=0,mask_cat_1b_sr_bin1=0,mask_cat_1b_sr_bin2=0,mask_cat_1b_sr_bin3=0,mask_cat_1b_sr_bin4=0,mask_cat_2b_sr_bin1=0,mask_cat_2b_sr_bin2=0,mask_cat_2b_sr_bin3=0,mask_cat_2b_sr_bin4=0,mask_d2016_cat_1b_sr_bin1=0,mask_d2016_cat_1b_sr_bin2=0,mask_d2016_cat_1b_sr_bin3=0,mask_d2016_cat_1b_sr_bin4=0,mask_d2016_cat_2b_sr_bin1=0,mask_d2016_cat_2b_sr_bin2=0,mask_d2016_cat_2b_sr_bin3=0,mask_d2016_cat_2b_sr_bin4=0,mask_d2017_cat_1b_sr_bin1=0,mask_d2017_cat_1b_sr_bin2=0,mask_d2017_cat_1b_sr_bin3=0,mask_d2017_cat_1b_sr_bin4=0,mask_d2017_cat_2b_sr_bin1=0,mask_d2017_cat_2b_sr_bin2=0,mask_d2017_cat_2b_sr_bin3=0,mask_d2017_cat_2b_sr_bin4=0,mask_d2018_cat_1b_sr_bin1=0,mask_d2018_cat_1b_sr_bin2=0,mask_d2018_cat_1b_sr_bin3=0,mask_d2018_cat_1b_sr_bin4=0,mask_d2018_cat_2b_sr_bin1=0,mask_d2018_cat_2b_sr_bin2=0,mask_d2018_cat_2b_sr_bin3=0,mask_d2018_cat_2b_sr_bin4=0,"

for year in "2016" "2017" "2018" "run2"
do
   for catg in "C" "1b" "2b"
   do
      datacard=datacards/datacard_bbDM"${year}"_"${catg}"/bbDM_datacard_"${year}"_THDMa_${catg}_allregion_2HDMa_Ma150_MChi1_MA600_tb35_st_0p7.txt
      datacardws=$(echo "$datacard" | sed 's|.txt|.root|g')
      if [ -f "$datacardws" ]; then
         echo "Datacard workspace already exists, continuing..."
      else
         echo "Datacard workspace does not exist, creating it..."
         # Create the datacard workspace
         text2workspace.py "$datacard" --channel-masks
      fi
      echo $datacardws
      for mode in "_result_bonly_CRonly"
      do
         for algorithm in "saturated" #"KS" "AD"
         do
            combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode} --setParameters ${maskParams}

            combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParameters ${maskParams} -t 200 --toysFrequentist -s 45239816 &
            combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParameters ${maskParams} -t 200 --toysFrequentist -s 76451209 &
            combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParameters ${maskParams} -t 200 --toysFrequentist -s 23987145 &
            combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParameters ${maskParams} -t 200 --toysFrequentist -s 65123847 &
            combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParameters ${maskParams} -t 200 --toysFrequentist -s 94761325 &
            combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParameters ${maskParams} -t 200 --toysFrequentist -s 32895761 &
            combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParameters ${maskParams} -t 200 --toysFrequentist -s 57239814 &
            combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParameters ${maskParams} -t 200 --toysFrequentist -s 12657398 &
            combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParameters ${maskParams} -t 200 --toysFrequentist -s 48912673 &
            combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParameters ${maskParams} -t 200 --toysFrequentist -s 73492816 &

            wait
            # ${mode}
            hadd higgsCombine${mode}_toy.GoodnessOfFit.mH120.Merged.root higgsCombine${mode}_toy.GoodnessOfFit.mH120.*.root

            ## plotting
            combineTool.py -M CollectGoodnessOfFit --input higgsCombine${mode}.GoodnessOfFit.mH120.root higgsCombine${mode}_toy.GoodnessOfFit.mH120.Merged.root -m 120.0 -o gof${mode}_${catg}_${year}.json
            plotGof.py gof${mode}_${catg}_${year}.json --statistic ${algorithm} --mass 120.0 -o gof${mode}_${catg}_${year} --title-right="B-only hypothesis("${catg}" "${year}")"

            for f in *gof${mode}_${catg}_${year}*; do mv -v -f -- "$f" ./gofplots_${algorithm} ; done

            rm -rf higgsCombine${mode}*.GoodnessOfFit.*.root
         done
      done
   done
done
