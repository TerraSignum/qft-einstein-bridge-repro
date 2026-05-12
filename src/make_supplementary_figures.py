"""Supplementary figures for the bridge note (iter-3 additions):
  fig_cosmological_anchors_residuals.pdf  - 16-row anchor residual scatter
  fig_lambda_2plus1_panel.pdf             - Lambda_munu 2+1 anisotropy panel
"""
from __future__ import annotations
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "paper" / "figures"
OUT.mkdir(parents=True, exist_ok=True)


def fig_cosmological_anchors_residuals():
    p = REPO / "data" / "cosmological_anchors.json"
    with open(p) as f:
        d = json.load(f)
    rows = [r for r in d.get("anchors", []) if r.get("residual_pct") is not None]
    if not rows:
        return
    ids = [r["id"] for r in rows]
    res = [float(r.get("residual_pct", 0)) for r in rows]
    tiers = [r.get("tier", "?") for r in rows]
    color = {"EXACT": "#3c6ea7", "PRECISE": "#d97f4a", "ORDER": "#7a8ca0",
             "STRUCTURAL": "#aaaaaa", "FACTOR2": "#5a3010"}
    fig, ax = plt.subplots(figsize=(10, 4.6))
    for i, (lab, r, t) in enumerate(zip(ids, res, tiers)):
        ax.bar(i, max(abs(r), 1e-3), color=color.get(t, "#444"),
                edgecolor="black", linewidth=0.6,
                label=t if t not in [b.get_label() for b in ax.containers] else None)
    ax.set_xticks(range(len(ids)))
    ax.set_xticklabels(ids, rotation=60, fontsize=8, ha="right")
    ax.set_ylabel(r"$|\mathrm{residual}|\,\%$")
    ax.axhline(1.0, color="#3c6ea7", linestyle="--", linewidth=0.8,
                label=r"EXACT $\leq 1\%$")
    ax.axhline(1.5, color="#d97f4a", linestyle="--", linewidth=0.8,
                label=r"PRECISE $\leq 1.5\%$")
    ax.set_yscale("log")
    ax.set_title("Cosmological-anchor residuals across 16 Einstein-sector observables")
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), fontsize=8, loc="upper right")
    ax.grid(True, axis="y", alpha=0.3)
    plt.tight_layout()
    out = OUT / "fig_cosmological_anchors_residuals.pdf"
    plt.savefig(out, dpi=200, bbox_inches="tight")
    plt.savefig(out.with_suffix(".png"), dpi=180, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {out.relative_to(REPO)}")


def fig_lambda_2plus1_panel():
    alpha_xi = 9/10
    gamma = 1/10
    lambda_t = alpha_xi**2
    lambda_s_neg = -gamma**2/2
    lambda_s_pos = +gamma**2/2
    trace = lambda_t + 2*lambda_s_neg + lambda_s_pos
    fig, ax = plt.subplots(figsize=(7.5, 4.4))
    components = [r"$\Lambda_{tt}$", r"$\Lambda_{xx}$", r"$\Lambda_{yy}$", r"$\Lambda_{zz}$"]
    values = [lambda_t, lambda_s_neg, lambda_s_neg, lambda_s_pos]
    colors = ["#3c6ea7", "#7a8ca0", "#7a8ca0", "#d97f4a"]
    bars = ax.bar(components, values, color=colors, edgecolor="black", linewidth=0.8)
    for b, v in zip(bars, values):
        ax.annotate(f"{v:+.3f}",
                     xy=(b.get_x() + b.get_width()/2, v + 0.02 if v > 0 else v - 0.05),
                     ha="center", fontsize=10)
    ax.axhline(0, color="black", linewidth=0.6)
    ax.set_ylabel(r"$\Lambda_{\mu\mu}$")
    ax.set_title(r"$\Lambda_{\mu\nu}$ 2+1 anisotropic diagonal" +
                  f"\n  trace = $\\alpha_\\xi^2 - \\gamma^2/2 = 161/200 = {trace:.3f}$")
    ax.text(0.5, 0.92, r"stable across all $N\in[28,200]$ (Paper~4B)",
              transform=ax.transAxes, ha="center", fontsize=9,
              bbox=dict(boxstyle="round,pad=0.3", facecolor="#fffbe0", edgecolor="black"))
    ax.grid(True, axis="y", alpha=0.3)
    ax.set_ylim(-0.05, 0.95)
    plt.tight_layout()
    out = OUT / "fig_lambda_2plus1_panel.pdf"
    plt.savefig(out, dpi=200, bbox_inches="tight")
    plt.savefig(out.with_suffix(".png"), dpi=180, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {out.relative_to(REPO)}")


def main():
    try: fig_cosmological_anchors_residuals()
    except Exception as e: print(f"cosmo_anchor: {type(e).__name__}: {e}")
    try: fig_lambda_2plus1_panel()
    except Exception as e: print(f"lambda_2plus1: {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
