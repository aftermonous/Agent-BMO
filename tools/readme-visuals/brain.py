from common import *

W, H = 880, 580
CW, CH = 220, 100

CHIPS = {
    "OBS":   (40, 80,  "U01", "MARKET OBSERVER", ["prices. volume. liquidity", "emits normalized snapshots"], "PLANNED", PH_MID),
    "STRAT": (330, 80, "U02", "STRATEGY ENGINE", ["rules that score candidates", "pluggable. versioned"], "PLANNED", PH_MID),
    "DEC":   (620, 80, "U03", "DECISION ENGINE", ["enter. exit. or pass", "each call logs its reason"], "PLANNED", PH_MID),
    "MEM":   (40, 240, "U04", "MEMORY", ["append-only state and history", "reconciled against chain"], "PLANNED", PH_MID),
    "RISK":  (330, 240, "U05", "RISK ENGINE", ["limits. simulation. checks", "can veto any action"], "PLANNED", AMBER),
    "KILL":  (620, 240, "U06", "EMERGENCY STOP", ["halts all new execution", "operator controlled"], "PLANNED", RED),
    "POS":   (40, 400, "U07", "POSITION MANAGER", ["size. entry. targets. stops", "triggers exits"], "PLANNED", PH_MID),
    "EXEC":  (330, 400, "U08", "EXECUTION ENGINE", ["build. simulate. sign. send", "confirms or retries"], "PLANNED", PH_MID),
    "WAL":   (620, 400, "U09", "WALLET", [WALLET_SHORT, "sole signing identity"], "LIVE", TEAL),
}

def chip(key):
    x, y, uid, name, lines, status, col = CHIPS[key]
    s = ""
    # pins
    for k in range(8):
        px = x + 20 + k * 25
        s += f'<rect x="{px}" y="{y-6}" width="8" height="6" fill="{PH_FAINT}"/>'
        s += f'<rect x="{px}" y="{y+CH}" width="8" height="6" fill="{PH_FAINT}"/>'
    s += f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" fill="{PANEL}" stroke="{col}" stroke-width="1.5"/>'
    s += f'<circle cx="{x+12}" cy="{y+12}" r="3" fill="none" stroke="{PH_DIM}"/>'
    s += txt(x + 22, y + 16, uid, 9.5, PH_DIM, ls=2)
    # status tag
    if status == "LIVE":
        s += f'<rect x="{x+CW-58}" y="{y+6}" width="50" height="15" fill="{TEAL}"/>'
        s += txt(x + CW - 33, y + 17, "LIVE", 9.5, BLACK, "middle", weight=700, ls=2)
    else:
        s += f'<rect x="{x+CW-72}" y="{y+6}" width="64" height="15" fill="none" stroke="{PH_DIM}"/>'
        s += txt(x + CW - 40, y + 17, status, 9.5, PH_DIM, "middle", ls=2)
    s += txt(x + 14, y + 46, name, 14, col if col != PH_MID else PH, weight=700, ls=2)
    for i, ln in enumerate(lines):
        s += txt(x + 14, y + 66 + i * 15, ln, 10.5, PH_MID)
    return s + "\n"

def build():
    s = open_svg(W, H, "Agent BMO module map",
                 "Nine conceptual modules. Market observer feeds strategy, strategy feeds decision, decision goes through "
                 "the risk engine, which can veto. Approved actions go to execution, which signs from the wallet. "
                 "Wallet state feeds the position manager, which sends exits and writes to memory. Memory informs strategy. "
                 "Only the wallet is live.",
                 css=f"""
.bus{{stroke-dasharray:4 6;animation:bus 1s linear infinite}}
@keyframes bus{{to{{stroke-dashoffset:-20}}}}
""")
    s += header(W, "AGENT BMO / MODULE MAP", "1 OF 9 LIVE")

    def c(key, side):
        x, y = CHIPS[key][0], CHIPS[key][1]
        return {"l": (x, y + CH / 2), "r": (x + CW, y + CH / 2), "t": (x + CW / 2, y), "b": (x + CW / 2, y + CH)}[side]

    cx = {k: CHIPS[k][0] + CW / 2 for k in CHIPS}
    edges = [
        (f"M{c('OBS','r')[0]},{c('OBS','r')[1]} H{c('STRAT','l')[0]-2}", PH_MID, "arr", "snapshots", None),
        (f"M{c('STRAT','r')[0]},{c('STRAT','r')[1]} H{c('DEC','l')[0]-2}", PH_MID, "arr", "scores", None),
        (f"M{cx['DEC']},186 V214 H{cx['RISK']+30} V{240-8}", PH_MID, "arr", "intent", (cx['DEC']-120, 208)),
        (f"M{c('KILL','l')[0]},{c('KILL','l')[1]} H{c('RISK','r')[0]+2}", RED, "arrR", "halt", None),
        (f"M{cx['RISK']},346 V{400-8}", AMBER, "arrA", "approved", (cx['RISK']+8, 374)),
        (f"M{c('RISK','l')[0]},{c('RISK','l')[1]} H{c('MEM','r')[0]+2}", RED, "arrR", "vetoes", None),
        (f"M{c('EXEC','r')[0]},{c('EXEC','r')[1]} H{c('WAL','l')[0]-2}", TEAL, "arr", "signed tx", None),
        (f"M{cx['WAL']},506 V532 H{cx['POS']} V{506+2}", PH_MID, "arr", "fills. balances", (cx['EXEC'], 548)),
        (f"M{c('POS','r')[0]},{c('POS','r')[1]} H{c('EXEC','l')[0]-2}", PH_MID, "arr", "exit orders", None),
        (f"M{cx['POS']},400 V{346+8}", PH_MID, "arr", "outcomes", (cx['POS']+8, 374)),
        (f"M{cx['MEM']},240 V202 H{cx['STRAT']-30} V{186+2}", PH_MID, "arr", "context", (cx['MEM']+40, 196)),
    ]
    for d, col, mk, lab, lp in edges:
        s += f'<path d="{d}" fill="none" stroke="{col}" stroke-opacity=".35" stroke-width="1.5" marker-end="url(#{mk})"/>'
        s += f'<path d="{d}" fill="none" stroke="{col}" stroke-width="1.5" class="bus"/>\n'
        if lp is None:
            # midpoint of horizontal segment
            parts = d.replace("M", "").split(" H")
            x0, y0 = map(float, parts[0].split(","))
            x1 = float(parts[1])
            lp = ((x0 + x1) / 2, y0 - 7)
            s += txt(lp[0], lp[1], lab, 9, col if col in (RED, AMBER, TEAL) else PH_DIM, "middle")
        else:
            s += txt(lp[0], lp[1], lab, 9, col if col in (RED, AMBER, TEAL) else PH_DIM,
                     "middle" if lab not in ("approved", "outcomes") else "start")

    for k in CHIPS:
        s += chip(k)

    # risk engine heartbeat
    x, y = CHIPS["RISK"][0], CHIPS["RISK"][1]
    s += f'<rect x="{x-5}" y="{y-5}" width="{CW+10}" height="{CH+10}" fill="none" stroke="{AMBER}" class="pulse" opacity=".4"/>\n'
    # wallet glow
    x, y = CHIPS["WAL"][0], CHIPS["WAL"][1]
    s += f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" fill="none" stroke="{TEAL}" stroke-width="2" filter="url(#glow)" class="pulse"/>\n'

    s += close_svg(W, H)
    return s
