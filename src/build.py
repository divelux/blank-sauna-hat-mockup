#!/usr/bin/env python3
"""Builds the Blank Sauna Hat Mockup: 4 layered SVG mockups (classic bell and bucket hat, front and 3/4 view),
PNG renders at 2000 px, a color sheet (preview.png) and a "how the layers work" sheet.

Each SVG (1000 x 1000) has the same named groups, bottom to top:
  ground-shadow     soft ellipse under the hat (delete it for a cut-out)
  base-felt         the hat itself; every shape inherits ONE fill set on this group -> change it to recolor the felt
  design-area       your artwork goes here: it is clipped to the printable/embroidery zone (clipPath #design-clip)
    placeholder-design   the sample monogram; delete it and paste your own art into design-area
  felt-texture      fine speckles, low opacity, so the felt does not look like plastic
  shading           flat dark and light shapes with opacity (no filters, no gradients); they sit over your design
  seams-and-loop    stitch lines, the edge trim, the hanging loop details
  design-area-guide dashed outline of the zone (hidden in the PNG renders; turn it on to place art)
This is an illustrative mockup, not a photo of a real hat. Needs: pip install resvg-py fonttools
License: artwork CC BY 4.0, script MIT - DIVELUX, https://diveluxsaunahat.com
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gfxlib as g

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = g.PAL
FELT = '#c9c4bb'          # light grey felt, the default
COLORS = [('light grey', '#c9c4bb'), ('graphite', '#5f5a55'), ('cream', '#eee3cc'), ('white', '#f4f1ea'),
          ('sand', '#cbb08a'), ('forest', '#4f6345'), ('night blue', '#33415a'), ('burgundy', '#6e2f33')]


def f(v):
    return ('%.1f' % v).rstrip('0').rstrip('.')


def texture(clip_id, box, n=900, seed=1):
    rnd = random.Random(seed)
    x0, y0, x1, y1 = box
    dots = []
    for _ in range(n):
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
        r = rnd.uniform(1.2, 3.2)
        c = '#000' if rnd.random() < .55 else '#fff'
        dots.append(f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(r * 1.6)}" ry="{f(r)}" transform="rotate({rnd.randint(0, 179)} {f(x)} {f(y)})" fill="{c}"/>')
    return f'<g id="felt-texture" clip-path="url(#{clip_id})" opacity=".09">{"".join(dots)}</g>'


def monogram(cx, cy, w, transform='', ink='#2a1b13'):
    """Placeholder design: a ring with two letters and a small birch leaf, drawn as paths (no fonts needed)."""
    s = w / 300
    letters = g.text_path('AB', 0, 0, 120, 'display', anchor='middle')
    leaf = 'M0 -34C20 -22 22 10 0 34C-22 10 -20 -22 0 -34z'
    return (f'<g id="placeholder-design" transform="translate({f(cx)} {f(cy)}) {transform} scale({f(s)})">'
            f'<circle r="140" fill="none" stroke="{ink}" stroke-width="9"/>'
            f'<circle r="122" fill="none" stroke="{ink}" stroke-width="3" stroke-dasharray="2 10" stroke-linecap="round"/>'
            f'<path d="{letters}" fill="{ink}" transform="translate(0 40)"/>'
            f'<g transform="translate(0 -88) rotate(90) scale(.55)"><path d="{leaf}" fill="{P["ember"]}"/></g>'
            f'<path d="M-60 78h120" stroke="{ink}" stroke-width="5" stroke-linecap="round"/></g>')


def doc(body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">'
            f'<title>{title} - DIVELUX blank sauna hat mockup (illustrative, not a photo)</title>{body}</svg>\n')


def guide(shape):
    return (f'<g id="design-area-guide" fill="none" stroke="{P["ember"]}" stroke-width="3" stroke-dasharray="12 9">{shape}'
            f'</g>')


# ------------------------------------------------------------------ classic bell hat
LOOP = 'M480 172C458 120 462 74 500 72C538 74 542 120 520 172ZM492 162C482 126 484 96 500 94C516 96 518 126 508 162Z'
BELL = 'M500 168C392 168 332 262 318 420C306 560 290 668 236 778Q500 818 764 778C710 668 694 560 682 420C668 262 608 168 500 168Z'


def ink_for(felt):
    r, gg, b = (int(felt[i:i + 2], 16) for i in (1, 3, 5))
    return '#f4ecdc' if (.299 * r + .587 * gg + .114 * b) < 120 else '#2a1b13'


def bell_front(felt=FELT, show_guide=True):
    zone = '<rect x="390" y="470" width="220" height="220" rx="20"/>'
    o = ['<defs><clipPath id="hat-clip"><path d="' + BELL + '"/></clipPath>'
         f'<clipPath id="design-clip">{zone}</clipPath></defs>',
         f'<g id="ground-shadow"><ellipse cx="500" cy="800" rx="320" ry="26" fill="#000" opacity=".12"/></g>',
         f'<g id="base-felt" fill="{felt}"><path fill-rule="evenodd" d="{LOOP}"/>'
         f'<path d="{BELL}"/><path d="M236 778Q500 818 764 778L768 798Q500 840 232 798Z"/></g>',
         f'<g id="design-area" clip-path="url(#design-clip)">{monogram(500, 580, 190, ink=ink_for(felt))}</g>',
         texture('hat-clip', (230, 160, 770, 830)),
         '<g id="shading" clip-path="url(#hat-clip)">'
         '<path d="M500 168C392 168 332 262 318 420C306 560 290 668 236 778Q300 790 352 795C338 690 340 560 352 420C366 280 420 196 500 168Z" fill="#000" opacity=".14"/>'
         '<path d="M500 168C608 168 668 262 682 420C694 560 710 668 764 778Q712 789 668 793C676 690 672 560 660 420C648 300 600 210 500 168Z" fill="#000" opacity=".07"/>'
         '<path d="M548 200C600 236 624 300 632 380C622 300 590 236 548 200Z" fill="#fff" opacity=".35"/>'
         '<path d="M470 190C430 214 404 260 392 330C410 270 436 228 470 190Z" fill="#fff" opacity=".22"/>'
         '<path d="M232 798Q500 840 768 798L766 788Q500 828 234 788Z" fill="#000" opacity=".18"/>'
         '<path d="M480 172C458 120 462 74 500 72C476 82 470 122 488 172Z" fill="#000" opacity=".12"/>'
         '</g>',
         '<g id="seams-and-loop" fill="none" stroke-linecap="round">'
         '<path d="M246 770Q500 808 754 770" stroke="#000" stroke-opacity=".28" stroke-width="3.5" stroke-dasharray="9 8"/>'
         '<path d="M480 168Q500 176 520 168" stroke="#000" stroke-opacity=".25" stroke-width="4"/></g>']
    if show_guide:
        o.append(guide(zone))
    return ''.join(o)


LOOP34 = 'M472 176C446 126 452 80 486 76C522 74 532 118 512 172ZM484 164C470 128 474 100 488 98C504 98 508 126 500 162Z'
BELL34 = 'M512 168C408 166 340 258 324 418C312 556 294 668 240 774Q470 822 770 786C716 676 700 558 690 420C676 262 620 170 512 168Z'


def bell_34(felt=FELT, show_guide=True):
    zone = '<path d="M468 470L668 452L676 676L476 700Z"/>'
    o = ['<defs><clipPath id="hat-clip"><path d="' + BELL34 + '"/></clipPath>'
         f'<clipPath id="design-clip">{zone}</clipPath></defs>',
         f'<g id="ground-shadow"><ellipse cx="520" cy="806" rx="320" ry="28" fill="#000" opacity=".12"/></g>',
         f'<g id="base-felt" fill="{felt}"><path fill-rule="evenodd" d="{LOOP34}"/>'
         f'<path d="{BELL34}"/><path d="M240 774Q470 822 770 786L772 806Q470 846 236 794Z"/></g>',
         f'<g id="design-area" clip-path="url(#design-clip)">{monogram(572, 576, 180, "skewY(-5) scale(.92 1)", ink=ink_for(felt))}</g>',
         texture('hat-clip', (230, 160, 780, 840), seed=2),
         '<g id="shading" clip-path="url(#hat-clip)">'
         # the far panel, turned away from the light
         '<path d="M512 168C408 166 340 258 324 418C312 556 294 668 240 774Q330 792 410 801C392 690 390 560 400 420C412 290 450 210 512 168Z" fill="#000" opacity=".17"/>'
         '<path d="M690 420C700 558 716 676 770 786Q738 792 706 795C704 690 694 560 680 430Z" fill="#000" opacity=".08"/>'
         '<path d="M560 196C618 232 646 300 654 390C640 304 610 238 560 196Z" fill="#fff" opacity=".35"/>'
         '<path d="M236 794Q470 846 772 806L770 796Q470 836 238 784Z" fill="#000" opacity=".18"/>'
         '</g>',
         '<g id="seams-and-loop" fill="none" stroke-linecap="round">'
         # the side seam runs over the crown, seen off-center in a 3/4 view
         '<path d="M512 170C452 220 420 300 410 420C400 560 404 690 412 800" stroke="#000" stroke-opacity=".3" stroke-width="4.5"/>'
         '<path d="M250 766Q470 812 760 778" stroke="#000" stroke-opacity=".28" stroke-width="3.5" stroke-dasharray="9 8"/>'
         '<path d="M478 174Q494 180 512 172" stroke="#000" stroke-opacity=".25" stroke-width="4"/></g>']
    if show_guide:
        o.append(guide(zone))
    return ''.join(o)


# ------------------------------------------------------------------ bucket hat
CROWN = 'M312 560C306 420 330 300 380 262C420 234 580 234 620 262C670 300 694 420 688 560Z'
BRIM = 'M318 520C230 548 152 604 130 672C126 686 132 694 146 701C236 744 360 764 500 764C640 764 764 744 854 701C868 694 874 686 870 672C848 604 770 548 682 520Z'


def bucket_front(felt=FELT, show_guide=True):
    zone = '<rect x="400" y="330" width="200" height="150" rx="16"/>'
    o = ['<defs><clipPath id="hat-clip"><path d="' + CROWN + BRIM + '"/></clipPath>'
         f'<clipPath id="design-clip">{zone}</clipPath></defs>',
         f'<g id="ground-shadow"><ellipse cx="500" cy="770" rx="370" ry="20" fill="#000" opacity=".14"/></g>',
         f'<g id="base-felt" fill="{felt}"><path d="{BRIM}"/><path d="{CROWN}"/></g>',
         f'<g id="design-area" clip-path="url(#design-clip)">{monogram(500, 405, 140, ink=ink_for(felt))}</g>',
         texture('hat-clip', (120, 230, 880, 770), seed=3),
         '<g id="shading" clip-path="url(#hat-clip)">'
         # underside of the brim and the crown sides
         '<path d="M110 660C220 742 360 780 500 780C640 780 780 742 890 660L880 640C780 700 630 720 500 720C370 720 220 700 120 640Z" fill="#000" opacity=".16"/>'
         '<path d="M312 560C306 420 330 300 380 262C400 248 430 241 460 238C410 280 384 400 386 560Z" fill="#000" opacity=".13"/>'
         '<path d="M688 560C694 420 670 300 620 262C604 251 580 244 556 240C604 290 624 400 620 560Z" fill="#000" opacity=".06"/>'
         # crown shadow cast on the brim
         '<path d="M312 556C380 586 620 586 688 556L700 580C620 612 380 612 300 580Z" fill="#000" opacity=".16"/>'
         '<path d="M420 252C470 242 530 242 580 252C540 262 460 262 420 252Z" fill="#fff" opacity=".3"/>'
         '</g>',
         '<g id="seams-and-loop" fill="none" stroke-linecap="round">'
         '<path d="M314 520C380 540 620 540 686 520" stroke="#000" stroke-opacity=".3" stroke-width="4"/>'
         '<path d="M318 548C380 566 620 566 682 548" stroke="#000" stroke-opacity=".3" stroke-width="4"/>'
         '<path d="M150 684C240 728 370 748 500 748C630 748 760 728 850 684" stroke="#000" stroke-opacity=".26" stroke-width="3.5" stroke-dasharray="9 8"/>'
         '<path d="M178 664C262 704 380 722 500 722C620 722 738 704 822 664" stroke="#000" stroke-opacity=".2" stroke-width="3.5" stroke-dasharray="9 8"/>'
         '</g>']
    if show_guide:
        o.append(guide(zone))
    return ''.join(o)


CROWN34 = 'M300 548C298 412 326 300 380 262C424 232 590 230 634 262C688 302 712 416 704 560Z'
BRIM34 = 'M308 506C210 530 132 586 118 654C116 668 120 678 132 686C214 738 350 762 512 768C666 772 800 748 872 712C886 704 890 694 886 682C866 610 790 556 698 522Z'


def bucket_34(felt=FELT, show_guide=True):
    zone = '<path d="M452 336L640 322L650 474L460 492Z"/>'
    o = ['<defs><clipPath id="hat-clip"><path d="' + CROWN34 + BRIM34 + '"/></clipPath>'
         f'<clipPath id="design-clip">{zone}</clipPath></defs>',
         f'<g id="ground-shadow"><ellipse cx="505" cy="772" rx="378" ry="20" fill="#000" opacity=".14"/></g>',
         f'<g id="base-felt" fill="{felt}"><path d="{BRIM34}"/><path d="{CROWN34}"/></g>',
         f'<g id="design-area" clip-path="url(#design-clip)">{monogram(550, 408, 134, "skewY(-4) scale(.92 1)", ink=ink_for(felt))}</g>',
         texture('hat-clip', (110, 225, 890, 775), seed=4),
         '<g id="shading" clip-path="url(#hat-clip)">'
         '<path d="M100 640C200 734 350 780 512 786C666 790 820 760 900 700L900 670C800 716 660 730 512 728C360 724 220 700 110 620Z" fill="#000" opacity=".16"/>'
         '<path d="M300 548C298 412 326 300 380 262C404 246 436 238 466 235C412 286 400 400 410 552Z" fill="#000" opacity=".17"/>'
         '<path d="M704 560C712 416 688 302 634 262C620 252 600 246 580 242C632 296 656 410 656 562Z" fill="#000" opacity=".05"/>'
         '<path d="M300 544C380 578 630 584 704 556L716 580C630 614 380 606 288 570Z" fill="#000" opacity=".16"/>'
         '<path d="M470 250C520 240 570 242 610 252C574 262 506 262 470 250Z" fill="#fff" opacity=".3"/>'
         '</g>',
         '<g id="seams-and-loop" fill="none" stroke-linecap="round">'
         '<path d="M468 240C424 290 406 400 412 552" stroke="#000" stroke-opacity=".28" stroke-width="4.5"/>'
         '<path d="M302 508C380 532 630 538 700 520" stroke="#000" stroke-opacity=".3" stroke-width="4"/>'
         '<path d="M304 536C380 558 630 564 702 548" stroke="#000" stroke-opacity=".3" stroke-width="4"/>'
         '<path d="M138 668C222 722 360 748 512 752C660 756 784 734 862 698" stroke="#000" stroke-opacity=".26" stroke-width="3.5" stroke-dasharray="9 8"/>'
         '</g>']
    if show_guide:
        o.append(guide(zone))
    return ''.join(o)


VIEWS = [('classic-bell-hat-front', 'Classic bell sauna hat, front', bell_front),
         ('classic-bell-hat-three-quarter', 'Classic bell sauna hat, 3/4 view', bell_34),
         ('bucket-hat-front', 'Bucket sauna hat, front', bucket_front),
         ('bucket-hat-three-quarter', 'Bucket sauna hat, 3/4 view', bucket_34)]


def main():
    for d in ('svg', 'png'):
        os.makedirs(os.path.join(ROOT, d), exist_ok=True)
    for name, title, fn in VIEWS:
        s = doc(fn(), title)
        open(os.path.join(ROOT, 'svg', name + '.svg'), 'w').write(s)
        # PNG renders: transparent, guide hidden; one with the sample design and one blank
        g.render(doc(fn(show_guide=False), title), os.path.join(ROOT, 'png', name + '.png'), width=2000)
        blank = doc(fn(show_guide=False), title)
        a = blank.index('<g id="placeholder-design"')
        b = blank.index('</g></g>', a) + 4
        g.render(blank[:a] + blank[b:], os.path.join(ROOT, 'png', name + '-blank.png'), width=2000)
    # preview: every view in several felt colors
    cells = []
    for i, (name, title, fn) in enumerate(VIEWS * 2):
        col = COLORS[i % len(COLORS)]
        inner = fn(felt=col[1], show_guide=False).replace('id="', f'id="c{i}-').replace('url(#', f'url(#c{i}-')
        cells.append((f'<svg x="20" y="10" width="320" height="320" viewBox="0 0 1000 1000">{inner}</svg>', f'{"Bell" if "bell" in name else "Bucket"} {"front" if "front" in name else "3/4"} · {col[0]}'))
    g.render(g.contact_sheet(cells, 4, 360, 370, 'Blank Sauna Hat Mockup',
                             'Classic bell and bucket hat, front and 3/4 view · layered SVG · any felt color · illustrative, not a photo',
                             label_size=15), os.path.join(ROOT, 'preview.png'))
    # how-to sheet: the layers of one view side by side
    full = bell_front()
    steps = []
    order = ['ground-shadow', 'base-felt', 'design-area', 'felt-texture', 'shading', 'seams-and-loop', 'design-area-guide']
    for k in range(1, len(order) + 1):
        keep = order[:k]
        body = full
        for gid in order[k:]:
            body = body.replace(f'<g id="{gid}"', f'<g id="{gid}" display="none"')
        body = body.replace('id="', f'id="s{k}-').replace('url(#', f'url(#s{k}-')
        steps.append((f'<svg x="20" y="10" width="300" height="300" viewBox="0 0 1000 1000">{body}</svg>', '+ ' + order[k - 1]))
    g.render(g.contact_sheet(steps, 4, 340, 350, 'How the layers stack',
                             'Group names inside every SVG, bottom to top. Put your art in design-area.', label_size=15,
                             width=1440), os.path.join(ROOT, 'layers.png'))
    print('ok')


if __name__ == '__main__':
    main()
