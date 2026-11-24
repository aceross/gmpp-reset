# The red projects stayed (updated 24 November 2026)

Companion code and data for *"The red projects stayed"* ([Of Particular Interest](https://ceross.substack.com)): which 2025-26 Government Major Projects Portfolio projects stayed in the April 2026 portfolio, by rating, rating source, category and cost.

- Draft: `draft_20261031.md` (live GOV.UK/IfG checks updated 24 November 2026) · Figure: `figures/fig1_kept_by_rating.png`
- Data: `data/gmpp_matched.csv` (189 projects with `retained` flag); console output in `data/analysis_output.txt`
- Raw: `data/raw/gmpp_2025_26.csv` (NISTA annual report data), `data/raw/gmpp_apr_2026.ods` (April 2026 list)
- Closure log: `CLOSURE_LOG.md`

## Dependencies

Install packages from `requirements.txt` (`matplotlib>=3.11.2` is required on macOS for proper `Avenir Next` Regular and DemiBold weights). `scripts/figure.py` also imports the house style module in `figure_style/plot_setup.py`.

## Reproduce

Using `uv` (Python 3.12 with `odfpy` and `matplotlib>=3.11.2`):

```
uv run --offline --python 3.12 --with pandas --with matplotlib --with openpyxl --with odfpy python -I scripts/analyse.py data/raw/gmpp_2025_26.csv data/raw/gmpp_apr_2026.ods data > data/analysis_output.txt
uv run --offline --python 3.12 --with pandas --with matplotlib --with openpyxl --with odfpy python -I scripts/figure.py data/gmpp_matched.csv figures/fig1_kept_by_rating.png
```

Or in an activated Python 3 environment with `requirements.txt` installed:

```
python3 -I scripts/analyse.py data/raw/gmpp_2025_26.csv data/raw/gmpp_apr_2026.ods data > data/analysis_output.txt
python3 -I scripts/figure.py data/gmpp_matched.csv figures/fig1_kept_by_rating.png
```

## Licence and attribution

The raw source files in `data/raw/` (`gmpp_2025_26.csv` from the [NISTA Major Projects Annual Report 2025-26](https://www.gov.uk/government/publications/nista-major-projects-annual-report-2025-26) and `gmpp_apr_2026.ods` from [Government Major Projects Portfolio data April 2026](https://www.gov.uk/government/publications/government-major-projects-portfolio)) contain public sector information licensed under the [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/) (© Crown copyright).
