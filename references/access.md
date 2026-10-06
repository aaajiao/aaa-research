# Access and browser procedure

Read when selecting a retrieval tool, handling access errors, or traversing dynamic results.

For repeatable direct-access checks or another host, see [portability.md](portability.md). For query controls and language-specific result differences, see [search.md](search.md). For reading the source after retrieval, see [media.md](media.md).

## Verified baseline, 2026-10-06

On one local Mac environment, ordinary connected Chrome could open AAA, search its current catalogue, apply an Online filter, load more results, and open record/event pages. Direct HTTP, the web reader, and a separate automation-browser session returned 403 for the main website. A fresh direct request still failed while Chrome worked. This establishes a usable session, not the server's rejection rule or a guarantee for other machines.

Public CDN files behaved separately: direct download of a PDF linked from the bot record worked although the web reader failed on that file. The current vocabulary PDF also opened with the web reader. Test a specific linked resource; do not infer that every CDN file is readable.

## Select the access path

1. If a connected ordinary browser is available, prefer it for interactive AAA searches. Inspect its current documentation and use supported navigation, DOM/accessibility inspection, and controls. Select a relevant existing tab or create a research tab. Keep user-entered form state intact.
2. If another tool already reads the needed current page successfully, use it. No particular browser or product is required by the research method.
3. When a direct reader returns 403, use a normal connected browser if available. Verify both a real search and a detail page before treating that path as working. If it also fails, report the limit and use public search indexes as discovery only.
4. If only indexed content is available, label it as such. Do not present an index crawl date as the material's publication date, or an old result count/access rule as current. Do not claim a completed live search.

Stop identical retries after a confirmed refusal. CAPTCHA or login should be handled through the host's normal user-hand-off policy. Changing headers, proxy rotation, exporting cookies, or guessing endpoints is not a maintained fallback. A server-side unattended workflow needs its own verified supported access path; local browser success does not prove it will work.

## Search interaction details

Use current DOM/accessibility observations rather than saved element numbers. Several pages include both a hidden navigation search and a visible main search, so scope locators to the relevant form. The page can implement custom dropdowns over native selects. Submit ordinary Collections filters through the main Search control, but inspect after sorting, Event Database selections or a Programme selection because these can submit/navigate automatically. The underlying select value alone is not proof that filtering ran.

In verification, Collections initially showed 20 cards for a query. Load More eventually expanded this to 40, with the same address. Its first immediate observation still showed 20. Wait for a meaningful new card/count or browser load signal, then inspect; do not repeatedly click while loading. Count visible record cards/links independently from the server's reported total. Follow the actual control for subsequent batches instead of generating page URLs from guesses.

If a control fails to match, take a fresh state and choose the observed control. A button rendered with an icon may have a different accessible name from its plain text. Do not prescribe one exact selector across every section.

## URLs and record identity

Search and view context may be appended to record URLs, including repeated archive segments. Follow actual record links; obtain an unfiltered/canonical link from page metadata or the page's language/share controls when available, then verify it. A working full URL is preferable to an invented shortened URL. Do not strip numeric suffixes from slugs or mistake a display-format parameter for a new record.

Deduplicate only after confirming identity through the record link/identifier and title/context. Alternate languages can represent one catalogue entity but also expose different matches and occasional broken links. Follow working page language links and retain source differences. Keep separate editions, parts, photographs, scans, and related records distinct.

## Original files

Find document/media links on the actual record. Keep the record URL alongside the original-file URL for provenance. A public linked PDF can be read directly with the available PDF reader or downloaded to task scratch space for extraction when permitted. Verify the response is the intended document, not an HTML error, and record pages read. Do not guess file names to obtain material marked Onsite or restricted.

For images, inspect the relevant full image when the claim depends on visual evidence; a thumbnail or caption alone does not suffice. For audiovisual evidence, use the recording or available transcript and record timestamps/sections. Treat transcription, translation, and OCR as additional layers that can introduce errors.

The query workflow does not require submitting access/reproduction forms, subscribing, contacting staff, or changing user accounts. Prepare such next steps only when requested; research authority is not authority to send an application.
