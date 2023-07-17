from pandas import DataFrame
import pandas as pd
xs = pd.read_csv("cross_section/mchi_vs_ma_scan_mA_600_fixed.csv",delimiter=",")#, names=["mA", "ma", "mchi", "mchi", "xsec"])
ma = xs.ma.unique().tolist()
mchi = xs.mchi.unique().tolist()
xs["xsec"] = xs.xsec

limits = pd.read_csv("bin/Apr23_run2_C/limits_bbDM_C_run2.txt",delimiter=" ", names=["mA","ma","expm2", "expm1", "exp", "expp1", "expp2", "obs"])
limits["mchi"] = 1
xs_skim_1 = xs[xs.mchi==1]
xs_1=xs_skim_1.set_index(["mA","ma"])

def getlimitdf(chi=0.1):
    xs_skim_0p1 = xs[xs.mchi==chi]
    xs_0p1=xs_skim_0p1.set_index(["mA","ma"])
    merged = xs_1.merge(xs_0p1,left_index=True, right_index=True, how='outer')
    print(merged)
    limits_0p1 = limits
    limits_0p1["mchi"] = chi
    limits_0p1["mA"] = 600
    limits_0p1 = limits_0p1.set_index(["mA","ma"])
    final=merged.merge(limits_0p1, left_index=True, right_index=True, how='outer')

    for ivar in ["expm2","expm1","exp","expp1","expp2","obs"]:
        final[ivar] = final[ivar] * final.xsec_x / final.xsec_y

    final = final.drop(labels=["sintheta_x" , "tanbeta_x",    "xsec_x",  "sintheta_y",  "tanbeta_y", "xsec_y", "mchi_x", "mchi_y"], axis=1)
    final = final.reset_index()
    final= final.drop(labels=["mA"], axis=1)
    final = final.set_index(["ma","mchi"])
    return final

dfs=[]

for imchi in mchi:
    df_tmp = getlimitdf(imchi)
    dfs.append(df_tmp)

df = pd.concat(dfs)

print (df[:5])
df.to_csv("limits_mchi_vs_ma_scan.txt",sep=" ")