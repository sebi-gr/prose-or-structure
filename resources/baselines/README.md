# General extraction baselines

`veriscore_extraction_non_qa.txt` and `VERISCORE_LICENSE` are unchanged files from
[Yixiao-Song/VeriScore](https://github.com/Yixiao-Song/VeriScore), pinned in
`provenance.json`. The original prompt is licensed under Apache-2.0. No upstream
Python package, retrieval, verification or fine-tuned model is used.

The implementation in `src/extraction_baselines.py` is a **VeriScore-based
extraction baseline**, not an exact reproduction of the complete published
method. It uses the original Non-QA prompt and examples with these adaptations:

- A small deterministic regex replaces spaCy sentence segmentation. It splits
  at whitespace after `.`, `!` or `?`, and at line breaks. Abbreviations such as
  `e.g.` can split incorrectly; preserved offsets make this inspectable. Both
  baselines use the same splitter, frozen before comparison runs.
- Every original title and report sentence is an extraction target once, so
  statements occurring only in a title are retained for both baselines. Report
  targets receive the complete title as labeled context; title targets receive
  the complete report as labeled context. No synthetic assembly headers are added
  as extraction targets. Treating titles separately is our adaptation.
- Each field's window contains up to three preceding sentences, the marked target
  and one following sentence. For fields with more than five sentences the first
  sentence is additionally prepended, following the upstream scanner. Windows do
  do not cross field or finding boundaries. Line/paragraph splitting uses the regex rule above.
- The same explicitly selected OpenAI model is used, with `reasoning_effort=none`,
  no tools, retries or repairs. Text completion is retained: no JSON response
  format or security profile is added to the upstream prompt.
- Parsing accepts only nonempty `- ` bullet lines, or the exact standalone
  `No verifiable claim.` sentinel. Unexpected prose, mixed sentinels, malformed
  bullets and truncated/refused responses are invalid, not empty extractions.
  Identical strings are deduplicated within a finding, with all target sentence
  IDs retained; no semantic deduplication or deletion of `Note:` text is applied.

The upstream exclusion of hypothetical content remains in force. Its effect on
modal security statements is a property to measure, not a reason to silently
rewrite the baseline. A target sentence is provenance for the extraction call,
not a verified supporting quotation for each generated proposition. Baseline
output does not invent the profile's families, qualifiers or verification tasks.

`sentence_claims.jsonl` contains original title/report substrings with zero-based
Unicode offsets and an exclusive end. `veriscore_claims.jsonl` is written only
after every planned extraction succeeds (including valid empty extractions).
On an API/key/output failure, the sentence baseline and all attempted requests,
raw responses and call manifests remain available; the remaining calls stop.
A completed empty parent review produces two empty output files and no API call.

The parent review is validated with `review_pair`; only its title/report text is
sent. Parent artifact hashes, resource snapshots, code hashes, actual parameters,
usage and duration are saved. Costs remain `null` without an accounting source.
These baselines measure report decomposition; they do not verify code truth.
