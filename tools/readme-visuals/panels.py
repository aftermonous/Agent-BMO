from common import *

# ---------------------------------------------------------------- ACTIVITY
def activity():
    W, H = 880, 330
    s = open_svg(W, H, "Agent BMO activity feed",
                 "Execution log. Empty. Awaiting first live execution. Zero entries. Rows will be generated from onchain data.")
    s += header(W, "AGENT BMO / EXECUTION LOG", "SOURCE: CHAIN. NOT HAND WRITTEN")
    cols = [(40, "TIME UTC"), (190, "STATE"), (300, "ASSET"), (420, "SIDE"), (500, "SIZE"), (610, "SIGNATURE")]
    for x, lab in cols:
        s += txt(x, 70, lab, 10, PH_DIM, ls=3)
    s += f'<line x1="40" y1="80" x2="{W-40}" y2="80" stroke="{PH_DIM}"/>\n'
    for r in range(6):
        y = 104 + r * 26
        s += f'<line x1="40" y1="{y+8}" x2="{W-40}" y2="{y+8}" stroke="{PH_FAINT}" stroke-dasharray="1 4"/>'
        for x, _ in cols:
            s += txt(x, y, "--", 11, PH_FAINT)
    s += "\n"
    # slow sweep across empty rows: the log is being watched, nothing has arrived
    s += (f'<rect x="40" y="86" width="{W-80}" height="2" fill="{PH}" opacity=".35">'
          f'<animate attributeName="y" values="86;250;86" dur="6s" repeatCount="indefinite"/></rect>\n')
    # centre message
    bw, bh = 470, 66
    bx, by = (W - bw) / 2, 138
    s += f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="{BLACK}" stroke="{AMBER}" stroke-width="1.5"/>'
    s += f'<rect x="{bx+4}" y="{by+4}" width="{bw-8}" height="{bh-8}" fill="none" stroke="{AMBER_DIM}"/>'
    s += txt(W / 2, by + 32, "AWAITING FIRST LIVE EXECUTION", 17, AMBER, "middle", weight=700, ls=3, extra=' filter="url(#glow)"')
    s += f'<rect x="{W/2+172}" y="{by+18}" width="9" height="17" fill="{AMBER}" class="blink"/>'
    s += txt(W / 2, by + 52, "no trades yet. nothing here will be invented.", 11, PH_MID, "middle")
    # status bar
    y = H - 44
    s += f'<line x1="40" y1="{y-16}" x2="{W-40}" y2="{y-16}" stroke="{PH_DIM}"/>'
    items = [("ENTRIES", "0", PH), ("FEED", "NOT CONNECTED", AMBER), ("RPC", "PLANNED", PH_MID), ("PNL", "NOT REPORTED", PH_MID)]
    x = 40
    for k, v, col in items:
        s += txt(x, y, k, 10, PH_DIM, ls=2)
        s += txt(x + 8 + len(k) * 8, y, v, 11, col, weight=700, ls=1)
        x += 8 + len(k) * 8 + len(v) * 7.6 + 44
    s += txt(40, H - 18, "when live, each row links to its transaction on an explorer.", 10.5, PH_DIM)
    s += close_svg(W, H)
    return s

# ---------------------------------------------------------------- SCREEN
SCREEN_STATES = ["IDLE", "SCANNING", "ANALYZING", "ENTERING", "HOLDING", "EXITING", "COOLDOWN"]

