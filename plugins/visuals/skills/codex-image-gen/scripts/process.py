# /// script
# requires-python = ">=3.10"
# dependencies = ["pillow", "numpy"]
# ///
"""Post-process a raw generated image into a shippable asset.

Pipeline order: key background -> trim -> make tileable -> resize -> logo -> export.
Output format follows the output extension (.jpg/.png/.webp).

  uv run process.py raw/logo.png out/logo.webp --key auto --trim --size 512x512 --contain
  uv run process.py raw/stone.png out/stone.jpg --tile --size 1024x1024
  uv run process.py raw/hero.png out/hero.jpg --size 1920x1080
  uv run process.py raw/post.png out/post.jpg --size 1080x1350 --logo brand/logo.png --logo-pos tr
  uv run process.py --selftest
"""
import argparse
import sys

import numpy as np
from PIL import Image, ImageOps


def key(img, color, tol):
    """Turn pixels near `color` transparent, with a soft ramp from tol to 2*tol."""
    rgba = np.asarray(img.convert("RGBA")).astype(np.float32)
    if color == "auto":
        corners = rgba[[0, 0, -1, -1], [0, -1, 0, -1], :3]
        bg = np.median(corners, axis=0)
    else:
        h = color.lstrip("#")
        bg = np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], np.float32)
    dist = np.linalg.norm(rgba[..., :3] - bg, axis=-1)
    alpha = np.clip((dist - tol) / tol, 0, 1)
    # Unmix the background from semi-transparent edge pixels so they don't keep a coloured halo.
    a = alpha[..., None]
    edge = (alpha > 0) & (alpha < 1)
    unmixed = (rgba[..., :3] - (1 - a) * bg) / np.maximum(a, 1e-3)
    rgba[..., :3] = np.where(edge[..., None], np.clip(unmixed, 0, 255), rgba[..., :3])
    rgba[..., 3] = np.minimum(rgba[..., 3], alpha * 255)
    return Image.fromarray(rgba.astype(np.uint8), "RGBA")


def trim(img, pad=0):
    box = img.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox() if img.mode == "RGBA" else None
    if not box:
        return img
    l, t, r, b = box
    return img.crop((max(l - pad, 0), max(t - pad, 0), min(r + pad, img.width), min(b + pad, img.height)))


def _blend_axis(a, axis, margin):
    """Cross-fade a with itself rolled by half along one axis so opposite edges match."""
    n = a.shape[axis]
    rolled = np.roll(a, n // 2, axis=axis)
    d = np.minimum(np.arange(n), n - 1 - np.arange(n)) / max(n * margin, 1)
    w = np.clip(d, 0, 1)
    shape = [1] * a.ndim
    shape[axis] = n
    w = w.reshape(shape)
    return a * w + rolled * (1 - w)


def tile(img, margin=0.25):
    a = np.asarray(img).astype(np.float32)
    a = _blend_axis(_blend_axis(a, 1, margin), 0, margin)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), img.mode)


def resize(img, size, contain):
    w, h = (int(v) for v in size.lower().split("x"))
    if contain:
        return ImageOps.contain(img, (w, h), Image.LANCZOS)
    return ImageOps.fit(img, (w, h), Image.LANCZOS)


