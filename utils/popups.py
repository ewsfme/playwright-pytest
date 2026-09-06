"""Helpers to keep Google Ads / cookie-consent popups from breaking tests.

automationexercise.com serves Google Ads (a fixed banner at the top of
the page, id="close_fixedban") and, depending on browser/locale, a
cookie-consent dialog from one of several common providers (Google
Funding Choices, OneTrust, Cookiebot, or a generic in-house banner).
Different browsers can trigger different consent flows (Firefox's
default locale/headers differ from Chromium's), so this file checks
every known variant rather than a single one.

The primary fix is blocking the ad/consent network calls entirely so
the popups never render (`block_ads`). `dismiss_popups` is a defensive
fallback in case something still slips through.
"""
AD_BLOCK_DOMAINS = [
    "doubleclick.net",
    "googlesyndication.com",
    "googleadservices.com",
    "adservice.google.com",
    "pagead2.googlesyndication.com",
    "fundingchoicesmessages.google.com",
    "google-analytics.com",
    "googletagmanager.com",
    "googletagservices.com",
]

# Buttons used by the most common cookie-consent providers/wordings.
COOKIE_BUTTON_SELECTORS = [
    "#onetrust-accept-btn-handler",  # OneTrust
    "#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll",  # Cookiebot
    "button:has-text('Allow all')",
    "button:has-text('Accept all')",
    "button:has-text('Accept All')",
    "button:has-text('I Agree')",
    "button:has-text('Agree')",
    "button:has-text('Got it')",
    "button:has-text('Accept')",
]


def block_ads(context):
    """Abort every network request going to a known ad/consent domain."""
    def _abort(route):
        route.abort()

    for domain in AD_BLOCK_DOMAINS:
        context.route(f"**://*{domain}/**", _abort)


def close_ad_banner(page):
    """Closes the fixed Google Ads banner at the top of the page, if present."""
    try:
        close_button = page.locator("#close_fixedban")
        if close_button.count() and close_button.first.is_visible():
            close_button.first.click(timeout=2000)
    except Exception:
        pass


def close_funding_choices_consent(page):
    """Closes Google's Funding Choices consent dialog (rendered in an iframe)."""
    try:
        consent_frame = page.frame_locator("iframe[src*='fundingchoicesmessages']")
        accept_button = consent_frame.locator("button:has-text('Accept'), button:has-text('AGREE')")
        if accept_button.count():
            accept_button.first.click(timeout=2000)
    except Exception:
        pass


def close_cookie_banner(page):
    """Closes whichever common cookie-consent banner rendered, if any.
    Different browsers/locales can trigger different providers, so every
    known selector is tried; the first one found and visible is clicked.
    """
    for selector in COOKIE_BUTTON_SELECTORS:
        try:
            button = page.locator(selector)
            if button.count() and button.first.is_visible():
                button.first.click(timeout=2000)
                return
        except Exception:
            continue


def dismiss_popups(page):
    """Runs every known popup-closing check. Never raises."""
    close_ad_banner(page)
    close_funding_choices_consent(page)
    close_cookie_banner(page)
