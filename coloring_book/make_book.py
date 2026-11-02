"""Generate a 16-page (cover + 15) chibi baby-animal coloring book, 8.5x11 in."""
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import math, os

W, H = letter
LW = 3.2          # standard outline width
BORDER_W = 6      # identical border on every page
M = 36            # border margin (0.5 in)

def border(c):
    c.setLineWidth(BORDER_W)
    c.roundRect(M, M, W - 2 * M, H - 2 * M, 18, stroke=1, fill=0)
    c.setLineWidth(LW)

def circ(c, x, y, r, fill=0):
    c.circle(x, y, r, stroke=1, fill=fill)

def ell(c, x, y, rx, ry, fill=0):
    c.ellipse(x - rx, y - ry, x + rx, y + ry, stroke=1, fill=fill)

def poly(c, pts, fill=0, close=True):
    p = c.beginPath(); p.moveTo(*pts[0])
    for q in pts[1:]: p.lineTo(*q)
    if close: p.close()
    c.drawPath(p, stroke=1, fill=fill)

def arc(c, x, y, r, a0, ext):
    c.arc(x - r, y - r, x + r, y + r, a0, ext)

# ---------------- animals ----------------
def animal(c, x, y, s, kind, arms="down"):
    """x,y = feet center. Chibi: big head, small body."""
    r = 62 * s                       # head radius
    by = y + 34 * s                  # body center
    hy = by + 30 * s + r * 0.85      # head center
    # feet
    ell(c, x - 18 * s, y + 6 * s, 14 * s, 8 * s)
    ell(c, x + 18 * s, y + 6 * s, 14 * s, 8 * s)
    # tail
    if kind == "bunny": circ(c, x + 34 * s, by - 6 * s, 10 * s)
    if kind == "fox":
        poly(c, [(x + 30*s, by - 10*s), (x + 75*s, by + 20*s), (x + 62*s, by - 18*s)])
    if kind == "cat":
        c.bezier(x + 30*s, by - 15*s, x + 70*s, by - 10*s, x + 60*s, by + 40*s, x + 75*s, by + 45*s)
    # body
    ell(c, x, by, 34 * s, 32 * s)
    ell(c, x, by - 4 * s, 18 * s, 18 * s)  # tummy patch
    # arms
    if arms == "down":
        ell(c, x - 34 * s, by + 2 * s, 9 * s, 16 * s)
        ell(c, x + 34 * s, by + 2 * s, 9 * s, 16 * s)
    elif arms == "front":
        ell(c, x - 18 * s, by + 10 * s, 12 * s, 9 * s)
        ell(c, x + 18 * s, by + 10 * s, 12 * s, 9 * s)
    elif arms == "up":
        ell(c, x - 40 * s, by + 26 * s, 9 * s, 16 * s)
        ell(c, x + 40 * s, by + 26 * s, 9 * s, 16 * s)
    # ears (behind head drawn first, filled white)
    c.setFillColorRGB(1, 1, 1)
    if kind in ("bear", "panda", "mouse"):
        er = r * (0.42 if kind == "mouse" else 0.3)
        for sx in (-1, 1):
            circ(c, x + sx * r * 0.72, hy + r * 0.72, er, fill=1)
            circ(c, x + sx * r * 0.72, hy + r * 0.72, er * 0.5, fill=kind == "panda")
            c.setFillColorRGB(1, 1, 1)
    elif kind == "bunny":
        for sx in (-1, 1):
            ell(c, x + sx * r * 0.38, hy + r * 1.35, r * 0.2, r * 0.6, fill=1)
            ell(c, x + sx * r * 0.38, hy + r * 1.35, r * 0.09, r * 0.42)
    elif kind in ("cat", "fox"):
        for sx in (-1, 1):
            poly(c, [(x + sx * r * 0.3, hy + r * 0.85), (x + sx * r * 0.85, hy + r * 1.25),
                     (x + sx * r * 0.88, hy + r * 0.45)], fill=1)
    elif kind == "pig":
        for sx in (-1, 1):
            poly(c, [(x + sx * r * 0.35, hy + r * 0.85), (x + sx * r * 0.8, hy + r * 1.15),
                     (x + sx * r * 0.85, hy + r * 0.55)], fill=1)
    elif kind == "chick":
        c.bezier(x, hy + r, x - 8*s, hy + r + 20*s, x + 10*s, hy + r + 22*s, x + 6*s, hy + r + 4*s)
    # head
    circ(c, x, hy, r, fill=1)
    c.setFillColorRGB(0, 0, 0)
    # face
    ey = hy - r * 0.05
    if kind == "panda":
        for sx in (-1, 1):
            ell(c, x + sx * r * 0.36, ey, r * 0.2, r * 0.25)
    for sx in (-1, 1):
        circ(c, x + sx * r * 0.36, ey, r * 0.1, fill=1)
        c.setFillColorRGB(1, 1, 1)
        circ(c, x + sx * r * 0.36 + r * 0.03, ey + r * 0.04, r * 0.03, fill=1)
        c.setFillColorRGB(0, 0, 0)
        ell(c, x + sx * r * 0.6, ey - r * 0.25, r * 0.12, r * 0.07)  # blush
    my = hy - r * 0.35
    if kind == "pig":
        ell(c, x, my + r * 0.05, r * 0.2, r * 0.14)
        circ(c, x - r * 0.07, my + r * 0.05, r * 0.03, fill=1)
        circ(c, x + r * 0.07, my + r * 0.05, r * 0.03, fill=1)
    elif kind == "chick":
        poly(c, [(x - r * 0.13, my + r * 0.12), (x + r * 0.13, my + r * 0.12), (x, my - r * 0.08)])
    else:
        if kind in ("bear", "panda", "fox"):
            ell(c, x, my + r * 0.06, r * 0.22, r * 0.16)
        ell(c, x, my + r * 0.12, r * 0.07, r * 0.05, fill=1)
        arc(c, x - r * 0.07, my + r * 0.02, r * 0.07, 200, 140)
        arc(c, x + r * 0.07, my + r * 0.02, r * 0.07, 200, 140)
        if kind in ("cat", "mouse", "bunny"):
            for sx in (-1, 1):
                for dy in (0.06, -0.04):
                    c.line(x + sx * r * 0.2, my + r * dy, x + sx * r * 0.5, my + r * (dy * 2))
    if kind == "chick":  # wings instead of arms already drawn; fine
        pass
    return hy, r

