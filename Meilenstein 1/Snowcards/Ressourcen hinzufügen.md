# {Req-ID} {Events/UCS}

| Req-ID | Req-Type | Events/UCs          |
|--------|----------|---------------------|
| 4.1    |funktional|Ressourcen hinzufügen|

### Description
Funktion zum Einfügen von Ressourcen in das System für Nutzer und Administratoren.

### Rationale
Der Nutzer soll Ressourcen und Metadaten (direct oder automatisch) in ein Eingabefenster geben. Wenn alle benötigten Informationen
vorhanden sind, wird ein hinzufügverfahren begonnen. 
Admin => direkt hinzufügen
Nutzer=> Verifizierungsverfahren

### Originator
Auftraggeber

### Fit Criterion
Bei unzureichenden eingaben erscheint innerhalb 1 Sekunde eine Fehlermeldung und das Eingabefenster wird nicht geschlossen.
Wenn die Eingabe akzeptiert wird:
Admin: Der neue Eintrag ist innerhalb von 3 Sekunden angelegt und öffentlich sichtbar.
Nutzer: Der neue Eintrag ist innerhalb von 3 Sekunden angelegt, bleibt jedoch vorerst versteckt.
	Der Server erhält innerhalb von 10 sekunden eine Versandbestätigung für alle 5 Nutzer.
	Bei mehrheitlicher Zustimmung wird der Eintrag automatisch innerhalb von 3 Sekunden öffentlich sichtbar

#### Ratings
| Customer Satisfation | Customer Dissatisfation | Priority |
|----------------------|-------------------------|----------|
| ...                  | ...                     | ...      |

### Supporting Material
...

### Conflicts
...

### History
- Erstellt am 21.8.24 von Robert Landgraf

---
