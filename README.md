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
All three scripts, the current prompts, codebook, schema, annotation template,
and tests are imported. Local adjustments are limited to a macOS test-fixture
path and the template's documentation link. The P/D study plan remains the
research direction of this repository.

| Component | Available here |
|---|---|
| Pinned VUL4J-18 preparation | Executable; five source/configuration files, separate references, hashes |
| Prose-report generator | Executable; one direct OpenAI request, stored inputs, raw response, and run metadata |
| P extractor and format validation | Executable; selected report only, exact quotes/offsets, claim IDs and context references |
| Codebook, annotation template, response schema | Imported development baseline; not yet the shared P/D profile |
| Offline regression tests | 29 tests using synthetic fixtures |
| Historical Java-PoV reproduction | Imported protocol; original raw logs are not available here |
| Historical JSPWiki report | Archived finding, request, raw response, prompt, and manifest; consistency verified |
| Manual annotation with 13 claims | Archived accepted development revision; linked to the exact report |
| Previous automatic decomposition runs | Historical summaries only; raw run artifacts are not archived here |
| Shared P/D claim profile, D generator, evaluation | Planned; not implemented |

The six-file development archive is available in every clone; source and import
hashes are documented in [docs/PROVENANCE.md](docs/PROVENANCE.md). Additional old
decomposition runs and PoV logs are optional historical evidence, not prerequisites
for the next step. The repository is ready to refine the claim profile using the
original report and annotation; it is not yet an implemented P/D comparison.

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
  --output data/runs/VUL4J-18-openai-001
```

Both model steps now call the direct OpenAI Chat Completions endpoint and reject
OpenRouter IDs. This imported change removes the old free-model restriction;
live calls can incur costs. No live call was made during the import. Select an
explicit compatible model, preferably a snapshot where available. Model access,
prompts, budgets, and repetitions for the study remain undecided.
`--max-output-tokens` sends `max_completion_tokens`; `--no-reasoning` sends
`reasoning_effort=none`, which requires model support. Without the flag the model
default applies. Requests use JSON mode and `store=false`. The output token limit
is not a monetary budget, and the historical OpenRouter run retains its original
provider and settings.

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

The imported [codebook](resources/claim_codebook.md) and
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
[response schema](resources/claim_response_schema.json). It excludes neighboring
findings, code, reference files, annotations, and the finding ID. The explicit
input JSONL is preserved in full on disk, but other findings are not sent.
Symlinks in the input path or its ancestors are rejected.

The inherited response contract uses `schema_version: "1"`, proposition,
family/subtype/reason, a free-text `qualifiers` field, exact source quotes with
one-based occurrence numbers, and local context IDs. Local validation resolves
quotes to zero-based Unicode-codepoint offsets (exclusive end), validates fields
and references, then adds run/finding IDs and `verification_status: not_evaluated`.
It does not validate granularity, coverage, semantic fidelity, or truth.
Dedicated context, code-reference, and verification-task fields for the shared
P/D profile remain design work; this extraction schema is the starting point.

Outputs include `findings_input.jsonl`, `finding.json`, all three resource
snapshots, `request.json`, `decomposition_raw.json` when received,
`run_manifest.json`, and `validation.json`. `claims.jsonl` exists only after the
whole output validates. An empty result is `no_claims`; invalid output and run
errors are retained without partial claims, repair, or retry. As with the
generator, `completed` means format-valid and `cost_usd` stays `null`.

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
src/                    Preparation, prose-report generation, and P extraction
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
and claim format/quotes/offsets/references. On Windows the symlink test explicitly skips if the privilege is
unavailable. Tests do not establish live API compatibility or research results.

Our code is under [MIT](LICENSE). Downloaded JSPWiki files retain their upstream
licenses and notices. Dataset attribution and pinned revisions are recorded in
[docs/PROVENANCE.md](docs/PROVENANCE.md); third-party material is not relicensed
by this repository.
