"""Claim-linked structural tests for the enhanced Quillan council layer.

These tests deliberately use a tiny synthetic configuration. They test structure and
runtime mechanics only; they do not test language-model quality, training quality,
expert specialization, AGI, consciousness, or production readiness.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import unittest

import torch


REPO_ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = REPO_ROOT / "Quillan-v4.2-model" / "quillan_council_enhanced.py"


def load_enhanced_module():
    spec = importlib.util.spec_from_file_location("quillan_council_enhanced", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class FixtureConfig:
    n_council_experts = 32
    n_embd = 8
    dropout = 0.0
    council_layers = [8, 4, 2, 1]


class EnhancedCouncilStructuralTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.manual_seed(1337)
        cls.mod = load_enhanced_module()

    def make_layer(self):
        torch.manual_seed(1337)
        return self.mod.CouncilMoELayer(FixtureConfig())

    def fixture_input(self):
        torch.manual_seed(2026)
        return torch.randn(2, 3, FixtureConfig.n_embd)

    def test_q_model_001_instantiates_32_experts(self):
        """Q-MODEL-001: the tested council configuration instantiates 32 experts."""
        layer = self.make_layer()
        self.assertEqual(layer.num_experts, 32)
        self.assertEqual(len(layer.experts), 32)
        self.assertTrue(all(isinstance(e, self.mod.CouncilExpert) for e in layer.experts))

    def test_q_model_002_sparse_top2_routing_executes(self):
        """Q-MODEL-002: each token receives exactly two valid expert selections."""
        layer = self.make_layer().eval()
        out = layer(self.fixture_input())

        self.assertEqual(layer.top_k, 2)
        self.assertEqual(tuple(out.active_experts.shape), (2, 3, 2))
        self.assertTrue(torch.all(out.active_experts >= 0))
        self.assertTrue(torch.all(out.active_experts < 32))
        self.assertTrue(torch.all(out.active_experts[..., 0] != out.active_experts[..., 1]))

    def test_q_model_003_router_telemetry_is_observable(self):
        """Q-MODEL-003: selected expert IDs and router logits are returned and finite."""
        layer = self.make_layer().eval()
        out = layer(self.fixture_input())

        self.assertEqual(tuple(out.router_logits.shape), (2, 3, 32))
        self.assertEqual(tuple(out.active_experts.shape), (2, 3, 2))
        self.assertTrue(torch.isfinite(out.router_logits).all().item())

        expected = torch.topk(
            torch.softmax(out.router_logits, dim=-1),
            k=2,
            dim=-1,
        ).indices
        self.assertTrue(torch.equal(out.active_experts, expected))

    def test_q_model_005_selected_experts_receive_expected_gradients(self):
        """Q-MODEL-005: selected experts and router receive finite nonzero gradients."""
        layer = self.make_layer().train()
        x = self.fixture_input().requires_grad_(True)
        out = layer(x)

        selected = set(int(i) for i in out.active_experts.detach().reshape(-1).tolist())
        self.assertTrue(selected)

        loss = out.hidden_states.square().mean()
        loss.backward()

        def expert_grad_norm(expert):
            total = torch.tensor(0.0)
            saw_grad = False
            for param in expert.parameters():
                if param.grad is not None:
                    saw_grad = True
                    self.assertTrue(torch.isfinite(param.grad).all().item())
                    total = total + param.grad.detach().abs().sum().cpu()
            return saw_grad, float(total.item())

        for idx, expert in enumerate(layer.experts):
            saw_grad, norm = expert_grad_norm(expert)
            if idx in selected:
                self.assertTrue(saw_grad, f"selected expert {idx} had no gradients")
                self.assertGreater(norm, 0.0, f"selected expert {idx} had zero gradient norm")
            else:
                self.assertTrue(
                    (not saw_grad) or norm == 0.0,
                    f"unselected expert {idx} unexpectedly received gradient {norm}",
                )

        self.assertIsNotNone(layer.router.weight.grad)
        self.assertTrue(torch.isfinite(layer.router.weight.grad).all().item())
        self.assertGreater(float(layer.router.weight.grad.detach().abs().sum().item()), 0.0)

    def test_q_model_004_consensus_score_and_modulation_execute(self):
        """Q-MODEL-004: scalar sigmoid consensus is bounded and modulates output."""
        layer = self.make_layer().eval()
        x = self.fixture_input()

        # Force a stable non-neutral consensus score so the modulation check cannot
        # accidentally pass/fail because a randomly initialized logit is ~0.
        final_linear = [m for m in layer.consensus.modules() if isinstance(m, torch.nn.Linear)][-1]
        with torch.no_grad():
            final_linear.weight.zero_()
            final_linear.bias.fill_(2.0)
            layer.consensus_weight.zero_()
            unmodulated = layer(x)
            layer.consensus_weight.fill_(1.0)
            modulated = layer(x)

        score = modulated.consensus_score
        self.assertEqual(tuple(score.shape), (2, 3, 1))
        self.assertTrue(torch.isfinite(score).all().item())
        self.assertTrue(torch.all(score > 0).item())
        self.assertTrue(torch.all(score < 1).item())
        self.assertEqual(tuple(modulated.hidden_states.shape), tuple(x.shape))
        self.assertFalse(torch.allclose(unmodulated.hidden_states, modulated.hidden_states))

        # Confirm the consensus influence parameter participates in differentiation.
        layer = self.make_layer().train()
        out = layer(self.fixture_input())
        out.hidden_states.sum().backward()
        self.assertIsNotNone(layer.consensus_weight.grad)
        self.assertTrue(torch.isfinite(layer.consensus_weight.grad).all().item())


if __name__ == "__main__":
    unittest.main(verbosity=2)
