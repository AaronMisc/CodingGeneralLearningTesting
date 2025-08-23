import pygame
import math
import array
import time

# Initialize pygame mixer
sample_rate = 44100
pygame.mixer.init(frequency=sample_rate, size=-16, channels=1)

def generate_tone(frequency, duration, volume=0.5):
    """Generate a tone as a pygame Sound object."""
    num_samples = int(duration * sample_rate)
    amplitude = int(volume * 32767)
    samples = array.array("h")
    
    for i in range(num_samples):
        sample = int(amplitude * math.sin(2 * math.pi * frequency * i / sample_rate))
        samples.append(sample)
    
    return pygame.mixer.Sound(buffer=samples.tobytes())

def note_to_freq(note_name):
    # Define the standard frequencies for each note in the chromatic scale
    note_frequencies = {
        'C': 261.63, 'C#': 277.18, 'D': 293.66, 'D#': 311.13,
        'E': 329.63, 'F': 349.23, 'F#': 369.99, 'G': 392.00,
        'G#': 415.30, 'A': 440.00, 'A#': 466.16, 'B': 493.88
    }

    # Extract the note and octave
    note = note_name[:-1]
    octave = int(note_name[-1])

    # Get the frequency for the note (without octave adjustment)
    base_freq = note_frequencies[note]

    # Calculate the frequency based on the octave (A4 = 440 Hz is the reference)
    freq = base_freq * 2 ** (octave - 4)

    return freq

melody = [
    ("R", 3), 
    ("C4", 2.25), ("B3", 0.25), ("C4", 0.25), ("D4", 0.25), ("C4", 0.25), ("B3", 0.25), ("A3", 0.25), ("C4", 0.5), ("C4", 0.25), ("A3", 0.25), ("C4", 1.5),
    ("B3", 0.25), ("C4", 0.25), ("A3", 0.25), ("G3", 0.25), ("E3", 0.25), ("F3", 0.25), ("G3", 2.25),
    ("F3", 0.25), ("E3", 0.25), ("D3", 0.25), ("E3", 0.25), ("F3", 0.25), ("G3", 0.25), ("A3", 0.25), ("G3", 2.25),
    ("A3", 0.25), ("B3", 0.25), ("A3", 0.25), ("G3", 0.25), ("F3", 0.25), ("E3", 0.25), ("D3", 0.25), ("E3", 0.25), ("D3", 0.25), ("C3", 2),
]
# Play the melody
for note, duration in melody:
    if note == 'R':  # Rest
        time.sleep(duration)
    else:
        tone = generate_tone(note_to_freq(note), duration, 1)
        tone.play()
        time.sleep(duration)

# Keep program running briefly to let the last note finish
pygame.time.delay(500)

