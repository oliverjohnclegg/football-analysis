---
name: player-role-analysis
description: Build football player analysis profiles for specific tactical roles. Use when the user asks to create a new positional profile, analyse a role, scout players for a position, or add a new profile to the football analysis system.
---

# Player Role Analysis Profile Builder

## Architecture

Each profile is a Python class in `src/profiles/` that extends `PositionalProfile` from `src/profiles/base.py`. The pipeline:

1. `src/fotmob_fetcher.py` fetches per-90 stats from FotMob's JSON API for Big 5 leagues
2. The profile filters by broad position, derives efficiency metrics, computes dimensions
3. `src/charts.py` renders dark-mode visualisations into `output/{slug}/`
4. `main.py` orchestrates via `--profile {slug} [--cached]`

## Available FotMob Stats

All stats are already fetched and cached. Reference them via `df.get("stat_name", 0)`:

| Stat Key | Meaning | Scale |
|----------|---------|-------|
| `accurate_pass` | Accurate passes | per 90 |
| `accurate_long_balls` | Accurate long balls | per 90 |
| `total_att_assist` | Chances created | total |
| `won_contest` | Successful dribbles | per 90 |
| `total_tackle` | Tackles | per 90 |
| `interception` | Interceptions | per 90 |
| `outfielder_block` | Blocks | per 90 |
| `effective_clearance` | Clearances | per 90 |
| `poss_won_att_3rd` | Possession won final 3rd | per 90 |
| `fouls` | Fouls committed | per 90 |
| `expected_assists` | xA | total |
| `expected_assists_per_90` | xA | per 90 |
| `expected_goals_per_90` | xG | per 90 |
| `goals_per_90` | Goals | per 90 |
| `ontarget_scoring_att` | Shots on target | per 90 |
| `total_scoring_att` | Total shots | per 90 |
| `big_chance_created` | Big chances created | total |
| `goal_assist` | Assists | total |

If a new stat is needed, add it to `FOTMOB_STATS` in `src/config.py` and delete `output/raw_all_players.csv` to force re-fetch. Available FotMob stat keys are listed in [reference.md](reference.md).

## Critical Principles

### 1. Stats-Only Derivation

NEVER use `rating` (FotMob's black-box score). NEVER apply team-strength modifiers, league adjustments, or any external context. The composite score must be derived entirely from on-pitch statistical output.

### 2. Efficiency Over Volume

Raw per-90 counts reward players at weaker teams who face more actions. Always prefer **ratio metrics** that measure HOW WELL, not HOW MUCH:

```python
# Base efficiency metrics (computed automatically by PositionalProfile):
clean_defend_rate    = (tackles + interceptions) / (tackles + interceptions + fouls)
interception_share   = interceptions / (tackles + interceptions)
progressive_pass_share = long_balls / passes
carry_to_foul_ratio  = dribbles / fouls

# Profile-specific examples:
chance_quality     = xA / chances_created        # quality of chances, not volume
shot_accuracy      = shots_on_target / shots     # clinical, not wasteful
xg_per_shot        = xG_per_90 / shots_per_90    # shot positioning quality
```

Create new derived ratios in `_derive_efficiency_metrics()`. Use `safe_ratio(num, denom)` from base to handle division by zero.

### 3. Geometric Mean Composite

The composite score uses a **weighted geometric mean**, not a weighted sum. This is handled by `_geometric_composite()` in the base class:

```
composite = Π(dimension_i ^ weight_i)   where Σ(weight_i) = 1
```

A player with dimensions [90, 90, 90, 15] scores ~50 (not ~72). One weak dimension cannot be hidden by strong ones. This naturally filters out one-dimensional players without needing position sub-filtering.

### 4. Dimension Design

Each dimension should blend **volume percentiles** with **efficiency percentiles**. Target 3-5 sub-metrics per dimension, mixing raw output with derived ratios:

```python
df["dimension_name"] = (
    pctl(df["raw_volume_stat"]) * 0.30
    + pctl(df["efficiency_ratio"]) * 0.30
    + pctl(df["another_stat"]) * 0.20
    + pctl(df["inverse_stat"], ascending=False) * 0.20  # lower = better
)
```

Sub-metric weights within a dimension must sum to 1.0. Dimension weights in `dimension_weights` must also sum to 1.0.

### 5. Let Stats Separate Players Naturally

FotMob only provides broad positions: `Midfielder`, `Defender`, `Attacker`, `Keeper`. Do NOT attempt granular sub-position filtering. Instead, design dimensions whose statistical signatures naturally draw the correct players to the top. For example, a #6 profile with a heavy `switch_play` dimension will naturally rank deep-lying distributors above attacking midfielders — no need to filter out AMs explicitly.

Avoid metrics that reward the WRONG archetype. If a #6 shouldn't create goalscoring chances, don't include xA in the #6's tempo dimension (that rewards #10s). Be deliberate about which stats belong to which role.

## Creating a New Profile

### Step 1: Create the profile file

Create `src/profiles/{slug}.py`:

```python
import pandas as pd
from src.profiles.base import PositionalProfile, ScatterChart, pctl, safe_ratio

class MyProfile(PositionalProfile):
    name = "System Name – Role Description"
    slug = "my_slug"
    position_keywords = ["Mid"]  # broad FotMob filter: Mid, Defender, Attack

    dimension_weights = {
        "dimension_a": 0.30,
        "dimension_b": 0.25,
        "dimension_c": 0.25,
        "dimension_d": 0.20,
    }

    radar_labels = ["Dim A", "Dim B", "Dim C", "Dim D"]
    ranking_title = "Top 25 – Role Profile Fit"
    radar_title = "Top 5 Candidates – Dimension Comparison"

    scatter_charts = [
        ScatterChart("dimension_a", "dimension_b", "X Label", "Y Label", "Title", "filename.png"),
    ]

    def _derive_efficiency_metrics(self, df):
        super()._derive_efficiency_metrics(df)
        # Add profile-specific derived ratios here

    def _compute_dimensions(self, df, nineties):
        # Compute each dimension as weighted sum of percentile-ranked metrics
        pass
```

### Step 2: Register the profile

Add to `src/profiles/__init__.py`:

```python
from src.profiles.my_slug import MyProfile
PROFILES["my_slug"] = MyProfile
```

### Step 3: Run

```bash
python main.py --profile my_slug --cached   # use cached data
python main.py --profile my_slug            # fresh fetch (~5 min)
```

Output lands in `output/{slug}/` with `analysis.csv`, `composite_rankings.png`, `radar_comparison.png`, and scatter PNGs.

## Validation Checklist

After running, verify the profile makes sense:

1. Check the top 10 — do recognisable players for that role appear?
2. Check known-good players for the role — where do they rank, and do the dimension breakdowns make sense?
3. Check known-BAD fits — players who play a different role should rank low. If a striker tops your CM profile, a dimension is rewarding the wrong archetype.
4. If a weak-team player ranks suspiciously high, check which dimension is inflated — likely a volume metric that needs an efficiency ratio counterpart.
