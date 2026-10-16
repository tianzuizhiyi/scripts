"""Submit the Giant daily request using credentials supplied by the environment."""

import os
import sys

import requests


def report_error(message):
    print(message, file=sys.stderr)
    if os.environ.get("GITHUB_ACTIONS") == "true":
        # Escape workflow-command control characters; never include credentials.
        escaped = message.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
        print(f"::error title=Giant daily request::{escaped}")


def main():
    names = ("GIANT_USER_ID", "GIANT_TOKEN", "GIANT_COOKIE")
    missing = [name for name in names if not os.environ.get(name)]
    if missing:
        report_error(
            "Missing environment variables: " + ", ".join(missing)
            + ". Add repository Actions Secrets GIANT_TOKEN and GIANT_COOKIE "
            "in Settings > Secrets and variables > Actions."
        )
        return 1

    secrets = (os.environ["GIANT_TOKEN"], os.environ["GIANT_COOKIE"])
    try:
        # Do not retry automatically: this POST may already have taken effect.
        response = requests.post(
            "https://opo.giant.com.cn/opo/index.php/day_pic/do_app_pic",
            data={"user_id": os.environ["GIANT_USER_ID"], "type": "1"},
            headers={
                "User-Agent": "Reqable/2.11.1",
                "token": secrets[0],
                "Cookie": secrets[1],
            },
            timeout=(15, 45),
            allow_redirects=False,
        )
    except requests.RequestException as exc:
        report_error(f"Request failed ({type(exc).__name__}); no automatic retry.")
        return 1

    body = response.text
    for secret in secrets:
        body = body.replace(secret, "[REDACTED]")
    print(f"HTTP {response.status_code}")
    print(body)
    # Business success must be determined from the API response body.
    if not 200 <= response.status_code < 300:
        report_error(f"Endpoint returned HTTP {response.status_code}; see the response in the step log.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
