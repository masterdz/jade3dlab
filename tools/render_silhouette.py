"""Silhouette renderer for the skinned character (clear body shape)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from PIL import Image

from jade_engine.bf_parser import load_bf
from jade_engine.level_loader import load_level_from_archive
from jade_engine import animations as A

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scratch", "farah_render")


def silhouette(verts, faces, size=420, yaw=0.6, flip=1):
    w = h = size
    mask = np.zeros((h, w), dtype=bool)
    v = np.asarray(verts, dtype=np.float64)
    center = v.mean(axis=0)
    v = v - center
    cy, sy = np.cos(yaw), np.sin(yaw)
    x1 = v[:, 0] * cy - v[:, 1] * sy
    y1 = v[:, 0] * sy + v[:, 1] * cy
    p = np.stack([x1, v[:, 2], y1], axis=1)
    span = max(np.abs(p[:, :2]).max(), 1e-6)
    scale = (w * 0.40) / span
    px = p[:, 0] * scale + w * 0.5
    py = -p[:, 1] * scale + h * 0.5
    pz = p[:, 2]

    for face in faces:
        i0, i1, i2 = face
        if max(i0, i1, i2) >= len(px):
            continue
        ax, ay, az = px[i0], py[i0], pz[i0]
        bx, by, bz = px[i1], py[i1], pz[i1]
        cx, cyy, cz = px[i2], py[i2], pz[i2]
        area = (bx - ax) * (cyy - ay) - (cx - ax) * (by - ay)
        if abs(area) < 1e-9:
            continue
        minx = int(max(0, np.floor(min(ax, bx, cx))))
        maxx = int(min(w - 1, np.ceil(max(ax, bx, cx))))
        miny = int(max(0, np.floor(min(ay, by, cyy))))
        maxy = int(min(h - 1, np.ceil(max(ay, by, cyy))))
        if minx > maxx or miny > maxy:
            continue
        xs = np.arange(minx, maxx + 1)
        ys = np.arange(miny, maxy + 1)
        gx, gy = np.meshgrid(xs, ys)
        w0 = ((bx - ax) * (gy - ay) - (gx - ax) * (by - ay)) / area
        w1 = ((cx - bx) * (gy - by) - (gx - bx) * (cyy - by)) / area
        w2 = 1.0 - w0 - w1
        inside = (w0 >= -1e-6) & (w1 >= -1e-6) & (w2 >= -1e-6)
        if inside.any():
            mask[miny:maxy + 1, minx:maxx + 1] |= inside
    img = np.zeros((h, w, 3), dtype=np.float32)
    img[mask] = (0.85, 0.85, 0.9)
    return Image.fromarray((img * 255).astype(np.uint8))


def main():
    os.makedirs(OUT, exist_ok=True)
    archive = load_bf("prince3.bf")
    e = next(x for x in archive.entries if "farah_wow" in x.name.casefold())
    level = load_level_from_archive(archive, e)
    body = next(m for m in level.meshes.values() if m.skin_bones and len(m.skin_bones) == 36)
    rest = A.build_skin_rest(body)

    clips = [c for c in level.animation_clips if c.frames > 10]
    clip = max(clips, key=lambda c: len({t.gizmo for t in c.tracks}))

    frames = [("rest", body.vertices)]
    for frame in (0, 8, 16, 24, 32, 40):
        if frame >= clip.frames:
            continue
        poses = A.compute_character_skeleton_poses(level, clip, float(frame), target_character="farah")
        posed = A.pose_mesh_vertices(body, clip, float(frame), rest=rest, master_anim=poses)
        frames.append((f"f{frame}", posed))

    for yaw, tag in ((0.6, "a"), (2.2, "b")):
        imgs = [silhouette(v, body.faces, yaw=yaw) for _, v in frames]
        sheet = Image.new("RGB", (300 * len(imgs), 300), (0, 0, 0))
        for i, im in enumerate(imgs):
            sheet.paste(im.resize((300, 300)), (300 * i, 0))
        sheet.save(os.path.join(OUT, f"sil_{tag}.png"))
        print(f"wrote sil_{tag}.png  ({[f[0] for f in frames]})")


if __name__ == "__main__":
    main()