def logo(img, path, pos, width):
    """Paste the real logo file in a corner; generators redraw logos inexactly."""
    mark = Image.open(path).convert("RGBA")
    w = round(img.width * width)
    mark = mark.resize((w, round(mark.height * w / mark.width)), Image.LANCZOS)
    m = round(img.width * 0.05)
    x = {"l": m, "r": img.width - mark.width - m, "c": (img.width - mark.width) // 2}[pos[1]]
    y = {"t": m, "b": img.height - mark.height - m}[pos[0]]
    out = img.convert("RGBA")
    out.alpha_composite(mark, (x, y))
    return out if img.mode == "RGBA" else out.convert("RGB")


def export(img, path, quality):
    ext = path.rsplit(".", 1)[-1].lower()
    if ext in ("jpg", "jpeg"):
        if img.mode == "RGBA":
            flat = Image.new("RGB", img.size, (255, 255, 255))
            flat.paste(img, mask=img.getchannel("A"))
            img = flat
        img.convert("RGB").save(path, quality=quality, optimize=True, progressive=True)
    elif ext == "webp":
        img.save(path, quality=quality, method=6)
    else:
        img.save(path, optimize=True)


def selftest():
    # Keying: black bg with a red square -> bg transparent, square opaque, trim crops to square.
    img = Image.new("RGB", (64, 64), (0, 0, 0))
    img.paste((255, 0, 0), (16, 16, 48, 48))
    k = key(img, "auto", 40)
    assert k.getpixel((0, 0))[3] == 0 and k.getpixel((32, 32))[3] == 255
    assert trim(k).size == (32, 32)
    # Unmixing: a 50/50 red/green edge pixel keyed against green comes back as pure red.
    e = Image.new("RGB", (8, 8), (0, 255, 0))
    e.putpixel((4, 4), (128, 128, 0))
    r, g, b, a = key(e, "#00FF00", 120).getpixel((4, 4))
    assert 0 < a < 255 and g < 40 and r > 200, (r, g, b, a)
    # Tiling: a horizontal gradient has a hard seam; after tile() opposite edges must match.
    g = Image.fromarray(np.tile(np.linspace(0, 255, 64, dtype=np.uint8), (64, 1)), "L").convert("RGB")
    t = np.asarray(tile(g)).astype(int)
    assert abs(t[:, 0] - t[:, -1]).max() <= 8, "left/right edges should match"
    assert abs(t[0] - t[-1]).max() <= 8, "top/bottom edges should match"
    # Resize: cover crops to exact size, contain fits inside.
    assert resize(Image.new("RGB", (300, 100)), "100x100", False).size == (100, 100)
    assert resize(Image.new("RGB", (300, 100)), "100x100", True).size == (100, 33)
    # Logo: a 20%-wide red mark lands in the top-right corner with a 5% margin; the far corner is untouched.
    import os, tempfile
    p = os.path.join(tempfile.mkdtemp(), "mark.png")
    Image.new("RGBA", (50, 25), (255, 0, 0, 255)).save(p)
    out = logo(Image.new("RGB", (200, 100), (0, 0, 0)), p, "tr", 0.2)
    assert out.mode == "RGB" and out.getpixel((165, 15)) == (255, 0, 0) and out.getpixel((5, 95)) == (0, 0, 0)
    print("selftest ok")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("src", nargs="?")
    p.add_argument("dst", nargs="?")
    p.add_argument("--key", metavar="auto|#RRGGBB", help="key this background colour to alpha ('auto' samples the corners)")
    p.add_argument("--tol", type=float, default=40, help="key tolerance in RGB distance (default 40)")
    p.add_argument("--trim", action="store_true", help="crop to non-transparent content")
    p.add_argument("--pad", type=int, default=0, help="padding kept around content when trimming")
    p.add_argument("--tile", action="store_true", help="cross-fade edges so the image tiles seamlessly")
    p.add_argument("--size", metavar="WxH", help="target size; crops to fill unless --contain")
    p.add_argument("--contain", action="store_true", help="fit inside --size without cropping")
    p.add_argument("--logo", metavar="PATH", help="composite this logo file (PNG with alpha) onto the result")
    p.add_argument("--logo-pos", choices=["tl", "tr", "bl", "br", "bc"], default="br")
    p.add_argument("--logo-width", type=float, default=0.18, help="logo width as a fraction of image width")
    p.add_argument("--quality", type=int, default=85)
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest:
        return selftest()
    if not (a.src and a.dst):
        p.error("src and dst are required")

    img = Image.open(a.src)
    img = img.convert("RGBA" if img.mode in ("RGBA", "LA", "P") else "RGB")
    if a.key:
        img = key(img, a.key, a.tol)
    if a.trim:
        img = trim(img, a.pad)
    if a.tile:
        img = tile(img)
    if a.size:
        img = resize(img, a.size, a.contain)
    if a.logo:
        img = logo(img, a.logo, a.logo_pos, a.logo_width)
    export(img, a.dst, a.quality)
    print(f"{a.dst} {img.width}x{img.height} {img.mode}")


if __name__ == "__main__":
    sys.exit(main())
