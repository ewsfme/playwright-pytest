"""Posts a test-run summary to Slack via an Incoming Webhook.

Called from the GitHub Actions pipeline after the Allure report has
been generated and deployed to GitHub Pages. It reads the pytest exit
status and the Allure summary counters, then sends one message with:
  - overall status (PASSED / FAILED)
  - pass/fail/skip counters
  - a link to the published GitHub Pages report

Required environment variables:
  SLACK_WEBHOOK_URL   - Slack Incoming Webhook URL (repo secret)
  REPORT_URL          - public GitHub Pages URL of the Allure report
  RUN_STATUS          - "success" or "failure" (from the job's outcome)
  GITHUB_REPOSITORY   - "owner/repo" (provided automatically by CI)
  GITHUB_RUN_ID        - CI run id (provided automatically by CI)

Optional:
  ALLURE_SUMMARY_PATH - path to allure-report/widgets/summary.json
                         (used to include pass/fail counts)
"""
import json
import os
import sys

import requests


def read_allure_summary(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        stats = data.get("statistic", {})
        return {
            "total": stats.get("total", 0),
            "passed": stats.get("passed", 0),
            "failed": stats.get("failed", 0),
            "broken": stats.get("broken", 0),
            "skipped": stats.get("skipped", 0),
        }
    except (FileNotFoundError, json.JSONDecodeError):
        return {"total": "n/a", "passed": "n/a", "failed": "n/a", "broken": "n/a", "skipped": "n/a"}


def build_message(status: str, stats: dict, report_url: str, repo: str, run_id: str) -> dict:
    emoji = "✅" if status.lower() == "success" else "❌"
    status_word = "PASSED" if status.lower() == "success" else "FAILED"
    run_url = f"https://github.com/{repo}/actions/runs/{run_id}"

    text = (
        f"{emoji} *AutomationExercise test run: {status_word}*\n"
        f"Total: {stats['total']} | Passed: {stats['passed']} | "
        f"Failed: {stats['failed']} | Broken: {stats['broken']} | Skipped: {stats['skipped']}\n"
        f"<{report_url}|View Allure report on GitHub Pages>\n"
        f"<{run_url}|View CI run>"
    )
    return {"text": text}


def main() -> int:
    webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
    report_url = os.environ.get("REPORT_URL", "")
    run_status = os.environ.get("RUN_STATUS", "failure")
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    run_id = os.environ.get("GITHUB_RUN_ID", "")
    summary_path = os.environ.get("ALLURE_SUMMARY_PATH", "allure-report/widgets/summary.json")

    if not webhook_url:
        print("SLACK_WEBHOOK_URL is not set, skipping Slack notification.")
        return 0

    stats = read_allure_summary(summary_path)
    payload = build_message(run_status, stats, report_url, repo, run_id)

    response = requests.post(webhook_url, data=json.dumps(payload),
                              headers={"Content-Type": "application/json"}, timeout=15)
    if response.status_code != 200:
        print(f"Slack notification failed: {response.status_code} {response.text}")
        return 1

    print("Slack notification sent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
