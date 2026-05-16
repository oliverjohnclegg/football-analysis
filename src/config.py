from pathlib import Path

SEASON_WEIGHTS = {
    "2025/2026": 1.0,
    "2024/2025": 0.5,
}
PRIMARY_SEASON = "2025/2026"
SEASONS = list(SEASON_WEIGHTS.keys())
MINIMUM_MINUTES = 900
MINIMUM_MINUTES_COMBINED = 1800
OUTPUT_DIR = Path("output")

FOTMOB_LEAGUES = {
    "ENG-Premier League": 47,
    "ESP-La Liga": 87,
    "GER-Bundesliga": 54,
    "ITA-Serie A": 55,
    "FRA-Ligue 1": 53,
}

FOTMOB_STATS = [
    "rating",
    "accurate_pass",
    "accurate_long_balls",
    "total_att_assist",
    "won_contest",
    "total_tackle",
    "interception",
    "outfielder_block",
    "effective_clearance",
    "poss_won_att_3rd",
    "fouls",
    "expected_assists",
    "expected_assists_per_90",
    "expected_goals_per_90",
    "goals_per_90",
    "ontarget_scoring_att",
    "total_scoring_att",
    "big_chance_created",
    "goal_assist",
    "saves",
    "clean_sheet",
]
