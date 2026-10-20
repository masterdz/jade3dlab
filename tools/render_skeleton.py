"""Render the posed skeleton as lines to verify the FK pose."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from PIL import Image

from jade_engine.bf_parser import load_bf
from jade_engine.level_loader import load_level_from_archive
from jade_engine import animations as A

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scratch", "farah_render")


def draw_skeleton(states, size=420, yaw=0.6):
    """states: list of (label, {gizmo: (x,y,z)})"""
    w = h = size
    img = np.zeros((h, w, 3), dtype=np.float32)
    allpts = np.array([p for _, s in states for p in s.values()])
    center = allpts.mean(axis=0)
    extent = np.abs(allpts - center).max()

    cols = [(1, 0.3, 0.3), (0.3, 1, 0.3), (0.3, 0.5, 1), (1, 0.9, 0.2), (1, 0.3, 1), (0.2, 1, 1)]

    def project(p):
        cy, sy = np.cos(yaw), np.sin(yaw)
        x = p[0] * cy - p[1] * sy
        y = p[0] * sy + p[1] * cy
        z = p[2]
        return (x * (w * 0.42) / extent + w * 0.5, -z * (w * 0.42) / extent + h * 0.5)

    for idx, (label, pts) in enumerate(states):
        col = cols[idx % len(cols)]
        ox = idx * 0  # stacked
        # draw a marker for each bone and a line to its parent
        for g, p in pts.items():
            a = project(p)
            s = 4
            x0, y0 = int(a[0]), int(a[1])
            for dy in range(-s, s + 1):
                for dx in range(-s, s + 1):
                    xx, yy = x0 + dx, y0 + dy
                    if 0 <= xx < w and 0 <= yy < h:
                        img[yy, xx] = col
        # parent links
        parents = A.FARAH_BIPED_PARENTS
        for g, p in pts.items():
            par = parents.get(g)
            if par is None or par not in pts:
                continue
            a = project(p)
            b = project(pts[par])
            n = int(max(abs(b[0] - a[0]), abs(b[1] - a[1]))) + 1
            for t in range(n + 1):
                xx = int(a[0] + (b[0] - a[0]) * t / max(1, n))
                yy = int(a[1] + (b[1] - a[1]) * t / max(1, n))
                if 0 <= xx < w and 0 <= yy < h:
                    img[yy, xx] = col
    return Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8))


def main():
    os.makedirs(OUT, exist_ok=True)
    archive = load_bf("prince3.bf")
    e = next(x for x in archive.entries if "farah_wow" in x.name.casefold())
    level = load_level_from_archive(archive, e)
    body = next(m for m in level.meshes.values() if m.skin_bones and len(m.skin_bones) == 36)
    rest = A.build_skin_rest(body)
    mb = {b.index: rest[b.index] for b in body.skin_bones if b.index in rest}

    clips = [c for c in level.animation_clips if c.frames > 10]
    clip = max(clips, key=lambda c: len({t.gizmo for t in c.tracks}))

    # rest skeleton
    states = []
    restpts = {g: (v[0][12], v[0][13], v[0][14]) for g, v in mb.items()}
    states.append(("rest", restpts))
    for frame in (0, 8, 16, 24, 32, 40):
        if frame >= clip.frames:
            continue
        poses = A.compute_character_skeleton_poses(level, clip, float(frame), target_character="farah")
        states.append((f"f{frame}", {g: (p[1][0], p[1][1], p[1][2]) for g, p in poses.items()}))

    imgs = [draw_skeleton([s]) for s in states]
    sheet = Image.new("RGB", (420 * len(imgs), 420), (0, 0, 0))
    for i, im in enumerate(imgs):
        sheet.paste(im, (420 * i, 0))
    sheet = sheet.resize((300 * len(imgs), 300))
    sheet.save(os.path.join(OUT, "skeleton.png"))
    print("wrote skeleton.png  frames:", [s[0] for s in states])


if __name__ == "__main__":
    main()