# ---------------- props / scenery ----------------
def ground(c, y=120):
    c.line(M + 4, y, W - M - 4, y)

def sun(c, x, y, r=34):
    circ(c, x, y, r)
    for i in range(10):
        a = math.radians(i * 36)
        c.line(x + math.cos(a) * (r + 8), y + math.sin(a) * (r + 8),
               x + math.cos(a) * (r + 24), y + math.sin(a) * (r + 24))
    arc(c, x, y - 4, 14, 200, 140)
    circ(c, x - 11, y + 8, 3, fill=1); circ(c, x + 11, y + 8, 3, fill=1)

def cloud(c, x, y, s=1):
    p = c.beginPath()
    p.moveTo(x - 50*s, y)
    p.arcTo(x - 60*s, y - 4*s, x - 20*s, y + 36*s, 90, 180)
    p.arcTo(x - 32*s, y + 10*s, x + 20*s, y + 56*s, 160, -140)
    p.arcTo(x + 5*s, y - 2*s, x + 55*s, y + 38*s, 120, -210)
    p.close()
    c.drawPath(p, stroke=1, fill=0)

def flower(c, x, y, s=1):
    c.line(x, y, x, y + 40 * s)
    for i in range(5):
        a = math.radians(i * 72 + 90)
        circ(c, x + math.cos(a) * 10 * s, y + 40 * s + math.sin(a) * 10 * s, 8 * s)
    c.setFillColorRGB(1, 1, 1); circ(c, x, y + 40 * s, 7 * s, fill=1); c.setFillColorRGB(0, 0, 0)
    ell(c, x + 10 * s, y + 15 * s, 9 * s, 4 * s)

