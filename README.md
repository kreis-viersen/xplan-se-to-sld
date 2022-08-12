# xplan-se-to-sld
SE-Style-Dateien der XPlanBox in SLD umwandeln

Das Skript erzeugt in einem Verzeichnis für jede SE-Datei eine SLD-Datei mit folgenden Änderungen:

- Ergänze SLD-"Hülle"
- Entferne substrings `xplan:` und `Code`, so wird z.B. aus xplan:allgArtDerBaulNutzungCode -> allgArtDerBaulNutzung.
  Dann passt das zu den Feldnamen nach dem XPlanGML Import in QGIS (attributbasiertes Styling).
- Verwende uom-Attribut gemäß SE-Spezifikation (ersetze "meter" durch "http://www.opengeospatial.org/se/units/metre"), siehe: https://gitlab.opencode.de/diplanung/ozgxplanung/-/issues/1#note_2177<br>Anmerkung: Dieses wird von QGIS erst ab Version 3.26 in `Meter im Maßstab` umgesetzt