dirname=$1
datacard=$2
year=$3
catg=$4

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


## Impacts
# << comment
mode="asimov_t0" ## asimov
combineTool.py -M Impacts -d $datacardws --doInitialFit --robustFit 1 -m 125 -t -1 --expectSignal 0 --rMin -10
wait
combineTool.py -M Impacts -d $datacardws --doFits  --robustFit 1 -m 125 --parallel 32 -t -1 --expectSignal 0 --rMin -10
wait
combineTool.py -M Impacts -d $datacardws -m 125 -o pullsANDimpacts/${dirname}/impacts_${catg}_${mode}.json
wait
plotImpacts.py -i  pullsANDimpacts/${dirname}/impacts_${catg}_${mode}.json -o pullsANDimpacts/${dirname}/impacts_${catg}_${mode}_${dirname}
rm -rf higgsCombine_initialFit_Test.MultiDimFit.mH125.root  higgsCombine_paramFit_Test_*.MultiDimFit.mH125.root
# comment

# << comment
mode="asimov_t1" ## asimov signal injected
combineTool.py -M Impacts -d $datacardws --doInitialFit --robustFit 1 -m 125 -t -1 --expectSignal 1 --rMin -10
wait
combineTool.py -M Impacts -d $datacardws --doFits  --robustFit 1 -m 125 --parallel 32 -t -1 --expectSignal 1 --rMin -10
wait
combineTool.py -M Impacts -d $datacardws -m 125 -o pullsANDimpacts/${dirname}/impacts_${catg}_${mode}.json
wait
plotImpacts.py -i  pullsANDimpacts/${dirname}/impacts_${catg}_${mode}.json -o pullsANDimpacts/${dirname}/impacts_${catg}_${mode}_${dirname}
rm -rf higgsCombine_initialFit_Test.MultiDimFit.mH125.root  higgsCombine_paramFit_Test_*.MultiDimFit.mH125.root
# comment