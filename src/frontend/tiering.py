import pandas as pd
import numpy as np

# Cumulative boundaries based on requested percentiles
# S = Top 1% (99-100)
# A+ = Next 3% (96-99)
# A = Next 4% (92-96)
# A- = Next 4% (88-92)
# B+ = Next 5% (83-88)
# B = Next 8% (75-83)
# B- = Next 10% (65-75)
# C+ = Next 10% (55-65)
# C = Next 10% (45-55)
# C- = Next 10% (35-45)
# D+ = Next 10% (25-35)
# D = Next 10% (15-25)
# D- = Next 5% (10-15)
# F = Final 10% (0-10)

TIER_CUTOFFS = [
    (99.0, 'S'),
    (96.0, 'A+'),
    (92.0, 'A'),
    (88.0, 'A-'),
    (83.0, 'B+'),
    (75.0, 'B'),
    (65.0, 'B-'),
    (55.0, 'C+'),
    (45.0, 'C'),
    (35.0, 'C-'),
    (25.0, 'D+'),
    (15.0, 'D'),
    (10.0, 'D-'),
    (0.0,  'F')
]

# Map tiers to HSL color background and text color (fg)
# Decreasing saturation and lightness for -, plain, +
TIER_COLORS = {
    'S':  {'bg': 'hsl(280, 100%, 60%)', 'fg': '#ffffff'},
    'A+': {'bg': 'hsl(120, 100%, 45%)', 'fg': '#ffffff'},
    'A':  {'bg': 'hsl(120, 80%, 35%)',  'fg': '#ffffff'},
    'A-': {'bg': 'hsl(120, 60%, 25%)',  'fg': '#ffffff'},
    'B+': {'bg': 'hsl(210, 100%, 55%)', 'fg': '#ffffff'},
    'B':  {'bg': 'hsl(210, 80%, 45%)',  'fg': '#ffffff'},
    'B-': {'bg': 'hsl(210, 60%, 35%)',  'fg': '#ffffff'},
    'C+': {'bg': 'hsl(60, 100%, 45%)',  'fg': '#000000'},
    'C':  {'bg': 'hsl(60, 80%, 35%)',   'fg': '#ffffff'},
    'C-': {'bg': 'hsl(60, 60%, 25%)',   'fg': '#ffffff'},
    'D+': {'bg': 'hsl(30, 100%, 50%)',  'fg': '#000000'},
    'D':  {'bg': 'hsl(30, 80%, 40%)',   'fg': '#ffffff'},
    'D-': {'bg': 'hsl(30, 60%, 30%)',   'fg': '#ffffff'},
    'F':  {'bg': 'hsl(0, 100%, 45%)',   'fg': '#ffffff'},
}

def calculate_tier(percentile: float) -> str:
    """Return the tier letter for a given percentile (0-100)."""
    # handle exact 100.0 edge case
    if percentile >= 99.0:
        return 'S'
        
    for cutoff, tier in TIER_CUTOFFS:
        if percentile >= cutoff:
            return tier
    return 'F'

def render_tier_badge(tier: str, text: str = None) -> str:
    """Generate HTML for a colored badge."""
    if text is None:
        text = tier
    style = TIER_COLORS.get(tier, {'bg': '#555', 'fg': '#fff'})
    return f'<span style="background-color: {style["bg"]}; color: {style["fg"]}; padding: 0.2rem 0.5rem; border-radius: 0.25rem; font-weight: bold; white-space: nowrap;">{text}</span>'

def apply_tiers_to_dataframe(df: pd.DataFrame, score_col: str, pillar_cols: list[str]) -> pd.DataFrame:
    """
    Computes percentiles for the composite score and all pillar columns,
    and assigns a tier string to each.
    """
    result = df.copy()
    
    # Compute percentile ranks (0 to 100)
    # Using 'min' or 'average' method. 'average' is default.
    result[f'{score_col}_pctl'] = result[score_col].rank(pct=True) * 100
    result[f'{score_col}_tier'] = result[f'{score_col}_pctl'].apply(calculate_tier)
    
    for col in pillar_cols:
        if col in result.columns:
            result[f'{col}_pctl'] = result[col].rank(pct=True) * 100
            result[f'{col}_tier'] = result[f'{col}_pctl'].apply(calculate_tier)
            
    return result
