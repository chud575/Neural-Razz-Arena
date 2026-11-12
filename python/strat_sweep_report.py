import sys
import pandas as pd, numpy as np
t=pd.read_csv("results/strat_sweep_trades.csv")
pd.set_option("display.width",250); pd.set_option("display.max_rows",400)
def io(g):
    a,b=g[g.period=="IS"],g[g.period=="OOS"]
    return pd.Series(dict(nIS=len(a), IS=a.r.mean(), nOOS=len(b), OOS=b.r.mean(), grossAll=g.gross.mean(), win=g.win.mean()*100, risk=g.risk_pct.median(), rr=g.rr.median()))
for tf in ("1h","4h"):
    for mode,window in (("close",1),("stop",1)):
        x=t[(t.tf==tf)&(t.window==window)&(t["mode"]==mode)&(t.typ!="3")]
        for mv in (0.5,1.0,2.0,3.0):
            y=x[x.move>=mv]
            print(f"\n== {tf} {mode} 2d/2u move>={mv}%")
            print(y.groupby("target").apply(io).round(3).to_string())
x=t[(t.tf=="1h")&(t.window==1)&(t["mode"]=="close")&(t.typ!="3")&(t.move>=1.0)&(t.target=="high")]
print("\n1h close >=1% target high"); 
for k in ("coin","d","wicks"): print(x.groupby(k).apply(io).round(3))
print("window2:", io(t[(t.tf=="1h")&(t.window==2)&(t["mode"]=="close")&(t.typ!="3")&(t.move>=1.0)&(t.target=="high")]).round(3).to_dict())
print("type 3:", io(t[(t.tf=="1h")&(t.window==1)&(t["mode"]=="close")&(t.typ=="3")&(t.move>=1.0)&(t.target=="high")]).round(3).to_dict())
