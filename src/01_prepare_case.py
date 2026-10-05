"""Prepare the VUL4J-18 source context and keep reference material separate."""

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import tempfile
from urllib.error import URLError
from urllib.request import urlopen


CASE_ID = "VUL4J-18"
DATASET_COMMIT = "376411da11fa705019f731404de1d0679fe73537"
CASE_COMMIT = "07ad7850a041876befb99847053e4b5e181597a5"
FIX_COMMIT = "88d89d6523802c044cfcb7930cba40d8eeb21da2"

DATASET_URL = (
    f"https://raw.githubusercontent.com/tuhh-softsec/Vul4J/{DATASET_COMMIT}"
    "/dataset/vul4j_dataset.csv"
)
CASE_URL = f"https://raw.githubusercontent.com/tuhh-softsec/Vul4J/{CASE_COMMIT}"
FIX_URL = f"https://raw.githubusercontent.com/apache/jspwiki/{FIX_COMMIT}"
CONSTRUCTOR = "jspwiki-main/src/main/java/org/apache/wiki/url/DefaultURLConstructor.java"
POV = "jspwiki-main/src/test/java/org/apache/wiki/WikiServletTest.java"

# A localized review: full files, original paths and original line numbers.
MODEL_FILES = (
    "jspwiki-main/src/main/java/org/apache/wiki/WikiServlet.java",
    CONSTRUCTOR,
    "jspwiki-main/src/main/java/org/apache/wiki/url/URLConstructor.java",
    "jspwiki-main/src/main/resources/ini/jspwiki.properties",
    "jspwiki-war/src/main/webapp/WEB-INF/web.xml",
)


# Lädt eine Quelldatei von der angegebenen URL mit 30 Sekunden Timeout.
# Gibt die unveränderten Bytes zurück; Downloadfehler gehen an den Aufrufer.
def download(url: str) -> bytes:
    with urlopen(url, timeout=30) as response:
        return response.read()


# Wandelt ein Dictionary in lesbares JSON mit abschließendem Zeilenumbruch um.
# Gibt UTF-8-Bytes zurück, die direkt als Datei gespeichert werden können.
def json_bytes(value: dict) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


# Erstellt den VUL4J-18-Export aus fixierten Quellen und prüft die Dataset-Zuordnung.
# Trennt Modellkontext von Referenzen und speichert Herkunft und Datei-Hashes.
# Veröffentlicht nur den vollständigen Export an einem neuen Ziel; führt keinen PoV aus.
def prepare_case(output: Path) -> None:
    if output.exists() or output.is_symlink():
        raise FileExistsError(f"Output already exists: {output}. Choose a new --output path.")

    dataset = download(DATASET_URL)
    rows = csv.DictReader(io.StringIO(dataset.decode("utf-8")))
    row = next((row for row in rows if row["vul_id"] == CASE_ID), None)
    if row is None:
        raise ValueError(f"{CASE_ID} is missing from the pinned dataset.")
    if (
        row["repo_slug"] != "apache/jspwiki"
        or row["cve_id"] != "CVE-2019-0225"
        or row["human_patch"] != f"https://github.com/apache/jspwiki/commit/{FIX_COMMIT}"
    ):
        raise ValueError("The dataset does not match the expected JSPWiki case and fix.")

    downloads = [
        (f"model_input/{path}", f"{CASE_URL}/{path}") for path in MODEL_FILES
    ]
    downloads.extend([
        (f"reference/fixed/{CONSTRUCTOR}", f"{FIX_URL}/{CONSTRUCTOR}"),
        (f"reference/pov/{POV}", f"{CASE_URL}/{POV}"),
        ("reference/LICENSE", f"{CASE_URL}/LICENSE"),
        ("reference/NOTICE", f"{CASE_URL}/NOTICE"),
    ])

    manifest = {
        "case_id": CASE_ID,
        "review_mode": "localized_review",
        "dataset_url": DATASET_URL,
        "dataset_sha256": hashlib.sha256(dataset).hexdigest(),
        "case_commit": CASE_COMMIT,
        "upstream_fix_commit": FIX_COMMIT,
        "pov_status": "not_run",
        "files": {},
    }
    files = {}
    for path, url in downloads:
        print(f"Downloading {path}", flush=True)
        content = download(url)
        files[path] = content
        manifest["files"][path] = {
            "url": url,
            "sha256": hashlib.sha256(content).hexdigest(),
        }

    files["reference/vul4j_row.json"] = json_bytes(row)
    files["manifest.json"] = json_bytes(manifest)

    # Publish only a complete case; failures must not leave a usable-looking output.
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=output.parent) as temporary:
        staging = Path(temporary) / "case"
        for path, content in files.items():
            target = staging / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
        staging.rename(output)

    print(f"Prepared {CASE_ID}: {output.resolve()}")
    print("Give the model only model_input/. The PoV was saved, not executed.")


# Liest das CLI-Ausgabeverzeichnis und startet die Fallvorbereitung.
# Meldet erwartete Download-, Datei- und Datenfehler mit Exit-Code 1.
def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path, default=Path("data") / CASE_ID,
        help="New output directory (default: data/VUL4J-18).",
    )
    args = parser.parse_args()
    try:
        prepare_case(args.output)
    except (OSError, URLError, ValueError) as error:
        parser.exit(1, f"Could not prepare case: {error}\n")


if __name__ == "__main__":
    main()
