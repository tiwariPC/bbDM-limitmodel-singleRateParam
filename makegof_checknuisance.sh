
freeznuisance="CMS2016_EleID,CMS2016_EleRECO,CMS2016_MuID,CMS2016_MuISO,CMS2016_PU,CMS2016_eff_b,CMS2016_fake_b,CMS2016_mu_scale_diboson,CMS2016_mu_scale_dyjets,CMS2016_mu_scale_singlet,CMS2016_mu_scale_smh,CMS2016_mu_scale_tt,CMS2016_mu_scale_wjets,CMS2016_pdf,CMS2016_prefire,CMS2016_trig_ele,CMS2016_trig_met,CMS2016_veto_tau,CMS2017_EleID,CMS2017_EleRECO,CMS2017_MuID,CMS2017_MuISO,CMS2017_PU,CMS2017_eff_b,CMS2017_fake_b,CMS2017_mu_scale_diboson,CMS2017_mu_scale_dyjets,CMS2017_mu_scale_singlet,CMS2017_mu_scale_smh,CMS2017_mu_scale_tt,CMS2017_mu_scale_wjets,CMS2017_pdf,CMS2017_prefire,CMS2017_trig_ele,CMS2017_trig_met,CMS2017_veto_tau,CMS2018_EleID,CMS2018_EleRECO,CMS2018_MuID,CMS2018_MuISO,CMS2018_PU,CMS2018_eff_b,CMS2018_fake_b,CMS2018_mu_scale_diboson,CMS2018_mu_scale_dyjets,CMS2018_mu_scale_singlet,CMS2018_mu_scale_smh,CMS2018_mu_scale_tt,CMS2018_mu_scale_wjets,CMS2018_pdf,CMS2018_prefire,CMS2018_trig_ele,CMS2018_trig_met,CMS2018_veto_tau,JECAbsolute,JECAbsolute_2016,JECAbsolute_2017,JECAbsolute_2018,JECBBEC1,JECBBEC1_2016,JECBBEC1_2017,JECBBEC1_2018,JECEC2,JECEC2_2016,JECEC2_2017,JECEC2_2018,JECFlavorQCD,JECHF,JECHF_2016,JECHF_2017,JECHF_2018,JECRelativeBal,JECRelativeSample_2016,JECRelativeSample_2017,JECRelativeSample_2018,lumi_2016,lumi_2017,lumi_2018,lumi_BeamBE,lumi_BeamCC,lumi_GhostS,lumi_LengthS,lumi_X_Y_Fact,norm_diboson,norm_dyjets,norm_smh,norm_stop"

maskParams="mask_sr=1,mask_cat_1b_sr=1,mask_cat_2b_sr=1,mask_d2016_cat_1b_sr=1,mask_d2016_cat_2b_sr=1,mask_d2017_cat_1b_sr=1,mask_d2017_cat_2b_sr=1,mask_d2018_cat_1b_sr=1,mask_d2018_cat_2b_sr=1"
unmaskParams="mask_sr=0,mask_cat_1b_sr=0,mask_cat_2b_sr=0,mask_d2016_cat_1b_sr=0,mask_d2016_cat_2b_sr=0,mask_d2017_cat_1b_sr=0,mask_d2017_cat_2b_sr=0,mask_d2018_cat_1b_sr=0,mask_d2018_cat_2b_sr=0"

