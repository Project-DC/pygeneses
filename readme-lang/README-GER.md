
# PyGeneses

[![GitHub](https://img.shields.io/github/license/Project-DC/pygeneses)](https://github.com/Project-DC/pygeneses/blob/master/LICENSE)  ![GitHub stars](https://img.shields.io/github/stars/Project-DC/pygeneses?style=plastic)  ![GitHub contributors](https://img.shields.io/github/contributors/Project-DC/pygeneses)  ![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)  ![GitHub last commit](https://img.shields.io/github/last-commit/Project-DC/pygeneses)

<p align="justify">PyGeneses ist ein auf PyTorch basierendes Deep Reinforcement Learning Framework, das Anwendern hilft, künstliche Wirkstoffe in bio-inspirierten Umgebungen zu simulieren. Das Framework bietet eingebaute Deep-RL-Algorithmen und die Visualisierung von Trainingsergebnissen in einem interaktiven Dashboard. Die Umgebungen sind eine vereinfachte Abstraktion unserer realen Welt, Agenten werden in diese Welt versetzt und können miteinander und mit der Umgebung interagieren.</p>

Die Stärke von PyGeneses ist seine saubere und einfache API, die:
- Erlaubt es einem Benutzer, eine eigene Simulation auszuführen, auch wenn er keine Kenntnisse über RL oder DL hat.
- Ermöglicht es einem Benutzer mit Erfahrung im Bereich Deep RL, das Modell und die Parameter umfassend zu optimieren.
<p align="justify">Was an PyGeneses spannend ist, fragen Sie, nun, mit PyGeneses können Sie eine funktionierende Simulation erstellen, indem Sie ohne jegliche Vorkenntnisse nur 2 Zeilen schreiben! PyGeneses bietet auch Werkzeuge, die Ihnen helfen, die Ergebnisse mit minimalem Aufwand zu visualisieren. Worauf warten Sie also, installieren Sie PyGeneses noch heute und werden Sie zum Gott Ihrer Schöpfung</p>

## Prima vita

<p align="justify">Prima vita ist eine Spezies künstlich simulierter Wesen, die im Rahmen des Projekts DC geschaffen wurde. Dieses Repository enthält eine in Pygame erstellte Simulationsumgebung, die mit Algorithmen des Deep Reinforcement Learning verwendet werden soll, um die Entwicklung von Prima Vita herauszufinden.</p>

## Installation

PyGeneses kann mittels pip entweder in Ihrem lokalen System oder auf einer Cloud-basierten Plattform installiert werden. Die Installationsschritte sind für die Cloud- und die lokale Installation gleich.

```bash
user@programmer~:$ pip install git+https://github.com/Project-DC/pygeneses
```

Da PyGeneses noch nicht in pypi verfügbar ist, müssen Sie den github-Repo-Link mit pip verwenden, um es vorerst zu installieren.

## Über die Pakete   
<p align="justify">Ab Version 0.1-beta besteht die Architektur von PyGeneses aus 4 Hauptmodulen. Jedes dieser Module bietet ein einzigartiges Merkmal oder eine einzigartige Funktionalität für das Framework. Beginnen wir also mit einer kurzen Einführung zu jedem dieser Module.</p>      

1. **pygeneses.envs**    
<p align="justify">Mit diesem Modul können Sie die integrierten bio-inspirierten Umgebungen erstellen, konfigurieren und optimieren. Im Moment steht nur eine einzige Umgebung mit dem Namen Prima Vita (First Life) zur Verfügung, aber es werden bald noch mehr folgen! Damit können Sie die gesamte Umgebung und die Spezies in nur wenigen Codezeilen einrichten und bietet sowohl API auf hoher Ebene als auch Kontrolle über die Umgebung auf niedriger Ebene. Die Schulung im Umgang mit der API umfasst die Protokollierung jeder Aktion eines Agens, so dass sie mit VitaBoard studiert werden kann.</p>   

2. **pygeneses.models** 
<p align="justify">Das Modul "Modelle" ermöglicht es uns, die neuronalen Netze zu importieren, die die Art benutzt, um zu lernen, was zu tun ist. Zur Zeit wird nur die Implementierung des Standardmodells (REINFORCE) zur Verfügung gestellt, aber wir werden ab v0.2 Unterstützung für benutzerdefinierte steckbare Netzwerke hinzufügen.</p>

3. **pygeneses.hypertune**    
<p align="justify">Das 'HyperTune'-Paket erlaubt es uns, verschiedene Hyperparameter zu konfigurieren und zu testen, die wir für eine Umgebung und Spezies bereitstellen können (eine Liste von Hyperparametern finden Sie im Abschnitt "Klassen" dieser Dokumentation). Dies beinhaltet das Testen einzelner Hyperparameter, Rastersuche und randomisierte Suche. Auf diese Weise können wir den besten Satz von Hyperparametern zur Darstellung eines Verhaltenstyps finden. Dadurch entstehen auch Protokolle, die wir mit Vitaboard untersuchen können.</p>

4. **pygeneses.vitaboard**   
<p align="justify">Vitaboard bietet ein fortschrittliches, interaktives Dashboard zur Untersuchung von Agenten nach der Ausbildungsphase. Nach dem Tod jedes Agenten werden seine Aktionen in eine Protokolldatei geschrieben. Und Vitaboard ermöglicht es uns, das Leben des Agenten zu visualisieren. Es bietet uns einen Lebensvisualisierer, Gruppenstatistiken und einen Visualisierer für die genetische Geschichte. Es erlaubt uns, die Verhaltensweisen zu identifizieren und zu verstehen, die ein Agent bei der Interaktion mit der Umgebung oder mit anderen Agenten in der Umgebung zeigt.</p>

## Beitragend

Die folgenden Ressourcen sind ein guter Ort, um mehr über PyGeneses zu erfahren:-

1.  Einführung in PyGeneses  [Dev.to](https://dev.to/projectdc/introduction-to-pygeneses-26oc),  [Medium](https://medium.com/oss-build/introduction-to-pygeneses-1ed08a1a076c).
2.  Erste Schritte mit PyGeneses [Dev.to](https://dev.to/projectdc/getting-started-with-pygeneses-1co2),  [Medium](https://medium.com/oss-build/getting-started-with-pygeneses-839ff6b3023f).
3. Studieren von Protokollen mit VitaBoard [Dev.to](https://dev.to/projectdc/guidelines-about-vitaboard-2m36), [Medium](https://medium.com/oss-build/studying-logs-using-vitaboard-41e13e3197d7)

Abgesehen von diesen Blog-Einträgen können Sie auch die  [offizielle Dokumente](https://project-dc.github.io/docs).

Bevor Sie weitergehen, gehen Sie bitte die Regeln in  [CONTRIBUTING.md](../CONTRIBUTING.md)

## Lizenz

PyGeneses ist unter der GNU GPL v3 lizenziert [LIZENZ](../LICENSE)

## Das Team

- [Siddhartha Dhar Choudhury](https://github.com/frankhart2018)
- [Pranshul Dobriyal](https://github.com/PranshulDobriyal)
- [Dhairya Jain](https://github.com/dhairyaj)
- [Farhad Bharucha](https://github.com/Farhad1234)
- [Aayush Agarwal](https://github.com/Aayush-99)
