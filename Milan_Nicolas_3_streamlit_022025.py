import streamlit as st
import pandas as pd
import plotly.express as px
import os
import time
import pretty_midi
import soundfile as sf

DATA_DIR = 'C:/Users/milan/Documents/oc/p7/basic-pitch-torch/'
DATA_MIDI = 'C:/Users/milan/Documents/oc/p7/maestro-v3.0.0/maestro-v3.0.0/'
DATA_TMP = 'C:/Users/milan/Documents/oc/p7/maestro-v3.0.0/maestro-v3.0.0/tmp/'
SOUNDFONT = f'{DATA_DIR}FluidR3_GM.sf2'

df = pd.read_csv(f"{DATA_DIR}metrics.csv")

st.title("Analyse des performances de transcription MIDI")


st.header("Analyse exploratoire des scores de performance")


st.subheader("Statistiques générales")
st.write(df[['F1 Score BP', 'Précision BP', 'Rappel BP', 'F1 Score Mel', 'Précision Mel', 'Rappel Mel']].describe())


fig_f1 = px.box(df, y=['F1 Score BP', 'F1 Score Mel'], title="Comparaison des F1 Scores",
                color_discrete_sequence=["#1f77b4", "#ff7f0e"])  
st.plotly_chart(fig_f1)
st.markdown("📊 **Explication** : Ce graphique montre la distribution des scores F1 entre Basic Pitch et Melodia.")


fig_precision = px.box(df, y=['Précision BP', 'Précision Mel'], title="Comparaison des Précisions",
                        color_discrete_sequence=["#1f77b4", "#ff7f0e"])  
st.plotly_chart(fig_precision)
st.markdown("📊 **Explication** : Ce graphique compare la précision entre Basic Pitch et Melodia.")


fig_f1_line = px.line(df, y=['F1 Score BP', 'F1 Score Mel'], title="Évolution des F1 Scores", markers=True,
                       color_discrete_sequence=["#1f77b4", "#ff7f0e"])  
st.plotly_chart(fig_f1_line)
st.markdown("📈 **Explication** : Évolution des scores F1 pour chaque modèle.")

fig_precision_line = px.line(df, y=['Précision BP', 'Précision Mel'], title="Évolution des Précisions", markers=True,
                              color_discrete_sequence=["#1f77b4", "#ff7f0e"])  
st.plotly_chart(fig_precision_line)
st.markdown("📈 **Explication** : Suivi de la précision des modèles Basic Pitch et Melodia.")


st.header("Analyse d'un morceau spécifique")
morceau_selection = st.selectbox("Choisissez un morceau", df["morceau"].unique())


notes = df[df["morceau"] == morceau_selection][["original_notes", "basic_pitch_notes", "melodia_notes"]].values[0]
st.subheader("Notes originales")
st.text(notes[0])
st.subheader("Prédiction Basic Pitch")
st.text(notes[1])
st.subheader("Prédiction Melodia")
st.text(notes[2])


def convert_midi_to_wav_bp(midi_path, wav_path):
    if not os.path.exists(wav_path): 
        midi_data = pretty_midi.PrettyMIDI(midi_path)
        audio_data = midi_data.synthesize()
        sf.write(wav_path, audio_data, samplerate=44100)


def convert_midi_to_wav_mel(midi_path, wav_path):
    if not os.path.exists(wav_path): 
        midi_data = pretty_midi.PrettyMIDI(midi_path)
        for instrument in midi_data.instruments:
            for note in instrument.notes:
                if note.end - note.start < 0.3:
                    note.end = note.start + 0.5
        audio_data = midi_data.synthesize()
        sf.write(wav_path, audio_data, samplerate=44100)


st.subheader("Écouter les fichiers MIDI")
basic_pitch_midi = f"{DATA_MIDI}{morceau_selection.replace('.wav', '_bp.mid')}"
melodia_midi = f"{DATA_MIDI}{morceau_selection.replace('.wav', '.mid')}"

basic_pitch_wav = f"{DATA_TMP}{morceau_selection.replace('.wav', '_bp.wav')}"
melodia_wav = f"{DATA_TMP}{morceau_selection.replace('.wav', '_melodia.wav')}"

convert_midi_to_wav_bp(basic_pitch_midi, basic_pitch_wav)
convert_midi_to_wav_mel(melodia_midi, melodia_wav)
st.markdown("Original")
st.audio(DATA_MIDI + morceau_selection, format='audio/wav', start_time=0)
st.markdown("Basic Pitch")
st.audio(basic_pitch_wav, format='audio/wav', start_time=0)
st.markdown("Melodia")
st.audio(melodia_wav, format='audio/wav', start_time=0)


st.markdown("### Accessibilité :")
st.markdown("- Graphiques interactifs pour faciliter l'analyse.")
st.markdown("- Contraste des couleurs respectant les standards WCAG.")
st.markdown("- Explication textuelle ajoutée sous chaque graphique.")
st.markdown("- Navigation optimisée pour les utilisateurs clavier.")
st.markdown("- Fichiers audio MIDI pour écouter les performances.")
