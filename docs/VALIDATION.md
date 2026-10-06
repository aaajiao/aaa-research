# Validation baseline for v1.0.0

**Verification date:** 6 October 2026 (Europe/Berlin).

This report records the automated helper tests and representative manual research workflows used to prepare v1.0.0. Manual checks used a connected ordinary Chrome browser on macOS. They establish what worked in that environment on that date, not a guarantee of future access, a clean unauthenticated browser profile, or complete coverage of Asia Art Archive (AAA).

Result counts below are observations used to test behaviour. They are not expected values for future runs.

## Automated checks

The eight test methods in [test_access_probe.py](../tests/test_access_probe.py) passed, including a run from a different working directory. The suite uses a simulated curl executable and makes no requests to AAA. It exercises:

- HTML and PDF candidate classification, missing expected text, and misleading content types.
- HTTP refusal and an HTTP 200 response containing a recognised challenge page.
- Redirects, server errors, invalid URLs, and a missing curl executable.
- An oversized response, including a transport that exits successfully despite exceeding the size limit.
- The process deadline and curl's own timeout, with partial-response accounting and temporary-file cleanup.

Run the suite from the repository root:

```sh
python3 tests/test_access_probe.py
```

Eight further tests in [test_release.py](../tests/test_release.py) cover version consistency, required documentation, local links, private-path and unfinished-template detection, payload exclusions, symlink rejection, reproducible ZIP metadata, and archive-content verification. All **16 offline tests** passed during release preparation. Run the complete suite with `python3 -m unittest discover -s tests -v`.

The project validator and internal reference-link checks also passed during preparation. These structural checks do not test research accuracy or live website access. The simulated transport suite was tested on macOS; it is not evidence of compatibility with every operating system or curl version. GitHub Actions runs the offline suite and release build on Python 3.10 and 3.13 on Linux.

## Manual Collections checks

The live interface was exercised for Online/Onsite access, Research/Library Collections, content type, format, From/To dates, combined filters, empty results, date/title sorting in both directions, Grid/Row views, and Reset.

The English `aaajiao` keyword search loaded 20 → 40 → 49 results. Thirteen item records under the linked personal archive were checked against the search results. The following cases informed the search procedure:

| Observation | Consequence recorded in the skill |
|---|---|
| Reset cleared controls but retained the previous results until a new submission; changing sort submitted automatically. | Verify the committed result state rather than assuming every control behaves alike. |
| The 2017-only and 2018-only searches each returned four materials; 2017–2018 returned ten. | A single-year filter can exclude multi-year material. Widen or remove bounds when overlap or historical subject coverage matters. |
| Online returned 25 and Onsite 23, compared with 49 unfiltered entries. | Distinguish material records from archive containers before reconciling counts. |
| The linked-person Collections view reported 53 entries. One run exposed 52; another sort exposed 40 but included an omitted catalogue. | A hidden Load More button is insufficient proof of completeness. A bounded comparison produced 53 distinct observed identities. |

The count reconciliation does not establish an exhaustive artist bibliography or show that every original document was read. See [search.md](../references/search.md) for the tested workflow and its limits.

## Language and link checks

The same keyword returned 49 English-interface entries and 48 Traditional-Chinese-interface entries, with different result sets. Both lists were traversed. The Chinese search surfaced *Heavy Artillery*, which was absent from the English keyword list; a linked-person query provided complementary results.

One Chinese result for a 2021 *404* exhibition-view record opened an error page. The language link on the corresponding working English record led to a valid Chinese record. Recovery used observed links rather than invented URL suffixes. Language switching could clear search conditions, requiring the query to be reapplied.

## Event Database and other sections

| Area | Representative verification |
|---|---|
| Event Database | Map cluster → individual marker → city-name popup → committed city chip; From/To bounds; Event (A–Z); one Load More increment from 10 to 20 events. |
| Touring-event dates | *China Avantgarde* disappeared under 1993–1993 and returned under 1993–1994. A Berlin city filter retained the complete tour's venue/date pairs. |
| Programmes | Year, type, and video conditions combined successfully; all 12 results in the selected query loaded. Series navigated to a separate page and dropped the previous year constraint. |
| Shortlists | Authored thematic essay → recommended location-code link → actual onsite library record. |
| Learning resources | Teaching-resource detail → five-page guide; complete text extraction and visual inspection of relevant pages. |
| LIKE A FEVER | Article body, author, date, notes, and earlier-version information. |
| Grant papers | Full HTML research paper, sections, notes, and author; a PDF is not required for this content type. |
| Collections Overview and Space II | Collecting scope, archive Information, historical context, material dates, processing history, and access conditions. |
| Restricted material | The Alain Sayag interview's restricted label, written-permission requirement, and linked application form's first step. No fields were filled and no application was submitted. |

The application form required a name and email before later steps; those later requirements remain unverified. The teaching page and its guide linked different external Graph Commons graph IDs; their equivalence was not assumed, and the external maps were not tested. Detailed paths are in [sections.md](../references/sections.md).

## Originals, OCR, video, and audio

An English scanned fax demonstrated why an existing text layer is not sufficient evidence: both embedded extraction and a fresh OCR pass misread the date. Visual inspection resolved it. The accessible PDF had one page, while the fax referred to a longer transmission and attachments; the missing material was not treated as read.

A Traditional-Chinese newspaper clipping had no usable text layer. Local OCR failed to recover its vertical body reliably. A bounded passage was instead read from enlarged images. This establishes a limited manual reading, not accurate automatic transcription of the article.

The online Sunny Pang interview played successfully. Two sampled frames with Chinese and English subtitles were compared with page 1 of a three-page English transcript. Separately, a 15-second audio interval, 00:36–00:51, was transcribed locally without supplying the reference text as a prompt. The machine output was broadly consistent with the written sources but contained a Cantonese recognition error. This is audio-derived ASR evidence, not a human listening check or a verified verbatim transcript.

The full interview was a separate Onsite record and was not accessed. Access and rights labels were retained per version. See [media.md](../references/media.md) for methods, source links, and uncertainty.

## Live access and remaining boundaries

A fresh ordinary Chrome tab could perform a real Collections search and open a record. Ordinary HTTP requests to that main-site record still returned 403, while its publicly linked PDF returned 200. The optional access helper was checked against these negative and positive live responses. The cause of the main-site refusal was not established.

This release does not establish:

- General unattended server access to AAA, or a verified public AAA API.
- Access to onsite or restricted originals, approval of an application, or permission to reproduce material.
- Reliable OCR for all scripts, vertical layouts, or handwriting; accurate general Cantonese ASR; human auditory review; or complete-recording coverage.
- A full audit of every record, filter combination, external link, or future website change.

The repository does not bundle browser credentials or profiles, downloaded archival originals, audio clips, or OCR/ASR models. Recheck the specific source and available tools when conducting new research. An access failure must remain explicit rather than becoming an empty result, a stale answer presented as current, or an invitation to bypass restrictions.
