"""Both sectors must source identical coefficient values."""

import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def _load(name):
    with open(REPO / "data" / name, "r", encoding="utf-8") as f:
        return json.load(f)


def test_bridge_lists_five_coefficients():
    bridge = _load("bridge_conditionals.json")
    cb = bridge["bridge_axes"]["shared_coefficients"]
    for k in ("alpha_xi", "D_Omega", "beta_pi", "gamma", "eps_sync2"):
        assert k in cb


def test_local_coefficients_match_bridge():
    bridge = _load("bridge_conditionals.json")
    coef = _load("causal_wave_coefficients.json")
    cb = bridge["bridge_axes"]["shared_coefficients"]
    for k in ("alpha_xi", "D_Omega", "beta_pi", "gamma", "eps_sync2"):
        assert abs(cb[k] - coef["coefficients"][k]) < 1e-6


def test_coefficients_are_in_unit_interval():
    coef = _load("causal_wave_coefficients.json")
    for k, v in coef["coefficients"].items():
        assert 0 < v < 1


def test_T_parity_axiom_shared():
    bridge = _load("bridge_conditionals.json")
    tp = bridge["bridge_axes"]["shared_T_parity_source"]
    # Reviewer-language axiom string only; no program-internal label.
    assert "T-parity" in tp["axiom"]
    assert "Xi" in tp["axiom"] or "defect field" in tp["axiom"]
    assert "QFT_sector" in tp["common_to"]
    assert "Einstein_sector" in tp["common_to"]
