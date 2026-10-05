# Erprobung des Claimprofils

**Profil 0.1 · 2026-10-05 · AI-assistierter Entwicklungsdurchgang (Codex).**
Die [Profilregeln](../claim_profile.md), das [Codebook](../claim_codebook.md) und
[Annotationsprotokoll](../annotation_protocol.md) wurden an JSPWiki und zwei
zusätzlichen Codefällen durchgegangen. [examples.json](examples.json) enthält
von Codex ausgearbeitete Formatbeispiele, keine neuen Modellläufe oder unabhängig
menschlich annotierte Referenz. Die neuen Codeinventare unten sind Arbeitsentwürfe.
Es wurden weder Benchmarks ausgeführt noch P/D-Vergleichsmetriken erhoben.

## Material und Geltungsbereich

| Fall | Tatsächlich betrachteter Code | Zweck und Grenze |
|---|---|---|
| VUL4J-18 / JSPWiki | Die fünf vollständigen Dateien aus `01_prepare_case.py`: WikiServlet, DefaultURLConstructor, URLConstructor, jspwiki.properties, web.xml | Vorhandener Report und manuelle Zerlegung; Pfad-/Query-Trennung, Bedingungen und Folgen prüfen. WikiEngine, Filterimplementationen und Ziel-JSPs fehlen. |
| VUL4J-47 / Jackson XML | [XmlFactory.java.txt](code/XmlFactory.java.txt): ausschließlich Originalzeilen 84–144 | Null-Zweig und Parserkonfiguration; kein vollständiger Parser-/Aufruferkontext. Lokale Textzeile 1 entspricht Originalzeile 84. |
| VUL4J-9 / Commons Configuration | [YAMLConfiguration.java](code/YAMLConfiguration.java): vollständige 145 Originalzeilen | YAML-Eingabefluss und LoaderOptions; SnakeYAML-Implementation/-Version und Aufrufer fehlen. |

Die JSPWiki-Dateien werden über den bestehenden Export reproduziert, nicht hier
dupliziert. [sources.json](sources.json) fixiert Herkunft, Commit, Zeilenscope und
Hashes der neuen Dateien; Lizenznachweise liegen daneben. Die vollständigen Ausgangsdateien
wurden gegen die fixierten Vul4J-Fallstände geprüft und sind dort bytegleich.
Das Jackson-Exzerpt ist eine unveränderte Zeilenauswahl, keine kompilierbare Klasse.
Alle folgenden Zeilennummern sind **Originalzeilen**, nicht neu nummerierte Auszüge.

Die drei Themenbereiche sind Pfadverarbeitung, XML-Parserkonfiguration und
YAML-Laden mit deserialisierungsbezogenen Fragen. VUL4J-9 hat im Dataset die
CWE-Zuordnung `Not Mapping`; daraus wird kein künstliches CWE-502-Label gemacht.
Datasetlabels, Fixes und PoVs dienten der Auswahl bzw. als externes Vorwissen,
nicht als Codebeweis. Sie gehören nicht in die P/D-Eingaben. Diese drei Fälle
und ihre gefixten Varianten bleiben Entwicklung und werden kein Evaluation-Holdout.

## JSPWiki: Reportreferenz

Originale: [Finding](../../data/runs/VUL4J-18-review-001/findings.jsonl) und
[Annotation vom 24.09.2026](../../data/annotations/VUL4J-18-review-001/manual_annotation_001.md).
Alle exakten Zitate bleiben dort unverändert. Die folgende Zuordnung benennt die
13 historischen Propositionen als `R01`–`R13`; sie ist kein Sollwert für die
Claimzahl neuer Ausgaben. SG annotierte mit Codex-Unterstützung und Vorwissen über
Code/Fix/PoV; weder damals noch hier lag unabhängige menschliche Doppelannotation vor.
Die alten Wahrheitsurteile bleiben `not_evaluated` und werden nicht überschrieben.

Passagenindex: **T** = kompletter Titel; **S1** beginnt „In WikiServlet.java line 89“,
**S2** „This value is then used“, **S3** „An attacker could craft a request“,
**S4** „Although the DefaultURLConstructor.parsePageFromURL method“.
S1–S4 bezeichnen die vier vollständigen Reportsätze der archivierten Annotation.
Bei Rückbezügen werden beide ganzen Originalpassagen als Quellen verwendet.