for algorithm in "saturated" "KS" "AD"
do
   for year in "2016" "2017" "2018" "run2"
   do
      for catg in "C" #"1b" "2b"
      do
         for mode in "_result_bonly_CRonly"
         do
            datacard=datacards/datacard_bbDM"${year}"_"${catg}"/bbDM_datacard_"${year}"_THDMa_${catg}_allregion_2HDMa_Ma150_MChi1_MA600_tb35_st_0p7.txt

            text2workspace.py $datacard --channel-masks
            datacardws=`echo $datacard | sed  's|.txt|.root|g'`

            echo $datacardws

            combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode} --setParametersForFit ${maskParams} --setParametersForEval ${unmaskParams} --freezeParameters r,${freeznuisance} --setParameters r=0

            combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParametersForFit ${maskParams} --setParametersForEval ${unmaskParams} --freezeParameters r,${freeznuisance} --setParameters r=0,${maskParams} -t 100 --toysFrequentist -s 12431 &
            # combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParametersForFit ${maskParams} --setParametersForEval ${unmaskParams} --freezeParameters r,${freeznuisance} --setParameters r=0,${maskParams} -t 100 --toysFrequentist -s 12432 &
            # combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParametersForFit ${maskParams} --setParametersForEval ${unmaskParams} --freezeParameters r,${freeznuisance} --setParameters r=0,${maskParams} -t 100 --toysFrequentist -s 12433 &
            # combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParametersForFit ${maskParams} --setParametersForEval ${unmaskParams} --freezeParameters r,${freeznuisance} --setParameters r=0,${maskParams} -t 100 --toysFrequentist -s 12434 &
            # combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParametersForFit ${maskParams} --setParametersForEval ${unmaskParams} --freezeParameters r,${freeznuisance} --setParameters r=0,${maskParams} -t 100 --toysFrequentist -s 12435 &
            # combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParametersForFit ${maskParams} --setParametersForEval ${unmaskParams} --freezeParameters r,${freeznuisance} --setParameters r=0,${maskParams} -t 100 --toysFrequentist -s 12436 &
            # combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParametersForFit ${maskParams} --setParametersForEval ${unmaskParams} --freezeParameters r,${freeznuisance} --setParameters r=0,${maskParams} -t 100 --toysFrequentist -s 12437 &
            # combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParametersForFit ${maskParams} --setParametersForEval ${unmaskParams} --freezeParameters r,${freeznuisance} --setParameters r=0,${maskParams} -t 100 --toysFrequentist -s 12438 &
            # combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParametersForFit ${maskParams} --setParametersForEval ${unmaskParams} --freezeParameters r,${freeznuisance} --setParameters r=0,${maskParams} -t 100 --toysFrequentist -s 12439 &
            # combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParametersForFit ${maskParams} --setParametersForEval ${unmaskParams} --freezeParameters r,${freeznuisance} --setParameters r=0,${maskParams} -t 100 --toysFrequentist -s 12430 &
            # combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParametersForFit ${maskParams} --setParametersForEval ${unmaskParams} --freezeParameters r,${freeznuisance} --setParameters r=0,${maskParams} -t 100 --toysFrequentist -s 124311 &
            # combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParametersForFit ${maskParams} --setParametersForEval ${unmaskParams} --freezeParameters r,${freeznuisance} --setParameters r=0,${maskParams} -t 100 --toysFrequentist -s 124312 &
            # combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParametersForFit ${maskParams} --setParametersForEval ${unmaskParams} --freezeParameters r,${freeznuisance} --setParameters r=0,${maskParams} -t 100 --toysFrequentist -s 124313 &
            # combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParametersForFit ${maskParams} --setParametersForEval ${unmaskParams} --freezeParameters r,${freeznuisance} --setParameters r=0,${maskParams} -t 100 --toysFrequentist -s 124314 &
            # combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParametersForFit ${maskParams} --setParametersForEval ${unmaskParams} --freezeParameters r,${freeznuisance} --setParameters r=0,${maskParams} -t 100 --toysFrequentist -s 124315 &
            # combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParametersForFit ${maskParams} --setParametersForEval ${unmaskParams} --freezeParameters r,${freeznuisance} --setParameters r=0,${maskParams} -t 100 --toysFrequentist -s 124316 &
            # combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParametersForFit ${maskParams} --setParametersForEval ${unmaskParams} --freezeParameters r,${freeznuisance} --setParameters r=0,${maskParams} -t 100 --toysFrequentist -s 124317 &
            # combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParametersForFit ${maskParams} --setParametersForEval ${unmaskParams} --freezeParameters r,${freeznuisance} --setParameters r=0,${maskParams} -t 100 --toysFrequentist -s 124318 &
            # combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParametersForFit ${maskParams} --setParametersForEval ${unmaskParams} --freezeParameters r,${freeznuisance} --setParameters r=0,${maskParams} -t 100 --toysFrequentist -s 124319 &
            # combine -M GoodnessOfFit -d $datacardws --algo=${algorithm} -n ${mode}_toy --setParametersForFit ${maskParams} --setParametersForEval ${unmaskParams} --freezeParameters r,${freeznuisance} --setParameters r=0,${maskParams} -t 100 --toysFrequentist -s 124320 &

            wait
            # ${mode}
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