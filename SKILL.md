---
name: aaa-research
description: Research Asia Art Archive (aaa.org.hk) collections, artists, exhibitions, publications, oral histories, programmes, and research texts. Use for AAA-based discovery, multilingual searches, archival context, bibliographies, exhibition timelines, and source or access verification. Not a general Asian-art search skill or a connector for the separate AAA in America catalogue.
metadata:
  version: "1.0.0"
---

# Asia Art Archive research

Turn a research question into a traceable answer using AAA's current website. Support both a quick factual lookup and a scoped research inventory; scale the work to the question. Reply in the user's language while preserving source titles, names, and relevant original-script text.

This is a research procedure, not a bundled database or API client. It needs a web search/read tool or a browser-control tool. It includes no credentials and must not claim to provide access to restricted originals.

## Choose what to load

- For a first visit or an unfamiliar section, read [site-map.md](references/site-map.md): entry points, filters, page families, and observed URL examples.
- For Collections filtering, pagination, bilingual inventories, or missing results, read [search.md](references/search.md). Date ranges, Reset, sorting and language switching have distinct behaviours.
- For browser setup, 403, dynamic results, or document retrieval, read [access.md](references/access.md). Local connected Chrome worked in verification; direct fetching did not reliably work. Tool names and browser handles depend on the host.
- For a new host or unattended use, read [portability.md](references/portability.md), including the optional bounded access probe and its failover outcomes.
- For people, exhibitions, collections, bibliography, oral history, teaching, or visit preparation, read the relevant part of [research-methods.md](references/research-methods.md), including its evidence and citation guidance.
- For Event Database controls, Programmes, authored texts, Shortlists, teaching guides or restricted-access instructions, read the relevant section of [sections.md](references/sections.md).
- For scanned originals, audio/video, subtitles, OCR or local transcription, read [media.md](references/media.md); use only capabilities available on the current host and preserve the evidence actually read.
- For thematic, multilingual, ambiguous, or low-recall searches, read [vocabulary.md](references/vocabulary.md). Discover the currently linked official vocabulary rather than freezing a historical copy.

## Research workflow

### 1. Define the question and the unit

Identify the person/organisation, event, topic, place, period, material type, and required access level. Distinguish a shortlist from an inventory. Do not impose a long research protocol on a request for one known title.

For dates, establish whether the user means the date of an event, the creation/publication of a document, or a period discussed by later research. For ambiguous names, resolve identity through original script, roles, affiliations, year, and place. Ask only when ambiguity would materially change the answer; continue by separating candidate identities where useful.

For an inventory, state the scope that can actually be checked: sections, query terms, languages, time range, record types, and access constraints. “All” requires a declared scope and traversal, not a high result count.

### 2. Choose complementary sources

Use Collections for archival records and library materials; Event Database for exhibition/event entities and venue-date relationships; Programmes for AAA activities; LIKE A FEVER and grant papers for authored research; Learning & Participation and Shortlists for teaching material and guided reading. Consult only sections relevant to the question.

Start with the most specific known title/name. Expand with verified variants and bilingual terms if needed. Use linked people, organisations, keywords, related events, and parent collections to move beyond free-text matches. Do not infer undocumented Boolean syntax, automatic synonym expansion, or the meaning of a search count.

### 3. Retrieve and inspect

Use the working access path documented in access.md. Search results are leads: open the actual record for claims and follow its parent archive or related event where context affects interpretation. Clear unrelated filters when moving to a new query; read the resulting filter labels and URL to confirm the query applied. Reset may require a new submission, while sorting may submit automatically. Verify the page rather than assuming every control behaves alike.

For an inventory, traverse the observed pagination/Load More controls and collect distinct record links until exhausted or a concrete limit is reached. Verify that new results arrived; an unchanged URL alone does not mean loading failed. If the scope includes an archive or folder, inspect its hierarchy and traverse relevant descendants, or explicitly report unexamined children. Keep container and item totals separate. Save a compact query log and coverage limits. For a research selection, stop once the question has adequate evidence and the relevant uncertainty is clear.

Compare loaded, deduplicated entities with the reported total using consistent units. If Load More ends early, inspect the current state and try one meaningful alternative sort/view or complementary observed entity query. Merge only verified identities; disclose unresolved count differences rather than fabricating missing rows or declaring completion from a hidden button.

For comprehensive multilingual coverage, query the relevant interface languages separately: observed English and Chinese result sets differed. Language switching can clear search conditions. Cross-check broken detail links using actually observed counterpart/parent links; do not invent URL repairs or merge records on translated title alone.

### 4. Keep the entities distinct

- An archive owner is not automatically a document's author, depicted artist, or rights holder. Preserve displayed roles.
- A catalogue record, an artwork, an exhibition photograph, an album, and an individual file/image are different units. A card's image count is not a work count.
- Keep collection → folder/series → item context and multipart relationships. Deduplicate verified copies of the same record across query/view/language URLs; do not merge on title alone or discard related but distinct records.
- Preserve assigned/translated title status, uncertain dates, and original-script names. Do not silently turn a catalogue anomaly into a fact.
- Material date, event date, archive date range, page/publication date, digitisation date, and retrieval date have different meanings. Preserve venue-date pairs for touring events.
- Material held by AAA does not imply AAA organised the event. An announcement describes a planned programme; it does not prove the content of a talk or that every scheduled activity occurred.

### 5. Read to the level needed

Track separately what the catalogue says is accessible and what was actually read: metadata, catalogue description, image/preview, document pages, transcript, or audio/video segment. Open linked original files for content-level conclusions. If a PDF is a scan, use available OCR or visual reading and verify uncertain names/dates against the image. Cite pages or timestamps actually examined.

Online, Onsite, restricted access, and reuse rights are separate questions. Read the record's current conditions; do not infer the whole object is online from a thumbnail, or generalise one collection's application requirements. If the original cannot be read, summarise only the available description and identify the gap. External editions must be labelled as external, even when linked from AAA.

### 6. Answer with evidence and coverage

Lead with the answer. Use a compact bibliography, table, timeline, or narrative only as useful. Give record-level links and enough identifiers to find the material; for substantive interpretation, add original-file pages/timestamps and distinguish the author's statement, AAA's description, and your inference. Check auto-generated citations against metadata.

For substantial research, keep or deliver an evidence ledger containing the fields relevant to the task: record title/URL; person and role; collection/folder or bibliographic locator; material and event dates; access and rights labels; reading level and page/time span; relevance and supported claim; retrieval date. A JSON/CSV export is optional when requested or useful, not mandatory for every answer.

Report what was searched, where traversal stopped, and inaccessible or conflicting evidence. “No result under these searches” is not “AAA has no material” or “the event did not happen.” Counts and access labels are dated observations, not permanent facts. Do not treat archive coverage as a measure of artistic significance.

## Completion checks

Before answering, check: correct identities and roles; correct event and date meaning; original versus catalogue description distinguished; parent context retained where needed; specific links support claims; access limits explicit; inventory completeness matches the work actually done. If two sources disagree, retain the disagreement and explain its consequence rather than choosing silently.

## Maintenance boundary

Representative workflows and boundary cases were verified on 2026-10-06; each reference distinguishes the tested scope from external access limits. Reinspect the live interface when controls, URLs, or access behaviour differ. No public AAA API or universal unattended catalogue path was established. Do not invent endpoints or make this skill depend on private browser state, copied cookies, a fixed browser ID, or a particular person's cached search results.