| Referenz | Historische ID | Passage | Zu erhaltende Proposition und Einschränkung |
|---|---|---|---|
| R01 | C01 | T | Kategorisches Path-Traversal-Label für WikiServlet/PathInfo; `other`. |
| R02 | C03 | S1 | Verwendung von parsePageFromURL in WikiServlet.java Zeile 89. |
| R03 | C04 | S1 | Seitenname stammt aus request.pathInfo. |
| R04 | C05 | S1 | Extraktion ohne **ausreichende** Validierung; nicht „keine Validierung“. |
| R05 | C07 | S1 + S2 | Extrahierter Seitenname wird direkt für die Dispatcher-URL verkettet; behauptete Zeilen 97–98. |
| R06 | C08 | S1 + S2 | Fehlende Sanitization bei genau dieser URL-Verkettung. |
| R07 | C09a | S3 | Angreifer **könnte** einen Request mit Traversalsequenzen konstruieren; Payload ist Beispiel, Rechte fehlen. |
| R08 | C09b | S3 | Damit **möglicherweise** unautorisierter Ressourcenzugriff **oder** Umgehung von Zugriffskontrollen. |
| R09 | C11a | S4 | Parser entfernt **nur** einen führenden Slash; behauptete Methodenzeilen 245–268. |
| R10 | C11b | S4 | Parser dekodiert den Pfad **nicht weiter**. |
| R11 | C11c | S4 | Parser validiert den Pfad **nicht weiter**, lokal auf diese Methode begrenzt. |
| R12 | C11d | S4 | Fehlende **zusätzliche** Servletprüfungen ermöglichen die Weiterleitung bösartiger Pfadsequenzen an interne JSPs; Kausalität erhalten. |
| R13 | C12 | S4 | Weiterleitung könnte Informationspreisgabe **oder** weitere Ausnutzung bewirken, **abhängig von der Verarbeitung des page-Parameters durch die Ziel-JSP**. |

**Aktuelle Entscheidungen:** T bleibt erhalten, weil sein kategorisches Label
stärker ist als die modal formulierten Wirkungen in S3/S4. Ein wirklich redundanter
Titel bekäme keinen Zusatzclaim. R10 kann nach der aktuellen Regel als `other`
geführt werden: fehlendes Dekodieren ist allein keine fehlende Schutzmaßnahme.
Die historische `protection_precondition`-Zuordnung bleibt im Original stehen;
diese Abweichung ist ein dokumentierter Grenzfall, keine rückwirkende Korrektur.
R02 und R03 dürfen gemeinsam dargestellt werden, solange beide Bedeutungen
rekonstruierbar bleiben; Nummern und Anzahl sind keine Abdeckungsmetrik.

## JSPWiki: getrennte Codereferenz

Hier beziehen sich kurze Dateinamen eindeutig auf das fünfteilige JSPWiki-Paket.
`K`-IDs gelten innerhalb dieses Falls; sie sind keine Gleichsetzung mit `R`-IDs.
`proposition` bedeutet im beschriebenen Scope durch Code gestützt;
`open_question` bezeichnet eine konkrete Grenze, keine bestätigte Schwachstelle.

| ID / Art | Proposition oder offene Frage | Codeanker und Relevanzgrenze |
|---|---|---|
| K01 / proposition | Der Servletpfad verwendet `jspPage`, während `pageName` über `m_engine.encodeName` in den Queryparameter `page` gelangt; danach wird weitergeleitet. | WikiServlet.java 89–100, besonders 96–98. Trennt zwei Datenflüsse. Belegt den Encode-Aufruf, nicht dessen Sicherheitswirksamkeit; WikiEngine fehlt. |
| K02 / proposition | `DefaultURLConstructor.getForwardPage` gibt `request.getPathInfo()` zurück. | DefaultURLConstructor.java 278–281. Relevant für den Dispatcherpfad **falls diese Implementation aktiv ist**; ihre Existenz beweist das nicht. |
| K03 / proposition | `parsePageFromURL` liest PathInfo, gibt bei null oder Länge ≤ 1 null zurück, entfernt sonst einen führenden Slash und gibt den Wert zurück; kein aktiver Decode-Aufruf. | DefaultURLConstructor.java 245–268. Null-/Längenprüfungen und kommentierten Decode-Aufruf unterscheiden; kein Beleg für ausreichende Traversalvalidierung. |
| K04 / open_question | Welche URLConstructor-Implementation liefert die laufende WikiEngine tatsächlich? | WikiServlet.java 96; jspwiki.properties 410–440, besonders auskommentierte Auswahl 438–439. Konfigurationsvorlage und Interface ersetzen keinen aktiven Deploymentzustand; WikiEngine fehlt. |
| K05 / open_question | Welche Authentisierung, Filter und Ziel-JSP-Verarbeitung begrenzen die erreichbaren Pfade und Auswirkungen? | WikiServlet.java 97–100; web.xml 57–77 mit Filterdefinitionen/-Mappings. Filterimplementationen und Ziel-JSPs fehlen: kein Nachweis unautorisierter Dateilektüre oder sicherer Unmöglichkeit. |

