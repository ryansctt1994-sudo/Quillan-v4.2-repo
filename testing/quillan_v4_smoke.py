#!/usr/bin/env python3
"""Smoke test and parameter receipt for Quillan-v4.2-model/🧠 Quillan v4.py.

Usage (from anywhere, needs torch):
    python3 testing/quillan_v4_smoke.py

1. Builds QuillanRoninV51 with the DEFAULT ModelConfig on PyTorch's "meta"
   device (no weights allocated) and prints the parameter count per
   module, so the file's "~3B" docstring can be compared with what the
   code actually builds.
2. Builds a tiny config on CPU and runs one forward pass per modality
   (TEXT, AUDIO, IMAGE), checking output shape and finiteness.

This shows the code instantiates and runs forward passes. It says nothing
about training, weights, quality, or benchmark results.
Exits non-zero if any forward pass fails.
"""
import importlib.util
import sys
from pathlib import Path

import torch

MODEL = Path(__file__).resolve().parents[1] / "Quillan-v4.2-model" / "🧠 Quillan v4.py"

spec = importlib.util.spec_from_file_location("quillan_v4", MODEL)
q = importlib.util.module_from_spec(spec)
spec.loader.exec_module(q)

with torch.device("meta"):
    full = q.QuillanRoninV51(q.ModelConfig())
counts = full.count_parameters()
print("Default ModelConfig parameter counts (meta device):")
for name, n in counts.items():
    print(f"  {name:13s} {n / 1e6:9.1f}M")

tiny = q.ModelConfig(
    hidden_dim=64, intermediate_dim=128, num_layers=2, router_dim=32, router_heads=2,
    num_experts=4, num_active_experts=2, expert_dim=64, diffusion_steps=2,
    diffusion_layers=1, time_embed_dim=16, vocab_size=100, audio_vocab_size=64,
    video_vocab_size=64, text_encoder_dim=32, audio_encoder_dim=32,
    video_encoder_dim=32, image_encoder_dim=32, text_decoder_dim=32,
    audio_decoder_dim=32, video_decoder_dim=32, image_decoder_dim=32,
    finalize_dim=32, max_seq_length=64,
)
torch.manual_seed(0)
model = q.QuillanRoninV51(tiny).eval()
cases = [
    ("TEXT", torch.randint(0, tiny.vocab_size, (2, 16)), {}),
    ("AUDIO", torch.randn(2, 1, 1600), {}),
    ("IMAGE", torch.randn(2, 3, 32, 32), {"image_shape": (32, 32)}),
]
failed = False
for name, x, kwargs in cases:
    try:
        with torch.no_grad():
            out = model(q.Modality[name], x, **kwargs)["output"]
        finite = bool(torch.isfinite(out).all())
        print(f"{'PASS' if finite else 'FAIL'} {name}: output shape {tuple(out.shape)}, finite={finite}")
        failed |= not finite
    except Exception as e:  # report every modality, then fail
        print(f"FAIL {name}: {type(e).__name__}: {e}")
        failed = True
sys.exit(1 if failed else 0)
