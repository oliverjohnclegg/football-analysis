# Reference: Player Role Analysis

## Full FotMob Stat Catalogue

These are known stat keys available on `data.fotmob.com/stats/{league_id}/season/{tournament_id}/{stat_key}.json`. To add a stat, append its key to `FOTMOB_STATS` in `src/config.py` and delete the cache.

### Passing
- `accurate_pass` – accurate passes per 90
- `accurate_long_balls` – accurate long balls per 90
- `total_att_assist` – total chances created
- `big_chance_created` – big chances created
- `goal_assist` – assists
- `expected_assists` – expected assists (total)
- `expected_assists_per_90` – expected assists per 90

### Shooting
- `goals_per_90` – goals per 90
- `expected_goals_per_90` – expected goals per 90
- `total_scoring_att` – total shots per 90
- `ontarget_scoring_att` – shots on target per 90

### Defending
- `total_tackle` – tackles per 90
- `interception` – interceptions per 90
- `outfielder_block` – blocks per 90
- `effective_clearance` – clearances per 90
- `fouls` – fouls committed per 90

### Possession
- `won_contest` – successful dribbles per 90
- `poss_won_att_3rd` – possession won in attacking 3rd per 90

### Other
- `rating` – FotMob rating (DO NOT USE in composites)
- `minutes_played` – total minutes (auto-fetched, not in FOTMOB_STATS)
- `matches_played` – total matches (auto-fetched)

### Potentially Useful (not yet fetched)
These may be available on FotMob. Test by adding to `FOTMOB_STATS`:
- `aerial_won` – aerial duels won
- `duel_won` – total duels won
- `touches` – total touches
- `dispossessed` – times dispossessed
- `possession_lost_ctrl` – possession lost
- `accurate_cross` – accurate crosses
- `total_offside` – offsides
- `saves` – GK saves

## Mathematical Foundations

### Percentile Ranking

`pctl(series)` computes rank-based percentile (0–100). This normalises all stats to the same scale regardless of units, making them combinable. A player at the 85th percentile is better than 85% of the pool in that metric.

For stats where LOWER is better (e.g., fouls, dispossessions), pass `ascending=False`:
```python
pctl(df["fouls"], ascending=False)  # fewer fouls = higher percentile
```

### safe_ratio

Robust division: replaces 0 denominators with NaN, then fills NaN with a default (0.0). Use for all derived efficiency metrics.

### Weighted Geometric Mean

```
score = exp(Σ wᵢ · ln(dimᵢ))
```

Where `wᵢ` are dimension weights summing to 1.0 and `dimᵢ` are dimension scores (clamped to ≥ 1.0 to avoid log(0)).

Properties:
- A single weak dimension *destroys* the composite (unlike arithmetic mean)
- Rewards balanced excellence across ALL dimensions
- Naturally produces a ranking where only well-rounded players for the role surface

The base class clamps dimension scores at 1.0 before log. This means a player scoring 0 in any percentile stat gets a floor of 1.0, which after log still heavily penalises them.

### Advanced Derived Metrics

When designing efficiency metrics, consider these patterns:

**Rate metrics** – success / attempts:
```python
pass_completion = safe_ratio(accurate_pass, total_pass)
tackle_success  = safe_ratio(won_tackles, total_tackles)
```

**Share metrics** – proportion of one action type:
```python
interception_share = safe_ratio(interceptions, tackles + interceptions)
```

**Intensity metrics** – actions per unit of play:
```python
pressing_intensity = safe_ratio(poss_won_att_3rd, matches_played)
```

**Balance metrics** – harmony between two outputs (harmonic mean):
```python
# Rewards players who contribute both goals AND assists, not just one
goal_involvement_balance = safe_ratio(
    xa90.clip(0.001) * xg90.clip(0.001),
    (xa90 + xg90).clip(0.001),
)
```

**Inverse metrics** – penalise negatives:
```python
pctl(df["fouls"], ascending=False)          # fewer fouls = better
pctl(df["dispossessed"], ascending=False)   # fewer dispossessions = better
```

## File Map

```
src/
├── config.py              # Leagues, seasons, min minutes, stat keys
├── fotmob_fetcher.py      # Data fetch + cache layer
├── charts.py              # Dark-mode matplotlib visualisations
├── profiles/
│   ├── __init__.py        # PROFILES registry dict
│   ├── base.py            # PositionalProfile ABC, pctl, safe_ratio, ScatterChart
│   ├── number_six.py      # Example: deep-lying playmaker
│   ├── number_eight.py    # Example: box-to-box midfielder
│   ├── wide_cb.py         # Example: ball-playing centre-back
│   └── right_am.py        # Example: half-space attacking midfielder
main.py                    # CLI entry point (--profile, --cached)
output/
├── raw_all_players.csv    # Cached raw FotMob data
└── {slug}/
    ├── analysis.csv
    ├── composite_rankings.png
    ├── radar_comparison.png
    └── *.png scatter charts
```
