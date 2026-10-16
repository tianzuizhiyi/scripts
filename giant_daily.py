"""Submit the Giant daily request using credentials supplied by the environment."""

import os
import sys

import requests


def main():
    names = ("GIANT_USER_ID", "GIANT_TOKEN", "GIANT_COOKIE")
    missing = [name for name in names if not os.environ.get(name)]
    if missing:
        print("Missing environment variables: " + ", ".join(missing), file=sys.stderr)
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
        print(f"Request failed ({type(exc).__name__}); no automatic retry.", file=sys.stderr)
        return 1

    body = response.text
    for secret in secrets:
        body = body.replace(secret, "[REDACTED]")
    print(f"HTTP {response.status_code}")
    print(body)
    # Business success must be determined from the API response body.
    return 0 if 200 <= response.status_code < 300 else 1


if __name__ == "__main__":
    sys.exit(main())
