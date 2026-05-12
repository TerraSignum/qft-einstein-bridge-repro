"""Both sectors draw from the same loop-class library."""

import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def _load(name):
    with open(REPO / "data" / name, "r", encoding="utf-8") as f:
        return json.load(f)


def test_library_lemmas_are_set_of_ten():
    lib = _load("loop_class_library.json")
    declared = set(lib["lemma_set"])
    assert declared == {
        1, 2, 3, 4, 5, 6, 7, 8,
        "pure-eps2",
        "lambda-s-closure",
    }


def test_qft_lemmas_subset_of_library():
    qft = _load("qft_sector_mapping.json")
    lib = _load("loop_class_library.json")
    base = set(lib["lemma_set"])
    for o in qft["observables"]:
        l = o["lemma"]
        # 2-loop compounds use form "1+2" etc.
        if isinstance(l, str) and "+" in l:
            parts = l.split("+")
            for p in parts:
                p_clean = p.strip()
                try:
                    p_clean = int(p_clean)
                except ValueError:
                    pass
                assert p_clean in base, f"compound part {p_clean} not in library"
        else:
            assert l in base


def test_einstein_lemmas_subset_of_library():
    einstein = _load("einstein_sector_mapping.json")
    lib = _load("loop_class_library.json")
    base = set(lib["lemma_set"])
    for o in einstein["observables"]:
        l = o["lemma"]
        if l is None:
            continue  # tree-level structural identities
        if isinstance(l, str) and "+" in l:
            parts = l.split("+")
            for p in parts:
                p_clean = p.strip()
                try:
                    p_clean = int(p_clean)
                except ValueError:
                    pass
                assert p_clean in base, f"compound part {p_clean} not in library"
        else:
            assert l in base


def test_compounds_are_capped_at_two_factors():
    qft = _load("qft_sector_mapping.json")
    einstein = _load("einstein_sector_mapping.json")
    for blob in (qft, einstein):
        for o in blob["observables"]:
            l = o.get("lemma")
            if isinstance(l, str) and "+" in l:
                assert l.count("+") <= 1, (
                    f"{o['name']} lemma {l} has more than 2 factors; "
                    f"three-loop compounds are forbidden."
                )