def heart(c, x, y, s=1):
    p = c.beginPath(); p.moveTo(x, y - 10*s)
    p.curveTo(x - 22*s, y + 6*s, x - 8*s, y + 22*s, x, y + 10*s)
    p.curveTo(x + 8*s, y + 22*s, x + 22*s, y + 6*s, x, y - 10*s)
    c.drawPath(p, stroke=1, fill=0)

def star(c, x, y, r=14):
    pts = []
    for i in range(10):
        a = math.radians(90 + i * 36); rr = r if i % 2 == 0 else r * 0.45
        pts.append((x + math.cos(a) * rr, y + math.sin(a) * rr))
    poly(c, pts)

def apple(c, x, y, s=1):
    circ(c, x - 8*s, y, 16*s); circ(c, x + 8*s, y, 16*s)
    c.setFillColorRGB(1,1,1); ell(c, x, y, 18*s, 13*s, fill=1); c.setFillColorRGB(0,0,0)
    c.line(x, y + 14*s, x + 3*s, y + 26*s)
    ell(c, x + 12*s, y + 22*s, 8*s, 4*s)

def carrot(c, x, y, s=1):
    poly(c, [(x - 9*s, y + 30*s), (x + 9*s, y + 30*s), (x, y - 20*s)])
    for dx in (-7, 0, 7): ell(c, x + dx*s, y + 40*s, 4*s, 10*s)
    c.line(x - 5*s, y + 15*s, x, y + 15*s); c.line(x + 1*s, y + 2*s, x + 5*s, y + 2*s)

def broccoli(c, x, y, s=1):
    poly(c, [(x - 8*s, y), (x + 8*s, y), (x + 6*s, y + 25*s), (x - 6*s, y + 25*s)])
    for dx, dy in ((-14, 32), (0, 42), (14, 32), (-6, 28), (8, 26)):
        circ(c, x + dx*s, y + dy*s, 12*s)

def banana(c, x, y, s=1):
    p = c.beginPath(); p.moveTo(x - 30*s, y + 10*s)
    p.curveTo(x - 10*s, y - 15*s, x + 20*s, y - 10*s, x + 32*s, y + 14*s)
    p.curveTo(x + 15*s, y + 2*s, x - 10*s, y, x - 30*s, y + 10*s)
    c.drawPath(p, stroke=1, fill=0)

def plate(c, x, y, s=1):
    ell(c, x, y, 70*s, 18*s); ell(c, x, y + 2*s, 50*s, 11*s)

def table(c, x, y, w=420, h=70):
    c.rect(x - w/2, y, w, 14)
    c.rect(x - w/2 + 20, y - h, 14, h); c.rect(x + w/2 - 34, y - h, 14, h)

def book(c, x, y, s=1, open_=True):
    if open_:
        p = c.beginPath(); p.moveTo(x, y)
        p.curveTo(x - 20*s, y + 10*s, x - 45*s, y + 10*s, x - 60*s, y + 4*s)
        p.lineTo(x - 60*s, y + 54*s)
        p.curveTo(x - 45*s, y + 60*s, x - 20*s, y + 60*s, x, y + 50*s)
        p.curveTo(x + 20*s, y + 60*s, x + 45*s, y + 60*s, x + 60*s, y + 54*s)
        p.lineTo(x + 60*s, y + 4*s)
        p.curveTo(x + 45*s, y + 10*s, x + 20*s, y + 10*s, x, y)
        p.close(); c.drawPath(p, stroke=1, fill=0)
        c.line(x, y, x, y + 50*s)
        for i in range(3):
            c.line(x - 48*s, y + (22 + i*10)*s, x - 12*s, y + (20 + i*10)*s)
        heart(c, x + 30*s, y + 28*s, 0.6*s)
    else:
        c.roundRect(x - 30*s, y, 60*s, 80*s, 4*s); c.line(x - 22*s, y, x - 22*s, y + 80*s)
        star(c, x + 4*s, y + 45*s, 12*s)

