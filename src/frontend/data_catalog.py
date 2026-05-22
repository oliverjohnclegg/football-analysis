import os
from pathlib import Path
import pandas as pd

from src.config import OUTPUT_DIR
from src.nationality_service import NationalityService
from src.profiles import PROFILES

def get_managers() -> list[str]:
    """Return a list of manager names found in the output directory."""
    if not OUTPUT_DIR.exists():
        return []
    managers = [d.name for d in OUTPUT_DIR.iterdir() if d.is_dir()]
    return sorted(managers)

def get_roles(manager: str) -> list[str]:
    """Return a list of roles for a given manager."""
    manager_dir = OUTPUT_DIR / manager
    if not manager_dir.exists():
        return []
    roles = [d.name for d in manager_dir.iterdir() if d.is_dir() and (d / "analysis.csv").exists()]
    return sorted(roles)

def load_role_data(manager: str, role: str) -> tuple[pd.DataFrame, list[str]]:
    """
    Load the analysis.csv for a given manager and role.
    Returns the dataframe and a list of the role's pillar columns.
    """
    csv_path = OUTPUT_DIR / manager / role / "analysis.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"No analysis.csv found for {manager}/{role}")
    
    df = pd.read_csv(csv_path)
    
    # Try to resolve pillar columns from profile definition
    slug = f"{manager}/{role}"
    profile_cls = PROFILES.get(slug)
    
    if profile_cls and hasattr(profile_cls, 'dimension_weights'):
        pillar_columns = list(profile_cls.dimension_weights.keys())
        # Verify the columns actually exist in the dataframe
        pillar_columns = [col for col in pillar_columns if col in df.columns]
    else:
        # Fallback: guess pillar columns based on standard structure
        # In base.py, the columns typically go: ... -> base_efficiency_metrics -> pillar_metrics -> composite_score
        # For simplicity, if we don't have the profile, we'll try to guess based on 'carry_to_foul_ratio' and 'composite_score'
        cols = list(df.columns)
        try:
            start_idx = cols.index("carry_to_foul_ratio") + 1
            end_idx = cols.index("composite_score")
            pillar_columns = cols[start_idx:end_idx]
        except ValueError:
            pillar_columns = []
            
    return df, pillar_columns
