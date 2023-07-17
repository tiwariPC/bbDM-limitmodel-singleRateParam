from pandas import DataFrame
import pandas as pd
xs = pd.read_csv("cross_section/mA_vs_ma_scan_tanb_35_sint_0p7_fixed.csv",delimiter=",")#, names=["mA", "ma", "mA", "mA", "xsec"])
ma = xs.ma.unique().tolist()
massA = xs.mA.unique().tolist()
xs["xsec"] = xs.xsec


#xs[(xs.mA==1200) & (xs.mA==0.7) & (xs.mA==35)]

# limits = pd.read_csv("bin/limits_bbDM_combined_2017.txt",delimiter=" ", names=["mA","ma","expm2", "expm1", "exp", "expp1", "expp2", "obs"])
limits = pd.read_csv("bin/Apr23_run2_C/limits_bbDM_C_run2.txt",delimiter=" ", names=["mA","ma","expm2", "expm1", "exp", "expp1", "expp2", "obs"])
limits["sintheta"] = 0.7

xs_skim1200 = xs[xs.mA==600]
xs1200=xs_skim1200.set_index(["sintheta","ma"])

def getlimitdf(A=1200):
    xs_skim_0p3 = xs[xs.mA==A]
    xs_0p3=xs_skim_0p3.set_index(["sintheta","ma"])
    merged = xs1200.merge(xs_0p3,left_index=True, right_index=True, how='outer')

    limits_0p3 = limits
    limits_0p3["mA"] = A
    limits_0p3["sintheta"] = 0.7
    limits_0p3 = limits_0p3.set_index(["sintheta","ma"])
    final=merged.merge(limits_0p3, left_index=True, right_index=True, how='outer')
    final_ = final[:-2]
    for ivar in ["expm2","expm1","exp","expp1","expp2","obs"]:
        final_[ivar] = final_[ivar] * final_.xsec_x / final_.xsec_y

    final_ = final_.drop(labels=["mA_x" , "tanbeta_x",    "xsec_x",  "mA_y",  "tanbeta_y", "xsec_y"], axis=1)
    final_ = final_.reset_index()
    final_= final_.drop(labels=["sintheta"], axis=1)
    print(final_)
    final_ = final_.set_index(["ma","mA"])
    return final_



#df1200 = getlimitdf(35)
#print (df1200)
dfs=[]

for iA in massA:
    df_tmp = getlimitdf(iA)
    dfs.append(df_tmp)

df = pd.concat(dfs)

#df_0p3 = getlimitdf(30)
#print (df_0p3)
#df= pd.concat([df1200, df_0p3])

print (df[:5])

df.to_csv("limits_mA_vs_ma_scan.txt",sep=" ")
