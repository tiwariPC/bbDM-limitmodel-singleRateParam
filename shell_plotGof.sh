for algorithm in "saturated"
do
   for year in "2017" #"run2" #"2016" "2017" "2018"
   do
      for catg in "2b" #"2b" "1b"
      do
         for mode in "_result_bonly_CRonly"
         do
            python plotGof.py gofplots_${algorithm}/gof${mode}_${catg}_${year}.json --statistic ${algorithm} --mass 120.0 -o gofplots_${algorithm}/gof${mode}_${catg}_${year} --title-right="B-only hypothesis("${catg}" "${year}")" --range 0 0.006

            # for f in *gof${mode}_${catg}_${year}*; do mv -v -f -- "$f" ./gofplots_${algorithm} ; done

            # rm -rf higgsCombine${mode}*.root
         done
      done
   done
done