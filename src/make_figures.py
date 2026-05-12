r"""
Generate the four figures of the Paper 5 bridge note.

  Figure 1 - Common-carrier diagram: same coefficients + same library -> two sectors.
  Figure 2 - Spinor-trace class tree (n = 1, 2, 4).
  Figure 3 - QFT side vs Einstein side observable inventory.
  Figure 4 - Shared falsification map.

Usage:
    python ./src/make_figures.py
"""

import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))

FIG_DIR = REPO / "paper" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.size": 11,
    "axes.titlesize": 12,
    "axes.labelsize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "grid.linestyle": "--",
})


def save_both(fig, stem):
    pdf = FIG_DIR / f"{stem}.pdf"
    png = FIG_DIR / f"{stem}.png"
    fig.savefig(pdf, format="pdf")
    fig.savefig(png, format="png")
    print(f"  Saved: {pdf.relative_to(REPO)} + .png")


def figure_1_common_carrier():
    """Common-carrier diagram: shared coefficients + library -> two sectors."""
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.set_axis_off()

    # Top: shared inputs
    ax.text(0.50, 0.92, "Shared inputs (causal-wave transport law)",
            ha="center", fontsize=12, fontweight="bold")
    inputs = [
        (0.18, 0.72, "Five measured\ncoefficients\n" + r"$\alpha_\xi, D(\Omega), \beta_\pi, \gamma, \varepsilon^{2}_{\mathrm{sync}}$",
         "#cfe2f3"),
        (0.50, 0.72, "Loop-class library\n9 lemmata,\n19 atomic classes",
         "#fce5cd"),
        (0.82, 0.72, "T-parity source axiom\n" + r"$\theta_\mathrm{em} = \pi$",
         "#d9ead3"),
    ]
    for (xc, yc, label, color) in inputs:
        rect = plt.Rectangle((xc - 0.13, yc - 0.10), 0.26, 0.18,
                             facecolor=color, edgecolor="black", lw=1.4)
        ax.add_patch(rect)
        ax.text(xc, yc, label, ha="center", va="center", fontsize=10)

    # Arrows from inputs down into two sectors
    for xc in [0.18, 0.50, 0.82]:
        ax.annotate("", xy=(0.30, 0.42), xytext=(xc, 0.62),
                    arrowprops=dict(arrowstyle="->", lw=1.0, color="#888"))
        ax.annotate("", xy=(0.70, 0.42), xytext=(xc, 0.62),
                    arrowprops=dict(arrowstyle="->", lw=1.0, color="#888"))

    # Bottom: two sectors
    qft = plt.Rectangle((0.10, 0.20), 0.40, 0.22, facecolor="#cce5ff", edgecolor="black", lw=1.4)
    einstein = plt.Rectangle((0.50, 0.20), 0.40, 0.22, facecolor="#ffd9d9", edgecolor="black", lw=1.4)
    ax.add_patch(qft)
    ax.add_patch(einstein)

    ax.text(0.30, 0.36, "QFT / electroweak", ha="center", fontsize=12, fontweight="bold")
    ax.text(0.30, 0.30, r"spinor-trace class $n = 1$", ha="center", fontsize=10)
    ax.text(0.30, 0.24,
            r"$v_\mathrm{EW},\;m_W,\;m_Z,\;m_H,\;\alpha_\mathrm{dn},\;\theta_{13}$",
            ha="center", fontsize=10)

    ax.text(0.70, 0.36, "Einstein / cosmological", ha="center", fontsize=12, fontweight="bold")
    ax.text(0.70, 0.30, r"$n \in \{0, 1, 2, 4\}$", ha="center", fontsize=10)
    ax.text(0.70, 0.24,
            r"$T_\mathrm{RH}\,(n=4),\;\sigma_8,\,\eta_B\,(n=2),\;\Omega_\mathrm{DM} h^{2}\,(n=1),\;\Lambda_\mathrm{QCD}\,(n=0)$",
            ha="center", fontsize=8.5)

    ax.text(0.50, 0.06,
            "Same five coefficients, same eight lemmata plus pure-sync class\n(nine library entries total), same T-parity source axiom; "
            "the two sectors share the loop-class library and overlap at $n=1$.",
            ha="center", fontsize=9.5, style="italic", color="#444")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title("Common carrier: QFT and Einstein sectors of the same transport law",
                 pad=10)
    save_both(fig, "fig1_common_carrier")
    plt.close(fig)


