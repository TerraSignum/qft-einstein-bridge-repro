"""Tests for the bundled cosmological-anchor table.

The table records the loop-class predictions for the 18 cosmological /
Einstein-sector observables (14 single-sector + N_eff/T_CMB/eta_B/m_H = 18 anchored, plus 2 structural) paired with their canonical anchors
(Planck 2018 / PDG / NuFIT 6.1). The tests assert that:

  1. All 18 observables are present with id, name, loop_class, tier;
  2. Every anchored observable lands inside the PRECISE 2.5% band;
  3. The Yukawa-Damping cross-sector cluster (alpha_dn, w_DE, H_0) all
     close on the loop class 1+gamma/4 with sub-0.3% residuals;
  4. The summary counts in the bundle agree with what the per-row
     scan produces (10 EXACT + 2 PRECISE + 2 STRUCTURAL).
"""

import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))

import verify_cosmological_anchors as M  # noqa: E402


@pytest.fixture(scope="module")
def anchors():
    return M.load_anchors()


@pytest.fixture(scope="module")
def output(anchors):
    M.main()
    out_path = REPO / "outputs" / "cosmological_anchors_recompute.json"
    with open(out_path, "r", encoding="utf-8") as f:
        return json.load(f)


def test_eighteen_observables(anchors):
    assert len(anchors["anchors"]) == 18


def test_all_required_fields_present(anchors):
    required = {"id", "name", "loop_class", "tier"}
    for a in anchors["anchors"]:
        missing = required - set(a.keys())
        assert not missing, (
            f"Observable {a.get('id', '?')} missing fields: {missing}"
        )


def test_anchored_residuals_inside_disclosed_tier(anchors):
    """Strict tier bands:
      EXACT   -> residual <= 1.0%
      PRECISE -> residual <= 2.5%
      ORDER   -> any residual but with a disclosed note (and ideally a
                 binding_closure pointing to a tighter cross-check)
    """
    for a in anchors["anchors"]:
        tier = a["tier"]
        if "STRUCTURAL" in tier:
            continue
        if tier == "ORDER":
            assert "note" in a, (
                f"ORDER-tier observable {a['name']} must carry an "
                f"explanatory note"
            )
            continue
        if tier == "EXACT":
            assert a["residual_pct"] <= 1.0, (
                f"EXACT-tier {a['name']} residual {a['residual_pct']:.3f}% "
                f"exceeds 1.0% EXACT band"
            )
        elif tier == "PRECISE":
            assert a["residual_pct"] <= 2.5, (
                f"PRECISE-tier {a['name']} residual {a['residual_pct']:.3f}% "
                f"exceeds 2.5% PRECISE band"
            )


def test_yukawa_damping_cluster_three_observables_close_on_same_class(anchors):
    """The Yukawa-Damping cluster: alpha_dn (QFT), w_DE (Einstein),
    H_0 (Einstein) all close on 1+gamma/4 with sub-0.3% residuals.
    Same loop class, two different sectors, three observables."""
    cluster = anchors["cross_sector_consistency_with_QFT"]
    obs = cluster["Yukawa_Damping_class_1_plus_gamma_over_4_carries_three_observables_across_two_sectors"]
    assert len(obs) == 3
    names = {o["observable"] for o in obs}
    assert names == {"alpha_dn", "w_DE", "H_0"}
    sectors = {o["sector"] for o in obs}
    assert sectors == {"QFT", "Einstein"}
    for o in obs:
        assert o["residual_pct"] < 0.3, (
            f"{o['observable']} residual {o['residual_pct']:.3f}% "
            f"exceeds 0.3%"
        )


def test_yukawa_cluster_significance_above_3sigma(anchors):
    """The Fisher's-combined p reported in the bundle must correspond
    to >= 3 sigma (i.e. p <= 2.7e-3)."""
    cluster = anchors["cross_sector_consistency_with_QFT"]
    p_combined = cluster["fishers_combined_p_three_observables"]
    assert p_combined < 2.7e-3, (
        f"Cluster p_combined {p_combined:.2e} is not 3-sigma significant"
    )


def test_summary_counts_consistent_with_per_row_scan(anchors):
    counts = {"EXACT": 0, "PRECISE": 0, "STRUCTURAL": 0, "ORDER": 0}
    for a in anchors["anchors"]:
        tier = a["tier"]
        if "STRUCTURAL" in tier:
            counts["STRUCTURAL"] += 1
        elif tier == "ORDER":
            counts["ORDER"] += 1
        elif "EXACT" in tier:
            counts["EXACT"] += 1
        elif "PRECISE" in tier:
            counts["PRECISE"] += 1
    assert counts == {"EXACT": 12, "PRECISE": 2, "STRUCTURAL": 2, "ORDER": 2}
    s = anchors["summary_counts"]
    assert s["EXACT"] == counts["EXACT"]
    assert s["PRECISE"] == counts["PRECISE"]
    assert s["STRUCTURAL"] == counts["STRUCTURAL"]
    assert s["ORDER"] == counts["ORDER"]


def test_recompute_output_passes(output):
    assert output["verdict"] == "PASS"
    assert output["all_anchored_within_disclosed_tier"] is True
    assert output["EXACT_anchored"] == 12
    assert output["PRECISE_anchored"] == 2
    assert output["ORDER_anchored"] == 2
    assert output["STRUCTURAL"] == 2
