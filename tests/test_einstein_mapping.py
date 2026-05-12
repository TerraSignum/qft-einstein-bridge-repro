"""Einstein sector dominant classes must include n in {2, 4}."""

import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def _einstein():
    with open(REPO / "data" / "einstein_sector_mapping.json", "r", encoding="utf-8") as f:
        return json.load(f)


def test_dominant_classes_include_2_and_4():
    e = _einstein()
    classes = set(e["spinor_trace_classes"])
    assert 2 in classes
    assert 4 in classes


def test_einstein_includes_omega_dm():
    e = _einstein()
    names = [o["name"] for o in e["observables"]]
    assert "Omega_DM_h2" in names


def test_einstein_includes_T_RH():
    e = _einstein()
    names = [o["name"] for o in e["observables"]]
    assert "T_RH" in names


def test_einstein_each_observable_has_n():
    e = _einstein()
    for o in e["observables"]:
        assert "n" in o
        assert o["n"] in (0, 1, 2, 4)
