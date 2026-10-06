# Reading original documents and audiovisual material

Use this guide when an answer depends on an original file or recording. Catalogue descriptions help discover material; they do not replace inspection of the relevant pages, images, or passage. The examples below were checked on 6 October 2026 and should be reopened when used in a new task.

## Scans, existing text layers, and OCR

1. On the live item, identify its access label and the publicly linked document. Keep both the record URL and attachment URL. Verify the retrieved file is a PDF with the expected title/content, rather than an HTML error or an unrelated preview.
2. Establish the actual file's page count. Extract embedded text if available, but inspect a rendered relevant page before deciding the text is trustworthy. A large amount of extractable text can still be damaged OCR. Watch for missing names, merged columns, broken dates, upside-down fax headers, and text ordered differently from the page.
3. If extraction is missing or poor, render the relevant pages at a readable resolution and use an available OCR engine with the correct language model. A typical local route is a PDF renderer such as Poppler followed by Tesseract; an integrated visual PDF reader is also suitable. Keep the source PDF unchanged and put derived text/images in task scratch space.
4. Compare OCR against the image for every name, number, date, and passage that supports the answer. An additional OCR pass is a candidate reading, not a correction by authority. If a critical word remains uncertain, quote only the clear portion or mark the uncertainty. Do not silently reconstruct illegible wording from expectation.
5. Cite the page actually inspected. Distinguish the PDF viewer's ordinal from a printed page number; use “PDF p. 1, unnumbered fax sheet” when appropriate. Record the pages read, not merely the document's total length.

For a short scan, direct visual reading may be faster and more reliable than OCR. For a long scan, OCR can locate candidate pages, followed by visual checks. If the required language model is absent, use a capable visual reader or explicitly limit the reading; an English OCR model does not validate Chinese text. Avoid promises of complete transcription from a partial visual sample.

### Verified scan example

