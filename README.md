# Projet P7 – Développez une preuve de concept

## 🎯 Objectif

Ce projet vise à démontrer la faisabilité d'une preuve de concept (PoC) dans le cadre d’une comparaison de modèles de transcription musicale automatique.

Nous cherchons à comparer un algorithme récent, **Basic Pitch** (Spotify), à une baseline plus ancienne, **Melodia**, pour la transcription MIDI à partir d'enregistrements audio. Le tout est appliqué au **dataset MAESTRO**, un jeu de données de performances pianistiques de haute qualité.

---

## 📂 Contenu du dépôt

- `Milan_Nicolas_1_Plan_prévisionnel_022025.pdf` : planification du projet
- `Milan_Nicolas_2_notebook_022025.ipynb` : pipeline d’analyse et d’évaluation
- `Milan_Nicolas_3_streamlit_022025.py` : application interactive (Streamlit)
- `Milan_Nicolas_4_Note_Méthodologique_022025.pdf` : note explicative complète
- `Milan_Nicolas_5_presentation_022025.pdf` : présentation finale du projet

---

## 📚 Dataset utilisé : MAESTRO

Le dataset **MAESTRO** (MIDI and Audio Edited for Synchronous Tracks and Organization) contient plus de 200 heures d’enregistrements pianistiques alignés précisément entre audio et MIDI (~3ms de décalage max).

- Performances issues de la compétition *International Piano-e-Competition*
- Instruments utilisés : Yamaha Disklavier (captures haute fidélité de vélocité, pédales, etc.)
- Audio qualité CD : 44,1–48 kHz, 16-bit stéréo
- Structuration en ensembles : train / validation / test
- Dominance de musique classique (XVIIᵉ au XXᵉ siècle)

Plus d'infos : [MAESTRO Dataset (Magenta)](https://magenta.tensorflow.org/datasets/maestro)

---

## 🧠 Modèles comparés

### Basic Pitch (Spotify)
Un modèle léger de transcription musicale basé sur des **CNN** optimisés :
- Prédiction simultanée des **onsets**, **hauteurs multiples** et **activations**
- Très bon compromis entre **précision** et **efficacité temps réel**
- Convient aux environnements avec ressources limitées

### Melodia (Baseline)
- Méthode heuristique par analyse spectrale
- Implémentée via **sonic-annotator** (CLI)
- Ne supporte pas la polyphonie (1 note à la fois)

---

## 🔬 Méthodologie

1. **Prétraitement**
   - Extraction des chemins audio + MIDI via `maestro-v3.0.0.csv`
   - Conversion des fichiers audio en **spectrogrammes CQT** via `librosa`
   - Normalisation et segmentation temporelle

2. **Prédiction**
   - Basic Pitch : utilisation de `predict(audio_path)` → MIDI
   - Melodia : extraction de pitch → conversion brute en MIDI

3. **Évaluation**
   - Comparaison note-à-note sur les fichiers MIDI prédits
   - Création d’un DataFrame de résultats par morceau et par métrique

---

## 📏 Métriques

- **F1-score** entre prédiction et vérité terrain (alignement MIDI)
- **Notes Correct** : évaluation de la justesse note à note

---

## 📊 Résultats

- **Basic Pitch** surpasse **Melodia** de façon globale
- Aucune instance où Basic Pitch fait moins bien
- Courbes de performances par morceau montrent une tendance cohérente
- Une écoute humaine reste essentielle pour juger la qualité subjective des transcriptions

---

## 🔍 Limites et améliorations possibles

- Les modèles de transcription ont du mal avec les enregistrements **complexes ou cacophoniques**
- L’alignement temporel est parfois **suffisant en métriques mais désagréable à l’oreille**
- Une **post-correction fine du timing** pourrait améliorer la musicalité
- Pas de sélection de features possible : **toutes les fréquences sont significatives**
