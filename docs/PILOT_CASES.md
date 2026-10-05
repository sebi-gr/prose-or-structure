# Pilot selection — source preparation only

Five new cases, two weakness families: two XXE (`CWE-611`) and three path-traversal (`CWE-22`) cases. Purposive feasibility sample for the pilot, not representative evidence or the main evaluation. The existing JSPWiki/Jackson XML/Commons Configuration development cases are excluded.

| Case | Project | Family | Complete files per variant | Vulnerable/fixed input bytes | Local review focus |
|---|---|---|---:|---:|---|
| VUL4J-15 | Apache CXF | CWE-611 | 4 | 33,258 / 33,365 | AtomPojoProvider plus entry/feed inheritance and AbstractAtomProvider parser handling |
| VUL4J-64 | OpenRefine | CWE-611 | 1 | 13,655 / 13,727 | Entire XmlImporter, stream wrapper and XMLInputFactory configuration |
| VUL4J-41 | Plexus Archiver | CWE-22 | 3 | 18,685 / 19,101 | Complete ZipUnArchiver, AbstractZipUnArchiver and AbstractUnArchiver extraction path |
| VUL4J-43 | Eclipse RDF4J | CWE-22 | 2 | 18,518 / 18,888 | Complete ZipUtil entry handling and IOUtil write helper |
| VUL4J-76 | Retrofit | CWE-22 | 2 | 20,669 / 21,830 | ParameterHandler conversion/encoding flag and RequestBuilder URL replacement |

Every input is below 34 KB per variant. No excerpts, omitted middle sections, injected labels, or patched reconstruction. All selected source files keep their original bytes. Case identifiers, variant labels, weakness/CVE labels, tests, patches, license metadata and selection notes are reference/runner metadata, not additional model context.

[`resources/pilot_cases.json`](../resources/pilot_cases.json) contains the pinned dataset URL/hash, five case entries, source URLs/hashes, paired revisions, licenses/notices and available public test-file URLs/hashes. `05_prepare_pilot.py` reconstructs the original sources under `data/pilot_cases/<case>/<variant>/model_input/` and keeps licenses/public benchmark tests in the case's separate `reference/` directory. Additional upstream-parent comparisons and patch inspection were performed during selection; their hashes/results are catalog metadata, not extra model input or files produced by the preparation script. The patch URL/hash is supplemental provenance rather than a raw-source download entry.

## Pair verification

- Both variants have the same relative source-path set within each case. All vulnerable files are from a pinned Vul4J case revision; fixed files are from the corresponding pinned upstream security-fix revision.
- Eleven of the twelve vulnerable source files match the upstream fix parent byte-for-byte. The remaining file, OpenRefine XmlImporter.java, differs only in trailing whitespace on original line 324 (one space in Vul4J versus eight in the upstream parent). That difference is recorded; neither source was normalized or edited.
- Each pair changes exactly the included source file touched by the named security commit; supporting files remain unchanged. The RDF4J commit also reformats the same file and expands documentation; these are upstream patch changes, not benchmark drift.
- Fixed variants control the selected patch; they are not labelled universally safe. For example, Plexus's string-prefix check and RDF4J's canonical-output/destination-path comparison still require exact scope and path assumptions to be assessed.
- GitHub redirects the historic RDF4J and Retrofit repositories to `eclipse-rdf4j/rdf4j` and `lysine-dev/retrofit`. Dataset repo slugs are preserved, canonical aliases recorded, and all raw source URLs name an immutable 40-character commit.
- CXF's dataset patch uses abbreviated `d9e2a6e7`; the resolved full commit is `d9e2a6e7260ea12efa5355ffdfbf0b2415bccd14`.

## Public reproduction material

All five dataset rows declare Maven builds and public failing-test selectors. The named test methods were located in the downloaded test files at the pinned Vul4J snapshots. Plexus's referenced `zip-slip.zip` fixture is also downloaded and hashed. Relevant selectors are recorded in each entry's `public_build_metadata`.

No Maven/Java build, PoV, model invocation or paid API call was run. Downloading a full test source is not a complete build checkout: further test fixtures/dependencies may be needed. Public metadata establishes availability of a reproduction recipe, not successful reproduction here. Reference material must remain excluded from both model routes.

## Context boundaries

CXF's Abdera parser and StaxUtils implementation are absent; a call to a hardened helper is not proof of its internal behavior. OpenRefine's actual XML provider and wider caller/deployment context are absent. Plexus omits external FileUtils/archive internals. RDF4J omits external callers and effective destination/runtime setup. Retrofit omits OkHttp internals, real API declarations and server authorization. All five omit actual attacker reachability, authentication and deployed permissions; concrete unresolved questions belong in the code reference rather than being filled from CVE labels.

These are deliberately bounded code-review contexts. A subsequent pilot can expose whether they contain enough information for the selected questions and quantify missing-context problems. Do not expand only one route's context or consult fixes while constructing model claims.

## Split exclusions

Exclude every selected project's cases/variants from future holdout, including both old and canonical GitHub names. Together with development exclusions, this removes the following current dataset IDs: **9, 15, 16, 18, 41, 43, 46, 47, 64, 65, 76**. The project list is stored in `future_holdout_excluded_projects`; future dataset additions from these same projects must also be excluded. No held-out claims or annotations have been inspected or generated.

Source licensing: CXF, Plexus and Retrofit carry Apache-2.0 notices/licenses; OpenRefine uses its Google-copyright BSD three-clause license; RDF4J's selected files use Eclipse Distribution License 1.0. Original headers remain in the full files. CXF's source tree contains a distribution license template and appended notice, not a rendered full license; a separately pinned, unmodified Apache-2.0 license text is supplied from Apache Commons Configuration with this origin stated explicitly. This license text does not import that development project's code into the pilot.