def figure_2_spinor_trace_tree():
    """Tree of spinor-trace classes."""
    fig, ax = plt.subplots(figsize=(11, 5.5))
    ax.set_axis_off()

    ax.text(0.5, 0.94, r"Spinor-trace component count $n$ separates QFT and Einstein",
            ha="center", fontsize=13, fontweight="bold")
    ax.text(0.5, 0.88,
            "n is read off from the observable's tree-level Dirac structure; the loop class follows by the determinism theorem of Paper 3.",
            ha="center", fontsize=9.5, style="italic", color="#444")

    # Four columns: n=0, n=1, n=2, n=4
    cols = [
        (0.13, "n = 0",
         "Pure-boson compound\n(Pure-Sync x EW-Mixed)",
         "Hadronic scale",
         "Lambda_QCD",
         "#e0e0e0"),
        (0.38, "n = 1",
         "Single spinor current\n(Yukawa, EW-Mixed,\nPMNS, Sub-Generation)",
         "QFT/EW + cosmo overlap",
         "v_EW, m_W, m_Z, m_H\nalpha_dn, theta_13\nalpha_s, V_us, V_cb\nOmega_DM h^2",
         "#cce5ff"),
        (0.63, "n = 2",
         "2-loop compound\n(Yukawa x Generation)",
         "Cosmological\n2-loop",
         "sigma_8, eta_B",
         "#ffd9d9"),
        (0.87, "n = 4",
         "Full spinor-trace\n(resummed propagator)",
         "Long-distance\npropagation",
         "T_RH, omega_b h^2",
         "#fff2cc"),
    ]
    for (xc, n_label, descr, sector, examples, color) in cols:
        rect = plt.Rectangle((xc - 0.11, 0.20), 0.22, 0.55,
                             facecolor=color, edgecolor="black", lw=1.4)
        ax.add_patch(rect)
        ax.text(xc, 0.71, n_label, ha="center", va="center",
                fontsize=13, fontweight="bold")
        ax.text(xc, 0.62, descr, ha="center", va="center", fontsize=9,
                style="italic", color="#444")
        ax.text(xc, 0.50, sector, ha="center", va="center",
                fontsize=10, fontweight="bold", color="#222")
        ax.text(xc, 0.34, examples, ha="center", va="center",
                fontsize=9, family="monospace")

    ax.text(0.5, 0.10,
            "Same loop-class library; sector specialization is purely by $n$.",
            ha="center", fontsize=10, style="italic", color="#444")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    save_both(fig, "fig2_spinor_trace_tree")
    plt.close(fig)


def figure_3_observable_inventory():
    """QFT side vs Einstein side: bar chart of observable counts."""
    with open(REPO / "data" / "qft_sector_mapping.json", "r", encoding="utf-8") as f:
        qft = json.load(f)
    with open(REPO / "data" / "einstein_sector_mapping.json", "r", encoding="utf-8") as f:
        einstein = json.load(f)

    qft_lemmas = {}
    for o in qft["observables"]:
        key = str(o.get("lemma"))
        qft_lemmas[key] = qft_lemmas.get(key, 0) + 1
    einstein_lemmas = {}
    for o in einstein["observables"]:
        key = str(o.get("lemma"))
        einstein_lemmas[key] = einstein_lemmas.get(key, 0) + 1

    all_lemmas = sorted(set(qft_lemmas) | set(einstein_lemmas), key=str)
    qft_counts = [qft_lemmas.get(l, 0) for l in all_lemmas]
    einstein_counts = [einstein_lemmas.get(l, 0) for l in all_lemmas]

    fig, ax = plt.subplots(figsize=(11, 5))
    x = list(range(len(all_lemmas)))
    width = 0.35
    bars1 = ax.bar([xi - width/2 for xi in x], qft_counts, width,
                   color="#4a90d9", edgecolor="black", lw=1, label="QFT sector")
    bars2 = ax.bar([xi + width/2 for xi in x], einstein_counts, width,
                   color="#cc3333", edgecolor="black", lw=1, label="Einstein sector")
    for b, v in zip(bars1, qft_counts):
        if v > 0:
            ax.text(b.get_x() + b.get_width()/2, v + 0.05, str(v),
                    ha="center", va="bottom", fontsize=10)
    for b, v in zip(bars2, einstein_counts):
        if v > 0:
            ax.text(b.get_x() + b.get_width()/2, v + 0.05, str(v),
                    ha="center", va="bottom", fontsize=10)

    ax.set_xticks(x)
    ax.set_xticklabels([f"Lemma {l}" if l != "None" else "tree" for l in all_lemmas],
                       rotation=30, ha="right")
    ax.set_ylabel("number of observables")
    ax.set_title("QFT sector vs Einstein sector inventory by lemma class", pad=10)
    ax.legend(loc="upper right", framealpha=0.95)
    save_both(fig, "fig3_observable_inventory")
    plt.close(fig)


