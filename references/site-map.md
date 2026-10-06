# Site map and observed controls

Checked with connected Chrome on 2026-10-06. Entry points below are navigation aids, not an API contract. Reopen live pages before relying on changing counts, filters, or schedules. Representative detail workflows for all listed sections were exercised; see [sections.md](sections.md) and [search.md](search.md) for tested interactions and exceptions. This does not establish complete content coverage.

| Research need | Entry point | What to inspect |
|---|---|---|
| Archives and library material | [Collections search](https://aaa.org.hk/en/collections/search) | Record cards and their detail pages; parent archive context; related events |
| Collection scope and arrangement | [Overview](https://aaa.org.hk/en/collections/overview) and links from collection records | Scope, history, dates covered, language, arrangement, access/use conditions |
| Exhibitions and events represented in the collection | [Event Database](https://aaa.org.hk/en/collections/event-database) | Event identity, role-specific people/organisations, venue-date pairs, related collection |
| Controlled concepts and exploratory browsing | [Browse](https://aaa.org.hk/en/collections/browse) | Keywords, visual book-cover archive, interactive map; coverage differs from catalogue search |
| Curated bibliography | [Shortlists](https://aaa.org.hk/en/collections/shortlists) | Editorial selection, rationale and linked material; not an exhaustive inventory |
| AAA talks, workshops, exhibitions and calls | [Programmes](https://aaa.org.hk/en/programmes) | Dates, current/past distinction, series, type, recordings and downloads |
| Authored essays and conversations | [LIKE A FEVER essays](https://aaa.org.hk/en/like-a-fever/like-a-fever/type/essays) | Author, article type, publication date, body, references and related records |
| Teaching and archive practice | [Learning resources](https://aaa.org.hk/en/learning-participation/resources) | Exercises, lesson plans, handbooks, linked downloads and original archive materials |
| Research grant outputs | [Papers & Presentations](https://aaa.org.hk/en/grants/the-robert-h-n-ho-family-foundation-greater-china-research-grant-papers) | Authored research, not merely an award announcement |

English /en/ and Traditional Chinese /tc/ are interface routes. Follow the language link exposed by a page; do not assume every field/article is translated or that a Chinese interface implies a Chinese original. AAA in America at aaa-a.org is a distinct site/catalogue and must be labelled separately if it enters the research.

## Collections search

Observed controls: Access level (Online or Onsite), Collection type (Research Collections or Library Collections), Content type, Format, From/To, free text, sort and grid/row views. Content types span correspondence, ephemera, interview documentation, transcript, artwork documentation, catalogues, and other material categories. Formats describe physical/digital form rather than subject matter. Read the actual list rather than keeping a frozen complete copy here.

The date controls are on a material search page. Interpret returned Publication/Creation dates separately from related-event dates. Testing found that single-year filters excluded two materials spanning 2017–2018; widen/remove date bounds when overlap matters. Sorting includes relevance, date, and title, and changes submit automatically. The access filter only exposed Online/Onsite, but individual records can contain additional restrictions. A broad search need not begin with Online: doing so may hide relevant onsite catalogues.

The same result page can contain an archive container, a publication, and an item with several images. Search counts therefore do not directly count works, people, exhibitions, or images.

Observed URL examples, obtained by actual form submission:

- https://aaa.org.hk/en/collections/search/search/keywords:aaajiao--sort:relevance
- https://aaa.org.hk/en/collections/search/search/access-level:online--keywords:aaajiao--sort:relevance

They demonstrate current state, not a general URL encoder. Prefer form controls; never substitute guessed numeric actor/keyword IDs.

## Event Database

The live interface offered city selection through map markers/popups, From/To years, text search, and event/venue/date ordering. A hidden cities field was present, but no visible city text/autocomplete input was found. Commit a map selection through its city popup and verify the active city chip; see [sections.md](sections.md). A record can have several venues with separate date ranges, plus artists, curators, organisers, and related archival/library materials.

Verified search example: https://aaa.org.hk/en/collections/event-database/search/keywords:china-avantgarde. The [1993 event record](https://aaa.org.hk/en/collections/event-database/china-avantgarde/search/keywords:china-avantgarde/page/1) includes a touring itinerary and roles. Preserve the pairings; do not flatten all venues to the earliest or latest date. Similar historical event titles require year/place disambiguation. Some event dates are unknown or only partly specified, so a latest-first list is not sufficient proof of chronological order.

## Linked entities and whole-site discovery

Record metadata links people, subjects, and venues to broader results. For example, the artist link for aaajiao was https://aaa.org.hk/en/search/search/actors:34483. This was opened and its Collections View All target traversed. Reuse a linked entity after resolving identity rather than inventing an identifier. A whole-site page has section previews and separate View All links; its grouped counts and a downstream mixed container/item total can differ. See [search.md](search.md) for the actual count-reconciliation test.

## Programmes and authored content

Programmes offered year, series, type, keyword and a video-related checkbox, and distinguished current/upcoming from past items. Year/type/video were tested together; Series navigates separately and can clear previous conditions. See [sections.md](sections.md). Verify the date and detail page before presenting an activity as available.

LIKE A FEVER navigation distinguishes essays, conversations, poetry/fiction, notes and series. Older indexed links can use legacy section names; follow redirects and current labels. Article search/discovery is not the same as full-text search of every archival PDF. Learning resources and grant outputs often link documents; inspect the linked source when using its content.

## Vocabulary and citations

The live [Keywords page](https://aaa.org.hk/en/collections/browse/keywords-120) linked [this 2019-named vocabulary PDF](https://cdn.aaa.org.hk/_source/Collection_documents/keywords-forpdf20190506.pdf). Discover the current link there before assuming a historical file is current.

The [bot record](https://aaa.org.hk/en/collections/search/archive/individual-file-aaajiao-2017-2018-bot/object/bot---bot) exposes a public PDF, access conditions, rights and Citation controls. Its citation popup omitted a creator and useful source context during verification. Use generated citations as drafts and check against record metadata; do not invent an official citation standard. The separate [Deep Simulator record](https://aaa.org.hk/en/collections/search/library/deep-simulator) illustrates bibliographic fields and onsite access.
