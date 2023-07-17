dirname=$1
datacard=$2
year=$3
catg=$4
masks_reg="mask_sr_bin1=1,mask_sr_bin2=1,mask_sr_bin3=1,mask_sr_bin4=1,mask_cat_1b_sr_bin1=1,mask_cat_1b_sr_bin2=1,mask_cat_1b_sr_bin3=1,mask_cat_1b_sr_bin4=1,mask_cat_2b_sr_bin1=1,mask_cat_2b_sr_bin2=1,mask_cat_2b_sr_bin3=1,mask_cat_2b_sr_bin4=1,mask_d2016_cat_1b_sr_bin1=1,mask_d2016_cat_1b_sr_bin2=1,mask_d2016_cat_1b_sr_bin3=1,mask_d2016_cat_1b_sr_bin4=1,mask_d2016_cat_2b_sr_bin1=1,mask_d2016_cat_2b_sr_bin2=1,mask_d2016_cat_2b_sr_bin3=1,mask_d2016_cat_2b_sr_bin4=1,mask_d2017_cat_1b_sr_bin1=1,mask_d2017_cat_1b_sr_bin2=1,mask_d2017_cat_1b_sr_bin3=1,mask_d2017_cat_1b_sr_bin4=1,mask_d2017_cat_2b_sr_bin1=1,mask_d2017_cat_2b_sr_bin2=1,mask_d2017_cat_2b_sr_bin3=1,mask_d2017_cat_2b_sr_bin4=1,mask_d2018_cat_1b_sr_bin1=1,mask_d2018_cat_1b_sr_bin2=1,mask_d2018_cat_1b_sr_bin3=1,mask_d2018_cat_1b_sr_bin4=1,mask_d2018_cat_2b_sr_bin1=1,mask_d2018_cat_2b_sr_bin2=1,mask_d2018_cat_2b_sr_bin3=1,mask_d2018_cat_2b_sr_bin4=1"

echo ${dirname} ${datacard} ${year} ${catg}

datacardws=$(echo "$datacard" | sed 's|.txt|.root|g')
if [ -f "$datacardws" ]; then
    echo "Datacard workspace already exists, continuing..."
else
    echo "Datacard workspace does not exist, creating it..."
    # Create the datacard workspace
    text2workspace.py "$datacard" --channel-masks
fi

# Print the name of the datacard workspace
echo "Datacard workspace name: $datacardws"


mkdir -p "pullsANDimpacts/"${dirname}

# <<comment
## CR only fit pulls
mode=fit_CRonly_result
# combine -M FitDiagnostics -d $datacardws -n _${catg}_${year}_${mode}_${dirname}  --saveShapes --saveWithUncertainties --setParameters ${masks_reg} --X-rtd MINIMIZER_analytic --cminFallbackAlgo Minuit2,0:1.0  --cminDefaultMinimizerStrategy 0 --out fitDiagnosticsDir

root -l -b -q plotPostNuisance_combine.C\(\"fitDiagnosticsDir/fitDiagnostics_${catg}_${year}_${mode}_${dirname}.root\",\"pullsANDimpacts/${dirname}/\",\"${catg}_${year}_${mode}_${dirname}\"\)

rm -rf higgsCombine_${catg}_${year}_${mode}_${dirname}.FitDiagnostics*
# comment

<<comment
## asimov b-only
mode=asimov_t0
combine -M FitDiagnostics  $datacardws --saveShapes --saveWithUncertainties -t -1 --expectSignal 0 -n _${catg}_${year}_${mode}_${dirname} --cminDefaultMinimizerStrategy 0 --out fitDiagnosticsDir
python diffNuisances.py fitDiagnosticsDir/fitDiagnostics_${catg}_${year}_${mode}_${dirname}.root --abs --all -g fitDiagnosticsDir/pulls_${catg}_${year}_${mode}_${dirname}.root
root -l -b -q PlotPulls.C\(\"fitDiagnosticsDir/pulls_${catg}_${year}_${mode}_${dirname}.root\",\"pullsANDimpacts/${dirname}/\",\"_${catg}_${year}_${mode}_${dirname}\"\)

rm -rf higgsCombine_${catg}_${year}_${mode}_${dirname}.FitDiagnostics*
comment
