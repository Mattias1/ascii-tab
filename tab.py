from midiutil.MidiFile3 import MIDIFile
import sys

# Read the relevant lines of the file
lines = []
if len(sys.argv) > 1:
    filename = sys.argv[1]
    try:
        beats_per_minute = 60 / float(sys.argv[2])
    except:
        beats_per_minute = 756
else:
    filename = 'mattys-tune.txt'
    beats_per_minute = 756
with open(filename) as f:
    for line in f:
        if len(line) > 3 and (line[1] == '|' or line[2] == '|'):
            line = line.replace('\n', '')
            lines.append(line)
assert len(lines) % 6 == 0

# Initialize all the variables used in a note (except pitch)
time = 0
duration = 10
volume = 100

# Create the MIDIFile Object with 1 track
song = MIDIFile(1)
song.addTrackName(0, time, "pianized_guitar_tab.")
song.addTempo(0, time, beats_per_minute)

# The root-pitches of the guitar
guitar = list(reversed([52, 57, 62, 67, 71, 76])) # Assume EADGBe tuning
def add_note(string, fret):
    song.addNote(0, string, guitar[i] + fret, time, duration, volume)

# Process the entire tab
for currentline in range(0, len(lines), 6):
    for chars in zip(*lines[currentline : currentline + 6]):
        time += 1
        for i, c in enumerate(chars):
            if c in '-x\\/bhp':
                # Ignore these characters for now
                continue
            elif c.isdigit():
                # It's a note, play it!
                add_note(i, int(c))
            else:
                # Awww
                time -= 1
                break

# And write it to disk.
try:
    binfile = open('song.mid', 'wb')
    song.writeFile(binfile)
    binfile.close()
    print('Done')
except:
    print('Error writing to song.mid, try again.')
    input()
    try:
        binfile = open('song.mid', 'wb')
        song.writeFile(binfile)
        binfile.close()
        print('Done')
    except:
        print('Failed!')

