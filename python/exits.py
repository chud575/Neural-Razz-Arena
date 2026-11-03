"""
Shared TP1 / TP2 scale-out exit logic (mirrors stepEntry() in the Pine scripts).

An entry dict holds: e (entry price), risk (risk unit for R), stop (moves to breakeven after TP1 if enabled),
tp1, tp2, done1 (TP1 taken), r and pct (running totals for the whole entry).

Rules (conservative, same as everywhere else):
  * the stop is checked first on every bar;
  * on a limit-fill bar only the stop is checked (stop_only=True);
  * after TP1 fills, the remainder is managed from the next bar;
  * gaps through a level fill at the open.
p1 = fraction closed at TP1 (0 = single target at TP2, 1 = everything at TP1).
"""
from __future__ import annotations


def make_entry(e: float, risk: float, stop: float, tp1: float, tp2: float, d: int, p1: float) -> dict:
    if (tp1 - tp2) * d > 0:          # TP1 never beyond TP2
        tp1 = tp2
    return dict(e=e, risk=risk, stop=stop, tp1=tp1, tp2=tp2, done1=p1 <= 0, r=0.0, pct=0.0)


def scale_step(o, h, l, i: int, d: int, en: dict, p1: float, be: bool, stop_only: bool = False):
    """Advance one entry one bar. Returns (closed, exit_px, reason, tp1_fill_px)."""
    rem = 1.0 if (p1 <= 0 or not en["done1"]) else 1.0 - p1
    x_px, reason, t1_px = None, "", None
    if (l[i] <= en["stop"]) if d == 1 else (h[i] >= en["stop"]):
        x_px = min(o[i], en["stop"]) if d == 1 else max(o[i], en["stop"])
        reason = "BE" if (en["done1"] and be and p1 > 0) else "SL"
    elif not stop_only:
        if not en["done1"] and ((h[i] >= en["tp1"]) if d == 1 else (l[i] <= en["tp1"])):
            t1_px = max(o[i], en["tp1"]) if d == 1 else min(o[i], en["tp1"])
            en["r"] += p1 * d * (t1_px - en["e"]) / en["risk"] if en["risk"] > 0 else 0.0
            en["pct"] += p1 * d * (t1_px - en["e"]) / en["e"] * 100
            en["done1"] = True
            if p1 >= 1:
                return True, t1_px, "TP1", t1_px
            if be:
                en["stop"] = en["e"]
        elif en["done1"] and ((h[i] >= en["tp2"]) if d == 1 else (l[i] <= en["tp2"])):
            x_px = max(o[i], en["tp2"]) if d == 1 else min(o[i], en["tp2"])
            reason = "TP"
    if x_px is None:
        return False, None, "", t1_px
    en["r"] += rem * d * (x_px - en["e"]) / en["risk"] if en["risk"] > 0 else 0.0
    en["pct"] += rem * d * (x_px - en["e"]) / en["e"] * 100
    return True, x_px, reason, t1_px
