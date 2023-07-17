from pandas import DataFrame
import pandas as pd
xs = pd.read_csv("cross_section/sintheta_vs_ma_scan_mA_600_fixed.csv",delimiter=",")#, names=["mA", "ma", "sintheta", "sintheta", "xsec"])
ma = xs.ma.unique().tolist()
st = xs.sintheta.unique().tolist()
xs["xsec"] = xs.xsec


#xs[(xs.mA==1200) & (xs.sintheta==0.7) & (xs.sintheta==35)]

# limits = pd.read_csv("bin/limits_bbDM_combined_2017.txt",delimiter=" ", names=["mA","ma","expm2", "expm1", "exp", "expp1", "expp2", "obs"])
limits = pd.read_csv("bin/Apr23_run2_C/limits_bbDM_C_run2.txt",delimiter=" ", names=["mA","ma","expm2", "expm1", "exp", "expp1", "expp2", "obs"])
limits["sintheta"] = 0.7


xs_skim_0p7 = xs[xs.sintheta==0.7]
xs_0p7=xs_skim_0p7.set_index(["mA","ma"])

def getlimitdf(sint=0.3):
    xs_skim_0p3 = xs[xs.sintheta==sint]
    xs_0p3=xs_skim_0p3.set_index(["mA","ma"])
    merged = xs_0p7.merge(xs_0p3,left_index=True, right_index=True, how='outer')

    limits_0p3 = limits
    limits_0p3["sintheta"] = sint
    limits_0p3["mA"] = 600
    limits_0p3 = limits_0p3.set_index(["mA","ma"])

    final=merged.merge(limits_0p3, left_index=True, right_index=True, how='outer')

    for ivar in ["expm2","expm1","exp","expp1","expp2","obs"]:
        final[ivar] = final[ivar] * final.xsec_x / final.xsec_y

    final = final.drop(labels=["sintheta_x" , "tanbeta_x",    "xsec_x",  "sintheta_y",  "tanbeta_y", "xsec_y"], axis=1)
    final = final.reset_index()
    final= final.drop(labels=["mA"], axis=1)
    final = final.set_index(["ma","sintheta"])
    return final



#df_0p7 = getlimitdf(35)
#print (df_0p7)
dfs=[]

for isint in st:
    df_tmp = getlimitdf(isint)
    dfs.append(df_tmp)

df = pd.concat(dfs)

#df_0p3 = getlimitdf(30)
#print (df_0p3)
#df= pd.concat([df_0p7, df_0p3])

print (df[:5])

df.to_csv("limits_sint_vs_ma_scan.txt",sep=" ")