[Letter from Suhanya Raffel to Gulammohammed Sheikh, 4 June 1998](https://aaa.org.hk/en/collections/search/archive/gulammohammed-sheikh-archive-curation-by-gulammohammed-sheikh/object/letter-from-suhanya-raffel-to-gulammohammed-sheikh-4-june-1998) was marked Online and linked a [one-page scanned fax](https://cdn.aaa.org.hk/_source/digital_collection/windows/k.s.chithra/20140518_013408_0.pdf).

The PDF had an existing text layer with substantial errors. The embedded extraction rendered the date as `416/98`; a fresh English OCR pass rendered it as `4GISS`. Visual inspection of PDF page 1 showed `4/6/98`, consistent with the catalogue title. The body discusses curatorial selection and requests for proposals; these are preparatory statements, not a final participant list.

The fax header indicates a three-page transmission including its cover, while the accessible PDF contains one page. The body mentions attachments. Report the accessible extent and this discrepancy; do not invent missing attachments or treat the file as the whole transmission. The test covered that one page and demonstrated OCR plus visual correction on a poor-text scan.

### Verified Chinese scan and OCR limitation

[Gaylord Chan Takes Art as Shelter](https://aaa.org.hk/en/collections/search/archive/ha-bik-chuen-archive/object/gaylord-chan-takes-art-as-shelter) linked a [one-page traditional-Chinese newspaper scan](https://cdn.aaa.org.hk/_source/hbc15775.pdf). Its embedded-text extraction produced only a page-break character, confirming that this file supplied no usable text layer. The catalogue dates the Wen Wei Po clipping to 10 April 1989.

The existing macOS Vision OCR engine, revision 3, advertised traditional-Chinese support. A local test with that language and English recovered some horizontal title/caption/byline text, but misread characters in the headline and did not recover the vertical article body. A cropped-body retry still produced no useful text. Language support alone therefore did not establish adequate recognition for this layout.

Visual reading of PDF page 1 confirmed the headline and the byline, 杜藍. A magnified passage under the lower section about transparent painting describes repainting a canvas while traces of earlier layers remain visible. This is a **manual visual reading of a bounded passage**, not successful automatic transcription of the article. Preserve the right-to-left ordering of vertical columns when quoting or transcribing such material; identify columns or a section heading in addition to the PDF page.

## Video, audio, subtitles, and transcripts

1. Resolve the exact version. An edited interview, full recording, selected transcript, full transcript, and translated transcript can be separate records with different access or rights labels. Follow sibling records and the parent folder when necessary; titles alone can obscure the distinction.
2. Inspect the visible player. Start playback through its normal controls and verify meaningful progress, a loaded duration, or a rendered frame. An available Play button or poster image alone does not prove playback works. If supported, read-only player state can confirm current time and duration; use the UI for seeking and playback changes.
3. For a content claim, examine the relevant bounded passage. Record whether the evidence was heard, visually observed, read as subtitles, or read in a transcript. A machine without audio perception must not claim to have listened merely because playback ran.
4. Check for captions or a linked transcript. Empty machine-readable subtitle tracks do not establish that a video has no subtitles: they may be embedded in the picture. Screenshots can support reading a sampled subtitled frame. A corresponding transcript offers searchable text, but must be identified by language and version.
5. Cite actual timestamps for observations from the recording and actual pages for transcript-based statements. Do not assign a transcript statement a timestamp by guess. For sampled frames, say they were sampled; do not describe the interval between them as continuously watched.
6. When comparing translated subtitles and transcript text, confirm meaning at the needed passage. Do not infer complete alignment, verbatim equivalence, or translation accuracy from a matching sample. Spoken-language and written-language metadata can legitimately differ.

If an embedded player fails, follow an official external recording/transcript link actually exposed on the page. If no readable alternative works, report the playable/readable evidence boundary. Do not guess asset names for onsite or restricted items, submit access forms as part of reading, or download remote audiovisual media solely to evade display limitations.

### Audio-derived transcription when needed

For a question that needs the spoken content, first check for an available audio-capable tool or existing local ASR runtime. A transcript or subtitles should not be relabelled as audio analysis. When permitted, process only a relevant short interval from the public player source actually observed on the page; record its offset and duration. Do not save the full recording merely to transcribe a short passage.

A tested local route used FFmpeg to extract a 15-second mono, 16 kHz audio clip and [faster-whisper](https://github.com/SYSTRAN/faster-whisper) with its multilingual base model, CPU int8. The runtime and approximately 145 MB model were placed in task scratch space, not bundled with this skill. Check existing tools first; this example is not a requirement to install this stack on every host. A host without an audio-capable tool should retain the transcript/subtitle boundary instead of inventing auditory verification.

For an independent comparison, give ASR the audio without the official transcript as a prompt. Use transcription rather than translation, choose a supported language setting, retain raw output, and add the clip's start offset to relative timestamps. Compare the result with the official text afterwards. Catalogue language, ASR language code, output language, and translation status belong in the evidence record. Model timestamps and spellings need checking before they support precise claims.

### Verified interview example

[Interview: Sunny Pang](https://aaa.org.hk/en/collections/search/archive/out-of-context-research-project-interview-11441/object/interview-sunny-pang) was Online, described a Cantonese interview conducted on 4 December 2017, and exposed a working embedded player. Its observed duration was 12:39.04. Playback started and advanced; frames sampled at approximately 00:36.33 and 00:46.33 contained Chinese and English subtitles even though no separate subtitle tracks appeared in the player state.

The [English transcript record](https://aaa.org.hk/en/collections/search/archive/out-of-context-research-project-pang-kamyiu-sunny/object/interview-sunny-pang-transcript) linked a [three-page PDF](https://cdn.aaa.org.hk/_source/ex-final-eng-sunny-pang-interview-transcription.pdf). Printed/PDF page 1 was visually checked against extracted text. Its opening account of collaboration among artistic disciplines agrees with the sampled subtitles. This comparison alone does not establish completeness or verify the spoken audio.

A separate follow-up actually transcribed audio from 00:36 to 00:51 of the public player source. Faster-whisper 1.2.1 with the multilingual base model and `language="zh"`, `task="transcribe"` produced Chinese text without a reference-text prompt. It recovered the sense of different artists sharing a working environment and opportunities, consistent with the sampled subtitles and transcript page 1. It also misrecognised a phrase: the ASR produced 街壁 where the visible Chinese subtitle used 界別. This is a limited audio-derived machine transcription, not a faithful Cantonese verbatim transcript or a human listening check. The broad Chinese language setting does not establish dialect-specific accuracy, and the English PDF is a translation to compare by meaning. Numerical warnings occurred during feature extraction; a follow-up check found finite audio and feature arrays. Retain that diagnostic qualification rather than treating the model output as error-free.

The separately linked [full video](https://aaa.org.hk/en/collections/search/archive/out-of-context-research-project-interview-11441/archive/out-of-context-research-project-interview-11441/object/interview-sunny-pang-full-version) was explicitly Onsite. Its contents were not accessed. The online video displayed CC BY-NC-ND 4.0, while the transcript displayed In Copyright. Preserve each record's actual label rather than transferring one version's conditions to another. Onsite and restricted are distinct labels: report whichever the specific record states and follow its current instructions if a later access request is authorised.

## Evidence to retain

For each substantive media claim, keep: record and attachment links; exact version/language; access and rights labels; actual page count or observed player duration; page/time scope inspected; reading method; OCR/transcription uncertainties; and the claim supported. Expose only what helps the user's question.

The verified baseline includes English scan OCR with visual checking; an image-only Chinese clipping with a limited OCR attempt and successful bounded manual reading; a readable English transcript; working video playback and sampled bilingual subtitles; and audio-derived ASR for a 15-second Cantonese passage. It does **not** establish accurate general Cantonese transcription, reliable vertical-Chinese OCR, human auditory review, complete-recording coverage, handwriting recognition, or access to restricted originals. Verify those capabilities when a task requires them.
