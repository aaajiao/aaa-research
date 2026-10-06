# Collections filters, completeness, and language differences

Read for filtered searches, inventories, language switching, or unexpectedly missing results. All examples below are dated observations from connected Chrome on 2026-10-06, not expected counts for future runs.

## Commit the query, then verify its state

Ordinary Collections filters require the main Search submission. The sorting control behaves differently: changing sort immediately submits the current form and navigates. Inspect the resulting URL, filter labels and material before taking the next action, rather than clicking a now-stale Search control.

Reset cleared the keyword chips and selected controls but left the previous results and URL in place. Submit Search after resetting, or open the observed base search page, then confirm the reset actually affected results. A blank form over old results is not a completed reset.

Grid and Row are display modes for the same query. Row exposes useful access, publisher/location and parent-archive information; it has a different DOM structure from Grid. A view preference may persist into later queries or the other interface language. Do not assume record cards are always h2 elements, that image/title links are unique, or that a URL always retains the view parameter.

## Filter and boundary observations

The aaajiao query reported 49 results, mixing a collection container with material records. Both collection-type choices, both access choices, a content-type value, a format value, date bounds, combined conditions and an empty result were exercised.

| Case | Observed result | Research consequence |
|---|---|---|
| Online / Onsite | 25 / 23 | Their sum was less than the unfiltered 49; access-filter totals do not automatically account for container cards. |
| Research / Library Collections | 27 / 22 | Keep the entity type and parent context when combining them. |
| Content type artist book | Deep Simulator only | The card's broad category label can differ from the record's more specific content types. |
| Printed matter | 20 records | Format describes the material, not whether a digital preview exists. |
| Library + artist book + Printed matter + 2022–2022 | Deep Simulator only | Several controls can constrain one result; verify the resulting state. |
| Online + artist book + 2022–2022 | No records | An empty online subset does not imply the material is absent. |

**Date-range recall matters.** A 2017-only search returned four materials, a 2018-only search four, while 2017–2018 returned ten. The wider search included two records labelled 2017–2018 that neither single-year search returned. Do not assume the filter implements interval overlap. Widen or remove material-date bounds and inspect ranges manually when the question concerns everything touching a year. This is especially important for undated materials and later publications discussing an earlier period.

Date earliest/latest and title A–Z/Z–A were exercised on the same ten-record subset. Sorting changed their order without changing the set. Preserve date precision; sorting alone cannot resolve approximate, missing, or multi-year dates.

## Traverse until a real endpoint

The unfiltered English query loaded 20 → 40 → 49 distinct result links, after which Load More was hidden. Loading was asynchronous. An address can remain unchanged during a batch and later acquire a page suffix. Observe new records and the control's visibility, not just the address or immediate card count.

The linked personal archive exposed 13 item records in its Records tab, plus an Information tab with five folders. Its 13 object-link identifiers matched items already present in the search. Inspect returned containers when the task covers their descendants; do not add the container's reported count to the search count, or count the same children twice.

In Row view, image, title and locator links can repeat the same record URL. Deduplicate those links before counting. Keep an evidence log of interface language, query, filters, loaded batches, server-reported total, collected links, containers examined and unfinished branches. These are coverage facts, not proof that every original has been read.

### Linked-entity search and count reconciliation

The actual aaajiao person link opened a whole-site page summarising one archive container, 52 research/library records and 24 events. Its separate View All controls led to entity-filtered Collections and Event Database lists. Those section previews were not full inventories. The Collections target reported 53 entries including the container, compared with 49 from the free-text query. Follow these real entity links to complement keywords; never invent actor IDs.

A relevance-sorted entity run loaded 52 distinct cards before Load More disappeared, despite the reported 53. A second, title-sorted run stopped at 40 but exposed a catalogue omitted by the first run. Their union contained 53 distinct observed record keys. This tested a bounded recovery, not a guarantee that totals always reconcile. Count agreement alone does not prove an artist-wide inventory or that every original has been read.

When a list ends early, first check loading/state and counting units. Try one useful alternate sort/view or complementary observed query and compare identities; stop unproductive retries. Retain the source query for recovered entries. If the discrepancy remains, report the accessible set and unresolved count, rather than guessing missing records. After a wait timeout, inspect state before clicking again: an asynchronous batch may have arrived despite the wait failure.

## English and Traditional Chinese are not interchangeable inventories

The search-page language link reset the query to the other language's base search page. Reapply the intended terms and filters, and check the visible state. Detail-page language links generally point at a corresponding record, but must still be verified.

The same aaajiao term returned 49 English and 48 Traditional Chinese results. Both runs were loaded to their endpoints. The Chinese run surfaced a Heavy Artillery library record that was absent from the English keyword run; two Guo Cheng records appeared only in the English run. These observations do not establish the search engine's reason for the difference. For comprehensive research, search both relevant language interfaces, resolve verified name variants and linked entities, and merge only confirmed record identities. A casual single-title lookup need not run a full bilingual inventory.

A Chinese result card for a 2021 404 exhibition-view record led to an error page at an object URL ending /404. The corresponding working English record ended /404-exhibition-views-404-401901; its own language link opened a valid Chinese record. This is a recovery through observed links, not a rule for inventing suffixes. Keep the broken result as a recorded issue and cite the working record actually read.

Because AAA also holds works titled 404, the text “404” alone is not an error signal. Check the full page title and the presence of the expected record metadata. Conversely, an HTTP 200 or a plausible result card does not prove a valid detail page.

Archive context can produce several URLs for one object. Do not deduplicate solely by the full URL, translated title, or guessed slug normalisation. Use explicit language/canonical links, identifiers as actually supplied, hierarchy, metadata and linked originals together. Keep suspected duplicates unresolved when evidence is insufficient.
