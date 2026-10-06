# Portable access and unattended preflight

Read when moving this skill to another host, running without an interactive user,
or deciding whether direct HTTP is usable. This procedure does not require CUA,
Chrome, a saved browser profile, or the optional script: use the supported browser
or web-reader tool available on the host and inspect its current documentation.

## What was actually verified

On 6 October 2026, a new ordinary Chrome tab could display the [bot record](https://aaa.org.hk/en/collections/search/archive/individual-file-aaajiao-2017-2018-bot/object/bot---bot)
and perform an `aaajiao` search through the Collections form. Fresh ordinary HTTP
requests using both Python's standard library and curl received HTTP 403 for
that record. A curl request to the [PDF linked by the record](https://cdn.aaa.org.hk/_source/individual-files/ajif00008.pdf)
received HTTP 200, `application/pdf`, and a PDF signature (126,642 bytes).

This establishes a working local browser path and a separately accessible public
file. It does **not** establish the cause of the refusal, an unauthenticated browser
profile, a public API, a general server-side extraction route, or operation from
another machine. No supported unattended catalogue access was established in this
test. Do not present the refusal as fixed or claim that no such service exists.

## Optional reproducible check

If direct HTTP is needed and Python 3 plus curl are already available, use
[`scripts/access_probe.py`](../scripts/access_probe.py) once for the specific known
public URL. Skip this check if the current task already has a working reader.
Substitute the actual, observed public record and attachment URLs below; do not
guess filenames or probe a list of possible paths.

```bash
python3 /path/to/aaa-research/scripts/access_probe.py 'PUBLIC_RECORD_URL' --contains 'EXPECTED RECORD TITLE'
python3 /path/to/aaa-research/scripts/access_probe.py 'RECORD_LINKED_PDF_URL' --kind pdf
```

The helper makes one GET, ignores curl's configuration file, uses no browser
cookies, credentials, header impersonation, redirects, or retries, and never
prints raw headers or response text. It accepts public HTTPS URLs on the observed
AAA hosts only, without query strings or embedded credentials. Query-bearing
links and other file formats remain usable through an appropriate browser/reader;
the script's narrow input scope is not a statement that those URLs are inaccessible.
It keeps the host's existing networking/proxy configuration unchanged.

Default timeout is 20 seconds; a separate process deadline is 22 seconds. The
response acceptance threshold is 512 KiB. The helper checks the actual response
file size even if curl exits successfully, rejecting an oversized body before
content classification. Older curl versions may still receive more than this
threshold when the length is unknown; the rate and time caps bound that transfer,
but are not a strict downloaded-byte cap. Temporary response bytes are removed,
including partial output after a timeout. `--timeout 1..30` and
`--max-bytes 1024..2097152` adjust the deadline and acceptance threshold. A larger
document exceeding the threshold is unverified, not unavailable.

The JSON report includes time, URL, HTTP status, MIME type, classification, and the
next action. `response_file_bytes` counts the received body saved by curl, including
partial output; it is not a wire-byte count and is `null` if unobserved.
`bytes_read` counts only the bytes the helper actually inspected. Oversized or
timed-out bodies are not read for content, so this can be zero even when the
response file contains bytes. Exit codes are:

| Exit | Meaning | Next action |
|---|---|---|
| `0` | HTML contains the expected text, or file starts with a PDF signature | Read and verify the source. A candidate is not a completed reading, proof of correct identity, or evidence that search/pagination works. |
| `10` | HTTP 401/403/429 or a recognised challenge page | Stop direct retries; try a supported ordinary browser. Respect rate-limit or hand-off requirements. |
| `11` | Other unverified result: timeout, transport/tool failure, redirect, wrong content, missing expected text, or response too large | Inspect through a supported reader/browser; preserve the reported limitation if none works. |
| `2` | Invalid command or input URL | Correct the input from an observed public link; do not invent another URL. |

HTML checks are deliberately conservative and do not detect every login or
challenge page. A PDF signature likewise cannot prove a complete, readable PDF.
Verify the actual record or open the downloaded document before substantive use.
The helper only probes access; it does not save research documents or crawl AAA.

The bundled standard-library regression suite runs without network access:

```bash
python3 /path/to/aaa-research/tests/test_access_probe.py
```

Its fake transport uses an executable Python shim, tested on macOS. It verifies content classification, refusal/challenge handling, oversized successful responses, missing transport, invalid inputs, process deadlines and temporary-file cleanup. It does not validate a new host's network policy or establish universal browser access.

## Failover contract

1. **Working reader or browser:** verify visible task-relevant content. Before
   relying on a browser for an inventory, demonstrate a real search and a detail
   page in that environment. Use current DOM/accessibility state and observed links.
2. **HTTP refusal or challenge:** retain the URL, time, status and reading level;
   stop identical retries. Continue in an available ordinary browser using the
   host's supported tool. Do not export cookies, copy a profile, rotate proxies,
   alter headers to evade the refusal, or reverse-engineer private endpoints.
3. **Browser unavailable or also blocked:** report catalogue access as unavailable
   for this run. An unattended process must stop the source-dependent step rather
   than silently substitute search snippets, fabricated empty results, or stale
   local metadata. Any useful indexed/cached material must be identified as such.
   CAPTCHA/login follows the host's normal hand-off policy; waiting is not approval.
4. **Record-linked file separately accessible:** it may support content-level
   research once read, even when live catalogue access is blocked. Retain its
   record provenance and distinguish a previously observed link from a currently
   verified record. Successful file access does not lift other item restrictions.
5. **New host or unattended deployment:** run its own task-relevant preflight.
   Do not claim unattended readiness from this Mac's browser success. Repeat a
   failed probe only after a relevant external state or access-path change, not
   on an automatic retry loop.

The baseline was tested with live negative catalogue and positive PDF responses.
The helper was also checked with simulated successful HTML/PDF, HTTP refusal,
HTTP 200 challenge HTML, a false PDF, a redirect, oversized response, server error,
missing expected text, invalid URLs, missing curl, an exit-zero oversized PDF from
a transport ignoring its size option, and timeout cleanup after partial output.
These tests validate failure handling, not future site policy.
