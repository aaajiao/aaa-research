# Changelog

Project releases use semantic version numbers. Website observations carry their own verification dates and can change independently of the skill version.

## [1.0.0] - 2026-10-06

Initial public release.

### Added

- A research skill for Asia Art Archive collections, people, exhibitions, publications, oral histories, programmes, authored texts, and teaching resources.
- Eight reference modules covering site navigation, query completeness, multilingual vocabulary, archival research, media evidence, section-specific controls, browser access, and portability.
- Verified guidance for bilingual search differences, nested records, date ranges, dynamic loading, inconsistent counts, broken links, and source citations.
- OCR, visual reading, subtitles, transcripts, and bounded local audio-transcription workflows with explicit evidence limits.
- An optional credential-free HTTP access probe with deadlines, content checks, clear failure outcomes, and regression tests.
- English and Simplified Chinese README files, validation notes, contribution and security guidance, CI, deterministic release packaging, and checksum assets.

### Known external limits

- Main-site HTTP requests can return 403; a supported ordinary browser remains the verified catalogue access path in the test environment.
- No public API or universal unattended server workflow has been established.
- Restricted originals require the source's permissions; OCR and ASR outputs require source verification.

[1.0.0]: https://github.com/aaajiao/aaa-research/releases/tag/v1.0.0
