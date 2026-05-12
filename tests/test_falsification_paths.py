"""Each shared falsification path must be machine-readable."""

import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def _bridge():
    with open(REPO / "data" / "bridge_conditionals.json", "r", encoding="utf-8") as f:
        return json.load(f)


def test_at_least_four_falsification_paths():
    b = _bridge()
    assert len(b["shared_falsification_paths"]) >= 4


def test_each_path_has_trigger_and_test():
    b = _bridge()
    for fp in b["shared_falsification_paths"]:
        assert fp["trigger"]
        assert fp["test"]
        assert len(fp["test"]) > 10


def test_T_parity_axiom_failure_documented():
    """The T-parity-axiom-failure falsification path must be present
    among the shared falsification paths."""
    b = _bridge()
    triggers = [fp["trigger"] for fp in b["shared_falsification_paths"]]
    assert "T-parity-axiom-failure" in triggers
    fp = next(f for f in b["shared_falsification_paths"]
              if f["trigger"] == "T-parity-axiom-failure")
    assert "T-parity" in fp["test"] or "theta_em" in fp["test"]


def test_mapping_inconsistency_falsification_documented():
    b = _bridge()
    triggers = [fp["trigger"] for fp in b["shared_falsification_paths"]]
    assert "mapping-inconsistency" in triggers


def test_structural_claim_documented():
    b = _bridge()
    sc = b["structural_claim"]
    assert "five-coefficient" in sc.lower() or "same five" in sc.lower()
    assert b["non_claim"]
