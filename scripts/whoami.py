import json
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent

with open(Path(__file__).resolve().parent / "whoami.json", encoding="utf-8") as f:
    data = list(json.load(f).items())

SCALE     = 3
FS        = 13 * SCALE
FS_SMALL  = 10 * SCALE
FS_PROMPT = 11 * SCALE
FS_WINBTN = 11 * SCALE

CANDIDATES = {
    "mono_bold": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
        "C:/Windows/Fonts/consolab.ttf",
        "/System/Library/Fonts/Menlo.ttc",
    ],
    "mono": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "C:/Windows/Fonts/consola.ttf",
        "/System/Library/Fonts/Menlo.ttc",
    ],
}


def find_font(kind):
    for p in CANDIDATES[kind]:
        if os.path.exists(p):
            return p
    return CANDIDATES[kind][0]


font_key    = ImageFont.truetype(find_font("mono_bold"), FS)
font_val    = ImageFont.truetype(find_font("mono"), FS)
font_small  = ImageFont.truetype(find_font("mono"), FS_SMALL)
font_prompt = ImageFont.truetype(find_font("mono"), FS_PROMPT)
font_winbtn = ImageFont.truetype(find_font("mono"), FS_WINBTN)

BG      = "#09090b"
SURFACE = "#0f0f11"
BORDER  = "#1e1e22"
KEY     = "#a78bfa"
VAL     = "#e4e4e7"
MUTED   = "#3f3f46"
ACCENT  = "#34d399"
WINBTN  = "#52525b"

pad_x, pad_y = 32 * SCALE, 26 * SCALE
line_h = FS + 10 * SCALE

tmp  = Image.new("RGB", (1, 1))
td   = ImageDraw.Draw(tmp)
key_w = max(int(td.textlength(k, font=font_key)) for k, _ in data)

W        = 580 * SCALE
top_bar  = 36 * SCALE
prompt_h = line_h + 10 * SCALE
H        = top_bar + pad_y + prompt_h + line_h * len(data) + pad_y

img  = Image.new("RGBA", (W, H), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

R = 16 * SCALE

draw.rounded_rectangle([0, 0, W - 1, H - 1], radius=R, fill=BG, outline=BORDER, width=SCALE)

draw.rounded_rectangle([0, 0, W - 1, top_bar + R], radius=R, fill=SURFACE)
draw.rectangle([0, top_bar, W - 1, top_bar + R], fill=SURFACE)
draw.line([(0, top_bar), (W - 1, top_bar)], fill=BORDER, width=SCALE)

title = "Windows PowerShell"
tw = int(draw.textlength(title, font=font_small))
dy_c = top_bar // 2
draw.text(((W - tw) // 2, dy_c - FS_SMALL // 2), title, font=font_small, fill=MUTED)

buttons = ["─", "□", "✕"]
btn_w   = 36 * SCALE
btn_x   = W - len(buttons) * btn_w - 4 * SCALE
for i, sym in enumerate(buttons):
    bx = btn_x + i * btn_w
    sw = int(draw.textlength(sym, font=font_winbtn))
    col = "#f87171" if sym == "✕" else WINBTN
    draw.text((bx + (btn_w - sw) // 2, dy_c - FS_WINBTN // 2),
              sym, font=font_winbtn, fill=col)

y = top_bar + pad_y
draw.text((pad_x, y), "PS C:\\Users\\Parzival> whoami", font=font_prompt, fill=MUTED)
y += prompt_h

colon_x = pad_x + key_w + 6 * SCALE
val_x   = colon_x + int(td.textlength(" : ", font=font_val)) + 4 * SCALE

for key, val in data:
    draw.text((pad_x, y), key, font=font_key, fill=KEY)
    draw.text((colon_x, y), " :", font=font_val, fill=BORDER)
    draw.text((val_x, y), val, font=font_val,
              fill=ACCENT if key == "status" else VAL)
    y += line_h

final = img.resize((W // SCALE, H // SCALE), Image.LANCZOS)
final.save(ROOT / "whoami.png", "PNG")
print("Saved", final.size)