def bookshelf(c, x, y):
    c.rect(x, y, 150, 220)
    for i in range(1, 3): c.line(x, y + i * 73, x + 150, y + i * 73)
    for row in range(3):
        bx = x + 8
        for wdt in (18, 22, 14, 26, 20, 24):
            if bx + wdt > x + 145: break
            hh = 50 + (wdt % 3) * 6
            c.rect(bx, y + row * 73 + 2, wdt, hh); bx += wdt + 2

def bike(c, x, y, s=1):
    for dx in (-60, 60):
        circ(c, x + dx*s, y + 34*s, 34*s); circ(c, x + dx*s, y + 34*s, 6*s)
    poly(c, [(x - 60*s, y + 34*s), (x - 10*s, y + 34*s), (x + 30*s, y + 80*s), (x - 25*s, y + 80*s)])
    c.line(x - 10*s, y + 34*s, x - 30*s, y + 90*s)
    c.line(x + 60*s, y + 34*s, x + 35*s, y + 105*s)
    c.line(x + 25*s, y + 110*s, x + 48*s, y + 104*s)
    ell(c, x - 30*s, y + 94*s, 18*s, 6*s)

def basket(c, x, y, s=1):
    poly(c, [(x - 45*s, y + 50*s), (x + 45*s, y + 50*s), (x + 35*s, y), (x - 35*s, y)])
    arc(c, x, y + 50*s, 40*s, 0, 180)
    for i in (-20, 0, 20): c.line(x + i*s, y + 2*s, x + i*1.25*s, y + 48*s)

def cart(c, x, y, s=1):
    poly(c, [(x - 70*s, y + 90*s), (x + 60*s, y + 90*s), (x + 45*s, y + 30*s), (x - 55*s, y + 30*s)])
    for i in range(1, 4): c.line(x - 70*s + i*32*s, y + 90*s, x - 55*s + i*25*s, y + 30*s)
    c.line(x - 62*s, y + 60*s, x + 52*s, y + 60*s)
    c.line(x + 60*s, y + 90*s, x + 80*s, y + 120*s); c.line(x + 72*s, y + 122*s, x + 92*s, y + 116*s)
    c.line(x - 55*s, y + 30*s, x - 55*s, y + 14*s); c.line(x + 45*s, y + 30*s, x + 45*s, y + 14*s)
    circ(c, x - 45*s, y + 8*s, 8*s); circ(c, x + 35*s, y + 8*s, 8*s)

def shelf_fruit(c, x, y):
    c.rect(x, y, 160, 200)
    c.line(x, y + 100, x + 160, y + 100)
    for i in range(3): apple(c, x + 30 + i * 50, y + 125, 0.8)
    for i in range(3): carrot(c, x + 30 + i * 50, y + 25, 0.8)

def pot(c, x, y, s=1):
    c.rect(x - 50*s, y, 100*s, 60*s)
    ell(c, x, y + 60*s, 50*s, 10*s)
    c.line(x - 50*s, y + 50*s, x - 70*s, y + 50*s); c.line(x + 50*s, y + 50*s, x + 70*s, y + 50*s)
    for dx in (-20, 0, 20):  # steam
        c.bezier(x + dx*s, y + 78*s, x + (dx - 10)*s, y + 92*s, x + (dx + 10)*s, y + 104*s, x + dx*s, y + 118*s)

def stove(c, x, y, w=220, h=150):
    c.rect(x - w/2, y, w, h); c.rect(x - w/2 + 25, y + 20, w - 50, h - 60)
    for i in range(3): circ(c, x - 50 + i * 50, y + h - 20, 8)

def chef_hat(c, x, y, s=1):
    c.rect(x - 30*s, y, 60*s, 18*s)
    circ(c, x - 22*s, y + 34*s, 20*s); circ(c, x + 22*s, y + 34*s, 20*s); circ(c, x, y + 46*s, 24*s)
    c.setFillColorRGB(1,1,1); c.rect(x - 28*s, y + 16*s, 56*s, 22*s, stroke=0, fill=1); c.setFillColorRGB(0,0,0)

