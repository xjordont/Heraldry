#!/usr/bin/env python3
"""Draw the coin mark as SVG. (The hand-drawn chapter arms and signature candidates below are retired;
the approved arms and logo are made by tools/prepare_marks.py.) Deterministic; writes cream and white variants (the paper colour shows
inside the marks) to typst/templates/marks/<substrate>/.

    python3 tools/make_heraldry_marks.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "typst/templates/marks"
PAPER = {"cream": "#FCFAF5", "white": "#FFFFFF"}
INK = "#000000"
SHIELD = "M0,0 H100 V50 C100,94 62,108 50,120 C38,108 0,94 0,50 Z"

# Heraldic hatching (the Petra Sancta system, which lets black and white show tinctures):
# argent plain, gules vertical, azure horizontal, vert bend, purpure bend sinister.
HATCH = {
    "argent": "",
    "gules": '<path d="{}" stroke="#000" stroke-width="0.9"/>'.format(" ".join(f"M{x},0 V120" for x in range(3, 100, 6))),
    "azure": '<path d="{}" stroke="#000" stroke-width="0.9"/>'.format(" ".join(f"M0,{y} H100" for y in range(3, 120, 6))),
    "vert": '<path d="{}" stroke="#000" stroke-width="0.9"/>'.format(" ".join(f"M{x},0 L{x + 120},120" for x in range(-120, 100, 8))),
    "purpure": '<path d="{}" stroke="#000" stroke-width="0.9"/>'.format(" ".join(f"M{x},0 L{x - 120},120" for x in range(0, 220, 8))),
}


def sword(rot):
    """A longsword pointing up, rotated about (50,58)."""
    return f'''<g transform="rotate({rot} 50 58)">
  <path d="M45,78 L45,20 L50,8 L55,20 L55,78 Z"/>
  <path d="M50,20 V74" stroke="P" stroke-width="1.4"/>
  <path d="M31,77 Q50,72 69,77 L69,84 Q50,79 31,84 Z"/>
  <rect x="46.8" y="84" width="6.4" height="14" rx="1.2"/>
  <path d="M47,88 L53,90 M47,93 L53,95" stroke="P" stroke-width="1"/>
  <circle cx="50" cy="102" r="5"/>
</g>'''


CHARGES = {
    # 1 The World of Heraldry: the orb and cross (globus cruciger), the world under a vanished crown
    1: ("azure", '''<path d="M47,16 H53 V25 H61 V31 H53 V38 H47 V31 H39 V25 H47 Z"/>
<circle cx="50" cy="62" r="24"/>
<path d="M26,58 H74 V65 H26 Z M46.5,38 H53.5 V58 H46.5 Z" fill="P"/>
<circle cx="61" cy="73" r="2.4" fill="P"/><circle cx="39" cy="73" r="2.4" fill="P"/>'''),
    # 2 Core Mechanics: a die, its faces showing one, two and three
    2: ("argent", '''<path d="M50,24 L78,39 L50,54 L22,39 Z"/>
<path d="M22,39 L50,54 L50,90 L22,75 Z"/>
<path d="M50,54 L78,39 L78,75 L50,90 Z"/>
<path d="M22,39 L50,54 L78,39 M50,54 V90" stroke="P" stroke-width="1.6" fill="none"/>
<ellipse cx="50" cy="39" rx="5" ry="3" fill="P"/>
<ellipse cx="30" cy="52" rx="3" ry="3.6" fill="P"/><ellipse cx="42" cy="72" rx="3" ry="3.6" fill="P"/>
<ellipse cx="58" cy="54" rx="3" ry="3.6" fill="P"/><ellipse cx="64" cy="64" rx="3" ry="3.6" fill="P"/><ellipse cx="70" cy="74" rx="3" ry="3.6" fill="P"/>'''),
    # 3 The Game Round: an hourglass, the turning of rounds
    3: ("gules", '''<rect x="25" y="18" width="50" height="7" rx="1.5"/><rect x="25" y="91" width="50" height="7" rx="1.5"/>
<rect x="28" y="25" width="4" height="66"/><rect x="68" y="25" width="4" height="66"/>
<path d="M36,25 C36,46 47,51 48,58 C47,65 36,70 36,91 H64 C64,70 53,65 52,58 C53,51 64,46 64,25 Z" fill="P" stroke="#000" stroke-width="3"/>
<path d="M41,33 H59 C58,42 52,47 50,52 C48,47 42,42 41,33 Z"/>
<path d="M50,56 V78" stroke="#000" stroke-width="1.4"/>
<path d="M38.5,89 C40,80 46,77 50,76 C54,77 60,80 61.5,89 Z"/>'''),
    # 4 Actions and Movement: a rowel spur
    4: ("vert", '''<path d="M34,16 H58 V60 C66,62 76,66 84,74 C88,78 88,88 84,90 H34 Z"/>
<rect x="31" y="14" width="30" height="7" rx="2"/>
<path d="M34,90 H86 V95 H34 Z"/>
<path d="M38,30 H54 M38,40 H54" stroke="P" stroke-width="1.4"/>
<path d="M34,74 H24 V70 H34 Z"/>
<path d="M16,72 L18,63 L20,69 L27,64 L22,71 L30,72 L22,74 L27,80 L20,75 L18,82 L16,75 L9,80 L14,74 L6,72 L14,70 L9,64 Z"/>
<circle cx="18" cy="72" r="2.2" fill="P"/>'''),
    # 5 Combat: two swords in saltire
    5: ("gules", sword(-33) + sword(33)),
    # 6 Your Adventuring Party: a war banner on its lance
    6: ("azure", '''<rect x="28" y="20" width="5" height="84" rx="1.5"/>
<path d="M30.5,9 L35,16 L30.5,23 L26,16 Z"/>
<path d="M33,24 H80 L70,38 L80,52 L73,52 L70,47 L67,52 H33 Z"/>
<path d="M46,30 L52,38 L46,46 L40,38 Z" fill="P"/><path d="M60,32 L64,38 L60,44 L56,38 Z" fill="P"/>'''),
    # 7 Equipment and Items: a great helm
    7: ("argent", '''<path d="M28,40 C28,20 72,20 72,40 V86 C72,94 28,94 28,86 Z"/>
<rect x="31" y="50" width="38" height="5" fill="P"/><rect x="48" y="49" width="4" height="7"/>
<path d="M50,22 V48 M50,57 V92" stroke="P" stroke-width="1.6"/>
<circle cx="59" cy="66" r="1.5" fill="P"/><circle cx="64" cy="66" r="1.5" fill="P"/><circle cx="59" cy="72" r="1.5" fill="P"/>
<circle cx="64" cy="72" r="1.5" fill="P"/><circle cx="59" cy="78" r="1.5" fill="P"/><circle cx="64" cy="78" r="1.5" fill="P"/>
<path d="M28,40 C30,36 34,35 36,36" stroke="P" stroke-width="1.2" fill="none"/>'''),
    # 8 Powers and Traditions: a flame rising from a brazier
    8: ("purpure", '''<path d="M50,14 C58,30 72,38 68,60 C66,74 58,82 50,82 C40,82 31,74 32,60 C32,48 41,44 44,32 C48,42 50,46 52,48 C55,38 53,28 50,14 Z"/>
<path d="M50,50 C56,58 60,64 58,72 C57,78 53,80 50,80 C46,80 42,77 43,70 C44,64 48,60 50,50 Z" fill="P"/>
<path d="M28,82 H72 L64,96 H36 Z"/><rect x="44" y="96" width="12" height="4"/><rect x="38" y="100" width="24" height="4" rx="1"/>'''),
    # 9 Monsters: a wyvern's head erased, jaws open
    9: ("vert", '''<path d="M30,100 L34,93 L28,88 L35,82 L29,76 L36,71 C36,57 40,46 47,38 L40,20 L53,33 C59,30 65,32 70,37 L86,46 L89,52 L76,55 L86,62 L84,65 L72,66 C64,70 59,76 56,84 L54,100 Z"/>
<path d="M47,38 L44,30 L50,35 Z M53,33 L55,25 L58,32 Z" fill="P"/>
<path d="M60,41 C64,38 68,40 69,43 C66,45 62,45 60,41 Z" fill="P"/><circle cx="66" cy="42.4" r="1.2"/>
<circle cx="84" cy="49" r="1.3" fill="P"/>
<path d="M76,55 L78,58.5 L80,55.4 L82,59 L84,56 Z M74,62 L76,59 L78,62.4 L80,59.6 L82,62.6 Z" fill="P"/>
<path d="M42,52 L36,56 L43,57 L38,62 L45,61" stroke="P" stroke-width="1.3" fill="none"/>'''),
    # 10 Scenarios: a ruined arch over rubble
    10: ("argent", '''<path d="M18,96 V48 C18,22 42,14 56,22 L52,30 L57,34 L50,40 C40,32 32,38 32,50 V96 Z"/>
<path d="M66,96 V56 L68,50 L72,54 L75,47 L80,52 L82,48 V96 Z"/>
<path d="M18,58 H32 M18,70 H32 M18,82 H32 M25,58 V70 M22,70 V82 M28,82 V96 M66,64 H82 M66,78 H82 M74,64 V78 M70,78 V96" stroke="P" stroke-width="1.3"/>
<path d="M22,40 L30,34 M30,28 L38,24" stroke="P" stroke-width="1.3"/>
<rect x="10" y="96" width="80" height="6"/>
<path d="M42,96 L45,88 L54,90 L56,96 Z M58,96 L60,92 L64,93 L63,96 Z"/>'''),
    # 11 Campaign Play: a castle of three towers
    11: ("gules", '''<path d="M22,42 H25 V38 H28 V42 H31 V38 H34 V42 H37 V62 H63 V42 H66 V38 H69 V42 H72 V38 H75 V42 H78 V96 H22 Z"/>
<path d="M39,30 H42 V25 H45 V30 H48 V25 H52 V30 H55 V25 H58 V30 H61 V96 H39 Z"/>
<path d="M44,96 V82 C44,74 56,74 56,82 V96 Z" fill="P"/>
<rect x="48.5" y="40" width="3" height="10" fill="P"/><rect x="28" y="54" width="3" height="8" fill="P"/><rect x="69" y="54" width="3" height="8" fill="P"/>'''),
    # 12 Learn to Play: a key, wards down
    12: ("azure", '''<circle cx="50" cy="30" r="14"/>
<path d="M50,21 L53,27 L59,30 L53,33 L50,39 L47,33 L41,30 L47,27 Z" fill="P"/>
<rect x="46.5" y="42" width="7" height="52"/><rect x="44" y="44" width="12" height="4" rx="1"/>
<path d="M53.5,76 H66 V82 H61 V86 H66 V94 H53.5 Z"/>'''),
    # 13 Basic Mode: a lantern
    13: ("argent", '''<circle cx="50" cy="17" r="4.5" fill="none" stroke="#000" stroke-width="2.4"/>
<path d="M36,32 L50,21 L64,32 Z"/><rect x="34" y="32" width="32" height="4"/>
<rect x="36" y="36" width="28" height="44"/>
<rect x="39.5" y="39" width="9" height="38" fill="P"/><rect x="51.5" y="39" width="9" height="38" fill="P"/>
<path d="M50,52 C53,58 55,62 53,67 C52,70 48,70 47,67 C45,62 48,58 50,52 Z"/>
<rect x="32" y="80" width="36" height="5"/><rect x="36" y="85" width="5" height="6"/><rect x="59" y="85" width="5" height="6"/>'''),
    # 14 Rules Reference: an open book with a ribbon marker
    14: ("purpure", '''<path d="M50,36 C40,28 28,28 18,32 V82 C28,78 40,78 50,86 Z" fill="P" stroke="#000" stroke-width="3.4" stroke-linejoin="round"/>
<path d="M50,36 C60,28 72,28 82,32 V82 C72,78 60,78 50,86 Z" fill="P" stroke="#000" stroke-width="3.4" stroke-linejoin="round"/>
<path d="M24,42 C32,39 40,39 45,43 M24,50 C32,47 40,47 45,51 M24,58 C32,55 40,55 45,59 M24,66 C32,63 40,63 45,67 M55,43 C60,39 68,39 76,42 M55,51 C60,47 68,47 76,50 M55,59 C60,55 68,55 76,58 M55,67 C60,63 68,63 76,66" stroke="#000" stroke-width="1.8" fill="none"/>
<path d="M50,86 V100 L46,96 L42,100 V84" />'''),
    # 15 Index: a quill pen
    15: ("azure", '''<path d="M28,96 C36,74 50,46 76,16 C74,40 64,62 44,80 C40,84 34,88 31,92 Z"/>
<path d="M33,90 C44,70 58,46 74,20" stroke="P" stroke-width="1.6" fill="none"/>
<path d="M48,62 L58,58 M53,52 L63,48 M58,43 L67,38 M43,72 L52,69" stroke="P" stroke-width="1.1"/>
<path d="M28,96 L25,104 L31,98 Z"/>'''),
}

SIGNATURES = {
    # Candidate signature marks (owner 2026-10-12: workshop the broken crown and show five or more)
    "broken-crown": ("The Broken Crown", "kings are buried", '''<path d="M14,70 H86 V88 H14 Z"/>
<path d="M14,70 L10,40 L24,56 L32,26 L42,54 L50,14 L58,54 L64,44 L66,49 L69,41 L73,56 L90,40 L86,70 Z"/>
<circle cx="10" cy="38" r="4"/><circle cx="32" cy="23" r="4"/><circle cx="50" cy="11" r="4.4"/><circle cx="90" cy="38" r="4"/>
<path d="M30,79 L34,75 L38,79 L34,83 Z M50,79 L54,75 L58,79 L54,83 Z M70,79 L74,75 L78,79 L74,83 Z" fill="P"/>
<path d="M60,70 L56,78 L61,82 L57,88" stroke="P" stroke-width="2" fill="none"/>'''),
    "crown-pierced": ("The Pierced Crown", "an oath broken by the sword", '''<path d="M18,60 H82 V76 H18 Z M18,60 L16,38 L30,50 L38,30 L50,46 L62,30 L70,50 L84,38 L82,60 Z"/>
<circle cx="16" cy="36" r="3.4"/><circle cx="38" cy="27" r="3.4"/><circle cx="62" cy="27" r="3.4"/><circle cx="84" cy="36" r="3.4"/>
<path d="M47,6 H53 V92 L50,99 L47,92 Z" stroke="P" stroke-width="2.4"/>
<path d="M36,14 Q50,10 64,14 V19 Q50,15 36,19 Z" stroke="P" stroke-width="1.6"/>
<path d="M33,68 L37,64 L41,68 L37,72 Z M59,68 L63,64 L67,68 L63,72 Z" fill="P"/>'''),
    "tattered-banner": ("The Rotting Banner", "banners rot in the rain", '''<rect x="22" y="8" width="5" height="92" rx="1.5"/><path d="M24.5,0 L29,7 L24.5,14 L20,7 Z"/>
<path d="M27,12 H84 L80,22 L86,30 L78,38 L84,48 L74,52 L76,62 L66,58 L62,68 L56,60 L50,70 L46,60 L38,66 L36,56 L27,58 Z"/>
<path d="M44,22 L54,34 L44,46 L34,34 Z" fill="P"/><circle cx="64" cy="26" r="2" fill="P"/><circle cx="70" cy="40" r="1.6" fill="P"/>'''),
    "broken-sword": ("The Broken Oath", "oaths are broken", '''<path d="M46,60 V22 L52,14 L50,30 L54,24 V60 Z"/>
<path d="M50,10 L56,4 L54,12 L58,9" stroke="#000" stroke-width="2" fill="none"/>
<path d="M28,60 Q50,54 72,60 L72,66 Q50,60 28,66 Z"/><circle cx="26" cy="63" r="4"/><circle cx="74" cy="63" r="4"/>
<rect x="46.5" y="66" width="7" height="20" rx="1.5"/><path d="M47,70 L53,73 M47,76 L53,79 M47,82 L53,85" stroke="P" stroke-width="1.2"/>
<path d="M50,86 L56,92 L50,98 L44,92 Z"/>
<path d="M62,82 L72,72 L75,75 L65,85 Z M66,88 L70,92" stroke="#000" stroke-width="1"/>'''),
    "black-rose": ("The Black Rose", "withered beauty", '''<path d="M50,96 C47,84 47,72 50,62" stroke="#000" stroke-width="4" fill="none"/>
<path d="M48.5,86 L41,84 L48,81 Z M50,76 L57,73 L51,72 Z"/>
<path d="M50,74 C40,70 30,74 26,82 C36,84 44,80 50,74 Z"/>
<path d="M28,40 C26,26 38,16 50,18 C62,16 74,26 72,40 C72,54 62,64 50,64 C38,64 28,54 28,40 Z"/>
<path d="M50,26 C58,26 62,34 58,40 C54,46 46,46 42,40 C38,34 42,26 50,26 Z" fill="none" stroke="P" stroke-width="2"/>
<path d="M50,32 C53,33 54,37 50,39 C46,37 47,33 50,32 Z" fill="P"/>
<path d="M33,36 C34,50 42,56 50,56 C58,56 66,50 67,36" fill="none" stroke="P" stroke-width="2"/>
<path d="M40,20 C44,24 46,28 46,32 M60,20 C56,24 54,28 54,32" fill="none" stroke="P" stroke-width="1.6"/>'''),
    "raven": ("The Carrion Raven", "the roads grow dark", '''<path d="M86,28 L74,26 C70,20 62,18 56,22 C50,26 48,34 50,42 C40,46 30,56 26,68 L10,80 L22,80 L16,88 L30,80 C38,82 48,80 56,74 C64,68 68,58 66,48 C70,42 70,36 70,32 Z"/>
<circle cx="63" cy="27" r="2" fill="P"/>
<path d="M52,50 C44,56 38,64 36,72 M58,52 C52,60 48,68 46,74" stroke="P" stroke-width="1.4" fill="none"/>
<path d="M44,78 L42,90 M52,76 L52,90" stroke="#000" stroke-width="2.6"/>
<path d="M38,90 L46,90 M48,90 L56,90" stroke="#000" stroke-width="2"/>
<path d="M18,92 C40,90 64,90 88,94 L88,97 C64,94 40,94 18,96 Z"/>'''),
}

COIN = '''<circle cx="50" cy="50" r="48"/>
{beads}
<circle cx="50" cy="50" r="35" fill="none" stroke="P" stroke-width="3"/>
<path d="M44,17 H56 V44 H83 V56 H56 V83 H44 V56 H17 V44 H44 Z" fill="P"/>
<path d="M47.5,20 H52.5 V47.5 H80 V52.5 H52.5 V80 H47.5 V52.5 H20 V47.5 H47.5 Z"/>
<circle cx="31" cy="31" r="5" fill="P"/><circle cx="69" cy="31" r="5" fill="P"/><circle cx="31" cy="69" r="5" fill="P"/><circle cx="69" cy="69" r="5" fill="P"/>'''


def svg(w, h, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}pt" height="{h}pt">\n{body}\n</svg>\n'


def arms_svg(n, paper):
    tincture, charge = CHARGES[n]
    charge = charge.replace('"P"', f'"{paper}"')
    hatch = HATCH[tincture]
    # fimbriation: the charge drawn first as a paper halo, so it stays crisp on the hatched field
    halo = f'<g fill="{paper}" stroke="{paper}" stroke-width="5" stroke-linejoin="round">{charge}</g>'
    body = f'''<defs><clipPath id="s"><path d="{SHIELD}"/></clipPath></defs>
<g transform="translate(6,6)">
<path d="{SHIELD}" fill="{paper}"/>
<g clip-path="url(#s)">{hatch}{halo}<g fill="#000">{charge}</g></g>
<path d="{SHIELD}" fill="none" stroke="#000" stroke-width="5"/>
<path d="M6,6 H94 V50 C94,88 60,100 50,111 C40,100 6,88 6,50 Z" fill="none" stroke="#000" stroke-width="1.2"/>
</g>'''
    return svg(112, 132, body)


def main():
    import math
    beads = "\n".join(f'<circle cx="{50 + 42 * math.cos(a):.2f}" cy="{50 + 42 * math.sin(a):.2f}" r="2.6" fill="P"/>'
                      for a in (i * math.pi / 15 for i in range(30)))
    for sub, paper in PAPER.items():
        d = OUT / sub
        d.mkdir(parents=True, exist_ok=True)
        # The hand-drawn arms and signature candidates are retired (owner approval 2026-10-13): the
        # chapter arms and the logo now come from tools/prepare_marks.py. Only the coin is drawn here.
        coin = COIN.format(beads=beads).replace('"P"', f'"{paper}"')
        (d / "coin.svg").write_text(svg(100, 100, f'<g fill="#000">{coin}</g>'))
        rev = coin.replace(f'"{paper}"', '"#TMP"').replace('"#000"', f'"{paper}"').replace('<circle cx="50" cy="50" r="48"/>', f'<circle cx="50" cy="50" r="48" fill="{paper}"/>')
        rev = rev.replace('"#TMP"', '"#000"')
        (d / "coin-reversed.svg").write_text(svg(100, 100, f'<g fill="{paper}">{rev}</g>'))
    print(f"wrote the coin to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
