# root -l -b -q PlotPulls.C\(\"fitDiagnosticsDir/pulls_C_run2_asimov_t0_pullsNimpactsrun2.root\",\"pullsANDimpacts/pullsNimpactsrun2/\",\"_C_run2_asimov_t0_pullsNimpactsrun2\"\)

# root -l -b -q plotPostNuisance_combine.C\(\"fitDiagnosticsDir/fitDiagnostics_C_run2_fit_CRonly_result_pullsNimpactsrun2.root\",\"pullsANDimpacts/pullsNimpactsrun2/\",\"C_run2_fit_CRonly_result_pullsNimpactsrun2\"\)




for year in "run2" #"2016" "2017" "2018"
do
  dirname="pullsNimpacts"${year}
  for catg in "C" #"2b" "1b"
  do
    mode="fit_CRonly_result"
    root -l -b -q plotPostNuisance_combine.C\(\"fitDiagnosticsDir/fitDiagnostics_${catg}_${year}_${mode}_${dirname}.root\",\"pullsANDimpacts/${dirname}/\",\"${catg}_${year}_${mode}_${dirname}\"\)
    mode="asimov_t0"
    root -l -b -q PlotPulls.C\(\"fitDiagnosticsDir/pulls_${catg}_${year}_${mode}_${dirname}.root\",\"pullsANDimpacts/${dirname}/\",\"_${catg}_${year}_${mode}_${dirname}\"\)
  done
done