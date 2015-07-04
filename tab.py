from midiutil.MidiFile3 import MIDIFile
import sys

# Read the relevant lines of the file
lines = []
if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = 'mattys-tune.txt'
with open(filename) as f:
    for line in f:
        if len(line) > 3 and (line[1] == '|' or line[2] == '|'):
            line = line.replace('\n', '')
            lines.append(line)
assert len(lines) % 6 == 0

# Initialize all the variables used in a note (except pitch)
track = 0
time = 0
channel = 0
duration = 10
volume = 100

# Create the MIDIFile Object with 1 track
song = MIDIFile(1)
song.addTrackName(track, time, "pianized_guitar_tab.")
song.addTempo(track, time, 120 * 6)

# The root-pitches of the guitar
guitar = list(reversed([52, 57, 62, 67, 71, 76])) # Assume EADGBe tuning
def add_note(string, fret):
    song.addNote(track, channel, guitar[i] + fret, time, duration, volume)

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

# Make sure the song doesn't end too soon
time += 20
#add_note(0, -guitar[0])

# And write it to disk.
try:
    binfile = open('song.mid', 'wb')
    song.writeFile(binfile)
    binfile.close()
except:
    print('Error writing to song.mid!')
    input()