def screen():
    W, H = 880, 470
    T = 2.4 * len(SCREEN_STATES)
    s = open_svg(W, H, "Agent BMO physical display",
                 "Concept of the built-in display. It cycles through agent states: idle, scanning, analyzing, entering, "
                 "holding, exiting, cooldown. Fields: state, asset, position, balance, last transaction, network. "
                 "All values are placeholders.",
                 css=".bars rect{transform-box:fill-box;transform-origin:bottom;animation:eq .8s ease-in-out infinite alternate}"
                     "@keyframes eq{from{transform:scaleY(.2)}to{transform:scaleY(1)}}")
    s += header(W, "AGENT BMO / FRONT DISPLAY", "READ ONLY. REPORTS STATE. TAKES NO INPUT")

    # display module (generic bezel, landscape panel)
    hx, hy, hw, hh = 40, 64, 420, 330
    s += f'<rect x="{hx}" y="{hy}" width="{hw}" height="{hh}" rx="10" fill="#03110a" stroke="{PH_DIM}" stroke-width="1.5"/>'
    for k in range(4):
        s += f'<circle cx="{hx+12 + (k%2)*(hw-24)}" cy="{hy+12 + (k//2)*(hh-24)}" r="3" fill="none" stroke="{PH_DIM}"/>'
    sx, sy, sw, sh = hx + 30, hy + 30, hw - 60, hh - 70
    s += f'<rect x="{sx-4}" y="{sy-4}" width="{sw+8}" height="{sh+8}" fill="none" stroke="{PH_FAINT}"/>'
    s += f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" fill="#010805"/>'
    s += f'<clipPath id="scr"><rect x="{sx}" y="{sy}" width="{sw}" height="{sh}"/></clipPath>'
    s += txt(hx + hw / 2, hy + hh - 14, "DISPLAY 01", 9, PH_DIM, "middle", ls=4)

    s += f'<g clip-path="url(#scr)">'
    # persistent top row
    s += txt(sx + 12, sy + 20, "AGENT BMO", 10, PH_MID, ls=2)
    s += f'<circle cx="{sx+sw-46}" cy="{sy+16}" r="3" fill="{PH}" class="pulse"/>'
    s += txt(sx + sw - 12, sy + 20, "SOL", 10, PH_MID, "end", ls=2)
    s += f'<line x1="{sx+10}" y1="{sy+28}" x2="{sx+sw-10}" y2="{sy+28}" stroke="{PH_FAINT}"/>'
    # persistent fields
    fy = sy + 150
    fields = [("ASSET", "--"), ("POS", "--"), ("BAL", "-- SOL"), ("LAST TX", "--")]
    for i, (k, v) in enumerate(fields):
        cx = sx + 14 + (i % 2) * (sw / 2)
        cy = fy + (i // 2) * 34
        s += txt(cx, cy, k, 9, PH_DIM, ls=2)
        s += txt(cx, cy + 15, v, 13, PH, weight=700)
    for i, st in enumerate(SCREEN_STATES):
        a, b = i * 2.4, (i + 1) * 2.4
        s += '<g opacity="0">'
        col = AMBER if st in ("ENTERING", "EXITING") else PH
        s += txt(sx + sw / 2, sy + 74, st, 30, col, "middle", weight=700, ls=4, extra=' filter="url(#glow)"')
        vy = sy + 98
        if st == "IDLE":
            s += f'<rect x="{sx+sw/2-6}" y="{vy}" width="12" height="18" fill="{PH}" class="blinkslow"/>'
        elif st == "SCANNING":
            s += f'<rect x="{sx+30}" y="{vy+8}" width="{sw-60}" height="2" fill="{PH_FAINT}"/>'
            s += (f'<rect x="{sx+30}" y="{vy+4}" width="40" height="10" fill="{PH}" opacity=".8">'
                  f'<animate attributeName="x" values="{sx+30};{sx+sw-70};{sx+30}" dur="1.2s" repeatCount="indefinite"/></rect>')
        elif st == "ANALYZING":
            bars = []
            for k in range(16):
                bars.append(f'<rect x="{sx+50+k*16}" y="{vy}" width="10" height="20" fill="{PH}" style="animation-delay:{-k*0.13:.2f}s"/>')
            s += '<g class="bars">' + "".join(bars) + '</g>'
        elif st in ("ENTERING", "EXITING"):
            steps = ["SIM", "SIGN", "SEND"]
            for k, lab in enumerate(steps):
                x = sx + 50 + k * 90
                s += f'<rect x="{x}" y="{vy}" width="70" height="20" fill="none" stroke="{AMBER_DIM}"/>'
                s += (f'<rect x="{x}" y="{vy}" width="70" height="20" fill="{AMBER}" opacity="0">'
                                            + discrete_opacity([(a + 0.3 + k * 0.6, b)], T, on=.3) + '</rect>')
                s += txt(x + 35, vy + 14, lab, 10, AMBER, "middle", weight=700, ls=2)
        elif st == "HOLDING":
            x0, x1 = sx + 40, sx + sw - 40
            s += f'<line x1="{x0}" y1="{vy+10}" x2="{x1}" y2="{vy+10}" stroke="{PH_DIM}" stroke-width="2"/>'
            s += f'<line x1="{x0}" y1="{vy+2}" x2="{x0}" y2="{vy+18}" stroke="{RED}" stroke-width="2"/>'
            s += f'<line x1="{x1}" y1="{vy+2}" x2="{x1}" y2="{vy+18}" stroke="{PH}" stroke-width="2"/>'
            s += f'<rect x="{(x0+x1)/2-4}" y="{vy+4}" width="8" height="12" fill="{WHITE}" class="blinkslow"/>'
            s += txt(x0, vy + 32, "STOP", 8.5, RED, "middle", ls=2)
            s += txt(x1, vy + 32, "TARGET", 8.5, PH, "middle", ls=2)
        elif st == "COOLDOWN":
            s += f'<rect x="{sx+40}" y="{vy+4}" width="{sw-80}" height="10" fill="none" stroke="{PH_DIM}"/>'
            s += (f'<rect x="{sx+42}" y="{vy+6}" width="{sw-84}" height="6" fill="{PH_MID}">'
                  f'<animate attributeName="width" values="{sw-84};0" dur="2.4s" begin="{a}s" repeatCount="indefinite"/></rect>')
        s += discrete_opacity([(a, b)], T) + '</g>\n'
    # network row at bottom of screen
    s += txt(sx + 14, sy + sh - 12, "NET  SOLANA", 9, PH_DIM, ls=2)
    s += txt(sx + sw - 14, sy + sh - 12, "PLACEHOLDER VALUES", 9, PH_FAINT, "end", ls=2)
    s += '</g>\n'
    s += f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" fill="url(#scan)"/>'

    # callouts on right
    rx = 520
    call = [
        ("STATE", "what the agent is doing now", sy + 64),
        ("ASSET", "token under analysis or held", fy + 6),
        ("POSITION", "size and status", fy + 6),
        ("BALANCE", "wallet balance, read from chain", fy + 40),
        ("LAST TX", "most recent signature", fy + 40),
        ("NETWORK", "chain and link health", sy + sh - 16),
    ]
    for i, (k, d, ty) in enumerate(call):
        y = 88 + i * 42
        s += f'<path d="M{rx-8},{y-4} H{rx-24} L{sx+sw+14},{ty}" fill="none" stroke="{PH_FAINT}"/>'
        s += f'<circle cx="{sx+sw+14}" cy="{ty}" r="2.5" fill="{PH_DIM}"/>'
        s += txt(rx, y, k, 12, PH, weight=700, ls=2)
        s += txt(rx, y + 15, d, 10.5, PH_MID)

    # state strip synced to screen
    y = H - 44
    x = 40
    for i, st in enumerate(SCREEN_STATES):
        w = len(st) * 8.4 + 22
        s += f'<rect x="{x}" y="{y-15}" width="{w}" height="22" fill="none" stroke="{PH_FAINT}"/>'
        s += (f'<rect x="{x}" y="{y-15}" width="{w}" height="22" fill="{PH}" opacity="0">'
              + discrete_opacity([(i * 2.4, (i + 1) * 2.4)], T, on=.9) + '</rect>')
        s += txt(x + w / 2, y, st, 11, PH_MID, "middle", weight=700, ls=1)
        s += (f'<g opacity="0">' + txt(x + w / 2, y, st, 11, BLACK, "middle", weight=700, ls=1)
              + discrete_opacity([(i * 2.4, (i + 1) * 2.4)], T) + '</g>')
        x += w + 8
    s += txt(W - 40, H - 16, "concept render. not firmware output.", 10, PH_DIM, "end")
    s += close_svg(W, H)
    return s

# ---------------------------------------------------------------- STATUS
def status():
    W, H = 880, 312
    s = open_svg(W, H, "Agent BMO build status",
                 "Live: wallet address, public spec. In development: physical unit, on-device runtime. "
                 "Planned: market observer, strategy and decision engines, risk engine, execution engine, "
                 "position manager and memory, public activity feed, agent state on the display.")
    s += header(W, "AGENT BMO / BUILD STATUS", "HONEST BY DEFAULT")
    cols = [
        ("LIVE", PH, "solid", ["wallet address", "public spec and diagrams"]),
        ("IN DEVELOPMENT", AMBER, "blink", ["physical unit", "  pi 5. printed shell. button pcb", "on-device runtime",
                                             "  wake word. local model. speech"]),
        ("PLANNED", PH_DIM, "hollow", ["market observer", "strategy + decision engines", "risk engine",
                                        "execution engine", "position manager + memory", "public activity feed",
                                        "agent state on display"]),
    ]
    cw = (W - 80 - 40) / 3
    for i, (lab, col, kind, items) in enumerate(cols):
        x = 40 + i * (cw + 20)
        s += f'<rect x="{x}" y="58" width="{cw}" height="{H-90}" fill="{PANEL}" stroke="{col if kind != "hollow" else PH_FAINT}"/>'
        if kind == "hollow":
            s += f'<circle cx="{x+20}" cy="80" r="6" fill="none" stroke="{col}" stroke-width="1.5"/>'
        else:
            s += f'<circle cx="{x+20}" cy="80" r="6" fill="{col}" filter="url(#glow)" class="{"blinkslow" if kind=="blink" else ""}"/>'
        s += txt(x + 36, 85, lab, 13, col if kind != "hollow" else PH_MID, weight=700, ls=3)
        s += f'<line x1="{x+14}" y1="98" x2="{x+cw-14}" y2="98" stroke="{PH_FAINT}"/>'
        for k, it in enumerate(items):
            sub = it.startswith("  ")
            s += txt(x + (30 if sub else 20), 122 + k * 22, it.strip(), 10.5 if sub else 12,
                     PH_DIM if sub else (PH if kind != "hollow" else PH_MID))
    s += txt(40, H - 12, "this panel is updated by hand in the repo. it changes when the code does.", 10, PH_DIM)
    s += close_svg(W, H)
    return s

# ---------------------------------------------------------------- DIVIDER
def divider():
    W, H = 880, 26
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="divider">'
         + style() + defs(W, H))
    s += f'<line x1="0" y1="13" x2="{W}" y2="13" stroke="{PH_DIM}" stroke-dasharray="2 5"/>'
    for k in range(0, W + 1, 110):
        s += f'<line x1="{k}" y1="8" x2="{k}" y2="18" stroke="{PH_DIM}"/>'
    s += (f'<rect x="0" y="11" width="70" height="4" fill="{PH}" filter="url(#glow)">'
          f'<animate attributeName="x" values="-70;{W}" dur="3.2s" repeatCount="indefinite"/></rect>')
    s += '</svg>\n'
    return s

# ---------------------------------------------------------------- EOF
def eof():
    W, H = 880, 120
    s = open_svg(W, H, "End of transmission", "End of transmission. Agent BMO is in standby.")
    s += txt(40, 50, "EOF", 11, PH_DIM, ls=4)
    s += txt(40, 80, "bmo@unit01:~$ agent status", 14, PH_MID)
    s += txt(40 + 8.4 * 28, 80, "standby. waiting for limits. waiting for release.", 14, AMBER)
    s += f'<rect x="{40 + 8.4*28 + 8.4*50:.0f}" y="68" width="9" height="16" fill="{AMBER}" class="blink"/>'
    s += txt(W - 40, 50, WALLET, 10, PH_DIM, "end", ls=1)
    s += close_svg(W, H)
    return s
