"""House style for Of Particular Interest figures (editorial serif register, Substack column width).

Import from a post's figure script:
    from plot_setup import PAL, figure, title_block, save

Charter ships with macOS; on other systems matplotlib falls back to Georgia or DejaVu Serif.
"""
import matplotlib as mpl

mpl.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

FONT = "Charter"
BASE_PT = 10.5
WIDTH_IN = 7.0  # saved at 200 dpi -> 1400 px, 2x Substack's column
SAVE_DPI = 200
CORNER_RADIUS_PX = 28  # 14 CSS px at 700 px column width; transparent outside corners

PAL = dict(
    paper="#F6F2EC",    # matches ceross.substack.com --web_bg_color; soft card in dark mode
    accent="#A23B2A",   # the subject of the figure's sentence (5.89:1 on #F6F2EC)
    accent2="#2F5D8A",  # second accent, used rarely
    ink="#262626",      # primary text (13.57:1 on #F6F2EC, WCAG AAA)
    muted="#595959",    # subtitles, notes, source lines (6.28:1 on #F6F2EC, WCAG AA)
    context="#82807C",  # non-subject bars/series (3.53:1 on #F6F2EC, WCAG 1.4.11 AA >= 3:1)
    faint="#E0DCD5",    # decorative gridlines, table rules on warm paper
)

_TRANSPARENT_PAPER = (246 / 255, 242 / 255, 236 / 255, 0.0)

mpl.rcParams.update({
    "font.family": "serif",
    "font.serif": [FONT, "Georgia", "DejaVu Serif"],
    "font.size": BASE_PT,
    "text.color": PAL["ink"],
    "axes.facecolor": "none",
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
    "savefig.dpi": SAVE_DPI,
    "figure.facecolor": _TRANSPARENT_PAPER,
})


def figure(aspect=0.62, nrows=1, ncols=1, **kw):
    fig, axes = plt.subplots(nrows, ncols, figsize=(WIDTH_IN, WIDTH_IN * aspect), **kw)
    fig.patch.set_facecolor(_TRANSPARENT_PAPER)
    return fig, axes


def title_block(fig, title, subtitle, source, top=0.965, left=0.035, subtitle_gap=None):
    """Assertive title, measurement subtitle and source line, all on one left edge."""
    gap = subtitle_gap if subtitle_gap is not None else (0.282 / fig.get_figheight())
    fig.text(left, top, title, ha="left", va="top", fontsize=BASE_PT * 1.45, weight="bold")
    fig.text(left, top - gap, subtitle, ha="left", va="top", fontsize=BASE_PT * 0.95, color=PAL["muted"])
    fig.text(left, 0.026, source, ha="left", va="bottom", fontsize=BASE_PT * 0.78, color=PAL["muted"])


def save(fig, path, radius_px=CORNER_RADIUS_PX):
    w_in, h_in = fig.get_size_inches()
    card = FancyBboxPatch(
        (0, 0),
        w_in,
        h_in,
        boxstyle=f"round,pad=0,rounding_size={radius_px / SAVE_DPI}",
        facecolor=PAL["paper"],
        edgecolor="none",
        transform=fig.dpi_scale_trans,
        zorder=-1000,
        clip_on=False,
    )
    fig.patches.append(card)
    fig.savefig(path, dpi=SAVE_DPI, facecolor=_TRANSPARENT_PAPER, edgecolor="none")
    plt.close(fig)
