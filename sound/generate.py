"""Generate the game's original music loop and effects using the Python standard library."""

import math
from pathlib import Path
import random
import struct
import wave

RATE = 22050
OUT = Path(__file__).parent


def save(name, samples):
    peak = max(1.0, max(abs(sample) for sample in samples) / 0.85)
    with wave.open(str(OUT / name), "wb") as output:
        output.setparams((1, 2, RATE, 0, "NONE", "not compressed"))
        output.writeframes(b"".join(struct.pack("<h", round(sample / peak * 32767)) for sample in samples))


def note(buffer, start, length, midi, level, bass=False):
    frequency = 440 * 2 ** ((midi - 69) / 12)
    for i in range(int(length * RATE)):
        index = round(start * RATE) + i
        if index >= len(buffer):
            break
        t = i / RATE
        envelope = min(1, t / 0.012) * min(1, (length - t) / 0.08)
        decay = math.exp(-t * (2.5 if bass else 4))
        phase = 2 * math.pi * frequency * t
        tone = math.sin(phase) + 0.2 * math.sin(2 * phase) + 0.06 * math.sin(3 * phase)
        buffer[index] += level * envelope * decay * tone


def music():
    beat = 60 / 108
    buffer = [0.0] * round(32 * beat * RATE)
    chords = [(48, 60, 64, 67, 71), (45, 60, 64, 67, 69),
              (41, 57, 60, 64, 67), (43, 59, 62, 65, 69)]
    melody = [76, 79, 74, 71, 72, 76, 79, 76,
              77, 76, 72, 69, 74, 77, 79, 71]
    rng = random.Random(574)
    for bar in range(8):
        chord = chords[bar % 4]
        start = bar * 4 * beat
        for pulse, pitch in [(0, chord[0]), (2, chord[0] + 7)]:
            note(buffer, start + pulse * beat, beat * 1.4, pitch, 0.14, bass=True)
        for pulse in [0.5, 2.5]:
            for pitch in chord[1:]:
                note(buffer, start + pulse * beat, beat * 0.9, pitch, 0.045)
        for step in range(2):
            note(buffer, start + (step * 2 + 1) * beat, beat * 0.8,
                 melody[bar * 2 + step], 0.13)
        for pulse in range(4):
            offset = round((start + (pulse + 0.5) * beat) * RATE)
            previous = 0.0
            for i in range(round(0.055 * RATE)):
                noise = rng.uniform(-1, 1)
                buffer[offset + i] += (noise - previous) * 0.012 * math.exp(-i / (RATE * 0.012))
                previous = noise
    save("background.wav", buffer)


def effect(name, length, start_hz, end_hz):
    samples = []
    phase = 0.0
    for i in range(round(length * RATE)):
        t = i / RATE
        progress = t / length
        phase += 2 * math.pi * (start_hz + (end_hz - start_hz) * progress) / RATE
        envelope = min(1, t / 0.006) * (1 - progress) ** 2
        samples.append(math.sin(phase) * envelope * 0.5)
    save(name, samples)


if __name__ == "__main__":
    music()
    effect("jump.wav", 0.18, 430, 1050)
    effect("landing.wav", 0.10, 220, 90)
