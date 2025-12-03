import mido # You might need: pip install mido
import os

# General MIDI Instrument Names (Program Numbers 1-128, list index 0-127)
GM_INSTRUMENTS = [
    "Acoustic Grand Piano", "Bright Acoustic Piano", "Electric Grand Piano", "Honky-tonk Piano",
    "Electric Piano 1", "Electric Piano 2", "Harpsichord", "Clavinet",
    "Celesta", "Glockenspiel", "Music Box", "Vibraphone",
    "Marimba", "Xylophone", "Tubular Bells", "Dulcimer",
    "Drawbar Organ", "Percussive Organ", "Rock Organ", "Church Organ",
    "Reed Organ", "Accordion", "Harmonica", "Tango Accordion",
    "Acoustic Guitar (nylon)", "Acoustic Guitar (steel)", "Electric Guitar (jazz)", "Electric Guitar (clean)",
    "Electric Guitar (muted)", "Overdriven Guitar", "Distortion Guitar", "Guitar Harmonics",
    "Acoustic Bass", "Electric Bass (finger)", "Electric Bass (pick)", "Fretless Bass",
    "Slap Bass 1", "Slap Bass 2", "Synth Bass 1", "Synth Bass 2",
    "Violin", "Viola", "Cello", "Contrabass",
    "Tremolo Strings", "Pizzicato Strings", "Orchestral Harp", "Timpani",
    "String Ensemble 1", "String Ensemble 2", "Synth Strings 1", "Synth Strings 2",
    "Choir Aahs", "Voice Oohs", "Synth Voice", "Orchestra Hit",
    "Trumpet", "Trombone", "Tuba", "Muted Trumpet",
    "French Horn", "Brass Section", "Synth Brass 1", "Synth Brass 2",
    "Soprano Sax", "Alto Sax", "Tenor Sax", "Baritone Sax",
    "Oboe", "English Horn", "Bassoon", "Clarinet",
    "Piccolo", "Flute", "Recorder", "Pan Flute",
    "Blown Bottle", "Shakuhachi", "Whistle", "Ocarina",
    "Lead 1 (square)", "Lead 2 (sawtooth)", "Lead 3 (calliope)", "Lead 4 (chiff)",
    "Lead 5 (charang)", "Lead 6 (voice)", "Lead 7 (fifths)", "Lead 8 (bass + lead)",
    "Pad 1 (new age)", "Pad 2 (warm)", "Pad 3 (polysynth)", "Pad 4 (choir)",
    "Pad 5 (bowed)", "Pad 6 (metallic)", "Pad 7 (halo)", "Pad 8 (sweep)",
    "FX 1 (rain)", "FX 2 (soundtrack)", "FX 3 (crystal)", "FX 4 (atmosphere)",
    "FX 5 (brightness)", "FX 6 (goblins)", "FX 7 (echoes)", "FX 8 (sci-fi)",
    "Sitar", "Banjo", "Shamisen", "Koto",
    "Kalimba", "Bag pipe", "Fiddle", "Shanai",
    "Tinkle Bell", "Agogo", "Steel Drums", "Woodblock",
    "Taiko Drum", "Melodic Tom", "Synth Drum", "Reverse Cymbal",
    "Guitar Fret Noise", "Breath Noise", "Seashore", "Bird Tweet",
    "Telephone Ring", "Helicopter", "Applause", "Gunshot"
]

def midi_to_text(input_filename):
    # Automatically create an output filename, e.g., "riff.mid" -> "riff_analysis.txt"
    base_name = os.path.splitext(input_filename)[0]
    output_filename = f"{base_name}_analysis.txt"

    mid = mido.MidiFile(input_filename)

    with open(output_filename, 'w') as f:
        f.write(f"--- Analysis of {input_filename} ---\n\n")
        f.write(f"Type: {mid.type}\n")
        f.write(f"Length: {mid.length:.2f} seconds\n")
        f.write(f"Ticks per beat: {mid.ticks_per_beat}\n")
        
        for i, track in enumerate(mid.tracks):
            f.write("\n" + "="*40 + "\n")
            
            # Find the instrument for this track
            instrument_name = "Unknown (Default)"
            for msg in track:
                if msg.type == 'program_change':
                    # MIDI channels 1-16, but channel 10 (index 9) is for percussion
                    if msg.channel == 9:
                        instrument_name = "Drumkit"
                    else:
                        instrument_name = GM_INSTRUMENTS[msg.program]
                    break # Found it, no need to look further

            f.write(f"Track {i}: {track.name} (Instrument: {instrument_name})\n")
            f.write("-" * 40 + "\n")

            curr_time = 0
            for msg in track:
                curr_time += msg.time
                if msg.type == 'note_on' and msg.velocity > 0:
                    # Convert MIDI note number to Note Name (e.g., 60 -> C4)
                    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
                    octave = (msg.note // 12) - 1
                    note = note_names[msg.note % 12]
                    f.write(f"Time: {curr_time} | Note: {note}{octave} (MIDI {msg.note}) | Vel: {msg.velocity}\n")
    
    print(f"Analysis complete. Output saved to '{output_filename}'")

# Replace with your actual filename
midi_to_text("riff.mid") 