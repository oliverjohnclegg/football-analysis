from __future__ import annotations

from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import numpy as np

from src.config import OUTPUT_DIR

if TYPE_CHECKING:
    import pandas as pd
    from src.profiles.base import PositionalProfile

BG, GRID, TEXT = "#0d1117", "#21262d", "#e6edf3"
ACCENT = ["#00f0ff", "#ff6b6b", "#ffd93d", "#6bff6b", "#c084fc"]


def _apply_style():
    plt.rcParams.update({
        "figure.facecolor": BG, "axes.facecolor": BG, "axes.edgecolor": GRID,
        "axes.labelcolor": TEXT, "text.color": TEXT, "xtick.color": TEXT,
        "ytick.color": TEXT, "grid.color": GRID, "font.family": "sans-serif",
        "font.size": 10,
    })


def _save(fig, out_dir, name):
    fig.savefig(out_dir / name, dpi=200, bbox_inches="tight")
    plt.close(fig)


def render_all(df: pd.DataFrame, profile: PositionalProfile):
    _apply_style()
    out_dir = OUTPUT_DIR / profile.slug
    out_dir.mkdir(parents=True, exist_ok=True)

    _composite_rankings(df, profile, out_dir)
    _radar_comparison(df, profile, out_dir)
    for sc in profile.scatter_charts:
        _scatter(df, sc.x_col, sc.y_col, sc.xlabel, sc.ylabel, sc.title, sc.filename, out_dir)
    print(f"  Charts saved to {out_dir}/")


def _composite_rankings(df, profile, out_dir, n=25):
    top = df.head(n)
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.barh(
        range(len(top)), top["composite_score"],
        color=ACCENT[0], alpha=0.85, edgecolor=ACCENT[0], linewidth=0.5,
    )
    ax.set_yticks(range(len(top)))
    ax.set_yticklabels(
        [f"{r['player']} ({r['team']})" for _, r in top.iterrows()],
        fontsize=9,
    )
    ax.invert_yaxis()
    ax.set_xlabel("Composite Profile Score")
    ax.set_title(profile.ranking_title, fontsize=14, fontweight="bold", pad=15)
    ax.grid(axis="x", alpha=0.3)
    plt.tight_layout()
    _save(fig, out_dir, "composite_rankings.png")


def _radar_comparison(df, profile, out_dir, n=5):
    top = df.head(n)
    dims = list(profile.dimension_weights.keys())
    angles = np.linspace(0, 2 * np.pi, len(dims), endpoint=False).tolist()
    angles += angles[:1]
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={"polar": True})
    ax.set_facecolor(BG)
    for i, (_, row) in enumerate(top.iterrows()):
        vals = [row[d] for d in dims] + [row[dims[0]]]
        ax.plot(angles, vals, color=ACCENT[i], linewidth=2, label=row["player"])
        ax.fill(angles, vals, color=ACCENT[i], alpha=0.08)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(profile.radar_labels, fontsize=10)
    ax.set_ylim(0, 100)
    ax.legend(loc="upper right", bbox_to_anchor=(1.35, 1.1), fontsize=9)
    ax.set_title(profile.radar_title, fontsize=13, fontweight="bold", pad=25)
    ax.tick_params(colors=TEXT)
    plt.tight_layout()
    _save(fig, out_dir, "radar_comparison.png")


def _annotate_top(ax, df, x_col, y_col, n=10):
    for _, row in df.head(n).iterrows():
        ax.annotate(
            row["player"], (row[x_col], row[y_col]),
            fontsize=7, alpha=0.9, xytext=(5, 5), textcoords="offset points",
        )


def _scatter(df, x_col, y_col, xlabel, ylabel, title, filename, out_dir):
    available = [c for c in [x_col, y_col, "composite_score", "player"] if c in df.columns]
    if len(available) < 4:
        return
    clean = df[available].dropna()
    fig, ax = plt.subplots(figsize=(12, 8))
    sc = ax.scatter(
        clean[x_col], clean[y_col], c=clean["composite_score"],
        cmap="cool", s=40, alpha=0.7, edgecolors="white", linewidth=0.3,
    )
    _annotate_top(ax, clean, x_col, y_col)
    plt.colorbar(sc, label="Composite Score")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title, fontsize=13, fontweight="bold", pad=15)
    ax.grid(alpha=0.2)
    plt.tight_layout()
    _save(fig, out_dir, filename)
