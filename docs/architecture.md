# Architektur

## Grundstruktur
Aufgrund der geringen Zeit und einem möglichsten schnellen Einstieg + Flexibilität haben wir uns dazu entschieden die Programmiersprache Pyhton zu verwenden.
Zusammen mit Pyhton haben wir die Möglichkeit auf die Machine Learning API `SciKit` zu verwenden.
Diese bietet uns eine flexible Struktur, um mit verschiedenen Techniken testen zu können.
Egal ob DecisionTrees, neuronale Netze oder andere Methoden.
Durch die einheitliche Struktur ist ein Umtauschen relativ leicht möglich.

- TODO vllt bisschen genauer auf die Struktur eingehen

Die Classifier Struktur soll wie folgt aufgebaut werden.
Wir haben `Feature`-Klassen, die einen Namen und einen Wert haben.
Der Wert eines Features entspricht dabei auch dem benötigten Eingabe der Machine Learning API.
Die Features werden dabei von `FeatureExtractor`s extrahiert.
Das bedeutet, dass wir für jede Gruppe an Features einen eigenen Extractor definieren.
Innerhalb einer `FeatureExtractorPipeline` werden die Extractors in einer definierten Reihenfolge ausgeführt und die Features in der Reihenfolge gespeichert.
Dadurch stellen wir immer die selbe Reihenfolge fest.
Für den Anfang soll pro Extractor eine eigene Datei + Klasse erstellt werden.

Zusätzlich ist es eventuell nicht schlecht, wenn wir auch noch nach Kategorien unterscheiden können.
Das könnte möglicherweise dann nützlich sein, wenn wir eigene Modelle je nach Kategorie ausführen wollen.
Dafür würden sich `FeatureCategory`s anbieten.
Diese kapseln selbst nochmal eigene Extractors.

Nach ersten Tests haben wir uns dazu entschlossen die Kategorien wieder rauszunehmen.
Durch automatisierte Teilung von Daten ist der Machine Learning Algorithmus auch selbst in der Lage Daten sinnvoll zu splitten.
Dadurch sparen wir uns Komplexität im Code und erleichtert uns das Programmieren von Extractors.
Zusätzlich werden thematisch zusammenhängende Extractor-Klassen in einer Datei gesammelt.
Beispielsweise kann man `CommonFeatures` wie zum Beispiel Anzahl an Sternen in einer einzigen Datei sammeln.
Dadurch haben wir weniger Datei, die import Statements reduzieren sich und das ganze wird überschaubar und testbarer (nur eine Testdatei).
