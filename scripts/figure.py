"""Figure 1: share of 2025-26 GMPP projects kept in the April 2026 portfolio, by rating and who gave it.

Usage: python3 -I scripts/figure.py data/gmpp_matched.csv figures/fig1_kept_by_rating.png
"""
import sys
from pathlib import Path

import pandas as pd

_style_dir = Path(__file__).resolve().parents[1] / "figure_style"
if not _style_dir.is_dir():
    _style_dir = Path(__file__).resolve().parents[2] / "figure_style"
sys.path.insert(0, str(_style_dir))
from plot_setup import BASE_PT, PAL, figure, save, title_block  # noqa: E402

ROWS = [
    ("NISTA", "Red"), ("NISTA", "Amber"), ("NISTA", "Green"),
    ("SRO only", "Red"), ("SRO only", "Amber"), ("SRO only", "Green"),
    ("No rating published", None),
]
GROUP_LABEL = {
    "NISTA": "Rated by NISTA",
    "SRO only": "Rated only by the project's own SRO",
    "No rating published": "No rating published",
}


def main(src, out):
    d = pd.read_csv(src)
    rows = []
    for source, rating in ROWS:
        g = d[d["rating_source"] == source]
        if rating:
            g = g[g["rating"] == rating]
        rows.append((source, rating or "Exempt or planning stage", int(g["retained"].sum()), len(g)))

    fig, ax = figure(aspect=0.66)
    fig.subplots_adjust(left=0.30, right=0.97, top=0.76, bottom=0.14)
    y, ticks, labels = 0, [], []
    group_y = {}
    for source, label, kept, n in rows:
        if source not in group_y:
            if group_y:
                y += 0.7
            group_y[source] = y
            y += 0.55
        gap_x = 0.18 if (kept > 0 and n - kept > 0) else 0.0
        if kept > 0:
            ax.barh(y, kept - gap_x / 2, color=PAL["accent"], height=0.62)
        if n - kept > 0:
            ax.barh(y, (n - kept) - gap_x / 2, left=kept + gap_x / 2, color=PAL["context"], height=0.62)
        ax.text(n + 1, y, f"{kept} of {n} kept", va="center", fontsize=BASE_PT * 0.85, color=PAL["ink"])
        ticks.append(y)
        labels.append(label)
        y += 1
    import matplotlib.transforms as mt
    to_fig_left = mt.blended_transform_factory(fig.transFigure, ax.transData)
    for source, gy in group_y.items():
        ax.text(0.035, gy - 0.05, GROUP_LABEL[source], transform=to_fig_left, ha="left",
                va="center", fontsize=BASE_PT * 0.9, weight="bold")
    ax.set_yticks(ticks, labels)
    ax.invert_yaxis()
    ax.set_xlim(0, 80)
    ax.set_xticks([])
    for side in ("left", "bottom"):
        ax.spines[side].set_visible(False)
    ax.tick_params(axis="y", length=0)
    key_y = group_y["NISTA"] - 0.05
    ax.barh(key_y, 2.2, left=50, height=0.4, color=PAL["accent"])
    ax.text(53, key_y, "kept", va="center", fontsize=BASE_PT * 0.85)
    ax.barh(key_y, 2.2, left=60, height=0.4, color=PAL["context"])
    ax.text(63, key_y, "dropped", va="center", fontsize=BASE_PT * 0.85)

    title_block(
        fig,
        "The reset kept NISTA's red projects and dropped the self-rated ones",
        "Projects in the 2025-26 Government Major Projects Portfolio, by delivery confidence rating at\n"
        "31 March 2026, and whether they were in the 81-project portfolio from 1 April 2026",
        "Source: NISTA Major Projects Annual Report 2025-26 data; GMPP data April 2026.\n"
        "189 projects; matched on GMPP ID (plus one missing-ID project by name).",
    )
    fig.texts[0].set_fontsize(BASE_PT * 1.38)
    fig.text(0.035, 0.088, "Bar length is the number of projects in each group.",
             ha="left", va="bottom", fontsize=BASE_PT * 0.8, color=PAL["muted"])
    save(fig, out)


if __name__ == "__main__":
    main(*sys.argv[1:3])
