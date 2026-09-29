from common import *

W, H = 880, 560

def build():
    s = open_svg(W, H, "Agent BMO boot sequence",
                 f"Agent BMO powers on. Autonomous onchain trading agent. Network Solana. Wallet {WALLET}. "
                 "Execution engine not loaded. Status settles to standby, pre-release.",
                 css=f"""
.flick{{animation:flick 1.2s linear 2.3s both}}
@keyframes flick{{0%{{opacity:0}}8%{{opacity:.9}}12%{{opacity:.1}}20%{{opacity:1}}24%{{opacity:.3}}32%{{opacity:1}}100%{{opacity:1}}}}
""")

    # header
    s += header(W, "AGENT BMO / UNIT 01 / POWER-ON SELF TEST", "SOLANA  PRE-RELEASE")
    # power led
    s += f'<circle cx="{W-262}" cy="26" r="4" fill="{PH}" filter="url(#glow)" class="pulse"/>'
    s += txt(W-252, 30, "PWR", 11, PH_MID, ls=2)

    # boot log
    lines = [
        ("power rail", "ok", PH),
        ("display bus", "ok", PH),
        ("resolve identity", WALLET_SHORT, PH),
        ("network target", "solana mainnet", PH),
        ("risk limits", "not configured", AMBER),
        ("execution engine", "not loaded", AMBER),
    ]
    y0 = 72
    for i, (k, v, col) in enumerate(lines):
        y = y0 + i * 21
        b = 0.25 + i * 0.3
        stamp = f"[{b*0.41:0.3f}]"
        dots = "." * (30 - len(k))
        s += f'<g opacity="0"><set attributeName="opacity" to="1" begin="{b:.2f}s" fill="freeze"/>'
        s += txt(40, y, stamp, 12, PH_DIM)
        s += txt(112, y, f"{k} {dots}", 12, PH_MID)
        s += txt(112 + 7.22 * 32, y, v, 12, col, extra=' font-weight="700"')
        s += '</g>\n'

    # memory test grid (POST) right side
    gx, gy = 560, 62
    s += txt(gx, gy, "MEM TEST", 10, PH_DIM, ls=2)
    s += txt(gx + 276, gy, "16 x 4", 10, PH_FAINT, "end")
    for r in range(4):
        for c in range(16):
            i = r * 16 + c
            x, y = gx + c * 17.4, gy + 10 + r * 17
            b = 0.2 + i * 0.03
            s += (f'<rect x="{x:.1f}" y="{y}" width="13" height="13" fill="{PH_FAINT}">'
                  f'<set attributeName="fill" to="{PH_MID}" begin="{b:.2f}s" fill="freeze"/></rect>')
    s += "\n"
    # small bar under grid
    s += f'<rect x="{gx}" y="{gy+84}" width="276" height="3" fill="{PH_FAINT}"/>'
    s += (f'<rect x="{gx}" y="{gy+84}" width="0" height="3" fill="{PH}">'
          f'<animate attributeName="width" from="0" to="276" begin="0.2s" dur="2s" fill="freeze"/></rect>')
    s += f'<g opacity="0"><set attributeName="opacity" to="1" begin="2.2s" fill="freeze"/>'
    s += txt(gx, gy + 104, "64/64 cells pass", 11, PH_MID)
    s += '</g>\n'

    # LED matrix wordmark
    off, on, ww = led_word("AGENT BMO", 0, 0, px=11, gap=2)
    mx = (W - ww) / 2 + 5
    my = 222
    s += f'<g transform="translate({mx:.1f},{my})">{off}<g class="flick" filter="url(#glowbig)">{on}</g></g>\n'

    # subtitle typed
    sub = "AUTONOMOUS ONCHAIN TRADING AGENT"
    cw = 9.6 * 1.0  # approx char advance at 16px mono + spacing
    fs, ls = 16, 4.2
    adv = fs * 0.6 + ls
    total = adv * len(sub)
    sx = (W - total) / 2 + ls / 2
    vals = ";".join(f"{adv*i:.1f}" for i in range(len(sub) + 1))
    s += f'<clipPath id="typeclip"><rect x="{sx-4:.1f}" y="300" height="30" width="0">'
    s += (f'<animate attributeName="width" values="{vals}" begin="3.1s" dur="1.3s" '
          f'calcMode="discrete" fill="freeze"/></rect></clipPath>\n')
    s += f'<g clip-path="url(#typeclip)">'
    s += txt(sx, 321, sub, fs, WHITE, ls=ls, weight=700)
    s += '</g>\n'

    # divider
    s += f'<line x1="40" y1="350" x2="{W-40}" y2="350" stroke="{PH_FAINT}" stroke-dasharray="2 4"/>\n'

    # status block
    bx, by = 60, 385
    rows = [
        ("STATUS", None),
        ("NETWORK", "SOLANA"),
        ("WALLET", WALLET),
        ("MODE", "AUTONOMOUS"),
        ("EXECUTION", "OFFLINE. AWAITING RELEASE"),
    ]
    for i, (k, v) in enumerate(rows):
        y = by + i * 29
        b = 4.3 + i * 0.18
        s += f'<g opacity="0"><set attributeName="opacity" to="1" begin="{b:.2f}s" fill="freeze"/>'
        s += txt(bx, y, k, 12, PH_DIM, ls=3)
        if k == "STATUS":
            s += f'<g><set attributeName="opacity" to="0" begin="7.2s" fill="freeze"/>'
            s += txt(bx + 150, y, "INITIALIZING", 15, AMBER, cls="blink", weight=700, ls=2)
            s += '</g>'
            s += f'<g opacity="0"><set attributeName="opacity" to="1" begin="7.2s" fill="freeze"/>'
            s += txt(bx + 150, y, "STANDBY", 15, AMBER, weight=700, ls=2)
            s += f'<rect x="{bx+150+7*11+6}" y="{y-13}" width="9" height="16" fill="{AMBER}" class="blinkslow"/>'
            s += '</g>'
        elif k == "WALLET":
            s += txt(bx + 150, y, v, 15, PH, weight=700, extra=' filter="url(#glowsoft)"')
        elif k == "EXECUTION":
            s += txt(bx + 150, y, v, 15, PH_MID, ls=1)
        else:
            s += txt(bx + 150, y, v, 15, PH, weight=700, ls=2)
        s += '</g>\n'

    # boot progress bar on right of status
    px, py, pw = 640, by + 31, 200
    s += f'<g opacity="0"><set attributeName="opacity" to="1" begin="4.3s" fill="freeze"/>'
    s += f'<rect x="{px}" y="{py+62}" width="{pw}" height="12" fill="none" stroke="{PH_DIM}"/>'
    s += (f'<rect x="{px+2}" y="{py+64}" width="0" height="8" fill="{PH}">'
          f'<animate attributeName="width" values="0;40;44;120;126;170;196" keyTimes="0;.2;.35;.55;.7;.9;1" '
          f'begin="4.4s" dur="2.8s" fill="freeze"/></rect>')
    s += txt(px, py + 54, "BOOT", 10, PH_DIM, ls=3)
    s += '<g>'
    s += txt(px + pw, py + 54, "LOADING", 10, PH_MID, "end", ls=2)
    s += f'<set attributeName="opacity" to="0" begin="7.2s" fill="freeze"/></g>'
    s += f'<g opacity="0"><set attributeName="opacity" to="1" begin="7.2s" fill="freeze"/>'
    s += txt(px + pw, py + 54, "COMPLETE", 10, PH, "end", ls=2)
    s += '</g></g>\n'

    # final prompt
    s += f'<g opacity="0"><set attributeName="opacity" to="1" begin="7.4s" fill="freeze"/>'
    s += txt(40, H - 22, "bmo@unit01:~$ agent --mode autonomous", 12, PH_MID)
    s += f'<rect x="{40 + 7.22*38:.1f}" y="{H-33}" width="8" height="14" fill="{PH}" class="blink"/>'
    s += txt(W - 40, H - 22, "trading disabled until risk limits are set", 11, AMBER_DIM.replace("6b4a00", "a57300"), "end")
    s += '</g>\n'

    s += close_svg(W, H, roll=True, roll_dur=6)
    return s
