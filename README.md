# Prose or Structure?

**Evaluating Security-Claim Generation in LLM-Based Code Analysis**

Small research prototype comparing **P: code → prose report → claims** with
**D: code → claims**, using identical code context and one shared claim profile.
We study grounding, relevant coverage, preserved conditions, checkability and
effort; report fidelity is an additional P metric. Neither route is assumed better.
A faithfully extracted report claim can still be false.

The [project sketch](prose_or_structure_projektskizze.pdf), dated 2026-10-03,
defines RQ1 (profile), RQ2 (paired comparison) and RQ3 (representation errors and
context fields). This is a research PoC, not a general verification platform.
Read [WORKPLAN.md](WORKPLAN.md), [HANDOFF.md](HANDOFF.md) and [AGENTS.md](AGENTS.md).

## Current state

Steps 2–3 are implemented; step 4 has an executable pilot protocol, source
preparation, complete P/D routes, controls and human-reference worksheets.
**No new live model results, human pilot annotations or Java/PoV reproductions yet.**
API access and a user-selected spending ceiling are still needed. Main-study
planning depends on the annotated pilot, not merely successful API calls.

| Script | Purpose |
|---|---|
| `01_prepare_case.py` | Original pinned VUL4J-18 development source export |
| `02_generate_findings.py` | Code → prose findings, explicit registered case/variant |
| `03_decompose_findings.py` | Saved finding or complete report (`--finding-id all`) → P claims |
| `04_generate_claims.py` | Code → D claims; optional one-step revision |
| `05_prepare_pilot.py` | Five cases, both variants, pinned sources and separate references |
| `06_run_pilot.py` | Dry-run by default; fixed paired plan and budget-guarded execution |
| `07_prepare_annotations.py` | Neutral code packets and blank human reference worksheets |

Common helpers validate the fixed profile, original report provenance, case
allowlists, the narrow context-field ablation and extraction baselines. Python
**3.9+**, standard library only. No package installation, Java or Maven needed
for preparation or offline tests.

## Prepare the pilot without API access

```bash
python3 -m unittest -v
python3 src/05_prepare_pilot.py --output data/pilot_cases
python3 src/06_run_pilot.py --cases data/pilot_cases --output data/pilot/preflight-001
python3 src/07_prepare_annotations.py --cases data/pilot_cases --output data/annotations/pilot-001
```

Each command requires a fresh output path; existing data is never overwritten.
Preparation downloads fixed public GitHub revisions. The dry-run validates all
sources and saves the ordered plan, contexts, budgets and hashes without calling
a model. Prepared sources, runs and annotation packets are ignored by Git.

[Pilot protocol 0.1](docs/PILOT_PROTOCOL.md) fixes five cases, two weakness families,
both vulnerable/fixed variants, two repetitions, balanced P/D order, D revision,
and four-context subsets for both-route ablation and extraction baselines.
[Case selection](docs/PILOT_CASES.md) explains scope, missing context and licenses;
[the catalog](resources/pilot_cases.json) records exact sources and hashes.
All development/pilot projects are excluded from future holdout. Fixed variants
control the specific patch, not whole-program security.

Only registered `model_input/` files are read for generation. References, CVEs,
variant labels, tests, patches and annotations are not model inputs. Both routes
receive the same unchanged bytes with original paths and line numbers. P extraction
receives only report material plus generic instructions, schema and codebook.
No tools or reference browsing are available to the models.

## Planned live execution

Set `OPENAI_API_KEY` in your process environment or local `.env`, following
[.env.example](.env.example). The environment takes precedence; `.env` is ignored.
Do not commit or paste credentials into repository documentation.

The selected pilot snapshot is `gpt-5.4-mini-2026-03-17`, reasoning `none`, default
service tier. Limits and dated pricing are in [pilot_config.json](resources/pilot_config.json).
Model access and live compatibility remain untested. Verify pricing before a later
live start. After choosing a USD ceiling, replace `APPROVED_USD_LIMIT`:

```bash
python3 src/06_run_pilot.py \
  --cases data/pilot_cases \
  --output data/pilot/live-001 \
  --execute --budget-usd APPROVED_USD_LIMIT
```

