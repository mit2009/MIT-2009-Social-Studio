"""Small, band-limited electronic voices for the club arrangement; no samples or vocals."""

import numpy as np
from scipy.signal import butter, sosfilt

from ..media import SAMPLE_RATE

VOICES = {"synth_pluck", "club_kick", "clap"}


def voice(event):
    kind, velocity = event["instrument"], event["velocity"] / 100
    if kind == "synth_pluck":
        length = event["duration"] + 0.22
        t = np.arange(round(length * SAMPLE_RATE)) / SAMPLE_RATE
        frequency = 440 * 2 ** ((event["midi"] - 69) / 12)
        result = np.zeros((len(t), 2))
        # Detuned band-limited partials: a bright attack closes into a warm body.
        for channel, cents in enumerate((-4, 4)):
            for harmonic in range(1, 19):
                f = frequency * harmonic * 2 ** (cents / 1200)
                if f > SAMPLE_RATE * 0.44:
                    break
                brightness = np.exp(-t * (harmonic - 1) * 4.6) / harmonic
                result[:, channel] += np.sin(2 * np.pi * f * t) * brightness
            result[:, channel] += 0.30 * np.sin(2 * np.pi * frequency * t)
        envelope = np.minimum(1, t / 0.003) * np.exp(-t * 2.1)
        envelope *= np.exp(-np.maximum(t - event["duration"], 0) * 24)
        envelope *= np.minimum(1, np.maximum(0, (length - t) / 0.012))
        result = np.tanh(result * 0.9) * (envelope * 0.27 * velocity)[:, None]
        return result
    # A fixed per-onset seed varies percussion reproducibly.
    rng = np.random.default_rng(round(event["start"] * 100000) + event["midi"])
    length = 0.30 if kind == "club_kick" else 0.23
    t = np.arange(round(length * SAMPLE_RATE)) / SAMPLE_RATE
    if kind == "club_kick":
        phase = 2 * np.pi * (51 * t + 90 * 0.013 * (1 - np.exp(-t / 0.013)))
        body = np.sin(phase) * np.exp(-t * 15)
        click = rng.normal(0, 1, len(t)) * np.exp(-t * 850) * 0.12
        result = np.tanh(1.4 * body + click) * 0.46 * velocity
        return np.column_stack((result, result))
    noise = rng.normal(0, 1, (len(t), 2))
    noise = sosfilt(butter(2, [950, 9200], btype="bandpass", fs=SAMPLE_RATE, output="sos"), noise, axis=0)
    envelope = np.zeros(len(t))
    for delay, amplitude in ((0, 0.7), (0.009, 0.8), (0.019, 1.0)):
        envelope += np.where(t >= delay, np.exp(-np.maximum(t - delay, 0) * 120) * amplitude, 0)
    envelope += 0.3 * np.exp(-t * 23)
    return np.tanh(noise * 0.8) * (envelope * 0.23 * velocity)[:, None]
