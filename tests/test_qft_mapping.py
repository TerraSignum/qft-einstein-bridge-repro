"""QFT sector observables must all sit at spinor-trace class n=1."""

import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def _qft():
    with open(REPO / "data" / "qft_sector_mapping.json", "r", encoding="utf-8") as f:
        return json.load(f)


def test_qft_class_is_one():
    q = _qft()
    assert q["spinor_trace_class"] == 1


def test_qft_observables_have_loop_class():
    q = _qft()
    for o in q["observables"]:
        assert "loop_class" in o
        assert o["loop_class"]


def test_qft_lemmas_subset_of_library():
    q = _qft()
    library_lemmas = {1, 2, 3, 4, 5, 6, 7, 8, "pure-eps2", "1+2", "1+5"}
    for o in q["observables"]:
        assert o["lemma"] in library_lemmas


def test_qft_includes_v_EW():
    q = _qft()
    names = [o["name"] for o in q["observables"]]
    assert "v_EW" in names
