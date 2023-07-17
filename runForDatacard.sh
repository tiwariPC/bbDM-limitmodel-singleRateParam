
pythonFile="prepareCards.py"
# pythonFile="prepareCards_perbin.py"
# pythonFile="prepareCards_perbin_channel.py"
for year in "16" "17" "18"
do
   rootfile="allmethistos/AllMETHistos_v${year}_12-02-02.root"
   python ${pythonFile} -y 20${year} -c 1b -reg SR WE WMU ZEE ZMUMU -f $rootfile
   python ${pythonFile} -y 20${year} -c 2b -reg SR TOPE TOPMU ZEE ZMUMU -f $rootfile
   python mergeCategoryDatacards.py -O datacards/datacard_bbDM20${year}_1b -T datacards/datacard_bbDM20${year}_2b -D datacards/datacard_bbDM20${year}_C
done

# python mergeCategoryDatacards.py -R datacards_bbDM_2017_R -B datacards_bbDM_2017_B -D combined_datacards_2017
# python runLimit_v3.py -runlimit -cards datacards_bbDM_2017_R -tag Sep21_R_2017 -scan 1d -par mA -fixpar "[ma=150,tb=1p0,st=0p35]" -model THDMa
# python runLimit_v3.py -runlimit -cards datacards_bbDM_2017_B -tag Sep21_B_2017 -scan 1d -par mA -fixpar "[ma=150,tb=1p0,st=0p35]" -model THDMa
# python runLimit_v3.py -runlimit -cards combined_datacards_2017 -tag Sep21_C_2017 -scan 1d -par mA -fixpar "[ma=150,tb=1p0,st=0p35]" -model THDMa

#python runLimit_v3.py -runlimit -cards datacards_bbDM_2017_R -tag Sep21_R_2017_unblind -scan 1d -par mA -fixpar "[ma=150,tb=1p0,st=0p35]" -model THDMa


#rootfile="AllMETHistos_hMETDphiTest0p5_2018.root"
#rootfile="AllMETHistos_2018_bbDM_v12_09_22_mjj100To150_DataOnSR_withVVVmetHemOnSR.root"
#rootfile="AllMETHistos_2018_bbDM_v12_09_21_NoJER_reNormScale_fixedBinBug.root"
#python prepareCards.py -y 2018 -c B -reg SR TOPE TOPMU ZEE ZMUMU -f $rootfile
#python prepareCards.py -y 2018 -c R -reg SR TOPE TOPMU ZEE ZMUMU -f $rootfile
#python mergeCategoryDatacards.py -R datacards_bbDM_2018_R -B datacards_bbDM_2018_B -D combined_datacards_2018
#python runLimit_v3.py -runlimit -cards datacards_bbDM_2018_R -tag Sep22_R_2018_hMETDphiTest0p5 -scan 1d -par mA -fixpar "[ma=150,tb=1p0,st=0p35]" -model THDMa
#python runLimit_v3.py -runlimit -cards datacards_bbDM_2018_B -tag Sep22_B_2018_hMETDphiTest0p5 -scan 1d -par mA -fixpar "[ma=150,tb=1p0,st=0p35]" -model THDMa
#python runLimit_v3.py -runlimit -cards combined_datacards_2018 -tag Sep22_C_2018_hMETDphiTest0p5 -scan 1d -par mA -fixpar "[ma=150,tb=1p0,st=0p35]" -model THDMa

#rootfile="AllMETHistos_run3.root"
#python prepareCards.py -y 2018 -c B -reg SR TOPE TOPMU ZEE ZMUMU -f $rootfile
#python prepareCards.py -y 2018 -c R -reg SR TOPE TOPMU ZEE ZMUMU -f $rootfile

#python mergeCategoryDatacards.py -R run3_datacards_bbDM_2018_R -B run3_datacards_bbDM_2018_B -D run3_combined_datacards
#python runLimit_v3.py -runlimit -cards run3_combined_datacards -tag test_C_run3 -scan 1d -par mA -fixpar "[ma=150,tb=1p0,st=0p35]" -model THDMa

#rootfile="AllMETHistos_HLLHC.root"
#python prepareCards.py -y 2018 -c B -reg SR TOPE TOPMU ZEE ZMUMU -f $rootfile
#python prepareCards.py -y 2018 -c R -reg SR TOPE TOPMU ZEE ZMUMU -f $rootfile
#python mergeCategoryDatacards.py -R HLLHC_datacards_bbDM_2018_R -B HLLHC_datacards_bbDM_2018_B -D HLLHC_combined_datacards
#python runLimit_v3.py -runlimit -cards HLLHC_combined_datacards -tag test_C_HLLHC -scan 1d -par mA -fixpar "[ma=150,tb=1p0,st=0p35]" -model THDMa
