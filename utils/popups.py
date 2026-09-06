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

COOKIE_BUTTON_SELECTORS = [
    "#onetrust-accept-btn-handler",
    "#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll",
    "button:has-text('Allow all')",
    "button:has-text('Accept all')",
    "button:has-text('Accept All')",
    "button:has-text('I Agree')",
    "button:has-text('Agree')",
    "button:has-text('Got it')",
    "button:has-text('Accept')",
]


def block_ads(context):
    def _abort(route):
        route.abort()

    for domain in AD_BLOCK_DOMAINS:
        context.route(f"**://*{domain}/**", _abort)


def close_ad_banner(page):
    try:
        close_button = page.locator("#close_fixedban")
        if close_button.count() and close_button.first.is_visible():
            close_button.first.click(timeout=2000)
    except Exception:
        pass


def close_funding_choices_consent(page):
    try:
        consent_frame = page.frame_locator("iframe[src*='fundingchoicesmessages']")
        accept_button = consent_frame.locator("button:has-text('Accept'), button:has-text('AGREE')")
        if accept_button.count():
            accept_button.first.click(timeout=2000)
    except Exception:
        pass


def close_cookie_banner(page):
    for selector in COOKIE_BUTTON_SELECTORS:
        try:
            button = page.locator(selector)
            if button.count() and button.first.is_visible():
                button.first.click(timeout=2000)
                return
        except Exception:
            continue


def dismiss_popups(page):
    close_ad_banner(page)
    close_funding_choices_consent(page)
    close_cookie_banner(page)
