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
[What Can We Verify? at `8f9b25e`](https://github.com/sebi-gr/What-Can-We-Verify/tree/8f9b25e1d5d53208f6f58dba9ffba8396a68dd5c).
The implementation, prompt, and tests are unchanged. The original research plan
has been replaced with the P/D study plan.

| Component | Available here |
|---|---|
| Pinned VUL4J-18 preparation | Executable; five source/configuration files, separate references, hashes |
| Prose-report generator | Executable; one OpenRouter request, stored inputs, raw response, and run metadata |
| Offline regression tests | 15 tests using synthetic fixtures |
| Historical Java-PoV reproduction | Imported protocol; original raw logs are not available here |
| Historical JSPWiki report | Described in the source repository; original run artifacts are not available here |
| 13 manual claims and first codebook | Mentioned in the sketch; original files are not available here |
| Shared claim schema, P extractor, D generator, evaluation | Planned; not implemented |

Missing originals are tracked in [docs/PROVENANCE.md](docs/PROVENANCE.md). They
must not be reconstructed from summaries and presented as historical evidence.
The repository is ready for development; it is not yet a complete experimental
dataset or an implemented P/D comparison.

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
tools. Future P extraction must receive only the report as case material, plus
its generic schema/codebook instructions; it must not inspect the source code.

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
[.env.example](.env.example) and set `OPENROUTER_API_KEY` there. A nonempty process
environment variable takes precedence. The file is ignored by Git. The loader
accepts a simple optionally quoted value, with no inline comments or expansion.

After selecting a currently available model and an explicit token limit, replace
the placeholders below. This is a command template, not a selected study model:

```bash
python3 src/02_generate_findings.py \
  --model 'PROVIDER/MODEL:free' \
  --max-output-tokens TOKEN_LIMIT \
  --output data/runs/VUL4J-18-review-001
```

The script accepts only explicit `:free` IDs, requests zero provider price
ceilings, and disables fallbacks. No current model availability is guaranteed.
Model IDs need not identify immutable revisions. Model, provider, reasoning
mode, prompts, budgets, and repetitions for the new study remain undecided.
`--no-reasoning` explicitly sends `reasoning.enabled=false`; without it, the
provider default applies. It changes the experimental condition and must not be
silently selected from the old proof of concept. The output token limit is not
a monetary budget.

One request is made with a 180-second timeout and no automatic retry, repair,
follow-up, or tools. The prompt requests a JSON envelope containing titles and
prose reports; this is not a structured-claim output. Input files are stored
unchanged; the sent view adds paths and original one-based line numbers.

| Run artifact | Contents |
|---|---|
| `model_input/`, `review_prompt_v1.txt` | Exact source and prompt bytes |
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

Generated cases, runs, annotations, and raw logs stay under ignored `data/`.
A fresh clone contains the scripts and documentation, not those artifacts.
An archival location for the study data must be selected before evaluation.
No live model request or Java reproduction is needed for the repository setup.

## Repository layout and checks

```text
src/                    Existing preparation and prose-report scripts
tests/                  Offline tests; responses are synthetic
resources/              Review prompt, historical PoV protocol, import checksums
docs/PROVENANCE.md      Import source, evidence inventory, and missing originals
.github/workflows/      Offline checks on pushes and pull requests
data/                   Local artifacts, ignored by Git
```

```bash
python3 -m unittest -v
git diff --check
```

The tests cover reference isolation, preserved bytes and hashes, overwrite
protection, failure handling, model restrictions, `.env` loading, and reasoning
control. On Windows the symlink test explicitly skips if the privilege is
unavailable. Tests do not establish live API compatibility or research results.

Our code is under [MIT](LICENSE). Downloaded JSPWiki files retain their upstream
licenses and notices. Dataset attribution and pinned revisions are recorded in
[docs/PROVENANCE.md](docs/PROVENANCE.md); third-party material is not relicensed
by this repository.
