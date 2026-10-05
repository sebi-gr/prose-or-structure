# Prose or Structure?

**Evaluating Security-Claim Generation in LLM-Based Code Analysis**

Research prototype comparing two routes from the same source-code context to
security claims in a shared format:

- **P — report first:** code → prose report → extracted claims.
- **D — direct:** code → structured claims.

The study compares code grounding, relevant coverage, preserved conditions and
uncertainty, checkability, and effort. Report fidelity is an additional metric
for P. A faithfully extracted claim can still be factually wrong. Neither route
is assumed to be better.

The [project sketch](prose_or_structure_projektskizze.pdf), version 0.1 dated
2026-10-03, defines the proposed research direction. This is a study of claim
generation and representation, with no general verification platform planned.

## Research questions

1. **Claim profile:** What context and relationships make security claims
   interpretable and usable as inputs to verification tasks?
2. **Generation route:** How do P and D differ in grounding, relevant coverage,
   conditions, and effort under a paired comparison?
3. **Representation errors:** Which errors change the resulting verification
   task, and do explicit context fields reduce them?

JSPWiki / **VUL4J-18** is a development case. The proposed pilot uses the same
five to ten code cases for both routes, followed by a separately held-out main
study whose size is determined after the pilot. Claims from one case are not
independent samples. Repaired variants control the specific vulnerability;
they are not automatically safe programs.

## Current state

