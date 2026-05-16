import time

import seleniumbase as sb
import tls_requests


class CloudflareBypass:
    def __init__(self, fbref_instance):
        self._fbref = fbref_instance
        self._cookies = {}
        self._ua = ""

    def patch(self):
        self._extract_cookies()
        bypass = self

        def create_session(headers=None):
            merged = {"User-Agent": bypass._ua}
            if bypass._fbref.__class__.__name__ == "FBref":
                from soccerdata.fbref import FBREF_HEADERS

                merged.update(FBREF_HEADERS)
            if headers:
                merged.update(headers)
            cookie_str = "; ".join(
                f"{k}={v}" for k, v in bypass._cookies.items()
            )
            merged["Cookie"] = cookie_str
            return tls_requests.Client(
                proxy=bypass._fbref.proxy(), headers=merged
            )

        self._fbref._init_session = create_session
        self._fbref._session = create_session()

    def _extract_cookies(self):
        driver = sb.Driver(uc=True, headless=False)
        driver.uc_open_with_reconnect(
            "https://fbref.com/en/comps/", reconnect_time=6
        )
        time.sleep(2)
        if "Just a moment" in driver.title:
            driver.uc_gui_click_captcha()
            time.sleep(5)
        self._cookies = {
            c["name"]: c["value"] for c in driver.get_cookies()
        }
        self._ua = driver.execute_script("return navigator.userAgent")
        driver.quit()

    def cleanup(self):
        pass