K01–K03 begrenzen relevante Operationen, K04–K05 die wesentlichen offenen
Voraussetzungen. Einzelne Imports oder triviale Zuweisungen werden nicht als
zusätzliche Abdeckungspunkte gezählt. Diese nachträgliche Entwicklungsanalyse
ist nicht gegenüber dem historischen Report oder Patchwissen verblindet.

## Zusätzliche Codereferenzen

Die IDs beginnen pro Fall erneut bei K01. Auch hier sind die Propositionen
AI-assistierte Entwürfe auf Grundlage des bezeichneten Codes, keine CVE-Urteile.

| Fall / ID / Art | Proposition oder offene Frage | Originalzeilen und Grenze |
|---|---|---|
| Jackson K01 / proposition | Wenn `xmlIn == null`, erzeugt der Konstruktor eine XMLInputFactory und setzt `IS_SUPPORTING_EXTERNAL_ENTITIES` auf `Boolean.FALSE`. | XmlFactory.java 112–116. Bedingte Zuweisung belegt; gesamte XXE-Sicherheit nicht belegt. |
| Jackson K02 / proposition | Bei nicht-null übergebenem `xmlIn` wird diese Entity-Property-Zuweisung im gezeigten Konstruktor übersprungen; die Factory gelangt an `_initFactories`. | 104–123, 138–144. Kein Beweis, dass die externe Factory unsicher konfiguriert ist. |
| Jackson K03 / proposition | Der gezeigte Hauptkonstruktor und `_initFactories` setzen `SUPPORT_DTD` nicht. | 104–123, 138–144. Lokale Negation; keine Behauptung über effektiven Default oder gesamte Anwendung. |
| Jackson K04 / open_question | Lädt das konkrete Provider-/Aufrufer-Setup externe DTDs oder zugängliche Ressourcen? | Grenze der Zeilen 84–144: Provider, Version, weitere Konfiguration, Eingabeherkunft und Laufzeitrechte fehlen. Gezielter Test wäre zusätzliche Evidenz. |
| YAML K01 / proposition | `read(Reader)` und `read(InputStream)` übergeben `in` an `yaml.load` einer mit `new Yaml()` erzeugten Instanz; das Ergebnis wird als Map an `load(map)` übergeben. | YAMLConfiguration.java 63–76 und 115–128. Zwei analoge Pfade, eine Inventareinheit; kein belegter Angreiferursprung. |
| YAML K02 / proposition | Die beiden Overloads mit `LoaderOptions` erzeugen `new Yaml(options)` und reichen ihre Eingabe an `yaml.load(in)` weiter. | 78–91 und 130–143. Optionswerte und interne Bibliothekssemantik sind offen. |
| YAML K03 / open_question | Welche Typen/Nebenwirkungen erlaubt `Yaml.load` bei tatsächlicher Version und Optionskonfiguration, und erreicht untrusted Input diese Methoden? | 63–91, 115–143. Dependency-Implementation, Aufrufer und Deployment fehlen; `new Yaml()` allein beweist weder Objektkonstruktion eines gefährlichen Typs noch Codeausführung. |

## Grenzfälle und semantische Zuordnung

