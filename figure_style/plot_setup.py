"""House style for Of Particular Interest figures (editorial serif register, Substack column width).

Import from a post's figure script:
    from plot_setup import PAL, figure, title_block, save

Charter ships with macOS; on other systems matplotlib falls back to Georgia or DejaVu Serif.
"""
import matplotlib as mpl

mpl.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

FONT = "Charter"
BASE_PT = 10.5
WIDTH_IN = 7.0  # saved at 200 dpi -> 1400 px, 2x Substack's column

PAL = dict(
    accent="#A23B2A",   # the subject of the figure's sentence (6.57:1 on white)
    accent2="#2F5D8A",  # second accent, used rarely
    ink="#262626",      # primary text (15.13:1 on white, WCAG AAA)
    muted="#595959",    # subtitles, notes, source lines (7.00:1 on white, WCAG AAA)
    context="#8C8C8C",  # non-subject bars/series (3.36:1 on white, WCAG 1.4.11 AA >= 3:1)
    faint="#E6E6E6",    # decorative gridlines, table rules
)

mpl.rcParams.update({
    "font.family": "serif",
    "font.serif": [FONT, "Georgia", "DejaVu Serif"],
    "font.size": BASE_PT,
    "text.color": PAL["ink"],
    "axes.labelsize": BASE_PT,
    "axes.labelcolor": PAL["ink"],
    "axes.edgecolor": PAL["ink"],
    "axes.linewidth": 0.6,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": False,
    "grid.color": PAL["faint"],
    "grid.linewidth": 0.6,
    "axes.axisbelow": True,
    "axes.formatter.useoffset": False,
    "xtick.color": PAL["ink"],
    "ytick.color": PAL["ink"],
    "xtick.labelsize": BASE_PT * 0.9,
    "ytick.labelsize": BASE_PT * 0.9,
    "legend.frameon": False,
    "figure.dpi": 100,
    "savefig.dpi": 200,
    "figure.facecolor": "white",
})


def figure(aspect=0.62, nrows=1, ncols=1, **kw):
    return plt.subplots(nrows, ncols, figsize=(WIDTH_IN, WIDTH_IN * aspect), **kw)


def title_block(fig, title, subtitle, source, top=0.97, left=0.035, subtitle_gap=None):
    """Assertive title, measurement subtitle and source line, all on one left edge."""
    gap = subtitle_gap if subtitle_gap is not None else (0.282 / fig.get_figheight())
    fig.text(left, top, title, ha="left", va="top", fontsize=BASE_PT * 1.45, weight="bold")
    fig.text(left, top - gap, subtitle, ha="left", va="top", fontsize=BASE_PT * 0.95, color=PAL["muted"])
    fig.text(left, 0.02, source, ha="left", va="bottom", fontsize=BASE_PT * 0.78, color=PAL["muted"])


def save(fig, path):
    fig.savefig(path, facecolor="white")
    plt.close(fig)
