# Contributing

Contributions should improve the agent's research decisions or a demonstrated retrieval failure. Keep the entrypoint focused and place conditional detail in a relevant reference module. Add a new dependency or script only when it makes a repeated operation measurably more reliable.

## Local development

Use Python 3.10 or newer. The project checks and access-probe tests use the standard library; the live access probe additionally needs curl. Browser tools, PDF readers, OCR and ASR are supplied by the agent's host and are not installed by the project.

From the repository root:

```bash
python3 scripts/validate_project.py
python3 -m unittest discover -s tests -v
python3 scripts/build_release.py
```

The automated suite uses fake transports and local fixtures. It does not contact AAA. Keep CI independent of the website's uptime, access policy and record counts. The optional access probe is documented in [portability.md](references/portability.md); make a live request only when it is necessary to validate a known public source.

## Changes to research guidance

- Preserve source URLs, the date checked, and whether the evidence came from a live page, a document, or an older search index.
- Verify a meaningful task, not only that an element or phrase exists. For example, show that a selected filter changes the visible result state or that an original document supports a cited claim.
- Distinguish material records, archive containers, images and events; retain roles, dates, access labels and provenance.
- Document incomplete evidence and unresolved contradictions. Never turn a negative query into proof that a source does not exist.
- Keep exact source quotations short. Do not commit archival originals, downloaded media, OCR/transcription models, credentials, browser profiles or private application details.

For substantive skill changes, run an independent agent on a realistic research request without giving it the expected answer. Record the observed outcome and limits. Do not make live site checks automatic on every pull request.

## Reporting a problem

Open an [issue](https://github.com/aaajiao/aaa-research/issues/new/choose) with the skill version, relevant public URL, date, host/tool capability, expected result and observed result. Say what was actually read. Remove cookies, tokens and private information from logs. For a vulnerability, follow [SECURITY.md](SECURITY.md).

## Versioning and releases

`VERSION` is the release source of truth. Keep `metadata.version` in `SKILL.md` in sync. Update the changelog and version-pinned README examples when preparing a release.

- Patch: corrections and compatible fixes to instructions, references or helpers.
- Minor: new compatible workflows or helper capabilities.
- Major: incompatible installation, helper CLI, or workflow-contract changes.

Run the checks and build the release. The builder writes `dist/aaa-research-v<version>.zip` and `dist/SHA256SUMS`; these files are release assets, not source files to commit. It includes an explicit skill payload and omits development-only material, caches and `.git`.

Commit the release files, create an annotated `v<version>` tag on that commit, and push the commit and tag. Confirm CI for that commit before publishing a GitHub Release. Attach the versioned ZIP and checksum file with release notes that state changes and remaining limits. Download the published assets and check them against the locally built files.

Do not replace a published version tag or asset to silently change a release; issue a new version. An observation date is not a guarantee that the website has remained unchanged.

## Licence

Contributions to original project code and documentation are made under the [MIT License](LICENSE). Source materials and third-party tools retain their own licences, as described in [NOTICE.md](NOTICE.md).
