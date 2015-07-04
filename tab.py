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

# Initialize the MIDIFile object (with 1 track)
time = 0
duration = 10
volume = 100
song = MIDIFile(1)
song.addTrackName(0, time, "pianized_guitar_tab.")
song.addTempo(0, time, beats_per_minute)

# The root-pitches of the guitar
guitar = list(reversed([52, 57, 62, 67, 71, 76])) # Assume EADGBe tuning
def add_note(string, fret):
    song.addNote(0, string, guitar[string] + fret, time, duration, volume)

# Process the entire tab
for current in range(0, len(lines), 6):  # The current base string
    for i in range(len(lines[current])): # The position in the current string
        time += 1
        for s in range(6):               # The number of the string
            c = lines[current + s][i]
            try: next_char = lines[current + s][i + 1]
            except: next_char = ''
            if c in '-x\\/bhp':
                # Ignore these characters for now
                continue
            elif c.isdigit():
                # Special case for fret 10 and higher
                if next_char.isdigit():
                    c += next_char
                    lines[current + s] = lines[current + s][:i+1] + '-' + lines[current + s][i+2:]
                # It's a note, play it!
                add_note(s, int(c))
            else:
                # Awww
                time -= 1
                break

# And write it to disk.
def save():
    binfile = open('song.mid', 'wb')
    song.writeFile(binfile)
    binfile.close()
    print('Done')
try:
    save()
except:
    print('Error writing to song.mid, try again.')
    input()
    try:
        save()
    except:
        print('Failed!')