The reusable baseline comes from
[What Can We Verify? at `5df7760`](https://github.com/sebi-gr/What-Can-We-Verify/tree/5df7760459b741ae36bd91af4af89f6e3ecfe18d).
The import record preserves the original hashes. The current code extends that
baseline with the shared profile and a direct route for the JSPWiki development
case. Preparation and the existing API transport are reused.

| Component | Available here |
|---|---|
| Pinned VUL4J-18 preparation | Five source/configuration files, separate references, hashes |
| Prose-report generator | One request, preserved inputs/response, run and variant metadata |
| P extractor | One selected saved finding; profile 0.1, exact quote offsets, no code in its request |
| D generator | Direct profile 0.1 claims from the verified identical P source context |
| Shared validation | Fields, conditions, local IDs, quotes; nonfatal D code-location diagnostics |
| Pairing checks | Original review artifacts checked; source hashes and actual sent code context must match |
| Offline regression tests | 60 tests with synthetic responses and archived development fixtures |
| Historical JSPWiki report and annotation | Six immutable originals, including the accepted 13-claim revision |
| Pilot, D revision control, baselines, ablation, evaluation | Planned; no comparison results yet |

Steps 2 and 3 are complete for the small development PoC. The next step is to
fix the pilot protocol before live comparison runs. No new model request or
Java/PoV run was made during implementation. Additional old decomposition/PoV
logs remain optional; [provenance](docs/PROVENANCE.md) records the available evidence.

## Shared profile and annotation

[Claim profile 0.1](resources/claim_profile.md) defines the common P/D contract
and its [JSON Schema](resources/claim_profile.schema.json). It separates the
proposition, explicit conditions, provenance and a derived verification question.
Missing information, explicit negation and stated uncertainty remain distinct.
The [annotation protocol](resources/annotation_protocol.md) separates P report
fidelity from code grounding and defines semantic coverage and adjudication.

The [development walkthrough](resources/profile_development/README.md) covers
JSPWiki, Jackson XML (VUL4J-47) and Commons Configuration YAML (VUL4J-9), with
pinned source fixtures and ten selected profile claims. These are AI-assisted
editorial examples, not model outputs, independent human ground truth or new
PoV executions. All three cases remain development data. Case-specific references
and examples must never be injected into generation prompts.

Both claim scripts now use profile 0.1. The old P response schema was replaced;
its history and old run snapshots remain unchanged. There is one active profile
and no automatic conversion of old claims.

## Start here

Read [HANDOFF.md](HANDOFF.md) for the verified state and
[WORKPLAN.md](WORKPLAN.md) for the next step and acceptance criteria.
[AGENTS.md](AGENTS.md) contains development and experimental rules.

Run from the repository root with **Python 3.9+**. The existing scripts use only
the standard library; no package installation is required.

```bash
python3 -m unittest -v
python3 src/01_prepare_case.py --help
python3 src/02_generate_findings.py --help
python3 src/03_decompose_findings.py --help
python3 src/04_generate_claims.py --help
```

Prepare the development case with internet access to `raw.githubusercontent.com`:

```bash
python3 src/01_prepare_case.py
```

This creates `data/VUL4J-18/` and refuses existing output directories. Use
`--output data/VUL4J-18-copy` for a separate export. Java and Maven are not needed
for preparation, and this command does not run the PoV.

| Output | Purpose |
|---|---|
| `model_input/` | Five full, unchanged source/configuration files with original paths |
| `reference/vul4j_row.json` | Benchmark metadata and build/test commands |
| `reference/fixed/`, `reference/pov/` | Upstream fixed file and benchmark PoV |
| `reference/LICENSE`, `reference/NOTICE` | Upstream licensing and attribution |
| `manifest.json` | Pinned sources, SHA-256 hashes, and `pov_status: not_run` |

Only `model_input/` belongs in a code-analysis model's context. References,
manifest, project documentation, patches, PoVs, and benchmark labels do not.
The implemented generator reads only its five allowlisted files, without agent
tools. The P extractor receives only the selected title/report as case material,
plus its schema/codebook instructions; it does not inspect the source code.

The five files are `WikiServlet.java`, `DefaultURLConstructor.java`,
`URLConstructor.java`, `jspwiki.properties`, and `web.xml`, at the paths fixed in
`src/01_prepare_case.py`. This is a selected context, not a runnable checkout or
a whole-repository scan. Missing filters, other constructors, `WikiEngine`, and
deployment settings limit the claims it can justify. Source configuration is
not evidence of a running deployment.

## Optional prose-report run

The inherited generator implements only the first stage of P. It is currently
specific to VUL4J-18; `--model-input` changes the directory, not the case ID or
file allowlist. It is not yet a multi-case study runner.

For a deliberately planned run, create a local `.env` from the blank
[.env.example](.env.example) and set `OPENAI_API_KEY` there. A nonempty process
environment variable takes precedence. The file is ignored by Git. The loader
accepts a simple optionally quoted value, with no inline comments or expansion.

After selecting a currently available model and an explicit token limit, replace
the placeholders below. This is a command template, not a selected study model:

```bash
python3 src/02_generate_findings.py \
  --model OPENAI_MODEL_ID \
  --max-output-tokens TOKEN_LIMIT \
  --case-variant vulnerable \
  --output data/runs/VUL4J-18-openai-001
```

All model steps call the direct OpenAI Chat Completions endpoint and reject
OpenRouter IDs. This imported change removes the old free-model restriction;
live calls can incur costs. No live call was made during the import. Select an
explicit compatible model, preferably a snapshot where available. Model access,
prompts, budgets, and repetitions for the study remain undecided.
`--max-output-tokens` sends `max_completion_tokens`; `--no-reasoning` sends
`reasoning_effort=none`, which requires model support. Without the flag the model
default applies. Requests use JSON mode and `store=false`. The output token limit
is not a monetary budget, and the historical OpenRouter run retains its original
provider and settings.

`--case-variant` records an explicit provenance label, never model context or a
truth judgment. It defaults to `unspecified`; inherited runs without the field
keep that value rather than gaining an inferred label.

One request is made with a 180-second timeout and no automatic retry, repair,
follow-up, or tools. The prompt requests a JSON envelope containing titles and
prose reports; this is not a structured-claim output. Input files are stored
unchanged; the sent view adds paths and original one-based line numbers.

| Run artifact | Contents |
|---|---|
| `model_input/`, `review_prompt.txt` | Exact source and prompt bytes |
| `request.json` | Request body, without the authorization header |
| `generation_raw.json` | Unmodified response bytes, when received |
| `findings.jsonl` | Validated titles/reports with run-scoped IDs, without text correction |
| `run_manifest.json` | IDs, model/provider, parameters, hashes, usage, duration, status, and errors |

`completed` means structurally valid findings, not true claims. `no_findings`
retains an empty JSONL file. Invalid or incomplete responses yield
`invalid_output`; request/provider/key failures yield `run_error`. Neither error
status creates findings. Started runs remain on disk; a forcibly interrupted
process can leave `running`. Existing output is never overwritten. Provider
usage is preserved; `cost_usd` remains `null` because billing is not calculated.

## Manual annotation and automatic extraction

The refined [codebook](resources/claim_codebook.md) and
[annotation template](resources/manual_annotation_template.md) provide the
development rules for faithful extraction. Copy the template into a new file
under `data/annotations/` for new manual work. The accepted historical
[annotation with 13 claims](data/annotations/VUL4J-18-review-001/manual_annotation_001.md)
and its exact [finding](data/runs/VUL4J-18-review-001/findings.jsonl) are now archived.
Keep this original annotation unchanged; new revisions need a new file.

The annotation records assisted development work with prior knowledge of
code/fix/PoV, not an independent truth reference. Its embedded original report,
finding hash, 13 claim IDs, 15 source quotes, and context references have been
checked. The historical codebook v0.2 and separate revision notes it names were
not supplied; today's codebook does not substitute for that old snapshot.
Keep exact quotes, conditions, uncertainty, and claim relationships. A sentence
can support several distinct propositions; do not enforce a target claim count.

`src/03_decompose_findings.py` can extract one finding from a saved generator
JSONL file. The following template uses the archived report; select the model
and token limit and a fresh output directory. A new report is unnecessary:

```bash
python3 src/03_decompose_findings.py \
  --findings data/runs/VUL4J-18-review-001/findings.jsonl \
  --finding-id 0721c0a0-bba7-48c1-a63c-da196a69d97c:F001 \
  --model OPENAI_MODEL_ID \
  --max-output-tokens TOKEN_LIMIT \
  --output data/decompositions/VUL4J-18-openai-001
```

The request includes only the selected title/report,
[decomposition prompt](resources/decomposition_prompt.txt), codebook, and
[shared response schema](resources/claim_profile.schema.json). It excludes neighboring
findings, code, reference files, annotations, and the finding ID. The explicit
input JSONL is preserved in full on disk, but other findings are not sent.
Symlinks in the input path or its ancestors are rejected.

P requires the associated `run_manifest.json`, `request.json` and
`generation_raw.json` beside the findings file. Before any request, it checks
original hashes and that the finding text/IDs match the recorded response.
These artifacts provide local provenance; their source text, review prompt,
metadata and other findings are not sent to the extractor.

The common response has `profile_version: "0.1"`, `route: "P"` or `"D"`, and
`claims`. Every claim contains the proposition, provisional family/subtype/reason,
six explicit context fields, report quotes, code references, context IDs and a
separate verification question/evidence requirements/assumptions. A small shared
stdlib validator enforces the fixed contract; no JSON Schema runtime is needed.
P quotes resolve to zero-based Unicode-codepoint offsets with an exclusive end.
The saved JSONL adds route/run/profile metadata and, for P, finding ID and offsets.
No truth status is generated. Format validity does not establish claim truth.

P saves `findings_input.jsonl`, `finding.json`, `review_manifest.json`, resource
snapshots, request, raw response when received, manifest and validation result.
`claims.jsonl` appears only after the entire response validates. Empty output is
`no_claims`; malformed output is `invalid_output`; request/setup failures are
`run_error`. There are no partial claims, repair calls or retries.

## Direct claims on the same context

Prepare the five source files first. Then the D command can use the archived
review as its context anchor; replace model/budget placeholders before a live run:

```bash
python3 src/04_generate_claims.py \
  --model-input data/VUL4J-18/model_input \
  --review-run data/runs/VUL4J-18-review-001 \
  --model OPENAI_MODEL_ID \
  --max-output-tokens TOKEN_LIMIT \
  --output data/direct/VUL4J-18-openai-001
```

D checks all five source hashes against the saved review and reconstructs the
exact numbered user message that P's report generator received. A mismatch stops
before an output directory or API request is created. Extra files are excluded
by the same fixed allowlist. The D request contains only these source bytes in
the numbered view plus its generic prompt, codebook and shared response schema;
it contains no prose report, findings, fix, reference annotation or manifest.

D stores its source/resource snapshots, `review_manifest.json`, request,
`generation_raw.json`, manifest, validation and validated claims. Both routes
record case/variant, route/stage, run IDs, profile/codebook versions and resource
hashes, source/input hashes, model/parameters, timing and reported usage. P links
its report as `parent_run_id`; both use `paired_review_run_id` to identify the
same context anchor. D has no causal report parent. Billing is not computed:
`cost_usd` remains null and provider usage is retained.

D's `validation.json` includes `code_ref_checks`: `resolved`, `unresolved_path`,
`out_of_range`, or `no_position`. These are nonfatal diagnostics. Claims with
incorrect source locations remain available for annotation, as do incorrect
locations quoted by P. A resolved range proves neither a symbol nor a claim.
P does not inspect code to validate claimed positions.

This is a development pairing, not a retrospective controlled experiment with
the old OpenRouter model. Current extraction operates **per finding**: P uses
one report call plus one extraction call for each of its N findings (**1 + N**);
D uses one call for the whole code context. The archived case has one finding,
matching the sketch's two-call P route. All findings must be included in any
case-level comparison. Before the pilot, fix the report unit to preserve the
proposed two-call design or explicitly account for additional extraction calls;
do not select only convenient findings. A review with `no_findings` needs no
P extraction and can still anchor D. A failed review cannot currently anchor D;
the pilot must predefine missing-route handling.

The scripts remain specific to VUL4J-18. The XML/YAML development examples are
not additional executable cases. D revision/budget control, baseline extraction,
context-field ablation and study-level aggregation belong to pilot preparation.

## Evidence and reproducibility

The imported [PoV protocol](resources/reproduce_vul4j18.md) records successful
builds and two expected assertion failures on the vulnerable variant versus
two passes on the fixed variant, on Windows on 2026-09-23. This is a historical
record, not a fresh execution in this repository; its `data/pov/` paths refer to
the original workspace. The underlying tests cover mocked forwarding behavior,
not arbitrary file reads or unauthenticated end-to-end exploitation.

The preparation manifest's `pov_status: not_run` describes the export step.
Keep reproduction evidence separately; do not change that field merely because
an earlier reproduction is documented elsewhere.

Six selected historical files are versioned under `data/runs/VUL4J-18-review-001/`
and `data/annotations/VUL4J-18-review-001/`, totaling about 108 KB. The run is an
OpenRouter/Nemotron development run, despite today's direct OpenAI implementation.
Its original `review_prompt_v1.txt` name remains. The prompt's CRLF bytes were
recovered from the archived request and match the historical manifest hash;
the other five delivered files are unchanged. `.gitattributes` disables newline
conversion for this archive.

The run's `model_input/` copy is intentionally omitted. Preparation regenerates
the five source files; their hashes and the reconstructed request text match the
archive. New outputs, case downloads, Java checkouts, toolchains, and caches stay
ignored. The Python preparation downloads the PoV source but does not execute it;
a fresh Java reproduction requires the full benchmark and separate setup.
Old decomposition/PoV logs are optional for continuing this development case.
Choose the main study's data archive before evaluation. No live model request or
Java reproduction was performed during this import.

## Repository layout and checks

```text
src/                    Preparation, P/D scripts, shared profile and pairing checks
tests/                  Offline tests; responses are synthetic
resources/              Prompts, codebook, schema, template, PoV protocol, checksums
docs/PROVENANCE.md      Import sources, evidence inventory, and verification limits
.github/workflows/      Offline checks on pushes and pull requests
data/                   Six archived originals; all other outputs ignored
```

```bash
python3 -m unittest -v
git diff --check
```

The tests cover reference isolation, preserved bytes and hashes, overwrite
protection, failure handling, model-ID checks, `.env` loading, reasoning control,
shared profile fields/quotes/offsets/references, identical P/D source context,
parent-artifact integrity and nonfatal code-location diagnostics. On Windows the symlink test explicitly skips if the privilege is
unavailable. Tests do not establish live API compatibility or research results.

Our code is under [MIT](LICENSE). Curated XML/YAML source fixtures retain their
Apache 2.0 licenses and notices under `resources/profile_development/`.
Downloaded JSPWiki files retain their upstream
licenses and notices. Dataset attribution and pinned revisions are recorded in
[docs/PROVENANCE.md](docs/PROVENANCE.md); third-party material is not relicensed
by this repository.
