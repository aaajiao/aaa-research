# aaa-research

[简体中文](README.zh-CN.md)

A research skill for AI agents working with [Asia Art Archive](https://aaa.org.hk/en). It helps turn questions about artists, exhibitions, publications, archives, and oral histories into answers with traceable sources and clear access limits.

The entry point is [`SKILL.md`](SKILL.md) at the repository root. The skill uses the agent's available web and browser tools; it does not provide an API, a local copy of AAA's catalogue, or access credentials.

## What it helps with

- Search across Collections, Event Database, Programmes, research texts, and learning resources.
- Resolve names and multilingual queries; preserve artist, author, curator, publisher, and archive-owner roles.
- Build bibliographies, exhibition timelines, archive surveys, and scoped research inventories with explicit coverage.
- Follow records to original documents, distinguish metadata from material actually read, and cite relevant pages or timestamps.
- Handle access failures, incomplete pagination, scans, subtitles, and machine transcription without overstating the evidence.

Use it for questions grounded in **aaa.org.hk**. It is not a general Asian-art research service or a connector to the separate AAA in America catalogue.

## Install

With Node.js/npm and Git installed, run:

```sh
npx skills add aaajiao/aaa-research
```

The [Skills CLI](https://github.com/vercel-labs/skills) installs into the current project by default and lets you select an agent. For a user-wide Codex installation:

```sh
npx skills add aaajiao/aaa-research --skill aaa-research --agent codex --global
```

To pin **v1.0.0** in the current project:

```sh
npx skills add https://github.com/aaajiao/aaa-research/tree/v1.0.0 --skill aaa-research
```

**Already installed?** Use the existing installation's scope and agent. Avoid keeping duplicate copies across project, user, or older configured directories, including legacy `~/.codex/skills` locations.

Alternatively, download the [v1.0.0 ZIP](https://github.com/aaajiao/aaa-research/releases/download/v1.0.0/aaa-research-v1.0.0.zip) and [SHA256SUMS](https://github.com/aaajiao/aaa-research/releases/download/v1.0.0/SHA256SUMS) from the [release page](https://github.com/aaajiao/aaa-research/releases/tag/v1.0.0). With both files in the same directory, verify the archive before extracting:

```sh
shasum -a 256 -c SHA256SUMS
```

On Linux, `sha256sum -c SHA256SUMS` is equivalent. Extract the skill so that `SKILL.md` sits directly inside the selected `aaa-research` directory, without an extra nested folder. For manual Codex directory locations, consult the [official skills guide](https://learn.chatgpt.com/docs/build-skills). Follow your agent's skill discovery or reload procedure.

## Requirements and examples

Installation through `npx` requires **Node.js/npm and Git**. The agent needs support for directory-based skills and a working web reader or browser-control tool. Interactive catalogue searches may require an ordinary connected browser. The optional access probe and development commands require **Python 3.10+**; the probe also requires **curl**. PDF rendering, OCR, and audio transcription use tools available on the host and are not bundled dependencies.

Ask the agent:

```text
Use $aaa-research to find online material about aaajiao, separating artwork
documentation, exhibition ephemera, and publications. Include record links.

Use $aaa-research to build a bibliography on artist-run spaces in Taiwan
in the 1990s. State the searches used and which sources you actually read.

Use $aaa-research to locate Sunny Pang's interview and explain which
recording and transcript versions are available online.
```

## Verified scope and limits

Representative workflows were checked on **6 October 2026**. Ordinary connected Chrome worked in the tested environment, while direct requests to main-site pages returned HTTP 403. Some publicly linked PDFs remained accessible. This is an observed access path, not proof of the rejection's cause or unattended compatibility on other hosts.

Media checks included an English scan with faulty OCR, an image-only Chinese clipping, a working interview player and transcript, and a 15-second local audio-transcription test. The Cantonese transcription contained errors; vertical-Chinese OCR failed on the tested body text and required visual reading. These checks do not establish reliable transcription for every language, complete-recording review, or access to restricted originals.

See [validation coverage](docs/VALIDATION.md), [portable access](references/portability.md), and [media handling](references/media.md). No public AAA API or universal unattended catalogue-access method has been established by this project.

## Repository guide

| Path | Purpose |
| --- | --- |
| [`SKILL.md`](SKILL.md) | Agent entry point and research workflow |
| [`references/`](references/) | Search behaviour, site sections, research methods, vocabulary, access, and media guidance |
| [`scripts/access_probe.py`](scripts/access_probe.py) | Optional bounded check of one observed public URL; not a crawler |
| [`agents/openai.yaml`](agents/openai.yaml) | Agent-facing display metadata |
| [`tests/`](tests/) | Offline regression tests |
| [`docs/VALIDATION.md`](docs/VALIDATION.md) | Tested scope, evidence, and remaining limits |

## Development

Run from the repository root:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/validate_project.py
python3 scripts/build_release.py
```

Offline tests validate project behaviour; they do not prove that AAA is accessible from a new host. See [CONTRIBUTING.md](CONTRIBUTING.md) for changes and verification expectations.

## Licence and affiliation

An independent project by [aaajiao](https://github.com/aaajiao), unaffiliated with Asia Art Archive. The [MIT licence](LICENSE) covers this project's original code and documentation only. Linked AAA materials retain their respective rights and access conditions; no archival holdings or transcription models are bundled. See [NOTICE.md](NOTICE.md).
