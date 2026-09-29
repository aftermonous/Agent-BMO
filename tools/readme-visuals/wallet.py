import qrcode
from common import *

W, H = 880, 340

def qr_svg(x, y, size):
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=0)
    q.add_data(WALLET)
    q.make(fit=True)
    m = q.get_matrix()
    n = len(m)
    quiet = 3
    cell = size / (n + 2 * quiet)
    s = f'<rect x="{x}" y="{y}" width="{size}" height="{size}" fill="{PH}"/>'
    rects = []
    for r, row in enumerate(m):
        for c, v in enumerate(row):
            if v:
                rects.append(f'<rect x="{x+(c+quiet)*cell:.2f}" y="{y+(r+quiet)*cell:.2f}" width="{cell+0.05:.2f}" height="{cell+0.05:.2f}"/>')
    s += f'<g fill="{BLACK}">' + "".join(rects) + '</g>'
    return s

def build():
    s = open_svg(W, H, "Agent BMO wallet",
                 f"Wallet address {WALLET}. Solana mainnet. Sole signing identity for the agent. Every transaction is public. "
                 "QR code encodes the address.")
    s += header(W, "AGENT BMO / WALLET", "IDENTITY REGISTER")

    qx, qy, qs = 40, 62, 236
    s += f'<rect x="{qx-8}" y="{qy-8}" width="{qs+16}" height="{qs+16}" fill="none" stroke="{PH_DIM}"/>'
    top = qr_svg(qx, qy, qs)
    # scanning beam over QR
    s += f'<clipPath id="qclip"><rect x="{qx}" y="{qy}" width="{qs}" height="{qs}"/></clipPath>'
    top += (f'<g clip-path="url(#qclip)"><rect x="{qx}" y="{qy}" width="{qs}" height="2" fill="{WHITE}" opacity=".4">'
          f'<animate attributeName="y" values="{qy-4};{qy+qs};{qy-4}" dur="3.6s" repeatCount="indefinite"/></rect></g>\n')
    s += txt(qx + qs / 2, qy + qs + 26, "SCAN TO VERIFY", 10, PH_DIM, "middle", ls=3)

    x0 = 318
    s += txt(x0, 76, "ADDRESS", 10, PH_DIM, ls=3)
    # address: vanity prefix separated for legibility
    s += (f'<text x="{x0}" y="110" font-size="19" font-weight="700" filter="url(#glowsoft)">'
          f'<tspan fill="{WHITE}">bmo</tspan><tspan fill="{PH}">{t(WALLET[3:])}</tspan></text>\n')
    s += f'<line x1="{x0}" y1="118" x2="{x0+34}" y2="118" stroke="{WHITE}" stroke-width="1.5"/>'
    s += txt(x0, 136, "vanity prefix", 9.5, PH_DIM, ls=1)
    s += txt(W - 40, 136, "44 chars. base58", 9.5, PH_DIM, "end", ls=1)

    rows = [
        ("NETWORK", "SOLANA MAINNET", PH),
        ("ROLE", "SOLE SIGNING IDENTITY OF THE AGENT", PH),
        ("VISIBILITY", "PUBLIC. EVERY TX IS ONCHAIN", PH),
        ("BALANCE", "READ IT FROM CHAIN. NOT FROM HERE", PH_MID),
        ("AUTONOMOUS TX", "0. EXECUTION NOT LIVE", AMBER),
    ]
    for i, (k, v, col) in enumerate(rows):
        y = 172 + i * 27
        s += f'<line x1="{x0}" y1="{y+9}" x2="{W-40}" y2="{y+9}" stroke="{PH_FAINT}"/>'
        s += txt(x0, y, k, 10.5, PH_DIM, ls=2)
        s += txt(x0 + 140, y, v, 12.5, col, weight=700, ls=1)
    s += f'<rect x="{x0+140+21*8.5+5:.0f}" y="{172+4*27-11}" width="7" height="13" fill="{AMBER}" class="blink"/>'

    s += txt(W - 40, H - 16, "screenshots are claims. the chain is the record.", 11, PH_MID, "end", ls=1)
    s += close_svg(W, H)
    return s.replace('</svg>\n', top + '</svg>\n')
