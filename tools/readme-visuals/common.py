"""Shared building blocks for Agent BMO README visuals."""
from xml.sax.saxutils import escape

WALLET = "bmoPFnjLBAFq6Gqau8RE4PNMAzYLw6GT5cNBudnJEmf"
WALLET_SHORT = "bmoPF...JEmf"

# Palette. Phosphor on black. Amber for limits. Red for vetoes.
# Teal is the only nod to the hardware shell.
BLACK = "#000000"
PANEL = "#020a06"
GRID = "#06180e"
PH = "#3dff8c"      # phosphor
PH_MID = "#22b863"
PH_DIM = "#136b3a"
PH_FAINT = "#0b3a21"
AMBER = "#ffb000"
AMBER_DIM = "#6b4a00"
RED = "#ff4d4d"
RED_DIM = "#5e1a1a"
TEAL = "#4fe3c9"
WHITE = "#e6fff0"

MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono','DejaVu Sans Mono',monospace"

def t(s):
    return escape(str(s))

def style(extra=""):
    return f"""<style>
text{{font-family:{MONO};}}
.b{{font-weight:700}}
.blink{{animation:blink 1.1s steps(1) infinite}}
.blinkslow{{animation:blink 2.4s steps(1) infinite}}
.pulse{{animation:pulse 2.6s ease-in-out infinite}}
@keyframes blink{{0%{{opacity:1}}50%{{opacity:0}}100%{{opacity:1}}}}
@keyframes pulse{{0%,100%{{opacity:.35}}50%{{opacity:1}}}}
@media (prefers-reduced-motion: reduce){{.blink,.blinkslow,.pulse{{animation:none}}}}
{extra}
</style>"""

def defs(w, h, extra=""):
    return f"""<defs>
<filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
  <feGaussianBlur stdDeviation="2.2" result="b"/>
  <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
<filter id="glowsoft" x="-10%" y="-40%" width="120%" height="180%">
  <feGaussianBlur stdDeviation="1.1" result="b"/>
  <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
<filter id="glowbig" x="-30%" y="-30%" width="160%" height="160%">
  <feGaussianBlur stdDeviation="5" result="b"/>
  <feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">
  <rect width="4" height="1" fill="#000" opacity=".38"/>
</pattern>
<pattern id="dots" width="20" height="20" patternUnits="userSpaceOnUse">
  <rect x="9.5" y="9.5" width="1" height="1" fill="{PH_FAINT}"/>
</pattern>
<radialGradient id="vig" cx="50%" cy="50%" r="75%">
  <stop offset="60%" stop-color="#000" stop-opacity="0"/>
  <stop offset="100%" stop-color="#000" stop-opacity=".75"/>
</radialGradient>
<linearGradient id="roll" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="{PH}" stop-opacity="0"/>
  <stop offset=".85" stop-color="{PH}" stop-opacity=".06"/>
  <stop offset="1" stop-color="{PH}" stop-opacity="0"/>
</linearGradient>
<marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
  <path d="M0,0 L10,5 L0,10 z" fill="{PH_MID}"/>
</marker>
<marker id="arrA" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
  <path d="M0,0 L10,5 L0,10 z" fill="{AMBER}"/>
</marker>
<marker id="arrR" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
  <path d="M0,0 L10,5 L0,10 z" fill="{RED}"/>
</marker>
{extra}
</defs>"""

def open_svg(w, h, title, desc, css="", extra_defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-labelledby="ttl dsc">\n<title id="ttl">{t(title)}</title>\n'
            f'<desc id="dsc">{t(desc)}</desc>\n' + style(css) + defs(w, h, extra_defs) +
            f'\n<rect width="{w}" height="{h}" rx="14" fill="{BLACK}"/>'
            f'\n<rect width="{w}" height="{h}" rx="14" fill="url(#dots)"/>\n')

def close_svg(w, h, roll=False, roll_dur=7):
    out = ""
    if roll:
        out += (f'<rect x="0" y="-120" width="{w}" height="120" fill="url(#roll)">'
                f'<animate attributeName="y" from="-120" to="{h}" dur="{roll_dur}s" repeatCount="indefinite"/></rect>\n')
    out += f'<rect width="{w}" height="{h}" rx="14" fill="url(#scan)" pointer-events="none"/>\n'
    out += f'<rect width="{w}" height="{h}" rx="14" fill="url(#vig)" pointer-events="none"/>\n'
    out += f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="13" fill="none" stroke="{PH_DIM}" stroke-width="1.5"/>\n'
    out += '</svg>\n'
    return out