def bowl(c, x, y, s=1):
    p = c.beginPath(); p.moveTo(x - 55*s, y + 30*s)
    p.curveTo(x - 50*s, y - 10*s, x + 50*s, y - 10*s, x + 55*s, y + 30*s); p.close()
    c.drawPath(p, stroke=1, fill=0)

def cake(c, x, y, s=1):
    c.rect(x - 60*s, y, 120*s, 50*s); c.rect(x - 45*s, y + 50*s, 90*s, 40*s)
    for i in range(5):
        arc(c, x - 48*s + i * 24*s, y + 50*s, 12*s, 180, 180)
    c.rect(x - 4*s, y + 90*s, 8*s, 26*s); ell(c, x, y + 124*s, 6*s, 9*s)
    for i in (-35, 0, 35): circ(c, x + i*s, y + 24*s, 7*s)

def slide(c, x, y):
    c.rect(x, y, 10, 220); c.rect(x + 60, y, 10, 220)
    for i in range(1, 6): c.line(x + 10, y + i * 36, x + 60, y + i * 36)
    c.rect(x - 5, y + 220, 80, 12)
    p = c.beginPath(); p.moveTo(x + 70, y + 220)
    p.curveTo(x + 150, y + 200, x + 170, y + 40, x + 260, y + 10)
    p.lineTo(x + 260, y - 15)
    p.curveTo(x + 160, y + 15, x + 140, y + 180, x + 70, y + 195)
    c.drawPath(p, stroke=1, fill=0)

def swing(c, x, y):
    poly(c, [(x - 110, y), (x - 80, y + 290), (x + 80, y + 290), (x + 110, y)], close=False)
    c.line(x - 80, y + 290, x - 55, y); c.line(x + 80, y + 290, x + 55, y)

def sandbox(c, x, y):
    c.rect(x - 90, y, 180, 30)
    poly(c, [(x - 30, y + 30), (x, y + 70), (x + 30, y + 30)])  # sand castle-ish
    c.rect(x - 14, y + 30, 28, 22)
    poly(c, [(x + 50, y + 30), (x + 70, y + 30), (x + 75, y + 55), (x + 45, y + 55)])

def tree(c, x, y, s=1):
    c.rect(x - 14*s, y, 28*s, 90*s)
    for dx, dy, r in ((0, 150, 55), (-45, 115, 40), (45, 115, 40), (-25, 180, 35), (28, 182, 35)):
        circ(c, x + dx*s, y + dy*s, r*s)
    c.setFillColorRGB(1,1,1); ell(c, x, y + 135*s, 60*s, 40*s, fill=1); c.setFillColorRGB(0,0,0)
    for (ax, ay) in ((-20, 140), (20, 150), (0, 120)):
        circ(c, x + ax*s, y + ay*s, 7*s)

def caption(c, text):
    c.setFont("Helvetica-Bold", 30)
    c.drawCentredString(W / 2, H - M - 54, text)

# ---------------- pages ----------------
def cover(c):
    border(c)
    c.setLineWidth(5)
    c.roundRect(90, H - 230, W - 180, 130, 30)
    c.setFont("Helvetica-Bold", 46)
    c.drawCentredString(W / 2, H - 155, "Cute Baby Animals")
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(W / 2, H - 205, "Coloring Book")
    c.setLineWidth(LW)
    for (sx, sy) in ((110, H - 280), (W - 110, H - 280), (W / 2, H - 285)):
        star(c, sx, sy, 16)
    ground(c, 150)
    animal(c, 170, 150, 1.0, "bunny", arms="up")
    animal(c, W / 2, 150, 1.25, "bear", arms="up")
    animal(c, W - 170, 150, 1.0, "cat", arms="up")
    heart(c, 130, 470, 1.2); heart(c, W - 130, 470, 1.2)
    flower(c, 75, 150, 0.9); flower(c, W - 75, 150, 0.9)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(W / 2, 95, "15 Fun Pages  ·  Ages 3-8")
    c.setFont("Helvetica", 14)
    c.drawCentredString(W / 2, 70, "This book belongs to: ______________________")

