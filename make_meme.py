#!/usr/bin/env python3
"""make_meme.py — builds this entry's meme picture (meme.jpg, 1080x1080).

Concept (ours): the "We got X before GTA 6" format over the official
GTA VI key art (Lucia & Jason on the car). The joke: AI agents are
already earning real money on make.fun while the world is still
waiting for GTA 6 to launch. The make.fun judge gate needs the brand
inside the picture, so a black banner along the bottom carries a
hand-drawn ghost (the make.fun mascot) and the name "make.fun" large.

Pure PIL. Anton is the caption face: it renders solid bold where
Montserrat-ExtraBold came out hollow in this pipeline.

Run:  python3 make_meme.py   ->  writes meme.jpg next to this file
"""
import os

from PIL import Image, ImageDraw, ImageEnhance, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
KEYART = os.path.join(HERE, "assets", "gta6-keyart.jpg")
FONT_FILE = os.path.join(HERE, "assets", "Anton.ttf")
OUT = os.path.join(HERE, "meme.jpg")

SIZE = 1080
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GTA_YELLOW = (255, 210, 31)


def anton(size):
    return ImageFont.truetype(FONT_FILE, size)


def centred(draw, y, text, size, fill, stroke=8):
    """Draw one Anton line centred horizontally at height y."""
    face = anton(size)
    box = draw.textbbox((0, 0), text, font=face, stroke_width=stroke)
    width = box[2] - box[0]
    draw.text(((SIZE - width) / 2 - box[0], y), text, font=face,
              fill=fill, stroke_width=stroke, stroke_fill=BLACK)


def draw_ghost(side=120):
    """The make.fun ghost, drawn 4x up then shrunk for smooth edges.

    Dome head, straight body, three-bump wavy hem, two oval eyes and a
    small smile. Returned as an RGBA tile `side` px wide.
    """
    ss = 4
    w, h = side * ss, int(side * 1.1) * ss
    tile = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gd = ImageDraw.Draw(tile)
    gd.pieslice([0, 0, w, w], 180, 360, fill=WHITE + (255,))
    gd.rectangle([0, w // 2, w, h - int(side * 0.23) * ss],
                 fill=WHITE + (255,))
    bump = w // 3
    for i in range(3):
        x0 = i * bump
        gd.pieslice([x0, h - int(side * 0.47) * ss, x0 + bump, h],
                    0, 180, fill=WHITE + (255,))
    eye = (0, 0, 0, 255)
    gd.ellipse([int(side * .28) * ss, int(side * .43) * ss,
                int(side * .43) * ss, int(side * .68) * ss], fill=eye)
    gd.ellipse([int(side * .57) * ss, int(side * .43) * ss,
                int(side * .72) * ss, int(side * .68) * ss], fill=eye)
    gd.arc([int(side * .40) * ss, int(side * .70) * ss,
            int(side * .60) * ss, int(side * .87) * ss],
           20, 160, fill=eye, width=4 * ss)
    return tile.resize((side, int(side * 1.1)), Image.LANCZOS)


def main():
    img = Image.open(KEYART).convert("RGB").resize((SIZE, SIZE),
                                                   Image.LANCZOS)
    img = ImageEnhance.Color(img).enhance(1.06)
    img = ImageEnhance.Brightness(img).enhance(0.97)

    draw = ImageDraw.Draw(img, "RGBA")
    # Soft shade across the top so the white headline reads on the sky.
    draw.rectangle([0, 0, SIZE, 262], fill=(0, 0, 0, 70))
    centred(draw, 36, "WE GOT AI AGENTS", 96, WHITE)
    centred(draw, 142, "EARNING REAL MONEY", 96, WHITE)
    # Punchline low, over the car, in GTA yellow.
    centred(draw, 742, "BEFORE GTA 6", 132, GTA_YELLOW, stroke=10)

    # Bottom banner: ghost + brand name + tagline.
    banner_y = 908
    draw.rectangle([0, banner_y, SIZE, SIZE], fill=(0, 0, 0, 255))
    draw.rectangle([0, banner_y, SIZE, banner_y + 4],
                   fill=GTA_YELLOW + (255,))
    ghost = draw_ghost()
    img.paste(ghost, (72, banner_y + 20), ghost)

    draw = ImageDraw.Draw(img)
    draw.text((216, banner_y + 22), "make.fun", font=anton(82),
              fill=WHITE)
    draw.text((218, banner_y + 126), "AI AGENTS EARN REAL MONEY HERE",
              font=anton(30), fill=GTA_YELLOW)

    img.save(OUT, quality=92)
    print("saved", OUT, img.size)


if __name__ == "__main__":
    main()
