#!/usr/bin/env python3
"""Script to validate links in the README.md file.

This script checks all URLs found in the README.md to ensure they are
accessible and returns valid HTTP status codes. It reports broken or
unreachable links for maintainers to review.
"""

import re
import sys
import time
import argparse
from typing import Optional

import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


DEFAULT_README_PATH = "README.md"
DEFAULT_TIMEOUT = 10  # seconds
DEFAULT_DELAY = 0.5   # seconds between requests to avoid rate limiting
URL_PATTERN = re.compile(r'https?://[^\s\)\]\>"]+', re.IGNORECASE)

# HTTP status codes considered as valid/acceptable
VALID_STATUS_CODES = {200, 201, 204, 301, 302, 307, 308}

# Domains known to block automated requests
SKIP_DOMAINS = {
    "twitter.com",
    "x.com",
    "facebook.com",
    "linkedin.com",
}


def extract_urls(filepath: str) -> list[str]:
    """Extract all URLs from the given markdown file."""
    urls = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        urls = URL_PATTERN.findall(content)
        # Remove trailing punctuation that may have been captured
        urls = [url.rstrip(".,;:!?") for url in urls]
        # Deduplicate while preserving order
        seen = set()
        unique_urls = []
        for url in urls:
            if url not in seen:
                seen.add(url)
                unique_urls.append(url)
        return unique_urls
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.", file=sys.stderr)
        sys.exit(1)


def should_skip(url: str) -> bool:
    """Check if a URL should be skipped based on its domain."""
    for domain in SKIP_DOMAINS:
        if domain in url:
            return True
    return False


def check_url(url: str, timeout: int = DEFAULT_TIMEOUT) -> tuple[bool, Optional[int], str]:
    """Check if a URL is accessible.

    Returns:
        A tuple of (is_valid, status_code, message)
    """
    if should_skip(url):
        return True, None, "Skipped (known bot-blocking domain)"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (compatible; public-apis-link-validator/1.0; "
            "+https://github.com/public-apis/public-apis)"
        )
    }

    try:
        response = requests.head(
            url, timeout=timeout, headers=headers, allow_redirects=True
        )
        # Some servers don't support HEAD, fall back to GET
        if response.status_code in {405, 403}:
            response = requests.get(
                url, timeout=timeout, headers=headers, allow_redirects=True, stream=True
            )

        if response.status_code in VALID_STATUS_CODES:
            return True, response.status_code, "OK"
        else:
            return False, response.status_code, f"HTTP {response.status_code}"

    except Timeout:
        return False, None, "Timeout"
    except ConnectionError:
        return False, None, "Connection error"
    except TooManyRedirects:
        return False, None, "Too many redirects"
    except Exception as e:
        return False, None, f"Error: {str(e)}"


def validate_links(
    filepath: str = DEFAULT_README_PATH,
    timeout: int = DEFAULT_TIMEOUT,
    delay: float = DEFAULT_DELAY,
) -> int:
    """Validate all links in the given file.

    Returns:
        Number of broken links found.
    """
    urls = extract_urls(filepath)
    print(f"Found {len(urls)} unique URLs in '{filepath}'.\n")

    broken = []

    for i, url in enumerate(urls, start=1):
        is_valid, status_code, message = check_url(url, timeout=timeout)
        status_label = f"[{status_code}]" if status_code else ""
        symbol = "✓" if is_valid else "✗"
        print(f"  {symbol} ({i}/{len(urls)}) {url} {status_label} {message}")

        if not is_valid:
            broken.append((url, message))

        time.sleep(delay)

    print(f"\nValidation complete. {len(broken)} broken link(s) found.")
    if broken:
        print("\nBroken links:")
        for url, reason in broken:
            print(f"  - {url} ({reason})")

    return len(broken)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate URLs found in a markdown file."
    )
    parser.add_argument(
        "--file",
        default=DEFAULT_README_PATH,
        help=f"Path to the markdown file (default: {DEFAULT_README_PATH})",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f"Request timeout in seconds (default: {DEFAULT_TIMEOUT})",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=DEFAULT_DELAY,
        help=f"Delay between requests in seconds (default: {DEFAULT_DELAY})",
    )
    args = parser.parse_args()

    broken_count = validate_links(
        filepath=args.file, timeout=args.timeout, delay=args.delay
    )
    sys.exit(1 if broken_count > 0 else 0)


if __name__ == "__main__":
    main()
