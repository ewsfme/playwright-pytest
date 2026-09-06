# AutomationExercise E2E Test Suite (Playwright + Pytest)

## Project description

This repository automates **Test Cases 1–10** published on
[automationexercise.com/test_cases](https://www.automationexercise.com/test_cases)
against the live site [automationexercise.com](https://www.automationexercise.com):

1. Register User
2. Login User with correct email and password
3. Login User with incorrect email and password
4. Logout User
5. Register User with existing email
6. Contact Us Form
7. Verify Test Cases Page
8. Verify All Products and product detail page
9. Search Product
10. Verify Subscription in home page

Key features:

- **Python + Playwright + Pytest**, structured with the **Page Object Model**
  (`pages/`) — locators and page-specific actions live only on their page;
  test files (`tests/`) contain scenarios and assertions only.
- **Allure** reporting: each test step is wrapped with `allure.step`, and a
  screenshot is attached automatically after every step, plus a final
  pass/fail screenshot.
- **Randomized test data** (`utils/data_generator.py`, built on `Faker`) —
  names, emails, addresses, and payment details are generated per run so the
  suite is idempotent against the live site.
- **Cross-browser & parallel execution** via `pytest-playwright` (`--browser`)
  and `pytest-xdist` (`-n`) — no code changes needed to switch browsers or
  concurrency, just CLI flags.
- **CI/CD**: a GitHub Actions workflow runs the suite on chromium, firefox and
  webkit, merges the Allure results, publishes the HTML report to **GitHub
  Pages**, and posts the outcome to **Slack**.

## Project structure

```
pages/        Page Objects (locators + page actions only)
tests/        Test scenarios, conftest.py fixtures
utils/        Random data generator, Slack notifier script
.github/      GitHub Actions pipeline
pytest.ini    Pytest configuration
```

## Requirements

- Python 3.10+
- Google Chrome / Firefox / WebKit dependencies (installed automatically by
  Playwright, see below)
- A Slack **Incoming Webhook URL** if you want to receive run notifications

## Steps to install

```bash
git clone <this-repo-url>
cd automationexercise-tests

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
playwright install --with-deps   # downloads chromium, firefox, webkit
```

## Steps to run tests

Run everything on the default browser (chromium):

```bash
pytest
```

Choose a browser via CLI argument:

```bash
pytest --browser firefox
pytest --browser webkit
```

Run in parallel (4 workers) on a chosen browser:

```bash
pytest --browser chromium -n 4
```

Run a single test case:

```bash
pytest tests/test_test_cases.py::TestAccountManagement::test_case_01_register_user
```

> Only Test Cases 1–10 (see above) are implemented in this version of the
> suite; the remaining scenarios from the source page can be added the same
> way, reusing the existing Page Objects.

Allure result files are written to `allure-results/` on every run (configured
in `pytest.ini`).

## Steps to generate the report

Locally, using the [Allure commandline](https://allurereport.org/docs/install/):

```bash
allure generate allure-results --clean -o allure-report
allure open allure-report
```

In CI, the pipeline (`.github/workflows/tests.yml`) generates the report
automatically after every run and publishes it to GitHub Pages at:

```
https://<github-username>.github.io/<repo-name>/latest/
```

(Each run is additionally archived at `.../<run-number>/`.)

## Slack notifications

After the GitHub Pages deploy step, the pipeline runs
`utils/slack_notifier.py`, which posts one message to a Slack channel via an
Incoming Webhook containing:

- overall run status (✅ PASSED / ❌ FAILED)
- passed/failed/broken/skipped counters (parsed from the Allure summary)
- a link to the published GitHub Pages report
- a link to the GitHub Actions run

### One-time setup

1. In Slack, create an **Incoming Webhook** for the channel that should
   receive notifications (Slack → *Add apps* → *Incoming Webhooks* → *Add to
   Slack* → choose the channel → copy the generated Webhook URL).
2. In the GitHub repo, go to **Settings → Secrets and variables → Actions**
   and add a secret named `SLACK_WEBHOOK_URL` with that URL.
3. Push to `main` (or trigger the workflow manually) — the notification is
   sent automatically at the end of the run.

## CLI/browser & parallelism reference

| Goal                          | Command                                   |
|-------------------------------|--------------------------------------------|
| Single browser, sequential    | `pytest --browser chromium`                |
| Single browser, parallel      | `pytest --browser firefox -n 4`            |
| All three browsers (CI matrix)| handled by the GitHub Actions matrix build |