The runner reserves a conservative full-call cost before every request. Its
`budget_ledger.json` records reservations and usage-based cost estimates, not
billing invoices. It stops before exceeding its ceiling and after uncertain
transport/usage or provider errors. No automatic retries, repairs, resume or model
fallback. Standalone scripts have output token limits but **no monetary guard**;
use the pilot runner for the study. Never rerun into an existing directory.

`plan.json` records all jobs and source/resource/implementation hashes;
`pilot_manifest.json` records completed, empty, failed and skipped jobs. Every
stage preserves source or report input, resource snapshots, request, received raw
response, manifest and validation. A format error preserves evidence and yields
no partial valid claim file. Empty outputs are separate from errors. D runs
independently of whether P succeeds. Scientific quality requires human annotation.

## Report unit, controls and annotation

P uses at most two calls per context: one report and one extraction covering
**all** findings. The lossless assembled report view is saved in `finding.json`;
all original title/report strings and the original JSONL remain available. Quote
offsets refer to that saved view. An empty report needs no extraction. Individual
finding selection remains available only for development commands.

The common [profile 0.1](resources/claim_profile.md) and
[codebook](resources/claim_codebook.md) separate propositions, conditions, quoted
source material, code references and derived verification tasks. The
[response schema](resources/claim_profile.schema.json) is enforced by a small
local validator. P resolves exact quotes to Unicode-codepoint offsets; D records
invalid code positions as diagnostics without discarding those claims. No truth
labels are generated. Ablation removes the explicit `context` object from both
routes while retaining conditions in propositions and local context IDs.

D revision sees only the same code and its previous D claims. The sentence
baseline is local; the [VeriScore-based baseline](resources/baselines/README.md)
uses its attributed, pinned extraction prompt, with documented adaptations.
Neither baseline is silently converted into a full profile or treated as a
truth judge. Count total route tokens/costs, not just the last call.

Human code references must be written before inspecting model outputs. The
neutral packets contain code and blank worksheets; keep their external
`linkage.json` away from annotators when possible. A separate reference for P
covers the actual report. Use the [annotation protocol](resources/annotation_protocol.md)
for coverage, fidelity, code grounding, uncertainty and adjudication. Independent
second annotation is planned for both variants of VUL4J-15 and VUL4J-41. Human
names, prior exposure and actual annotation times remain to be supplied.

## Development and inherited evidence

The starting code came from
[What Can We Verify? at 5df7760](https://github.com/sebi-gr/What-Can-We-Verify/tree/5df7760459b741ae36bd91af4af89f6e3ecfe18d).
[PROVENANCE.md](docs/PROVENANCE.md) records the import and evidence limits.
Six immutable historical files retain the original JSPWiki review, provider
request/response/prompt/manifest and accepted 13-claim annotation. They are
OpenRouter/Nemotron development artifacts with assisted annotation and prior
fix/PoV knowledge, not independent pilot truth. Original hashes and CRLF bytes
remain unchanged. Additional historic decomposition or PoV logs are optional.

[Profile development](resources/profile_development/README.md) covers JSPWiki,
Jackson XML (VUL4J-47) and Commons Configuration (VUL4J-9). Its ten example claims
are AI-assisted editorial fixtures, never model context or independent human data.

Legacy development commands remain available via `--help`. For VUL4J-18,
`01_prepare_case.py` exports five files; D uses `--review-run` to verify source
hashes and the exact original report request. Pilot D instead uses the registered
case/variant and pinned catalog, with no P-report dependency. Pilot pairing is
recorded by case/variant/repetition in the plan. Stage run IDs retain causal parents.

The [historic PoV protocol](resources/reproduce_vul4j18.md) describes earlier
Windows tests; raw logs were not imported and this repo has not re-executed them.
Downloaded PoV source is not a reproduced exploit or proof of every claim.

## Checks and licensing

```bash
python3 -m unittest -v
git diff --check
```

Tests use synthetic responses and local fixtures, covering source integrity,
request separation, report provenance, quotes, variants, ablation, revision,
cost stops and failure recording. They do not establish live-model compatibility
or research results. Windows may skip symlink checks without sufficient privileges.

Our code is [MIT](LICENSE). Third-party prompts, fixtures and downloaded sources
retain their own licenses/notices. Baseline attribution is under
`resources/baselines/`; source attribution is in the case catalog. Only the six
explicitly archived historical data files are tracked; all new generated data stays
local until a research-data archive is deliberately chosen.
