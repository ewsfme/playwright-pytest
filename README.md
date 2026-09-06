# Playwright + Pytest + Allure

E2E tests for [automationexercise.com](https://www.automationexercise.com)

## Stack

- Python 3.11+
- Playwright
- Pytest
- Allure
- GitHub Actions

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install
Run tests

# all tests
pytest

# specific browser
pytest --browser chromium

# parallel
pytest -n 4

# with Allure results
pytest --alluredir=allure-results
Allure report
allure serve allure-results