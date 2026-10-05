"""Validate the fixed P/D claim profile; no semantic or truth assessment."""

from copy import deepcopy
import json
from pathlib import Path
import re

PROFILE_VERSION = "0.1"
CODEBOOK_VERSION = "0.1"
RESOURCES = Path(__file__).resolve().parents[1] / "resources"
SCHEMA = RESOURCES / "claim_profile.schema.json"
CODEBOOK = RESOURCES / "claim_codebook.md"
FAMILIES = ("location", "data_flow", "protection_precondition",
            "exploitability_impact", "other", "unclear")
CLAIM_ID = re.compile(r"C[0-9]{2,}[a-z]?")
CLAIM_FIELDS = {"claim_id", "proposition", "family", "subtype", "family_reason",
                "context", "source_quotes", "code_refs", "context_claim_ids", "verification"}
CONTEXT_FIELDS = {"actor", "preconditions", "negation", "modality", "quantifier", "scope"}
CODE_REF_FIELDS = {"path", "line_start", "line_end", "symbol"}


# Lädt JSON-Objektpaare ohne doppelte Schlüssel und ohne stilles Überschreiben.
# Wird für Modellantworten und gespeicherte Eingaben verwendet.
def unique_object(pairs: list) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON object key.")
        result[key] = value
    return result


# Prüft die exakt erlaubten Objektfelder und benennt Abweichungen.
# Ändert oder repariert die Eingabe nicht.
def require_keys(value: object, expected: set, label: str) -> None:
    if not isinstance(value, dict):
        raise ValueError(f"{label}: expected a JSON object.")
    differences = []
    missing = sorted(expected - set(value))
    unexpected = sorted(set(value) - expected)
    if missing:
        differences.append(f"missing fields {json.dumps(missing)}")
    if unexpected:
        differences.append(f"unexpected fields {json.dumps(unexpected)}")
    if differences:
        raise ValueError(f"{label}: {'; '.join(differences)}.")


# Verlangt nichtleeren Text; Leerzeichen und Formulierungen bleiben unverändert.
# Verwendet den Feldnamen ausschließlich in der Fehlermeldung.
def require_text(value: object, label: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label}: expected nonempty text.")


# Prüft eine Liste eindeutiger, nichtleerer Texte, ohne sie zu normalisieren.
# Die Mindestanzahl ist nur für benötigte Evidenz größer als null.
def require_text_list(value: object, label: str, minimum: int = 0) -> None:
    if not isinstance(value, list) or len(value) < minimum:
        raise ValueError(f"{label}: expected a list with at least {minimum} entries.")
    for item in value:
        require_text(item, label)
    if len(set(value)) != len(value):
        raise ValueError(f"{label}: duplicate entries.")


# Akzeptiert nur eine vollständig beendete Textantwort ohne Refusal oder Tools.
# Liefert deren JSON ohne Reparatur; Reasoning ist kein Teil der Claim-Ausgabe.
def parse_response(response: dict) -> dict:
    if not isinstance(response, dict):
        raise ValueError("Provider response must be a JSON object.")
    choices = response.get("choices")
    if not isinstance(choices, list) or len(choices) != 1 or not isinstance(choices[0], dict):
        raise ValueError("Expected exactly one completion.")
    choice = choices[0]
    if choice.get("finish_reason") == "length":
        raise ValueError("Output token limit reached (finish_reason=length); response is incomplete.")
    if choice.get("error") or choice.get("finish_reason") != "stop":
        raise ValueError("Completion did not finish normally.")
    message = choice.get("message")
    if (not isinstance(message, dict) or message.get("role") != "assistant"
            or message.get("refusal") or message.get("tool_calls")
            or not isinstance(message.get("content"), str)):
        raise ValueError("Refusal, tool call or non-text output; not an empty claim list.")
    return json.loads(message["content"], object_pairs_hook=unique_object)


# Prüft Form und Eindeutigkeit der Codebezüge, nicht ihre inhaltliche Richtigkeit.
# Falsche Pfade/Positionen bleiben für die getrennte Bewertung erhalten.
def validate_code_refs(refs: object, label: str) -> None:
    if not isinstance(refs, list):
        raise ValueError(f"{label}: code_refs must be a list.")
    seen = set()
    for index, ref in enumerate(refs):
        ref_label = f"{label}.code_refs[{index}]"
        require_keys(ref, CODE_REF_FIELDS, ref_label)
        for key in ("path", "symbol"):
            if ref[key] is not None:
                require_text(ref[key], f"{ref_label}.{key}")
        if ref["path"] is None and ref["symbol"] is None:
            raise ValueError(f"{ref_label}: path or symbol is required.")
        start, end = ref["line_start"], ref["line_end"]
        if start is not None or end is not None:
            if type(start) is not int or type(end) is not int or start < 1 or end < start:
                raise ValueError(f"{ref_label}: lines must both be null or ordered positive integers.")
        identity = (ref["path"], start, end, ref["symbol"])
        if identity in seen:
            raise ValueError(f"{ref_label}: duplicate code reference.")
        seen.add(identity)