def header(w, left, right, y=30):
    """Thin machine header bar used on every panel."""
    return (f'<line x1="24" y1="{y+10}" x2="{w-24}" y2="{y+10}" stroke="{PH_FAINT}"/>\n'
            f'<text x="24" y="{y}" font-size="11" fill="{PH_MID}" letter-spacing="2">{t(left)}</text>\n'
            f'<text x="{w-24}" y="{y}" font-size="11" fill="{PH_DIM}" text-anchor="end" letter-spacing="2">{t(right)}</text>\n')

def txt(x, y, s, size=12, fill=PH, anchor="start", cls="", ls=0, weight=None, extra=""):
    c = f' class="{cls}"' if cls else ""
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    l = f' letter-spacing="{ls}"' if ls else ""
    wt = f' font-weight="{weight}"' if weight else ""
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}"{a}{l}{wt}{c}{extra}>{t(s)}</text>\n'

def discrete_opacity(windows, T, base=0, on=1):
    """SMIL discrete opacity. windows = list of (start,end) seconds inside cycle T."""
    pts = [(0.0, base)]
    for s, e in sorted(windows):
        pts.append((s / T, on))
        pts.append((min(e, T) / T, base))
    # collapse duplicate key times, keep last value
    clean = []
    for k, v in pts:
        k = round(k, 5)
        if clean and abs(clean[-1][0] - k) < 1e-9:
            clean[-1] = (k, v)
        else:
            clean.append((k, v))
    if clean[-1][0] >= 1:
        clean = clean[:-1] if len(clean) > 1 else clean
    kt = ";".join(f"{k:.5f}" for k, _ in clean)
    vs = ";".join(str(v) for _, v in clean)
    return (f'<animate attributeName="opacity" values="{vs}" keyTimes="{kt}" '
            f'dur="{T}s" calcMode="discrete" repeatCount="indefinite"/>')

def discrete_attr(attr, schedule, T):
    """schedule = list of (time_s, value) with first at 0."""
    kt = ";".join(f"{s/T:.5f}" for s, _ in schedule)
    vs = ";".join(str(v) for _, v in schedule)
    return (f'<animate attributeName="{attr}" values="{vs}" keyTimes="{kt}" '
            f'dur="{T}s" calcMode="discrete" repeatCount="indefinite"/>')

# 5x7 pixel glyphs for the LED matrix wordmark
GLYPHS = {
    "A": ["01110","10001","10001","11111","10001","10001","10001"],
    "G": ["01110","10001","10000","10111","10001","10001","01111"],
    "E": ["11111","10000","10000","11110","10000","10000","11111"],
    "N": ["10001","11001","10101","10011","10001","10001","10001"],
    "T": ["11111","00100","00100","00100","00100","00100","00100"],
    "B": ["11110","10001","10001","11110","10001","10001","11110"],
    "M": ["10001","11011","10101","10101","10001","10001","10001"],
    "O": ["01110","10001","10001","10001","10001","10001","01110"],
    "I": ["11111","00100","00100","00100","00100","00100","11111"],
    "D": ["11110","10001","10001","10001","10001","10001","11110"],
    "L": ["10000","10000","10000","10000","10000","10000","11111"],
    " ": ["00000"]*7,
}

def led_word(word, x, y, px=10, on=PH, off="#08240f", gap=1.6, cols_extra=0):
    """Returns (svg_off, svg_on, width). Off pixels drawn as dim matrix."""
    off_s, on_s = [], []
    cx = x
    for ch in word:
        g = GLYPHS[ch]
        for r, row in enumerate(g):
            for c, bit in enumerate(row):
                rx, ry = cx + c * px, y + r * px
                off_s.append(f'<rect x="{rx}" y="{ry}" width="{px-gap}" height="{px-gap}"/>')
                if bit == "1":
                    on_s.append(f'<rect x="{rx}" y="{ry}" width="{px-gap}" height="{px-gap}"/>')
        # inter-char column (off pixels)
        for r in range(7):
            off_s.append(f'<rect x="{cx+5*px}" y="{y+r*px}" width="{px-gap}" height="{px-gap}"/>')
        cx += 6 * px
    return (f'<g fill="{off}">' + "".join(off_s) + '</g>',
            f'<g fill="{on}">' + "".join(on_s) + '</g>', cx - x)
