import math
from common import *

W, H = 880, 668
CX, CY, R = 440, 336, 212
T = 13.5  # 1.5 s per state
STATES = [
    ("SCAN", "read new pools and price moves"),
    ("FILTER", "drop tokens that fail hard rules"),
    ("ANALYZE", "score survivors against strategy"),
    ("DECIDE", "act or pass. reason is logged"),
    ("VALIDATE", "risk limits. simulate the tx"),
    ("EXECUTE", "sign and send from bmo wallet"),
    ("MANAGE", "track position against plan"),
    ("EXIT", "target. stop. or timeout"),
    ("REPEAT", "write memory. return to scan"),
]
N = len(STATES)
STEP = T / N
EXITS = {1: "drop", 3: "pass", 4: "veto"}

def pos(i, r=R):
    a = math.radians(-90 + i * 360 / N)
    return CX + r * math.cos(a), CY + r * math.sin(a)

def build():
    s = open_svg(W, H, "Agent BMO trading loop",
                 "A nine state machine: scan, filter, analyze, decide, validate, execute, manage, exit, repeat. "
                 "A sweep and a packet travel the ring. Filter, decide and validate can drop, pass or veto.",
                 css=f"""
.spin{{transform-origin:{CX}px {CY}px;animation:spin 60s linear infinite}}
.spinr{{transform-origin:{CX}px {CY}px;animation:spin 90s linear infinite reverse}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
""")
    s += header(W, "AGENT BMO / CORE LOOP", "STATE MACHINE. NOT RUNNING YET")

    # outer tick ring, slowly rotating
    ticks = []
    for k in range(120):
        a = math.radians(k * 3)
        r1 = 262 if k % 10 else 252
        x1, y1 = CX + r1 * math.cos(a), CY + r1 * math.sin(a)
        x2, y2 = CX + 270 * math.cos(a), CY + 270 * math.sin(a)
        ticks.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"/>')
    s += f'<g class="spin" stroke="{PH_DIM}" stroke-width="1">' + "".join(ticks) + '</g>\n'
    s += f'<circle cx="{CX}" cy="{CY}" r="244" fill="none" stroke="{PH_FAINT}" stroke-dasharray="1 5" class="spinr"/>\n'

    # sweep wedge (trailing fade)
    wedge = []
    for k in range(10):
        a0, a1 = -90 - k * 5, -90 - (k + 1) * 5
        p0 = (CX + R * math.cos(math.radians(a0)), CY + R * math.sin(math.radians(a0)))
        p1 = (CX + R * math.cos(math.radians(a1)), CY + R * math.sin(math.radians(a1)))
        op = 0.30 * (1 - k / 10)
        wedge.append(f'<path d="M{CX},{CY} L{p0[0]:.1f},{p0[1]:.1f} A{R},{R} 0 0 0 {p1[0]:.1f},{p1[1]:.1f} Z" '
                     f'fill="{PH}" opacity="{op:.3f}"/>')
    s += (f'<g>' + "".join(wedge) +
          f'<line x1="{CX}" y1="{CY}" x2="{CX}" y2="{CY-R}" stroke="{PH}" stroke-width="1.5" opacity=".8"/>'
          f'<animateTransform attributeName="transform" type="rotate" from="0 {CX} {CY}" to="360 {CX} {CY}" '
          f'dur="{T}s" repeatCount="indefinite"/></g>\n')

    # ring
    s += f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="none" stroke="{PH_DIM}" stroke-width="2"/>\n'
    # direction chevrons between nodes
    for i in range(N):
        a = -90 + (i + 0.5) * 360 / N
        x, y = pos(i + 0.5)
        s += (f'<path d="M-5,-6 L3,0 L-5,6" fill="none" stroke="{PH_MID}" stroke-width="1.8" '
              f'transform="translate({x:.1f},{y:.1f}) rotate({a+90:.1f})"/>')
    s += "\n"

    # rejection exits
    for i, lab in EXITS.items():
        x0, y0 = pos(i, R + 38)
        x1, y1 = pos(i, R + 66)
        col = RED if lab == "veto" else PH_DIM
        s += (f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="{col}" '
              f'stroke-dasharray="3 3" marker-end="url(#{"arrR" if col == RED else "arr"})"/>')
        lx, ly = pos(i, R + 82)
        anchor = "start" if lx > CX + 10 else ("end" if lx < CX - 10 else "middle")
        s += txt(lx, ly + 4, lab, 11, col if col == RED else PH_MID, anchor, ls=2)
    s += "\n"

    # centre readout disc
    s += f'<circle cx="{CX}" cy="{CY}" r="128" fill="{BLACK}" stroke="{PH_FAINT}"/>\n'
    s += f'<circle cx="{CX}" cy="{CY}" r="120" fill="none" stroke="{PH_FAINT}" stroke-dasharray="2 3"/>\n'
    s += txt(CX, CY - 52, "CURRENT STATE", 10, PH_DIM, "middle", ls=3)

    # nodes
    for i, (lab, desc) in enumerate(STATES):
        x, y = pos(i)
        start, end = (i - 0.5) * STEP, (i + 0.5) * STEP
        win = [(start, end)] if start >= 0 else [(0, end), (T + start, T)]
        s += f'<g>'
        s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="38" fill="{PANEL}" stroke="{PH_DIM}" stroke-width="1.5"/>'
        # active overlay
        col = AMBER if lab == "VALIDATE" else (TEAL if lab == "EXECUTE" else PH)
        s += (f'<g opacity="0">'
              f'<circle cx="{x:.1f}" cy="{y:.1f}" r="38" fill="{col}" opacity=".16"/>'
              f'<circle cx="{x:.1f}" cy="{y:.1f}" r="38" fill="none" stroke="{col}" stroke-width="2.5" filter="url(#glow)"/>'
              f'<circle cx="{x:.1f}" cy="{y:.1f}" r="46" fill="none" stroke="{col}" stroke-width="1" opacity=".5"/>'
              + discrete_opacity(win, T) + '</g>')
        s += txt(x, y - 5 + 0.5, f"{i:02d}", 9, PH_DIM, "middle", ls=1)
        s += txt(x, y + 12, lab, 12 if len(lab) < 8 else 11, WHITE if False else PH, "middle", weight=700, ls=1)
        s += '</g>\n'
        # centre readout per state
        s += f'<g opacity="0">'
        s += txt(CX, CY - 8, lab, 30, col, "middle", weight=700, ls=4, extra=' filter="url(#glow)"')
        s += txt(CX, CY + 20, desc, 11, PH_MID, "middle")
        # step counter
        s += txt(CX, CY + 52, f"{i+1:02d} / {N:02d}", 11, PH_DIM, "middle", ls=3)
        s += discrete_opacity(win, T) + '</g>\n'

    # packet riding the ring
    s += (f'<path id="ring" d="M{CX},{CY-R} A{R},{R} 0 0 1 {CX},{CY+R} A{R},{R} 0 0 1 {CX},{CY-R}" fill="none"/>'
          f'<circle r="5" fill="{WHITE}" filter="url(#glowbig)"><animateMotion dur="{T}s" repeatCount="indefinite">'
          f'<mpath href="#ring"/></animateMotion></circle>\n')

    # progress bar across a cycle
    s += f'<rect x="{CX-80}" y="{CY+70}" width="160" height="3" fill="{PH_FAINT}"/>'
    s += (f'<rect x="{CX-80}" y="{CY+70}" width="0" height="3" fill="{PH_MID}">'
          f'<animate attributeName="width" values="0;160" dur="{T}s" repeatCount="indefinite"/></rect>\n')
    s += txt(CX, CY + 90, "ONE CYCLE", 9, PH_DIM, "middle", ls=3)

    s += txt(24, H - 20, "shown at 1.5 s per state. real cadence is set by strategy and market.", 10.5, PH_DIM)
    s += txt(W - 24, H - 20, "no terminal state", 10.5, PH_MID, "end", ls=2)
    s += close_svg(W, H)
    return s
