#!/usr/bin/env python3
import os
from PIL import Image

GALLERY_DIR   = os.path.join(os.path.dirname(__file__), 'gallery')
ROOT_DIR      = os.path.dirname(__file__)
GALLERY_WIDTH = 1200
ROBOT_WIDTH   = 860
WEBP_QUALITY  = 82
JPEG_QUALITY  = 85

def convert(src_path, out_dir, target_width):
    img = Image.open(src_path).convert('RGBA')
    w, h = img.size
    new_h = int(target_width * h / w)
    img = img.resize((target_width, new_h), Image.LANCZOS)

    stem = os.path.splitext(os.path.basename(src_path))[0]

    webp_path = os.path.join(out_dir, stem + '.webp')
    img.save(webp_path, 'WEBP', quality=WEBP_QUALITY, method=6)

    bg = Image.new('RGB', img.size, (0, 0, 0))
    bg.paste(img, mask=img.split()[3])
    jpg_path = os.path.join(out_dir, stem + '.jpg')
    bg.save(jpg_path, 'JPEG', quality=JPEG_QUALITY, optimize=True, progressive=True)

    orig_kb = os.path.getsize(src_path) / 1024
    webp_kb = os.path.getsize(webp_path) / 1024
    jpg_kb  = os.path.getsize(jpg_path) / 1024
    print(f'{stem[:36]:36s}  {orig_kb:7.0f}KB → WebP {webp_kb:5.0f}KB  JPEG {jpg_kb:5.0f}KB')
    return target_width, new_h

print('--- Gallery ---')
dims = {}
for fname in sorted(os.listdir(GALLERY_DIR)):
    if fname.lower().endswith('.png'):
        w, h = convert(os.path.join(GALLERY_DIR, fname), GALLERY_DIR, GALLERY_WIDTH)
        stem = os.path.splitext(fname)[0]
        dims[stem] = (w, h)

print('--- Hero ---')
rw, rh = convert(os.path.join(ROOT_DIR, 'robot.png'), ROOT_DIR, ROBOT_WIDTH)
print(f'\nrobot dimensions: {rw}x{rh}')
print('\nDone.')
