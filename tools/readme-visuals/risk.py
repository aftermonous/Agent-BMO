from common import *

W = 880
GATES = [
    ("EMERGENCY STOP", "kill_switch", "halt flag is off"),
    ("COOLDOWN", "cooldown_sec", "timer has elapsed"),
    ("TOKEN VALIDATION", "token_checks", "mint and authority ok"),
    ("LIQUIDITY FLOOR", "min_liquidity_usd", "pool depth over floor"),
    ("MAX POSITION SIZE", "max_position_sol", "size under cap"),
    ("WALLET EXPOSURE", "max_exposure_pct", "exposure under cap"),
    ("LOSS LIMIT", "max_daily_loss_sol", "daily loss under limit"),
    ("SLIPPAGE LIMIT", "max_slippage_bps", "quote within limit"),
    ("TX SIMULATION", "simulate_before_send", "simulation succeeds"),
]
FAIL = 7
T = 15.0
A0, B0, STEP = 0.8, 8.3, 0.45
RY0, RH = 132, 32

def build():
    H = RY0 + len(GATES) * RH + 110
    s = open_svg(W, H, "Agent BMO risk gate",
                 "Every action passes nine gates in order: emergency stop, cooldown, token validation, liquidity floor, "
                 "max position size, wallet exposure, loss limit, slippage limit, transaction simulation. "
                 "Candidate A clears all gates and is allowed. Candidate B fails the slippage limit and is blocked. "
                 "Values are unset. Illustration only.")
    s += header(W, "AGENT BMO / RISK GATE", "ALL GATES MUST PASS. ANY GATE CAN VETO")

    # candidate indicator
    s += txt(40, 76, "INPUT", 10, PH_DIM, ls=3)
    s += '<g>' + txt(110, 76, "CANDIDATE A", 13, PH, weight=700, ls=2) + discrete_opacity([(0, 7.5)], T, base=0) + '</g>'
    s += '<g opacity="0">' + txt(110, 76, "CANDIDATE B", 13, PH, weight=700, ls=2) + discrete_opacity([(7.5, T)], T) + '</g>'
    s += txt(W - 40, 76, "illustration. no real orders. limits not yet set", 10.5, PH_DIM, "end")

    # column heads
    cols = [(84, "GATE"), (318, "CONFIG KEY"), (540, "CHECK"), (W - 40, "RESULT")]
    for x, lab in cols:
        s += txt(x, 112, lab, 9.5, PH_DIM, "end" if lab == "RESULT" else "start", ls=3)
    s += f'<line x1="40" y1="120" x2="{W-40}" y2="120" stroke="{PH_DIM}"/>\n'

    # scanning cursor
    sched = [(0, -100)]
    for i in range(len(GATES)):
        sched.append((A0 + i * STEP, RY0 + i * RH))
    sched.append((A0 + len(GATES) * STEP, -100))
    for i in range(FAIL + 1):
        sched.append((B0 + i * STEP, RY0 + i * RH))
    sched.append((B0 + (FAIL + 1) * STEP, -100))
    s += f'<rect x="40" y="-100" width="{W-80}" height="{RH-4}" fill="{PH}" opacity=".07">{discrete_attr("y", sched, T)}</rect>\n'

    for i, (lab, key, chk) in enumerate(GATES):
        y = RY0 + i * RH
        cy = y + RH / 2 - 2
        s += f'<line x1="40" y1="{y+RH-4}" x2="{W-40}" y2="{y+RH-4}" stroke="{PH_FAINT}"/>'
        s += txt(40, cy + 4, f"{i+1}", 10, PH_DIM)
        # lamp base
        s += f'<rect x="56" y="{cy-6}" width="12" height="12" fill="{PH_FAINT}"/>'
        ta = A0 + i * STEP
        tb = B0 + i * STEP
        greens = [(ta, 7.5)]
        if i < FAIL:
            greens.append((tb, T))
        s += f'<rect x="56" y="{cy-6}" width="12" height="12" fill="{PH}" filter="url(#glow)" opacity="0">{discrete_opacity(greens, T)}</rect>'
        s += txt(84, cy + 4, lab, 12.5, PH, weight=700, ls=1)
        s += txt(318, cy + 4, key, 11.5, PH_MID)
        if i == FAIL:
            s += '<g>' + txt(540, cy + 4, chk, 11.5, PH_DIM) + discrete_opacity([(0, tb)], T) + '</g>'
            s += '<g opacity="0">' + txt(540, cy + 4, "quote exceeds limit", 11.5, RED) + discrete_opacity([(tb, T)], T) + '</g>'
        else:
            s += txt(540, cy + 4, chk, 11.5, PH_DIM)
        s += f'<g opacity="0">' + txt(W - 40, cy + 4, "PASS", 11.5, PH, "end", weight=700, ls=2) + discrete_opacity(greens, T) + '</g>'
        if i == FAIL:
            s += f'<rect x="56" y="{cy-6}" width="12" height="12" fill="{RED}" filter="url(#glow)" opacity="0">{discrete_opacity([(tb, T)], T)}</rect>'
            s += (f'<rect x="40" y="{y}" width="{W-80}" height="{RH-4}" fill="{RED}" opacity="0">'
                  f'{discrete_opacity([(tb, T)], T, on=.14)}</rect>')
            s += f'<g opacity="0">' + txt(W - 40, cy + 4, "FAIL", 11.5, RED, "end", weight=700, ls=2) + discrete_opacity([(tb, T)], T) + '</g>'
        if i > FAIL:
            s += f'<g opacity="0">' + txt(W - 40, cy + 4, "SKIPPED", 11.5, PH_DIM, "end", ls=2) + discrete_opacity([(tb, T)], T) + '</g>'
        s += "\n"

    # verdict bar
    vy = RY0 + len(GATES) * RH + 22
    s += f'<rect x="40" y="{vy}" width="{W-80}" height="46" fill="{PANEL}" stroke="{PH_DIM}"/>'
    s += txt(58, vy + 28, "VERDICT", 10, PH_DIM, ls=3)
    ta_end = A0 + len(GATES) * STEP
    tb_end = B0 + (FAIL + 1) * STEP
    s += '<g>' + txt(160, vy + 29, "EVALUATING", 14, PH_DIM, ls=3, cls="blink") + discrete_opacity([(0, ta_end), (7.5, tb_end)], T, base=0) + '</g>'
    s += ('<g opacity="0">' + f'<rect x="40" y="{vy}" width="{W-80}" height="46" fill="none" stroke="{PH}" stroke-width="2"/>'
          + txt(160, vy + 29, "ALLOW. HANDOFF TO EXECUTION ENGINE", 14, PH, weight=700, ls=2, extra=' filter="url(#glow)"')
          + discrete_opacity([(ta_end, 7.5)], T) + '</g>')
    s += ('<g opacity="0">' + f'<rect x="40" y="{vy}" width="{W-80}" height="46" fill="{RED}" fill-opacity=".1" stroke="{RED}" stroke-width="2"/>'
          + txt(160, vy + 29, "BLOCKED. ORDER DROPPED. REASON LOGGED", 14, RED, weight=700, ls=2, extra=' filter="url(#glow)"')
          + discrete_opacity([(tb_end, T)], T) + '</g>\n')

    s += txt(40, H - 20, "design rule: unset limits mean no execution. there are no silent defaults.", 10.5, AMBER)
    s += close_svg(W, H)
    return s
