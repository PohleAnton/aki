# Anwendung künstlicher Intelligenzen: Let AI Entertain You

Hier wird der Code für das Modul "Anwendung künstlicher Intelligenzen" dokumentiert. Dieses Repository enthält Implementierungen und Experimente zur automatisierten Generierung und Bewertung von Textinhalten mithilfe großer Sprachmodelle (LLMs).

## Links

- **Link zum Paper:** [Let AI Entertain You (PDF)](https://arxiv.org/pdf/2312.12457)
- **Weitere Literatur:** [LLM as a Judge (PDF)](https://arxiv.org/pdf/2306.05685)

> **Hinweis**: Relevant ist hier nur der Ordner `LetAIEntertainYou`.

## Inhaltsverzeichnis

- [Überblick](#überblick)
- [Vorgehen und Dateistruktur](#vorgehen-und-dateistruktur)
- [Verwendete Modelle und Experimente](#verwendete-modelle-und-experimente)
- [Ergebnisse der Modelle](#ergebnisse-der-modelle)
- [Fine-Tuning und Quantisierung](#fine-tuning-und-quantisierung)
- [Trainierte Modelle](#trainierte-modelle)

## Überblick

Aufgrund der eingeschränkten Verfügbarkeit öffentlicher Datensätze wurden synthetische Daten generiert. Diese Daten dienen als Grundlage für die Implementierung und Evaluierung verschiedener Modelle zur automatisierten Textbewertung und -generierung.

## Vorgehen und Dateistruktur

1. **Datenerzeugung**: Da die Datensätze nicht öffentlich sind, wurden zunächst synthetische Posts mithilfe eines Kontos bei *nextdoor* generiert.
   - **DataGen.py**: Diese Datei enthält die Skripte zur Generierung der synthetischen Daten über OpenAI API.
   - **Daten**: 2700 Posts wurden erstellt und in `./data` als CSV-Dateien gespeichert. Jede Datei enthält eine Spalte 'Posts' mit der gesamten Liste.

2. **Betreffzeilengenerierung**: Mit `RuleBasedGenerator.py` wurden regelbasierte Betreffzeilen generiert, die als Vergleichsdaten dienen.

3. **Experimente mit Modellen**: Verschiedene Modelle wurden getestet, darunter GPT-3, Llama3 und Vicuna.
   - Die Experimente ergaben, dass Llama3 zuverlässiger als GPT-3 und Vicuna ist, auch wenn es langsamer arbeitet. Dies ermöglichte eine verlässliche A/B-Datensatzbasis für Reward-Modelle.
   - **Ergebnisse des Experiments**:
     - *User-Befragung*: Zunächst wurde eine Umfrage angedacht. `./alt/create_survey.js` erzeugt aus einem GoogleSheet eine Google-Umfrage.
     - *LLM as a Judge*: Die Ergebnisse der Bewertung durch GPT-4 sind in folgenden Dateien gespeichert:
       - **Basisvergleich**: `./Models/Judgements.py`
       - **Pointwise-Bewertung**: `./Models/Judgements_AV.py`
       - **Pairwise-Bewertung**: `./Models/Judgements_Pair_AC.py`

4. **Stichproben-Ergebnisse**:
   - In verschiedenen Stichproben wurde festgestellt, dass GPT-4 eine Konsistenz von etwa 65% erreicht. Ein Bias zugunsten des ersten Eintrags wurde beobachtet.

## Verwendete Modelle und Experimente

Im Paper wurde deutlich, dass ein Vergleich für 900 Einträge durchgeführt wurde. Die Datenstruktur und die Modelle führten zu folgenden Ergebnissen:

- Vergleich für `Regel`, `Basis`, und `Best of N`:
  - *Regel*: 295
  - *Basis*: 327
  - *Best of N*: 278

- Vergleich für `Best of N – Regel – Basis`:
  - *Regel*: 260
  - *Basis*: 334
  - *Best of N*: 306

Besonders drastische Bewertungsunterschiede sind in `./Models/Judgements_Pair_AC.py` dokumentiert. 

### Training und Bewertung

Das Training und die Bewertung der Reward-Modelle erfolgte durchgehend mit dem regelbasierten Datensatz in der 1. und dem LLM-generierten Datensatz in der 2. Spalte. Dieser Ansatz ermöglicht konsistente Ergebnisse.

- **Pointwise-Modelle**: `./Models/Pointwise_BERT.py`
- **Pairwise-Modelle**: `./Models/Pairwise_BERT.py`
- **Rejection Sampling**: Die Methodik für das Rejection Sampling ist in den jeweiligen Modellen dokumentiert.

## Ergebnisse der Modelle

Die erzielten Ergebnisse im erneuten GPT-4 Vergleich:

- **Vor dem Training**:
  - *Regelbasiert*: 53,4%
  - *LLM generiert*: 46,6%

- **Pointwise – 20 Epochen**:
  - *Regelbasiert*: ca. 51%
  - *LLM generiert*: ca. 49%

- **Pairwise – 40 Epochen**:
  - *Regelbasiert*: ca. 52,3%
  - *LLM generiert*: ca. 47,7%

> Anmerkung: Im Paper wurde lediglich für 4 Epochen trainiert, jedoch führte hier das Pairwise-Verfahren erst nach 40 Epochen zu signifikanten Verbesserungen.

## Fine-Tuning und Quantisierung

Das Fine-Tuning wurde wie folgt durchgeführt:

- **Llama3 Fine-Tuning**:
  - In `./Models/TryLlamaAgain.py` wurde das Modell für 2 Epochen weitertrainiert, wobei nur der letzte Layer nicht eingefroren wurde.
  - Die Ergebnisse:
    - *Epoch 1, Average Loss*: 0.9336
    - *Epoch 2, Average Loss*: 0.8570

- **Quantisierung mit 4-Bit**: Es wurde auch mit der 4-Bit-Quantisierung experimentiert, allerdings ohne weiteren Erfolg im Training.

Alternativer Ansatz:
```bash
autotrain llm --train --project-name my-llm --model hiieu/Meta-Llama-3-8B-Instruct-function-calling-json-mode --data-path LetAIEntertainYou/data/test --peft --quantization int4 --lr 2e-4 --batch-size 8 --epochs 1 --trainer sft
