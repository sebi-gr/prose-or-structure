"""Use the shared profile with a narrowly scoped explicit-context-field ablation."""

from copy import deepcopy
import json
from pathlib import Path

import claim_profile


# Ersetzt genau eine bekannte Ressourcenpassage für die vorab definierte Ablation.
# Bricht bei geänderten Vorlagen ab, statt widersprüchliche Modellanweisungen zu erzeugen.
def replace_once(text: str, original: str, replacement: str) -> str:
    if text.count(original) != 1:
        raise ValueError("Context ablation resource changed; review its explicit field instructions.")
    return text.replace(original, replacement, 1)


# Lädt die unveränderten Standardressourcen oder leitet die Variante ohne context-Objekt ab.
# Ändert nur Feldanweisungen/Schema; Bedingungen in Propositionen und Kontext-IDs bleiben erhalten.
# Gibt die tatsächlich zu sendenden und zu archivierenden Bytes zurück, ohne Dateien zu ändern.
def resources(prompt_path: Path, no_context_fields: bool = False) -> dict:
    result = {path.name: path.read_bytes()
              for path in (prompt_path, claim_profile.CODEBOOK, claim_profile.SCHEMA)}
    if not no_context_fields:
        return result
    schema = json.loads(result[claim_profile.SCHEMA.name], object_pairs_hook=claim_profile.unique_object)
    claim = schema["$defs"]["claim"]
    claim["required"].remove("context")
    del claim["properties"]["context"]
    schema["title"] += " — explicit context fields omitted"
    result[claim_profile.SCHEMA.name] = (json.dumps(schema, indent=2, ensure_ascii=False) + "\n").encode("utf-8")

    prompt = result[prompt_path.name].decode("utf-8")
    if prompt_path.name == "decomposition_prompt.txt":
        prompt = replace_once(prompt,
                              "family_reason, context, source_quotes,",
                              "family_reason, source_quotes,")
        prompt = replace_once(prompt,
                              "Use the common codebook's six context fields; null means not stated, not false.\n"
                              "Keep those qualifications in the proposition too. Copy code references only as",
                              "Keep all qualifications in the proposition. Copy code references only as")
    elif prompt_path.name == "direct_claim_prompt.txt":
        prompt = replace_once(prompt,
                              "  and scope in the proposition and in the six context fields. Use null only for\n"
                              "  an aspect not stated; explicit absence and explicit uncertainty remain text.",
                              "  and scope in the proposition. Explicit absence and explicit uncertainty remain text.")
    else:
        raise ValueError(f"No explicit-context ablation defined for prompt: {prompt_path.name}")
    prompt += "\nFor this variant, omit the context object entirely. Preserve all conditions in the proposition.\n"
    result[prompt_path.name] = prompt.encode("utf-8")

    codebook = result[claim_profile.CODEBOOK.name].decode("utf-8")
    codebook = replace_once(codebook,
                           "`context` hat sechs Text-oder-null-Felder: `actor` (Akteur und Rechte),\n"
                           "`preconditions` (nicht als erfüllt zu behauptende Voraussetzungen), `negation`\n"
                           "(Verneinung mit Bezugsgegenstand), `modality` (sprachliche Möglichkeit/Gewissheit),\n"
                           "`quantifier` (Quantor und Bezugsobjekt), `scope` (Pfad/Version/Konfiguration).\n"
                           "`null` heißt nicht angegeben; ausdrücklich unbekannt und explizit verneint\n"
                           "als Text erhalten. Eine kategorische Aussage ohne Modalwort hat `modality: null`.\n"
                           "Diese Aspekte müssen auch in der Proposition erhalten bleiben.",
                           "Akteur und Rechte, Voraussetzungen, Verneinung mit Bezugsgegenstand, sprachliche\n"
                           "Möglichkeit/Gewissheit, Quantoren und Geltungsbereich müssen in der Proposition\n"
                           "erhalten bleiben. Voraussetzungen nicht als erfüllt behaupten; ausdrücklich\n"
                           "unbekannte und explizit verneinte Angaben sprachlich erhalten.")
    codebook = replace_once(codebook,
                           "gehören in die Proposition und `context.preconditions`.",
                           "gehören in die Proposition.")
    result[claim_profile.CODEBOOK.name] = codebook.encode("utf-8")
    return result


# Prüft Standardclaims oder exakt denselben Vertrag ohne das explizite context-Objekt.
# Temporäre Nullfelder dienen nur dem gemeinsamen Validator und werden nie als Ausgabe gespeichert.
# Originalantwort und übrige Regeln einschließlich P-Zitate und Kontext-IDs bleiben unverändert.
def validate(document: dict, route: str, finding: dict = None,
             no_context_fields: bool = False) -> list:
    if not no_context_fields:
        return claim_profile.validate_claims(document, route, finding)
    claim_profile.require_keys(document, {"profile_version", "route", "claims"}, "Response")
    if not isinstance(document["claims"], list):
        raise ValueError("Expected a claims list.")
    adapted = deepcopy(document)
    for index, claim in enumerate(adapted["claims"]):
        claim_profile.require_keys(claim, claim_profile.CLAIM_FIELDS - {"context"}, f"claims[{index}]")
        claim["context"] = {key: None for key in claim_profile.CONTEXT_FIELDS}
    claims = claim_profile.validate_claims(adapted, route, finding)
    for claim in claims:
        del claim["context"]
    return claims