def figure_4_shared_falsification():
    """Shared falsification map: each path lists trigger title + wrapped
    description; both apply to BOTH sectors simultaneously."""
    import textwrap
    with open(REPO / "data" / "bridge_conditionals.json", "r", encoding="utf-8") as f:
        bridge = json.load(f)
    paths = bridge["shared_falsification_paths"]

    label_map = {
        "T-parity-axiom-failure": "T-parity-axiom failure",
        "EMT-04b-FAL": "T-parity-axiom failure",
        "constraint-violation": "Constraint violation",
        "mapping-inconsistency": "Mapping inconsistency",
        "cross-sector-reclassification":
            "Cross-sector reclassification failure",
    }

    # Wrap each test description; track total line count for figure sizing.
    wrap_width = 92
    wrapped = []
    for p in paths:
        title = label_map.get(p["trigger"], p["trigger"])
        lines = textwrap.wrap(p["test"], width=wrap_width)
        wrapped.append((title, lines))

    # Vertical layout: each box has a 1-line title + N wrapped lines + padding.
    # Figure height tracks total content.
    line_h = 0.16  # inch per text line
    title_h = 0.32
    pad = 0.18
    box_heights = [title_h + len(lines) * line_h + 2 * pad
                   for (_, lines) in wrapped]
    fig_h = 0.9 + sum(box_heights)  # plus header
    fig, ax = plt.subplots(figsize=(11, fig_h))
    ax.set_axis_off()

    # Header
    ax.text(0.5, 1 - 0.20 / fig_h,
            "Shared falsification paths",
            ha="center", va="top", fontsize=13, fontweight="bold",
            transform=ax.transAxes)
    ax.text(0.5, 1 - 0.50 / fig_h,
            "Each path falsifies BOTH the QFT sector and the "
            "Einstein sector simultaneously.",
            ha="center", va="top", fontsize=10, style="italic",
            color="#444", transform=ax.transAxes)

    # Boxes
    y_cursor = 1 - 0.90 / fig_h
    for (title, lines), bh in zip(wrapped, box_heights):
        bh_frac = bh / fig_h
        rect = plt.Rectangle(
            (0.05, y_cursor - bh_frac), 0.90, bh_frac,
            facecolor="#ffe6e6", edgecolor="#990000", lw=1.0,
            transform=ax.transAxes,
        )
        ax.add_patch(rect)
        # Title
        ax.text(0.07, y_cursor - (pad + 0.10) / fig_h, title,
                ha="left", va="top", fontsize=11, fontweight="bold",
                color="#990000", transform=ax.transAxes)
        # Wrapped description
        for k, ln in enumerate(lines):
            ax.text(0.07,
                    y_cursor - (pad + title_h + k * line_h) / fig_h,
                    ln, ha="left", va="top", fontsize=9, color="#333",
                    family="serif", transform=ax.transAxes)
        y_cursor -= bh_frac

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    fig.tight_layout()
    save_both(fig, "fig4_shared_falsification")
    plt.close(fig)


def main():
    print("Generating Paper 5 figures into paper/figures/")
    print()
    figure_1_common_carrier()
    figure_2_spinor_trace_tree()
    figure_3_observable_inventory()
    figure_4_shared_falsification()
    print()
    print("All four figures generated.")


if __name__ == "__main__":
    main()
