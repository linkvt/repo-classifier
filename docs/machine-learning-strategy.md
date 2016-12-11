# Strategie
## Einfacher DecisionTree
Zuerst wird mit einem einfachen DecisionTree-Algorithmus gestartet.
Das sollen vor allem einen schnellen Start ermöglichen und damit schnell Ergebnisse liefern.
Die Probleme, die damiteinhergehen sind unterschiedlich:
- Wenn wir eine Vielzahl von Features haben, kann der Baum unbalanciert aufgebaut werden und die Klassifizierung 
durch viele Nodes stark verschlechtern
- Probleme mit Overfitting, wenn Features nicht gut gewählt sind

## Mehrere Bäume verbinden (Ensemble Learning)
Falls wir merken, dass wir zu viele Features haben und diese sinnvoller in eigenen Bäumen abgearbeitet werden sollten, 
wechseln wir zu dieser Strategie.
Dabei werden mehrere Bäume aufgebaut, die anschließend wieder zusammengefügt werden 
(möglicherweise auch mit Gewichtungen etc).
Hierbei müssen wir dann aufpassen, welche Baumgruppen wir erzeugen, d.h. welche Features passen zusammen.

## Feature Selection
Eine weitere Möglichkeit, um viele Features dezimieren zu können, ist die Auswahl von guten Features.
Dabei wird geprüft, wie wahrscheinlich bestimmte Features vorkommen. Liegen diese unter einem Schwellwert, können 
sie möglicherweise ausgeschlossen werden, da sie keinen relevanten Beitrag liefern.

## Neuronale Netze
Falls ein DecisionTree nicht für unsere Aufgabe ausreicht, wird versucht auf NN zu wechseln.
Herausforderungen hierbei können z.B. die entstehenden Laufzeit bzw. Trainingsaufwände sein.
Aber auch die geeignete Wahl von hidden layers und hidden neurons wird hinzukommen.

