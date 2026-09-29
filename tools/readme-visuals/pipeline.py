from common import *

W = 880
NODES = [
    ("MARKET", "solana dex pools. prices. volume. liquidity"),
    ("OBSERVE", "ingest feeds. normalize snapshots"),
    ("ANALYZE", "score candidates against strategy"),
    ("DECIDE", "enter. exit. or pass"),
    ("RISK CHECK", "hard limits. simulation. token checks"),
    ("EXECUTE", "build. sign. send. confirm"),
    ("BMO WALLET", WALLET_SHORT + "  sole signer"),
    ("POSITION MANAGEMENT", "size. entry. targets. stops"),
    ("EXIT", "target hit. stop hit. or timeout"),
    ("MEMORY / HISTORY", "append-only log. reconciled to chain"),
]
X0, NW, NH, GAP, Y0 = 250, 380, 50, 86, 78
CX = X0 + NW / 2
SINK_X, SINK_W = 36, 170
SINKS = {2: ("DISCARD", "no signal", PH_DIM), 3: ("PASS", "no action taken", PH_DIM),
         4: ("BLOCKED", "limit breach. logged", RED)}
LOOP_X = 812
T = 12.0
SPEED = 230.0

def ny(i):
    return Y0 + i * GAP

def build():
    H = ny(len(NODES) - 1) + NH + 70
    s = open_svg(W, H, "Agent BMO signal path",
                 "Intended control flow. Market data enters, is observed, analyzed, decided on and risk checked. "
                 "Most candidates are discarded, passed or blocked. Survivors execute from the BMO wallet, are managed, "
                 "exited and written to memory. The loop repeats.",
                 css=f"""
.flow{{stroke-dasharray:3 7;animation:flow 1.1s linear infinite}}
.flowup{{stroke-dasharray:3 7;animation:flow .9s linear infinite}}
@keyframes flow{{to{{stroke-dashoffset:-20}}}}
""")
    s += header(W, "AGENT BMO / SIGNAL PATH", "SPEC v0. INTENDED BEHAVIOR")

    # spine
    s += f'<line x1="{CX}" y1="{ny(0)+NH}" x2="{CX}" y2="{ny(len(NODES)-1)}" stroke="{PH_DIM}" stroke-width="2"/>\n'
    s += f'<line x1="{CX}" y1="{ny(0)+NH}" x2="{CX}" y2="{ny(len(NODES)-1)}" stroke="{PH}" stroke-width="2" class="flow" opacity=".6"/>\n'

    # repeat loop on right
    ly_bot = ny(9) + NH / 2
    ly_top = ny(1) + NH / 2
    s += (f'<path d="M{X0+NW},{ly_bot} H{LOOP_X} V{ly_top} H{X0+NW+4}" fill="none" stroke="{PH_DIM}" '
          f'stroke-width="2" marker-end="url(#arr)"/>\n')
    s += (f'<path d="M{X0+NW},{ly_bot} H{LOOP_X} V{ly_top} H{X0+NW+10}" fill="none" stroke="{PH}" '
          f'stroke-width="2" class="flowup" opacity=".5"/>\n')
    mid = (ly_bot + ly_top) / 2
    s += (f'<g transform="translate({LOOP_X+18},{mid}) rotate(-90)">'
          + txt(0, 0, "REPEAT. CONTINUOUSLY", 12, PH_MID, "middle", ls=5) + '</g>\n')

    # sinks
    for i, (lab, sub, col) in SINKS.items():
        y = ny(i)
        s += (f'<line x1="{X0}" y1="{y+NH/2}" x2="{SINK_X+SINK_W}" y2="{y+NH/2}" stroke="{col}" '
              f'stroke-width="1.5" stroke-dasharray="4 4" marker-end="url(#{"arrR" if col == RED else "arr"})"/>\n')
        s += (f'<rect id="sink{i}" x="{SINK_X}" y="{y+6}" width="{SINK_W}" height="{NH-12}" fill="{PANEL}" '
              f'stroke="{col}" stroke-width="1.5"/>\n')
        s += txt(SINK_X + 12, y + 24, lab, 12, col if col == RED else PH_MID, weight=700, ls=2)
        s += txt(SINK_X + 12, y + 38, sub, 10, PH_DIM)

    # nodes
    for i, (lab, sub) in enumerate(NODES):
        y = ny(i)
        stroke, fill, lc = PH_MID, PANEL, PH
        dash = ""
        if i == 0:
            stroke, dash = PH_DIM, ' stroke-dasharray="5 4"'
        if i == 4:
            stroke, lc = AMBER, AMBER
        if i == 6:
            stroke, lc = TEAL, TEAL
        s += (f'<rect x="{X0}" y="{y}" width="{NW}" height="{NH}" fill="{fill}" stroke="{stroke}" '
              f'stroke-width="1.5"{dash}/>\n')
        # corner ticks
        s += f'<path d="M{X0-4},{y+10} V{y-4} H{X0+10}" fill="none" stroke="{stroke}" opacity=".6"/>'
        s += f'<path d="M{X0+NW+4},{y+NH-10} V{y+NH+4} H{X0+NW-10}" fill="none" stroke="{stroke}" opacity=".6"/>\n'
        s += txt(X0 - 12, y + 30, f"S{i}", 10, PH_DIM, "end") if i not in SINKS else ""
        s += txt(X0 + 16, y + 22, lab, 14, lc, weight=700, ls=2)
        s += txt(X0 + 16, y + 39, sub, 10.5, PH_MID)
        if i == 4:
            s += f'<rect x="{X0}" y="{y}" width="{NW}" height="{NH}" fill="none" stroke="{AMBER}" stroke-width="3" class="pulse" opacity=".5"/>'
        if i == 0:
            # market scanner sweep
            s += f'<clipPath id="mclip"><rect x="{X0}" y="{y}" width="{NW}" height="{NH}"/></clipPath>'
            s += (f'<g clip-path="url(#mclip)"><rect x="{X0}" y="{y}" width="46" height="{NH}" fill="{PH}" opacity=".10">'
                  f'<animate attributeName="x" values="{X0-46};{X0+NW}" dur="2.4s" repeatCount="indefinite"/></rect>'
                  f'<line x1="{X0}" y1="{y}" x2="{X0}" y2="{y+NH}" stroke="{PH}" stroke-width="1.5" opacity=".7">'
                  f'<animate attributeName="x1" values="{X0};{X0+NW+46}" dur="2.4s" repeatCount="indefinite"/>'
                  f'<animate attributeName="x2" values="{X0};{X0+NW+46}" dur="2.4s" repeatCount="indefinite"/></line></g>\n')
            s += txt(X0 + NW - 12, y + 22, "EXTERNAL", 9.5, PH_DIM, "end", ls=2)
        if i == 6:
            s += txt(X0 + NW - 12, y + 22, "ONCHAIN", 9.5, TEAL, "end", ls=2)

    # packets
    top = ny(0) + NH / 2
    def path_to_sink(i):
        yy = ny(i) + NH / 2
        return f"M{CX},{top} V{yy} H{SINK_X+SINK_W/2}", (yy - top) + (CX - SINK_X - SINK_W / 2)
    full_d = f"M{CX},{top} V{ly_bot} H{LOOP_X} V{ly_top} H{X0+NW}"
    full_len = (ly_bot - top) + (LOOP_X - CX) + (ly_bot - ly_top) + (LOOP_X - X0 - NW)

    schedule = [  # (offset, kind)
        (0.0, "full"), (1.0, 2), (2.0, 3), (2.6, "full"), (3.4, 4), (4.6, 2),
        (5.6, 3), (6.8, 4), (7.8, 2), (8.8, 2),
    ]
    flashes = {2: [], 3: [], 4: []}
    for k, (off, kind) in enumerate(schedule):
        if kind == "full":
            d, L, col, r = full_d, full_len, PH, 5.5
        else:
            d, L = path_to_sink(kind)
            col = AMBER if kind == 4 else PH_MID
            r = 4.5
        dur = L / SPEED
        end = off + dur
        assert end <= T, (kind, end)
        a, b = off / T, end / T
        kp = "0;0;1;1" if a > 0 else "0;1;1"
        kt = f"0;{a:.4f};{b:.4f};1" if a > 0 else f"0;{b:.4f};1"
        s += f'<path id="pp{k}" d="{d}" fill="none" stroke="none"/>'
        s += (f'<circle r="{r}" fill="{col}" filter="url(#glow)" opacity="0">'
              f'<animateMotion dur="{T}s" repeatCount="indefinite" keyPoints="{kp}" keyTimes="{kt}" calcMode="linear">'
              f'<mpath href="#pp{k}"/></animateMotion>'
              + discrete_opacity([(off, end)], T) + '</circle>\n')
        if kind != "full":
            flashes[kind].append((end, min(end + 0.45, T)))
        else:
            # hop through the wallet: tint the node when a live packet passes
            yy = ny(6)
            tw = off + (yy + NH / 2 - top) / SPEED
            s += (f'<rect x="{X0}" y="{yy}" width="{NW}" height="{NH}" fill="{TEAL}" opacity="0">'
                  + discrete_opacity([(tw - 0.12, tw + 0.35)], T, on=.18)
                  + '</rect>\n')
            yy = ny(5)
            te = off + (yy + NH / 2 - top) / SPEED
            s += (f'<rect x="{X0}" y="{yy}" width="{NW}" height="{NH}" fill="{PH}" opacity="0">'
                  + discrete_opacity([(te - 0.12, te + 0.35)], T, on=.14)
                  + '</rect>\n')
    for i, wins in flashes.items():
        col = RED if i == 4 else PH
        y = ny(i)
        s += (f'<rect x="{SINK_X}" y="{y+6}" width="{SINK_W}" height="{NH-12}" fill="{col}" opacity="0">'
              + discrete_opacity(wins, T, on=.22) + '</rect>\n')
        if i == 4:
            s += (f'<g opacity="0">' + txt(SINK_X + SINK_W - 12, y + 24, "VETO", 11, RED, "end", weight=700, ls=2)
                  + discrete_opacity(wins, T) + '</g>\n')

    # legend
    ly = H - 30
    s += f'<circle cx="44" cy="{ly-4}" r="5" fill="{PH}" filter="url(#glow)"/>'
    s += txt(56, ly, "candidate that clears every stage", 11, PH_MID)
    s += f'<circle cx="324" cy="{ly-4}" r="4.5" fill="{PH_MID}"/>'
    s += txt(336, ly, "dropped. no signal or no edge", 11, PH_MID)
    s += f'<circle cx="584" cy="{ly-4}" r="4.5" fill="{AMBER}"/>'
    s += txt(596, ly, "vetoed by risk engine", 11, PH_MID)

    s += close_svg(W, H)
    return s