def p_bake(c):
    caption(c, "Baking a Cake")
    ground(c); table(c, W/2, 230)
    cake(c, W/2 - 90, 244, 0.9)
    hy, r = animal(c, W/2 + 110, 244, 1.05, "bear", arms="front")
    chef_hat(c, W/2 + 110, hy + r * 0.85, 1.0)
    bowl(c, W/2 + 110, 268, 0.7)
    star(c, 100, 640); star(c, W - 100, 620)

def p_soup(c):
    caption(c, "Cooking Veggie Soup")
    ground(c); stove(c, W/2 - 110, 120)
    pot(c, W/2 - 110, 270, 0.9)
    hy, r = animal(c, W/2 + 130, 120, 1.15, "bunny", arms="front")
    carrot(c, W/2 + 130, 190, 0.9)
    carrot(c, 90, 140, 0.8)

def p_pancakes(c):
    caption(c, "Pancake Breakfast")
    ground(c); table(c, W/2, 230)
    plate(c, W/2, 262, 1.0)
    for i in range(4): ell(c, W/2, 275 + i * 14, 48, 10)
    c.roundRect(W/2 - 18, 330, 36, 12, 5)
    animal(c, W/2 - 150, 244, 0.85, "panda", arms="front")
    animal(c, W/2 + 150, 244, 0.85, "pig", arms="front")
    sun(c, W - 110, 640)

def p_cookies(c):
    caption(c, "Making Cookies")
    ground(c); table(c, W/2, 230)
    c.rect(W/2 - 170, 244, 160, 14)
    for i in range(4): circ(c, W/2 - 150 + i * 40, 280, 15); circ(c, W/2 - 154 + i*40, 284, 3, fill=1)
    hy, r = animal(c, W/2 + 110, 244, 1.0, "mouse", arms="front")
    chef_hat(c, W/2 + 110, hy + r * 0.85, 0.9)
    heart(c, 100, 640, 1.3)

def p_shop_cart(c):
    caption(c, "Grocery Shopping")
    ground(c); shelf_fruit(c, 70, 121)
    cart(c, W/2 + 70, 120, 1.1)
    apple(c, W/2 + 40, 225, 0.9); broccoli(c, W/2 + 90, 205, 0.9)
    animal(c, W/2 - 30, 120, 0.95, "cat", arms="front")

def p_market(c):
    caption(c, "Fruit Market")
    ground(c)
    c.rect(90, 120, W - 180, 150)
    for i in range(6):
        arc(c, 128 + i * 72, 520, 36, 180, 180)
    c.line(92, 520, W - 92, 520)
    c.rect(96, 270, 10, 250); c.rect(W - 106, 270, 10, 250)
    for i in range(3): apple(c, 170 + i * 46, 300, 0.85)
    banana(c, 400, 295, 1.0); banana(c, 440, 305, 1.0)
    animal(c, W/2, 270, 0.9, "fox", arms="front")

def p_basket(c):
    caption(c, "Picking Veggies")
    ground(c)
    animal(c, W/2 - 60, 120, 1.15, "bunny", arms="front")
    basket(c, W/2 + 120, 121, 1.2)
    carrot(c, W/2 + 100, 180, 0.8); carrot(c, W/2 + 140, 182, 0.8)
    for i in range(4): flower(c, 80 + i * 30, 120, 0.7)
    sun(c, W - 110, 640); cloud(c, 160, 610)

def p_library(c):
    caption(c, "Story Time")
    ground(c); bookshelf(c, 70, 121)
    animal(c, W/2 + 80, 120, 1.15, "bear", arms="front")
    book(c, W/2 + 80, 175, 1.0)
    book(c, W - 100, 121, 0.8, open_=False)

def p_reading_tree(c):
    caption(c, "Reading Under a Tree")
    ground(c); tree(c, 150, 120, 1.3)
    animal(c, W/2 + 80, 120, 1.05, "chick", arms="front")
    book(c, W/2 + 80, 170, 0.9)
    sun(c, W - 110, 640); flower(c, W - 90, 120)

