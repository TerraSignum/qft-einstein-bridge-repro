"""Version-lock matrix generator for the bridge-note paper.

Computes SHA-256 content hash of each companion-paper manuscript
file and emits a LaTeX table version-locking the whole P1-P5
collection at the moment the bridge note compiles.
"""
import hashlib
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EMG = REPO.parent
OUT = REPO / "paper" / "tables" / "tab_version_lock_matrix.tex"
OUT.parent.mkdir(parents=True, exist_ok=True)

CLAIM_LEVELS = {
    "P1":   ("conditional EW closure", "$S_{\\rm bounce}$, T-parity, MS-bar"),
    "P2":   ("$\\mathcal R$-coefficient backbone (hypothesis)",
             "P3 library, P4 metric, T-parity"),
    "P3":   ("loop-class library + topology-tuple protocol",
             "$\\mathcal R$ from P2"),
    "P4":   ("bulk-percentile Einstein-class closure",
             "$\\Lambda^{\\rm back}$, P2 $\\mathcal R$"),
    "P4-A": ("linearised Schwarzschild + PPN", "P4 closure"),
    "P4-B": ("source decomposition + halo audit",
             "P4 closure, P3 strict-EXACT $D_\\Omega$"),
    "P4-C": ("indirect-witness chain", "P4 closure"),
    "P4-D": ("Atiyah--Singer bridge (proposed)",
             "P4-C chirality witness"),
    "P5":   ("technical consistency note",
             "P1, P2, P3, P4 versions hashed below"),
}

REPOS = [
    ("P1",   "hbr-ew-scale-repro",                          "manuscript.tex"),
    ("P2",   "causal-wave-landings-repro",                  "manuscript.tex"),
    ("P3",   "loop-class-closure-repro",                    "manuscript.tex"),
    ("P4",   "emergent-gr-closure-repro",                   "manuscript.tex"),
    ("P4-A", "emergent-gr-schwarzschild-ppn-repro",         "manuscript.tex"),
    ("P4-B", "emergent-gr-anisotropic-source-dm-de-repro",  "manuscript.tex"),
    ("P4-C", "emergent-gr-h3c-witnesses-repro",             "manuscript.tex"),
    ("P4-D", "emergent-gr-atiyah-singer-chirality-repro",   "manuscript.tex"),
    ("P5",   "qft-einstein-bridge-repro",                   "bridge_note.tex"),
]

lines = []
A = lines.append
A(r"\begin{tabular}{l p{0.30\textwidth} l p{0.20\textwidth}"
  r" p{0.20\textwidth}}")
A(r"\toprule")
A(r"Paper & Repo & SHA-256 (12 hex) & Accepted claim level &"
  r" Depends on \\")
A(r"\midrule")
for label, repo, name in REPOS:
    p = EMG / repo / "paper" / name
    if not p.exists():
        A(f"{label} & {repo} & --- & --- & --- \\\\")
        continue
    h = hashlib.sha256(p.read_bytes()).hexdigest()[:12]
    repo_short = repo.replace("emergent-gr-", "egr-")
    repo_short = repo_short.replace("-repro", "")
    repo_short = repo_short.replace("_", r"\_")
    claim, deps = CLAIM_LEVELS.get(label, ("", ""))
    A(f"{label} & \\texttt{{{repo_short}}} & "
      f"\\texttt{{{h}}} & {claim} & {deps} \\\\")
A(r"\bottomrule")
A(r"\end{tabular}")
OUT.write_text("\n".join(lines), encoding="utf-8")
print(f"Wrote {OUT}")
