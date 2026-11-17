#!/usr/bin/env python3
"""Brighten a 2x2 robot-camera video with fixed exposure gains per camera.

Uses the Grana paper's scripts/photo_white.py method: bright neutral pixels
anchor a linear-light exposure gain, with soft highlight rolloff. Video gains
are fixed across time to avoid introducing exposure flicker. A clipping guard
limits gains for views that already contain bright close-ups.

Requires Python 3, NumPy, ffmpeg, and ffprobe. The original input is never edited.
Example:
  python3 tools/brighten_supervision_video.py original.mp4 cameras.mp4 \
    --poster cameras.jpg --report processing.json

SPDX-License-Identifier: Apache-2.0
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

import numpy as np

LUMA = np.array([0.2126, 0.7152, 0.0722])
VIEWS = ("top", "left", "right", "bottom")


def linear(rgb):
    value = np.asarray(rgb, dtype=np.float64) / 255
    return np.where(value <= 0.04045, value / 12.92, ((value + 0.055) / 1.055) ** 2.4)


def transform(rgb, gain, target):
    value = linear(rgb) * gain
    white = float(linear(target))
    excess = np.maximum(value - white, 0)
    value = np.where(value > white, white + (1 - white) * (1 - np.exp(-excess / (1 - white))), value)
    value = np.clip(value, 0, 1)
    encoded = np.where(value <= 0.0031308, value * 12.92, 1.055 * value ** (1 / 2.4) - 0.055)
    return np.clip(encoded * 255 + 0.5, 0, 255).astype(np.uint8)


def white_point(rgb):
    pixels = rgb.reshape(-1, 3).astype(np.float64)
    luma = pixels @ LUMA
    chroma = np.ptp(pixels, axis=1)
    bright = luma > np.percentile(luma, 70)
    if not bright.any():
        return None
    neutral = bright & (chroma < np.percentile(chroma[bright], 50)) & (chroma < 24)
    return pixels[neutral].mean(axis=0) if neutral.mean() >= 0.02 else None


def probe(path):
    result = subprocess.check_output([
        "ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
        "stream=width,height,r_frame_rate,nb_frames,start_time,time_base,duration", "-of", "json", str(path),
    ])
    return json.loads(result)["streams"][0]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--poster", type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--target-white", type=float, default=225)
    parser.add_argument("--max-added-clipping", type=float, default=0.01,
                        help="Maximum added fraction of pixels reaching 255 in any channel, on calibration samples.")
    parser.add_argument("--crf", type=int, default=18)
    args = parser.parse_args()
    if args.source.resolve() == args.output.resolve():
        parser.error("Use a separate output so the original video is preserved.")
    if not 0 < args.target_white < 255 or not 0 <= args.max_added_clipping <= 1:
        parser.error("Target white must lie in (0,255) and clipping allowance in [0,1].")
    original = probe(args.source)
    width, height = original["width"], original["height"]
    if width % 4 or height % 4:
        parser.error("The 2x2 input width and height must be divisible by four.")
    # Sample at 2 Hz; quarter-resolution calibration leaves the encoded video untouched.
    sample_width = 640
    sample_height = int(height * sample_width / width / 4) * 4
    raw = subprocess.check_output([
        "ffmpeg", "-v", "error", "-i", str(args.source), "-vf",
        f"fps=2,scale={sample_width}:{sample_height}", "-pix_fmt", "rgb24", "-f", "rawvideo", "pipe:1",
    ])
    samples = np.frombuffer(raw, dtype=np.uint8).reshape(-1, sample_height, sample_width, 3)
    half_w, half_h = sample_width // 2, sample_height // 2
    # Exclude each camera's label strip when estimating white, as in paper Fig. 8.
    label_height = round(48 * sample_width / width)
    views = {}
    for index, name in enumerate(VIEWS):
        y, x = (index // 2) * half_h, (index % 2) * half_w
        crops = samples[:, y + label_height:y + half_h:2, x:x + half_w:2]
        whites = [white_point(crop) for crop in crops]
        whites = [float(white @ LUMA) for white in whites if white is not None]
        estimated = float(np.clip(np.median([linear(args.target_white) / linear(white) for white in whites]), 1, 4)) if whites else 1.0
        raw_clipping = np.mean(np.any(crops == 255, axis=-1), axis=(1, 2))
        gain = estimated
        while True:
            lookup = transform(np.arange(256), gain, args.target_white)
            corrected = lookup[crops]
            clipping = np.mean(np.any(corrected == 255, axis=-1), axis=(1, 2))
            if np.max(clipping - raw_clipping) <= args.max_added_clipping or gain <= 1.001:
                break
            gain = max(1.0, gain * 0.98)
        views[name] = {
            "estimated_gain": estimated, "applied_gain": gain,
            "original_white_median": float(np.median(whites)) if whites else None,
            "max_original_clipping": float(raw_clipping.max()), "max_corrected_clipping": float(clipping.max()),
        }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="grana-video-exposure-") as temporary:
        filters = ["[0:v:0]format=gbrp,split=4[in0][in1][in2][in3]"]
        for index, name in enumerate(VIEWS):
            lookup = transform(np.arange(256), views[name]["applied_gain"], args.target_white) / 255
            lut = Path(temporary) / f"{name}.cube"
            lut.write_text("LUT_1D_SIZE 256\n" + "\n".join(f"{v:.9f} {v:.9f} {v:.9f}" for v in lookup) + "\n")
            x, y = (index % 2) * (width // 2), (index // 2) * (height // 2)
            filters.append(f"[in{index}]crop={width // 2}:{height // 2}:{x}:{y},lut1d=file={lut}:interp=linear[{name}]")
        filters.extend(["[top][left]hstack=inputs=2[upper]", "[right][bottom]hstack=inputs=2[lower]", "[upper][lower]vstack=inputs=2,format=yuv420p[out]"])
        # No temporal filters: retain the original frame rate, PTS, and frame count.
        subprocess.run([
            "ffmpeg", "-hide_banner", "-loglevel", "warning", "-y", "-i", str(args.source),
            "-filter_complex_threads", "2", "-filter_complex", ";".join(filters), "-map", "[out]", "-an",
            "-c:v", "libx264", "-preset", "medium", "-crf", str(args.crf), "-threads", "4",
            "-fps_mode", "passthrough", "-video_track_timescale", str(Fraction(original["time_base"]).denominator),
            "-movflags", "+faststart", str(args.output),
        ], check=True)
    output = probe(args.output)
    for key in ("width", "height", "r_frame_rate", "nb_frames", "start_time", "time_base", "duration"):
        if output.get(key) != original.get(key):
            raise RuntimeError(f"Video timing or geometry changed: {key}: {original.get(key)} -> {output.get(key)}")
    if args.poster:
        args.poster.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(args.output), "-frames:v", "1", "-q:v", "2", "-update", "1", str(args.poster)], check=True)
    report = {
        "method": "Paper Fig. 8 white-anchored linear-light gain and soft highlight rolloff; fixed per-camera gains with a sampled clipping guard.",
        "source_sha256": hashlib.sha256(args.source.read_bytes()).hexdigest(),
        "output_sha256": hashlib.sha256(args.output.read_bytes()).hexdigest(),
        "target_white": args.target_white, "calibration_frames": len(samples), "max_added_clipping": args.max_added_clipping,
        "views": views, "video": output,
    }
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
