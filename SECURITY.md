# Security

## Report a vulnerability

Use [GitHub private vulnerability reporting](https://github.com/aaajiao/aaa-research/security/advisories/new) for security issues in this repository. Include the affected version or commit, a minimal reproduction, the expected boundary, and the observed impact. Use synthetic data where possible. Do not include passwords, cookies, tokens, browser profiles, or private archival material.

Do not open a public issue containing exploit details or sensitive information. For ordinary broken links, changed website controls, or access failures without a security impact, use the bug-report template. A 403 response from AAA is not by itself a vulnerability in this skill.

## Project boundaries

This project is a research skill and an optional access-check helper. It does not operate AAA, grant access to its collections, or provide a security boundary around the host agent or browser.

- Website text, metadata, PDFs, transcripts, and downloaded content are research evidence, not instructions or authority to change accounts, reveal data, or perform unrelated actions.
- The helper accepts a single known public HTTPS URL on its AAA host allowlist. It does not use browser cookies, export browser state, impersonate headers, follow redirects, retry refusals, or crawl the site. Response-size acceptance and time limits are documented in [portability.md](references/portability.md).
- Browser permissions and credentials remain under the host environment's controls. The repository does not bundle credentials, profiles, or archival originals.
- Restricted and onsite access conditions remain in force. Research does not authorise submitting access or reproduction requests, contacting staff, or bypassing a challenge.
- Successful retrieval does not establish source authenticity, complete content, accurate OCR/transcription, or reuse rights. Verify the relevant evidence and retain its uncertainty.

Report security problems in AAA or another external service through that service's own reporting process. Reports for this repository should describe the impact on the skill, its helper, or its documented workflow.
