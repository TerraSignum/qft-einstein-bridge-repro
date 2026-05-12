r"""
Bridge consistency check between the QFT and Einstein sectors.

Verifies:
  1. Both sectors source their five coefficients from the same JSON.
  2. The QFT sector maps its observables to spinor-trace class n=1.
  3. The Einstein sector's dominant classes are n=2 and n=4 (with
     allowance for tree-level structural identities at n=1).
  4. Both sectors share the same loop-class library (lemmata 1-8 plus
     pure-sync).
  5. The shared T-parity source axiom (defect field Xi T-odd,
     theta_em=pi) is documented as a conditional applying to both
     sectors.
  6. Every documented falsification path applies to both sectors
     symmetrically.

Usage:
    python ./src/check_bridge_consistency.py
"""

import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "data"
OUTPUTS = REPO / "outputs"
OUTPUTS.mkdir(parents=True, exist_ok=True)


def load(name):
    with open(DATA / name, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    bridge = load("bridge_conditionals.json")
    qft = load("qft_sector_mapping.json")
    einstein = load("einstein_sector_mapping.json")
    coef = load("causal_wave_coefficients.json")
    lib = load("loop_class_library.json")

    print("=" * 80)
    print("QFT-Einstein bridge consistency check")
    print("=" * 80)
    print()

    # 1. Shared coefficients
    print("--- (1) Shared coefficients ---")
    cb = bridge["bridge_axes"]["shared_coefficients"]
    keys = ["alpha_xi", "D_Omega", "beta_pi", "gamma", "eps_sync2"]
    all_ok = True
    for k in keys:
        a = cb[k]
        b = coef["coefficients"][k]
        ok = abs(a - b) < 1e-6
        if not ok:
            all_ok = False
        print(f"  {k}: bridge={a}, local={b}  -- {'OK' if ok else 'MISMATCH'}")
    print(f"  Verdict: {'PASS' if all_ok else 'FAIL'}")
    print()

    # 2. QFT sector -> n=1
    print("--- (2) QFT sector spinor-trace class ---")
    n_qft = qft["spinor_trace_class"]
    print(f"  Declared:        n = {n_qft}")
    print(f"  Bridge expects:  {bridge['QFT_sector_mapping']['spinor_trace_class']}")
    qft_ok = n_qft == bridge["QFT_sector_mapping"]["spinor_trace_class"]
    print(f"  Verdict: {'PASS' if qft_ok else 'FAIL'}")
    print()

    # 3. Einstein sector -> n in {2, 4} (with tree-level n=1 allowed)
    print("--- (3) Einstein sector spinor-trace classes ---")
    n_einstein = einstein["spinor_trace_classes"]
    print(f"  Declared dominant: n in {n_einstein}")
    print(f"  Bridge expects:    n in {bridge['Einstein_sector_mapping']['spinor_trace_classes']}")
    einstein_ok = (set(n_einstein) ==
                   set(bridge["Einstein_sector_mapping"]["spinor_trace_classes"]))
    print(f"  Verdict: {'PASS' if einstein_ok else 'FAIL'}")
    print()

    # 4. Shared loop library
    print("--- (4) Shared loop library ---")
    lemma_qft = {o.get("lemma") for o in qft["observables"]}
    lemma_einstein = {o.get("lemma") for o in einstein["observables"]}
    base = set(lib["lemma_set"])

    def _lemma_in_library(l):
        if l is None:
            return True  # tree-level structural identity
        if isinstance(l, str) and "+" in l:
            parts = [p.strip() for p in l.split("+")]
            for p in parts:
                try:
                    p_clean = int(p)
                except ValueError:
                    p_clean = p
                if p_clean not in base:
                    return False
            return True
        return l in base

    qft_violations = [l for l in lemma_qft if not _lemma_in_library(l)]
    einstein_violations = [l for l in lemma_einstein if not _lemma_in_library(l)]
    in_qft_only = lemma_qft - lemma_einstein
    in_einstein_only = lemma_einstein - lemma_qft
    library_ok = (not qft_violations) and (not einstein_violations)
    print(f"  Library lemmas: {sorted([str(x) for x in lib['lemma_set']])}")
    print(f"  QFT uses:       {sorted([str(x) for x in lemma_qft])}")
    print(f"  Einstein uses:  {sorted([str(x) for x in lemma_einstein])}")
    print(f"  QFT-only:       {sorted([str(x) for x in in_qft_only])}")
    print(f"  Einstein-only:  {sorted([str(x) for x in in_einstein_only])}")
    if qft_violations:
        print(f"  QFT lemmas outside library: {qft_violations}")
    if einstein_violations:
        print(f"  Einstein lemmas outside library: {einstein_violations}")
    print(f"  Verdict: {'PASS' if library_ok else 'FAIL'} "
          f"(both sectors draw from the same library; specialization is by n, not by class)")
    print()

    # 5. T-parity source axiom
    print("--- (5) Shared T-parity source axiom ---")
    tp = bridge["bridge_axes"]["shared_T_parity_source"]
    print(f"  Axiom:        {tp['axiom']}")
    print(f"  Consequence:  {tp['consequence']}")
    print(f"  Common to:    {tp['common_to']}")
    tp_ok = ("T-parity" in tp["axiom"]
             and "QFT_sector" in tp["common_to"]
             and "Einstein_sector" in tp["common_to"])
    print(f"  Verdict: {'PASS' if tp_ok else 'FAIL'}")
    print()

    # 6. Falsification paths
    print("--- (6) Shared falsification paths ---")
    fp_required_keys = {"trigger", "test", "applies_to"}
    fp_violations = []
    for fp in bridge["shared_falsification_paths"]:
        missing = fp_required_keys - set(fp.keys())
        if missing:
            fp_violations.append((fp.get("trigger", "?"), f"missing keys: {missing}"))
        applies = set(fp.get("applies_to", []))
        if not {"QFT_sector", "Einstein_sector"}.issubset(applies):
            fp_violations.append(
                (fp.get("trigger", "?"),
                 f"applies_to does not cover both sectors: {applies}")
            )
        print(f"  trigger='{fp.get('trigger', '?')}': {fp.get('test', '(no test field)')}")
    expected_fp_count = 4
    fp_count_ok = len(bridge["shared_falsification_paths"]) >= expected_fp_count
    fp_ok = (not fp_violations) and fp_count_ok
    if fp_violations:
        print(f"  Violations: {fp_violations}")
    print(f"  Verdict: {'PASS' if fp_ok else 'FAIL'} "
          f"({len(bridge['shared_falsification_paths'])} of >={expected_fp_count} required paths "
          f"apply to both sectors)")
    print()

    print("--- Aggregate ---")
    overall = all_ok and qft_ok and einstein_ok and library_ok and tp_ok and fp_ok
    print(f"  Bridge consistent: {'PASS' if overall else 'FAIL'}")

    out = {
        "shared_coefficients_ok": all_ok,
        "qft_sector_ok": qft_ok,
        "einstein_sector_ok": einstein_ok,
        "library_ok": library_ok,
        "T_parity_shared": tp_ok,
        "falsification_paths_ok": fp_ok,
        "n_qft_observables": len(qft["observables"]),
        "n_einstein_observables": len(einstein["observables"]),
        "shared_falsification_paths": len(bridge["shared_falsification_paths"]),
        "overall": "PASS" if overall else "FAIL",
    }
    out_path = OUTPUTS / "bridge_consistency_report.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print()
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
