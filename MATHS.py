import pandas as pd
from midiutil import MIDIFile

# -------------------------
# Load climate data
# -------------------------
url = "https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv"
df = pd.read_csv(url, skiprows=1)

# Select only required columns

data = df[["Year", "J-D"]].copy()
data["Temp"] = pd.to_numeric(data["J-D"], errors="coerce")
data = data.dropna()
# -------------------------
# Convert temperature to pitch
# -------------------------
min_temp = data["Temp"].min()
max_temp = data["Temp"].max()

def temp_to_pitch(temp):
    return int(60 + (temp - min_temp) / (max_temp - min_temp) * 24)

# -------------------------
# Create MIDI music
# -------------------------
midi = MIDIFile(1)
track = 0
time = 0

midi.addTrackName(track, time, "Climate Sonification")
midi.addTempo(track, time, 60)

for temp in data["Temp"]:
    pitch = temp_to_pitch(temp)
    midi.addNote(track, 0, pitch, time, 1, 80)
    time += 1

# -------------------------
# Save the music file
# -------------------------
with open("climate_music.mid", "wb") as f:
    midi.writeFile(f)

print("Done! Music saved as climate_music.mid")