def p_bedtime(c):
    caption(c, "Bedtime Story")
    ground(c, 120)
    c.roundRect(80, 120, 300, 70, 10); c.rect(80, 120, 20, 200); c.rect(360, 120, 20, 140)
    ell(c, 140, 210, 40, 18)
    animal(c, 210, 190, 0.8, "panda", arms="front")
    book(c, 210, 230, 0.75)
    arc(c, W - 120, 620, 40, 300, 240)
    for (sx, sy) in ((440, 560), (500, 480), (120, 580)): star(c, sx, sy, 14)
    animal(c, W - 130, 120, 0.8, "mouse", arms="down")

def p_salad(c):
    caption(c, "Healthy Lunch")
    ground(c); table(c, W/2, 230)
    bowl(c, W/2, 250, 1.0)
    broccoli(c, W/2 - 25, 270, 0.7); carrot(c, W/2 + 25, 280, 0.6)
    animal(c, W/2 - 160, 244, 0.85, "pig", arms="front")
    animal(c, W/2 + 160, 244, 0.85, "bunny", arms="front")
    apple(c, W/2 + 80, 262, 0.7)

def p_fruit_picnic(c):
    caption(c, "Fruit Picnic")
    ground(c)
    poly(c, [(80, 120), (W - 80, 120), (W - 130, 220), (130, 220)])
    for i in range(1, 6): c.line(80 + i * 75, 120, 130 + i * 58.6, 220)
    apple(c, 220, 170, 0.8); banana(c, W/2, 160, 1.0); apple(c, 400, 170, 0.8)
    animal(c, 170, 220, 0.85, "cat", arms="front")
    animal(c, W - 170, 220, 0.85, "bear", arms="front")
    sun(c, W - 110, 650); cloud(c, 170, 620)

def p_bike(c):
    caption(c, "Bike Ride")
    ground(c)
    bike(c, W/2, 121, 1.3)
    animal(c, W/2 - 30, 245, 0.85, "fox", arms="up")
    tree(c, 125, 120, 0.75); sun(c, W - 110, 640); cloud(c, 260, 640, 0.8)

def p_tricycle(c):
    caption(c, "Racing Friends")
    ground(c)
    bike(c, 180, 121, 0.85); animal(c, 160, 205, 0.6, "pig", arms="up")
    bike(c, W - 180, 121, 0.85); animal(c, W - 200, 205, 0.6, "bunny", arms="up")
    for i in range(3): flower(c, W/2 - 30 + i * 30, 120, 0.7)
    c.line(W/2, 120, W/2, 420); poly(c, [(W/2, 420), (W/2 + 70, 400), (W/2, 380)])
    sun(c, 110, 640)

def p_slide(c):
    caption(c, "Fun on the Slide")
    ground(c); slide(c, 110, 135)
    c.line(110, 120, 110, 135); c.line(180, 120, 180, 135)
    animal(c, 150, 367, 0.6, "cat", arms="up")
    animal(c, 430, 120, 0.9, "panda", arms="up")
    sun(c, W - 110, 650)

def p_swing(c):
    caption(c, "Swinging High")
    ground(c); swing(c, 200, 120)
    c.rect(130, 175, 140, 10)
    animal(c, 200, 185, 0.7, "bear", arms="up")
    sandbox(c, W - 170, 121)
    animal(c, W - 170, 151, 0.6, "chick", arms="front")
    cloud(c, W - 160, 600)

PAGES = [p_bake, p_soup, p_pancakes, p_shop_cart, p_market, p_basket,
         p_library, p_reading_tree, p_bedtime, p_salad, p_fruit_picnic,
         p_bike, p_tricycle, p_slide, p_swing]

def main():
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "baby_animals_coloring_book.pdf")
    c = canvas.Canvas(out, pagesize=letter)
    c.setTitle("Cute Baby Animals Coloring Book")
    c.setLineJoin(1); c.setLineCap(1); c.setLineWidth(LW)
    cover(c); c.showPage()
    for f in PAGES:
        c.setLineJoin(1); c.setLineCap(1); c.setLineWidth(LW)
        border(c); f(c); c.showPage()
    c.save(); print(out)

if __name__ == "__main__":
    main()
