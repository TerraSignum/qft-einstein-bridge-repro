# qft-einstein-bridge-repro

**A common loop-topological carrier for electroweak and emergent-gravity sectors.**

[![CI: reproduce](https://github.com/[anonymized]/qft-einstein-bridge-repro/actions/workflows/reproduce.yml/badge.svg)](https://github.com/[anonymized]/qft-einstein-bridge-repro/actions/workflows/reproduce.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

This repository is a short companion (bridge note) to Papers 2-4 of the
Emergence reproducibility-paper series. It documents that the QFT/electroweak
sector (Paper 1, Paper 3) and the cosmological/Einstein sector (Paper 4)
share the same five measured causal-wave coefficients, the same finite
loop-class library, and the same T-parity source axiom; the two sectors
differ only in the spinor-trace component count `n`.

## Result in one line

```
Same five coefficients (alpha_xi, D_Omega, beta_pi, gamma, eps_sync^2).
Same loop-class library (Lemmas 1-8 plus pure-sync).
Same T-parity source axiom (theta_em = pi).
QFT sector lives at spinor-trace class n = 1.
Einstein sector dominant classes are n = 2 and n = 4.
Four shared falsification paths apply to both sectors symmetrically.
```

## Scope

This is **not a new physics paper**. It is a structural mapping between
two emergent sectors that have already been documented in companion
preprints. The point is to make explicit that QFT and GR in the Emergence
framework are not two independent theories that happen to use similar
formulas; they are two regimes of the same five-coefficient transport
law.

## What this is **not**

- Not a derivation of quantum-gravity UV completion
- Not a new numerical claim with its own targets
- Not a closed-form unification statement
- Not a substitute for Papers 1-4

## Installation (Windows PowerShell)

```powershell
git clone https://github.com/[anonymized]/qft-einstein-bridge-repro.git
cd qft-einstein-bridge-repro

py -3.11 -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Reproduce the result

```powershell
python .\src\check_bridge_consistency.py
pytest
```

## Repository structure

```
qft-einstein-bridge-repro/
├── README.md
├── LICENSE
├── CITATION.cff
├── requirements.txt
├── pyproject.toml
├── data/
│   ├── causal_wave_coefficients.json     (mirror of emergence-core-data)
│   ├── loop_class_library.json
│   ├── qft_sector_mapping.json
│   ├── einstein_sector_mapping.json
│   └── bridge_conditionals.json
├── src/
│   ├── check_bridge_consistency.py
│   └── make_figures.py
├── tests/
│   ├── test_same_coefficients.py
│   ├── test_qft_mapping.py
│   ├── test_einstein_mapping.py
│   ├── test_shared_loop_library.py
│   └── test_falsification_paths.py
├── outputs/
│   ├── expected_output.txt
│   └── bridge_consistency_report.json
├── paper/
│   ├── bridge_note.tex
│   ├── bridge_note.pdf
│   └── figures/
└── .github/workflows/
    └── reproduce.yml
```

## Falsification

The bridge fails if any of:

1. The two sectors use different coefficient values.
2. A QFT-side observable cannot be assigned to the loop-class library
   (i.e. its tree-level Dirac structure is not in the n in {0,1,2,4}
   enumeration of the bridge function Phi_bridge).
3. The Einstein side is missing all n in {2, 4} entries entirely
   (so the cross-sector overlap at n in {2,4} cannot be tested).
4. The two sectors draw from different loop-class libraries.
5. The T-parity source axiom does not apply to both sectors.

## Citation

```bibtex
@misc{bucciarelli2026bridge,
  author    = {Bucciarelli, Sandro},
  title     = {A common loop-topological carrier for electroweak and emergent-gravity sectors},
  year      = {2026},
  version   = {0.1.0},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.XXXXXXX}
}
```

## License

MIT License. See [LICENSE](LICENSE).