| Fall | Regelentscheidung aus dem Durchgang |
|---|---|
| JSPWiki: „ohne ausreichende Validierung“ | Nicht zu „ohne jede Prüfung“ verstärken. K03 zeigt Null-/Längengrenzen, entscheidet aber nicht ihre Eignung gegen Traversal. |
| JSPWiki: „nur Slash entfernen“ | „Nur“ benötigt eine festgehaltene Lesart: alleinige Stringtransformation oder gesamtes Methodenverhalten? K03 zeigt zusätzliche Guard-Zweige; Mehrdeutigkeit dokumentieren. |
| JSPWiki: Titel versus S3/S4 | Kategorisches Label und mögliche Auswirkungen getrennt erhalten; keine stärkere Gewissheit aus dem Titel in alle Claims übertragen. |
| JSPWiki: S4-Kausalität und Impact | R12 und R13 trennbar, aber Ursache, `could`, `or` und Ziel-JSP-Bedingung bleiben erhalten. `context_claim_ids` ersetzt diese Inhalte nicht. |
| Jackson: false / nicht gesetzt / unbekannt | Explizites `Boolean.FALSE` in K01 ist nicht dasselbe wie die fehlende DTD-Zuweisung in K03 oder die unbekannte effektive Konfiguration in K04. |
| Jackson: Custom Factory | Weglassen der null-Bedingung erweitert die Aussage unzulässig auf übergebene Factories. |
| YAML: lokale Abwesenheit | Vor `yaml.load` ist in den gezeigten Methoden keine explizite Eingabeprüfung zu sehen. Daraus folgt nicht „keine Validierung im System“ oder „SnakeYAML hat keine Schutzmaßnahmen“. |
| YAML: Catch nach Aufruf | Catch-/Rethrow-Code beweist nicht, dass während `yaml.load` keine Nebenwirkung möglich ist; die Bibliotheksausführung fehlt. |

**Zuordnungsübungen, keine Messergebnisse:** Ein P-Claim, der R13 mit „könnte“,
„oder“ und der Ziel-JSP-Bedingung erhält, ist reporttreu (`faithful`, `full` zu R13).
Seine behauptete Wirkung bleibt im Codepaket `inconclusive` wegen K05.
„Ein Angreifer liest beliebige Dateien ohne Anmeldung“ erfasst R13 höchstens
teilweise: Wirkung, Akteurrechte und Modalität sind verändert bzw. ergänzt.

Ein reporttreuer R05-Claim wird nicht durch Treue automatisch codegestützt:
K01 zeigt den Encode-Aufruf und die getrennte Herkunft von `jspPage`. Die Lesart
„unveränderter Seitenname als Dispatcherpfad“ ist damit widerlegt; bei uneindeutiger
„direkt“-Formulierung zuerst die Lesart dokumentieren. Umgekehrt ist ein P-Zusatz
über `encodeName` aus K01 zwar codegestützt, aber nicht im Report enthalten und
folglich keine treue Extraktion. P darf diese Reparatur nicht still vornehmen.

„Jede XMLInputFactory erhält hier die Entity-Property false“ ist durch Jackson
K02 widerlegt. „Das konkrete Deployment verhindert alle XXE-Zugriffe“ bleibt
wegen K04 offen. Eine einzige Aussage zu beiden YAML-Eingabetypen kann K01 voll
abdecken; zwei semantisch gleiche Claims erzeugen keine doppelte Abdeckung.
Zusatzannahmen über Angreiferrechte bleiben von Originalaussage und Evidenz getrennt.

## Ergebnis für den nächsten Schritt

Die Beispiele benötigen keine neue Ontologie: vollständige Propositionen,
expliziter Kontext, getrennte Report-/Codebezüge und abgeleitete Prüfaufgaben
reichen als vorläufiger Vertrag. Schritt 3 hat diesen Vertrag inzwischen in P und D umgesetzt.
Vor Pilot/Evaluation bleiben unabhängige menschliche Annotation, vorab fixierte
Referenzen und dokumentierte Adjudikation erforderlich; dieser Durchgang ersetzt sie nicht.

Formale Prüfung am 05.10.2026: vier JSON-Ausgaben mit zehn Claims gegen Draft
2020-12 validiert; acht gezielt fehlerhafte Formatvarianten abgelehnt, leere
Ausgaben beider Routen akzeptiert. Originalzitate/Offsets mit dem vorhandenen
P-Validator geprüft; Kontext-IDs, Codezeilen, Quellausschnitte, Lizenz-/Archivhashes
und lokale Dokumentlinks abgeglichen. Schema-Prüfung einmalig mit temporär
installiertem `jsonschema`; keine neue Laufzeitabhängigkeit. Dies war der Prüfstand von Schritt 2. Seit Schritt 3 prüfen gemeinsame
Offline-Tests auch diese Fixtures mit dem ausführbaren Profilvalidator.