# Prüft P-Zitate und löst überlappende Vorkommen auf; D verlangt eine Leerliste.
# Neue Dictionaries enthalten Unicode-Codepoint-Offsets, nullbasiert und Ende exklusiv.
def resolve_quotes(quotes: object, route: str, finding: dict, label: str) -> list:
    if not isinstance(quotes, list) or (route == "P" and not quotes) or (route == "D" and quotes):
        raise ValueError(f"{label}: source_quotes must be nonempty for P and empty for D.")
    result = []
    seen = set()
    for quote in quotes:
        require_keys(quote, {"field", "quote", "occurrence"}, f"{label}.source_quotes")
        if quote["field"] not in ("title", "report"):
            raise ValueError(f"{label}: quote field must be title or report.")
        require_text(quote["quote"], f"{label}.quote")
        occurrence = quote["occurrence"]
        if type(occurrence) is not int or occurrence < 1:
            raise ValueError(f"{label}: quote occurrence must be a positive integer.")
        identity = (quote["field"], quote["quote"], occurrence)
        if identity in seen:
            raise ValueError(f"{label}: duplicate source quote.")
        seen.add(identity)
        source = finding[quote["field"]]
        start = -1
        for _ in range(occurrence):
            start = source.find(quote["quote"], start + 1)
            if start < 0:
                raise ValueError(f"{label}: exact quote occurrence not found in {quote['field']}.")
        result.append({**quote, "start": start, "end": start + len(quote["quote"])})
    return result


# Prüft den festen Profilvertrag, lokale IDs und routenspezifische Herkunft.
# Liefert unabhängige Claim-Kopien mit P-Offsets; liest keine Dateien und bewertet keine Wahrheit.
def validate_claims(document: dict, route: str, finding: dict = None) -> list:
    if route not in ("P", "D"):
        raise ValueError("Expected route P or D.")
    require_keys(document, {"profile_version", "route", "claims"}, "Response")
    if document["profile_version"] != PROFILE_VERSION or document["route"] != route:
        raise ValueError(f"Expected profile_version '{PROFILE_VERSION}' and route '{route}'.")
    if not isinstance(document["claims"], list):
        raise ValueError("Expected a claims list.")
    if route == "P":
        if not isinstance(finding, dict):
            raise ValueError("P requires the original title and report.")
        for field in ("title", "report"):
            require_text(finding.get(field), f"Finding.{field}")
    result = []
    ids = set()
    for index, claim in enumerate(document["claims"]):
        label = f"claims[{index}]"
        require_keys(claim, CLAIM_FIELDS, label)
        for key in ("claim_id", "proposition", "family", "family_reason"):
            require_text(claim[key], f"{label}.{key}")
        if not CLAIM_ID.fullmatch(claim["claim_id"]) or claim["claim_id"] in ids:
            raise ValueError(f"{label}: invalid or duplicate claim_id.")
        ids.add(claim["claim_id"])
        if claim["family"] not in FAMILIES:
            raise ValueError(f"{label}: unknown family.")
        if claim["family"] == "exploitability_impact":
            if claim["subtype"] not in ("exploitability", "impact", "unclear"):
                raise ValueError(f"{label}: exploitability_impact requires a subtype.")
        elif claim["subtype"] is not None:
            raise ValueError(f"{label}: subtype must be null for this family.")
        require_keys(claim["context"], CONTEXT_FIELDS, f"{label}.context")
        for key, value in claim["context"].items():
            if value is not None:
                require_text(value, f"{label}.context.{key}")
        references = claim["context_claim_ids"]
        require_text_list(references, f"{label}.context_claim_ids")
        if any(not CLAIM_ID.fullmatch(ref) for ref in references):
            raise ValueError(f"{label}: invalid context claim ID.")
        if claim["claim_id"] in references:
            raise ValueError(f"{label}: self context reference.")
        validate_code_refs(claim["code_refs"], label)
        verification = claim["verification"]
        require_keys(verification, {"question", "required_evidence", "assumptions"}, f"{label}.verification")
        require_text(verification["question"], f"{label}.verification.question")
        require_text_list(verification["required_evidence"], f"{label}.verification.required_evidence", 1)
        require_text_list(verification["assumptions"], f"{label}.verification.assumptions")
        resolved = deepcopy(claim)
        resolved["source_quotes"] = resolve_quotes(claim["source_quotes"], route, finding, label)
        result.append(resolved)
    for claim in result:
        if any(reference not in ids for reference in claim["context_claim_ids"]):
            raise ValueError(f"{claim['claim_id']}: unresolved context claim ID.")
    return result


# Vergleicht bereits formal gültige Codebezüge ausschließlich mit gelieferten Pfad-/Inhaltswerten.
# Liest niemals das Dateisystem, ergänzt keine Pfade und liefert Diagnosen mit nullbasiertem ref_index.
# Auch ein auflösbarer Zeilenbereich bestätigt weder das Symbol noch die Aussage.
def check_code_refs(claims: list, files: dict) -> list:
    diagnostics = []
    for claim in claims:
        for index, ref in enumerate(claim["code_refs"]):
            path = ref["path"]
            if path is None:
                status = "no_position"
            elif path not in files:
                status = "unresolved_path"
            elif ref["line_start"] is None:
                status = "no_position"
            else:
                content = files[path]
                text = content.decode("utf-8") if isinstance(content, bytes) else content
                status = "resolved" if ref["line_end"] <= len(text.splitlines()) else "out_of_range"
            diagnostics.append({"claim_id": claim["claim_id"], "ref_index": index, "status": status})
    return diagnostics
