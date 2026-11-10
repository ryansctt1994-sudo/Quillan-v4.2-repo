"""Executable tests for quillan_council_enhanced.py.

These check the properties the module can actually guarantee: shapes, valid routing,
a consensus score in [0, 1], normalised expert weights, gradient flow and determinism.
They do not measure model quality. Quality claims need a reproducible experiment
(see EVIDENCE_STATUS.md).
"""
from types import SimpleNamespace

import pytest
import torch
import torch.nn as nn

from quillan_council_enhanced import CouncilExpert, CouncilMoELayer, CouncilOutput, HierarchicalConsensus

B, T, C, N_EXPERTS = 2, 5, 16, 6


def make_config(**overrides):
    base = dict(n_council_experts=N_EXPERTS, n_embd=C, dropout=0.0, council_layers=[8, 4, 2, 1])
    base.update(overrides)
    return SimpleNamespace(**base)


@pytest.fixture
def layer():
    torch.manual_seed(0)
    return CouncilMoELayer(make_config()).eval()


@pytest.fixture
def inputs():
    torch.manual_seed(1)
    return torch.randn(B, T, C)


def test_expert_preserves_shape():
    expert = CouncilExpert(C, dropout=0.0)
    assert expert(torch.randn(3, C)).shape == (3, C)


def test_consensus_gives_one_raw_score_per_token():
    consensus = HierarchicalConsensus(C, [8, 4, 2, 1])
    assert consensus(torch.randn(B, T, C)).shape == (B, T, 1)


def test_layer_returns_council_output_with_expected_shapes(layer, inputs):
    out = layer(inputs)
    assert isinstance(out, CouncilOutput)
    assert out.hidden_states.shape == (B, T, C)
    assert out.active_experts.shape == (B, T, 2)
    assert out.router_logits.shape == (B, T, N_EXPERTS)
    assert out.consensus_score.shape == (B, T, 1)


def test_routing_picks_two_distinct_valid_experts_per_token(layer, inputs):
    chosen = layer(inputs).active_experts
    assert chosen.min() >= 0 and chosen.max() < N_EXPERTS
    assert torch.all(chosen[..., 0] != chosen[..., 1])


def test_consensus_score_is_a_probability(layer, inputs):
    score = layer(inputs).consensus_score
    assert torch.all(score >= 0.0) and torch.all(score <= 1.0)


class ConstantExpert(nn.Module):
    def __init__(self, value):
        super().__init__()
        self.value = float(value)

    def forward(self, x):
        return torch.full_like(x, self.value)


def test_expert_weights_are_normalised_and_bounded(layer, inputs):
    """With constant experts, each token's output must lie between its two chosen experts' values.
    Unnormalised weights would push the output outside that range."""
    layer.experts = nn.ModuleList([ConstantExpert(i + 1) for i in range(N_EXPERTS)])
    with torch.no_grad():
        layer.consensus_weight.zero_()  # no consensus modulation, so only the mixture is measured
    out = layer(inputs)
    for b in range(B):
        for t in range(T):
            a, c = out.active_experts[b, t].tolist()
            low, high = min(a, c) + 1.0, max(a, c) + 1.0
            value = out.hidden_states[b, t, 0].item()
            assert low - 1e-5 <= value <= high + 1e-5, (b, t, value, low, high)


def test_gradients_reach_router_and_experts(layer, inputs):
    layer.train()
    out = layer(inputs)
    loss = out.hidden_states.pow(2).mean() + out.consensus_score.mean()
    loss.backward()
    assert layer.router.weight.grad is not None and layer.router.weight.grad.abs().sum() > 0
    assert any(p.grad is not None and p.grad.abs().sum() > 0 for p in layer.experts[0].parameters())


def test_same_seed_gives_identical_output():
    def run():
        torch.manual_seed(7)
        module = CouncilMoELayer(make_config()).eval()
        torch.manual_seed(8)
        return module(torch.randn(B, T, C)).hidden_states

    assert torch.allclose(run(), run())


def test_layer_has_exactly_the_configured_number_of_experts(layer):
    assert len(layer.experts) == N_EXPERTS
    assert layer.top_k == 2
