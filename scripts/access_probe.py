#!/usr/bin/env python3
"""Bounded, credential-free HTTP preflight for one known public AAA URL.

Requires Python 3 and curl; does not search, download an archival deliverable,
read browser state, follow redirects, retry, or bypass access controls.
"""

import argparse
import datetime
import html
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit


ALLOWED_HOSTS = {"aaa.org.hk", "www.aaa.org.hk", "cdn.aaa.org.hk"}
CHALLENGE_MARKERS = (
    "<title>just a moment", "<title>access denied", "<title>403 forbidden",
    "<title>verify you are human", "<title>attention required",
)


def public_url(value):
    """Only accept unsigned public HTTPS URLs on AAA's observed hosts."""
    try:
        parsed = urlsplit(value)
        valid = (parsed.scheme == "https" and parsed.hostname in ALLOWED_HOSTS
                 and parsed.port in (None, 443) and not parsed.username
                 and not parsed.password and not parsed.query)
    except ValueError:
        valid = False
    if not valid:
        raise argparse.ArgumentTypeError(
            "Use a public HTTPS URL on aaa.org.hk or cdn.aaa.org.hk, "
            "without credentials, signed parameters, or a query string."
        )
    return urlunsplit((parsed.scheme, parsed.netloc, parsed.path or "/", "", ""))


def classify(status, content_type, body, expected_kind, contains=None):
    """Classify observed bytes, without asserting content identity or completeness."""
    mime = content_type.split(";", 1)[0].strip().lower()
    text = html.unescape(body.decode("utf-8", errors="replace"))
    if status in (401, 403, 429):
        return "http_refused"
    if 300 <= status < 400:
        return "redirect_not_followed"
    if not 200 <= status < 300:
        return "http_error"
    if any(marker in text.lower() for marker in CHALLENGE_MARKERS):
        return "possible_challenge"
    if expected_kind == "pdf":
        return "pdf_candidate" if body.startswith(b"%PDF-") else "unexpected_content"
    if mime not in ("text/html", "application/xhtml+xml"):
        return "unexpected_content"
    if not contains:
        return "html_requires_content_check"
    if contains.casefold() not in text.casefold():
        return "expected_text_not_observed"
    return "html_candidate"


def next_step(classification):
    if classification in ("html_candidate", "pdf_candidate"):
        return ("Read the actual source and verify identity, provenance, relevant "
                "content, and access conditions. This preflight is not a completed reading.")
    if classification == "http_refused":
        return ("Do not repeat this HTTP request. Try a supported ordinary browser "
                "and verify visible task-relevant content. If unavailable, report the limit.")
    return ("Use a supported browser/read tool and inspect the actual page or file. "
            "If that is unavailable, report unverified access; do not infer absence of material.")


def probe(url, kind, contains=None, timeout=20, max_bytes=524288):
    report = {
        "checked_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "url": url, "transport": "curl_without_config_or_browser_state",
        "kind_expected": kind, "timeout_seconds": timeout,
        "max_bytes": max_bytes, "http_status": None, "content_type": None,
        "response_file_bytes": None, "bytes_read": 0,
        "classification": "transport_error",
    }
    executable = shutil.which("curl")
    if not executable:
        report["classification"] = "curl_unavailable"
        report["next_step"] = next_step(report["classification"])
        return report

    with tempfile.TemporaryDirectory(prefix="aaa-access-probe-") as directory:
        response_path = Path(directory) / "response"
        # --disable is intentionally the first curl argument: ignore .curlrc.
        # No credentials, cookie jar, custom headers, retries, or redirect following.
        # Rate and wall-clock caps also bound legacy curl's unknown-length responses.
        command = [
            executable, "--disable", "--silent", "--show-error",
            "--proto", "=https", "--max-time", str(timeout),
            "--connect-timeout", str(min(timeout, 8)),
            "--max-filesize", str(max_bytes), "--limit-rate", "512K",
            "--output", str(response_path),
            "--write-out", "%{http_code}\n%{content_type}", "--url", url,
        ]
        try:
            completed = subprocess.run(command, capture_output=True, timeout=timeout + 2)
            report["curl_exit_code"] = completed.returncode
            metadata = completed.stdout.decode("utf-8", errors="replace").splitlines()
            if metadata and metadata[0].isdigit():
                report["http_status"] = int(metadata[0]) or None
            report["content_type"] = metadata[1] if len(metadata) > 1 else ""
            if response_path.exists():
                report["response_file_bytes"] = response_path.stat().st_size
                # Some older transports do not enforce --max-filesize for a
                # response without Content-Length. Never accept its prefix.
                if completed.returncode == 0 and report["response_file_bytes"] <= max_bytes:
                    with response_path.open("rb") as stream:
                        body = stream.read(max_bytes)
                else:
                    body = b""
                report["bytes_read"] = len(body)
            else:
                report["response_file_bytes"] = 0
                body = b""
            if report["http_status"] in (401, 403, 429):
                report["classification"] = "http_refused"
            elif completed.returncode == 28:
                report["classification"] = "timeout"
            elif (completed.returncode == 63
                  or report["response_file_bytes"] > max_bytes):
                report["classification"] = "response_exceeds_limit"
            elif completed.returncode != 0:
                report["classification"] = "transport_error"
            elif report["http_status"] is not None:
                report["classification"] = classify(
                    report["http_status"], report["content_type"], body, kind, contains
                )
        except subprocess.TimeoutExpired:
            report["classification"] = "timeout"
        except OSError:
            report["classification"] = "transport_error"
        finally:
            # subprocess.run kills and waits for a timed-out child before raising.
            # Count its partial body, without reading it, before temporary cleanup.
            if report["response_file_bytes"] is None:
                try:
                    report["response_file_bytes"] = (
                        response_path.stat().st_size if response_path.exists() else 0
                    )
                except OSError:
                    pass
    report["next_step"] = next_step(report["classification"])
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", type=public_url, help="A known public page or record-linked file")
    parser.add_argument("--kind", choices=("html", "pdf"), default="html")
    parser.add_argument("--contains", help="Expected task-specific text for an HTML candidate")
    parser.add_argument("--timeout", type=int, default=20, choices=range(1, 31), metavar="1..30")
    parser.add_argument("--max-bytes", type=int, default=524288)
    args = parser.parse_args(argv)
    if not 1024 <= args.max_bytes <= 2097152:
        parser.error("--max-bytes must be between 1024 and 2097152")
    result = probe(args.url, args.kind, args.contains, args.timeout, args.max_bytes)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["classification"] in ("html_candidate", "pdf_candidate"):
        return 0
    if result["classification"] in ("http_refused", "possible_challenge"):
        return 10
    return 11


if __name__ == "__main__":
    sys.exit(main())
