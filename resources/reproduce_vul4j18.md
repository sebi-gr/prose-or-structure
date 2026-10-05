# VUL4J-18: Java-PoV reproduction

Status: successfully reproduced on Windows 11 amd64, 2026-09-23.
Local evidence: `data/pov/VUL4J-18-001/` (ignored by Git).

## Sources and comparison

- Dataset: `376411da11fa705019f731404de1d0679fe73537`, row VUL4J-18; saved as `vul4j_row.json`.
- Complete [benchmark snapshot](https://github.com/tuhh-softsec/Vul4J/tree/07ad7850a041876befb99847053e4b5e181597a5): `07ad7850a041876befb99847053e4b5e181597a5`.
- [Source archive](https://codeload.github.com/tuhh-softsec/Vul4J/zip/07ad7850a041876befb99847053e4b5e181597a5): SHA-256 `9e7919c0a716a71918003cb490e45fef250153c870c991c4654ab8dc310c7a6b`.
- `vulnerable/`: original benchmark archive, with the archive's top-level directory stripped to keep Windows paths shorter.
- `fixed/`: a separate extraction of the same archive, changing only `jspwiki-main/src/main/java/org/apache/wiki/url/DefaultURLConstructor.java` to the original bytes from [upstream fix 88d89d6](https://github.com/apache/jspwiki/commit/88d89d6523802c044cfcb7930cba40d8eeb21da2).
- `human-fix.diff`: only `getForwardPage()` changes from `request.getPathInfo()` to the constant `"Wiki.jsp"`. Both copies retain identical benchmark tests.
- The five vulnerable source hashes match the completed review input. `provenance.json` records source hashes and the comparison setup.

This compares the benchmark's vulnerable version with its human fix applied; it does not claim that the entire fixed snapshot is a pristine upstream checkout.

## Toolchain and commands

Portable Eclipse Temurin JDK `8u504-b01` and Apache Maven `3.9.16`, extracted under `tools/`. Downloads came from the official Temurin GitHub release and Apache distribution; SHA-256 (JDK) and SHA-512 (Maven) matched published checksums before extraction. URLs/checksums and `java-version.log`/`maven-version.log` are saved locally. Nothing was installed globally.

Each invocation uses a local `settings.xml` selecting `data/pov/VUL4J-18-001/m2` as the Maven repository. `JAVA_HOME` and `PATH` are set only for the child process. The two variant builds run sequentially, each followed by its own tests before the next variant installs artifacts into that cache.

The benchmark declares `mvn -DskipTests clean install`. This run limits that build to the PoV module and its required reactor modules with `-pl jspwiki-main -am`; unrelated WAR/portable/integration-test modules are excluded. The dataset's other command options remain unchanged. No production logic or PoV assertions are modified to make the build pass.

From each variant directory, using the portable Maven and Java paths:

```text
mvn -s ../settings.xml -DskipTests clean install -pl jspwiki-main -am <dataset-options>
mvn -s ../settings.xml test -pl jspwiki-main -Dtest=org.apache.wiki.WikiServletTest#testNastyDoPost,org.apache.wiki.WikiServletTest#testDoGet <dataset-options>
```

`<dataset-options>` is the exact `cmd_options` field in the pinned row:

```text
-Dhttps.protocols=TLSv1.2 -Denforcer.skip=true -Dcheckstyle.skip=true -Dcobertura.skip=true -DskipITs=true -Drat.skip=true -Dlicense.skip=true -Dpmd.skip=true -Dfindbugs.skip=true -Dgpg.skip=true -Dskip.npm=true -Dskip.gulp=true -Dskip.bower=true -Danimal.sniffer.skip=true -V -B
```

On Windows, quote the entire `-Dtest=...` argument when invoking Maven from PowerShell. Each attempt has a unique log and JSON sidecar with the exact command, working directory, Java location, timestamps, duration and exit code. The local `run_step.py` automates only those commands and refuses existing log names; it is a saved experiment helper, not a new pipeline component.

## Result

Both snapshots built successfully. The two unchanged PoV tests then produced the
expected differential result:

| Variant | Tests | Failures | Errors | Skips | Maven result |
|---|---:|---:|---:|---:|---|
| Vulnerable | 2 | 2 | 0 | 0 | failure caused only by the two PoV assertions |
| Fixed | 2 | 0 | 0 | 0 | success |

On the vulnerable version, both `testNastyDoPost` and `testDoGet` expected
`/Wiki.jsp?page=Main&` but observed `/?page=Main&`. On the fixed version, both
assertions passed. The vulnerable test command exited 1; this is the expected PoV
signal, not a setup failure. The fixed test command exited 0.

Full commands, timestamps, durations and exit codes are stored in the four JSON
sidecars `vulnerable-build-01.json`, `vulnerable-test-01.json`,
`fixed-build-01.json` and `fixed-test-01.json`. Their corresponding `.log` files
contain complete Maven output. Surefire XML/text reports remain inside each
variant's `jspwiki-main/target/surefire-reports/`. `reproduction_result.json`
summarizes the checked outcome.

## Success criterion and scope

The criterion was met: both named tests ran in both versions, without skips or
setup errors. The vulnerable assertions failed on the unexpected forwarding URL;
the fixed assertions passed with `/Wiki.jsp?page=Main&`.

These tests exercise `WikiServlet` with Stripes servlet mocks. Even a successful differential result demonstrates only the forwarding behavior covered by those tests. It does not independently prove arbitrary file reads, unauthenticated remote exploitation, behavior of a deployed server or every claim in the generated finding. The original preparation manifest remains unchanged (`pov_status: not_run` describes the preparation step); reproduction evidence is kept separately.
