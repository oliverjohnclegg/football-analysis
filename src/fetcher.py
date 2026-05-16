import pandas as pd
import soccerdata as sd
import soccerdata.fbref as fbref_module
from lxml import etree, html

from src.config import LEAGUES, SEASONS, STAT_TYPES
from src.selenium_bypass import CloudflareBypass


def _patched_parse_table(html_table):
    for elem in list(html_table.xpath(".//span[contains(@class, 'f-i')]")):
        parent = elem.getparent()
        if parent is not None:
            etree.strip_elements(parent, "span", with_tail=False)
    for elem in list(html_table.xpath(".//tbody/tr[contains(@class, 'spacer')]")):
        if elem.getparent() is not None:
            elem.getparent().remove(elem)
    for elem in list(html_table.xpath(".//tbody/tr[contains(@class, 'thead')]")):
        if elem.getparent() is not None:
            elem.getparent().remove(elem)

    table_html = html.tostring(html_table)
    dfs = pd.read_html(table_html, flavor="lxml")
    if len(dfs) == 1:
        return dfs[0].convert_dtypes()
    return max(dfs, key=len).convert_dtypes()


fbref_module._parse_table = _patched_parse_table


class FBrefFetcher:
    def __init__(self):
        self._fbref = sd.FBref(leagues=LEAGUES, seasons=SEASONS)
        self._bypass = CloudflareBypass(self._fbref)
        self._bypass.patch()

    def fetch_all_player_stats(self) -> dict[str, pd.DataFrame]:
        results = {}
        for stat_type in STAT_TYPES:
            print(f"  -> {stat_type}...")
            results[stat_type] = self._fbref.read_player_season_stats(
                stat_type=stat_type
            )
        self._bypass.cleanup()
        return results
