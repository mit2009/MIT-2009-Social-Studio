"""Build a local, portable listening sheet; no hosting, uploads or feedback collection."""

import argparse
import html
import json
import shutil
import subprocess
import zipfile
from pathlib import Path

import numpy as np

from mit2009_studio import media

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("session", type=Path)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    session, source, out = args.session.resolve(), args.source.resolve(), args.output.resolve()
    sweep = session / "orchestration-sweep-01"
    verification = json.loads((sweep / "verification.json").read_text())
    assert verification["complete"] and media.digest(source) == verification["source_sha256"]
    out.mkdir(parents=True, exist_ok=False)
    (out / "audio").mkdir()
    staging = sweep / "share-staging"
    staging.mkdir(exist_ok=False)
    source_audio = media.read_audio(source, 60)
    opening = media.playback_start(source_audio)
    media.write_audio(staging / "seed.wav", source_audio[opening:])
    tracks = [
        {"label": "Seed", "name": "Original musical idea", "source": staging / "seed.wav"},
        {"label": "Guide", "name": "Plain melody reference", "source": session / "melody-check.wav"},
        {
            "label": "A",
            "name": "Funk band / closer following",
            "source": session / "mrt2-06-closer/audio.wav",
        },
        {"label": "B", "name": "Funk band / higher lead", "source": session / "mrt2-07-lead/audio.wav"},
        {"label": "C", "name": "Dance-pop direction", "source": session / "mrt2-08-dance/audio.wav"},
    ]
    tracks += [
        {"label": v["label"], "name": v["name"], "source": sweep / v["id"] / "audio.wav"}
        for v in verification["runs"]
    ]
    encodings = []
    for track in tracks:
        path = out / "audio" / f"{track['label']}.mp3"
        subprocess.run(
            [
                media.executable("ffmpeg"),
                "-hide_banner",
                "-loglevel",
                "error",
                "-nostdin",
                "-n",
                "-i",
                str(track["source"]),
                "-map_metadata",
                "-1",
                "-vn",
                "-af",
                "volume=-1dB",
                "-c:a",
                "libmp3lame",
                "-b:a",
                "192k",
                str(path),
            ],
            check=True,
        )
        decoded = media.read_audio(path, 60)
        original = media.read_audio(track["source"], 60)
        assert decoded.shape == original.shape and np.isfinite(decoded).all()
        assert float(np.max(np.abs(decoded))) < 1
        if track["label"] not in ("Seed", "Guide"):
            assert decoded.shape == (720000, 2)
        meter = subprocess.run(
            [
                media.executable("ffmpeg"),
                "-hide_banner",
                "-nostdin",
                "-i",
                str(path),
                "-af",
                "loudnorm=I=-18:TP=-1:LRA=11:print_format=json",
                "-f",
                "null",
                "-",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        stats = json.loads(meter.stderr[meter.stderr.rfind("{") : meter.stderr.rfind("}") + 1])
        assert float(stats["input_tp"]) < 0
        encodings.append(
            {
                "label": track["label"],
                "name": track["name"],
                "file": str(path.relative_to(out)),
                "sha256": media.digest(path),
                "master_sha256": media.digest(track["source"]),
                "decoded_duration_seconds": len(decoded) / 48000,
                "true_peak_dbtp": float(stats["input_tp"]),
                "lufs": float(stats["input_i"]),
            }
        )
    rows = []
    for track in tracks[2:]:
        letter, name = track["label"], html.escape(track["name"])
        options = '<option value="">Not rated</option>' + "".join(
            f"<option>{i}</option>" for i in range(1, 6)
        )
        rows.append(f'''<article class="card" data-track="{letter}">
<h3>Version {letter}</h3><audio controls preload="metadata" src="audio/{letter}.mp3"></audio>
<details><summary>Musical direction</summary><p>{name}. This is the requested direction; listen for what actually comes through.</p></details>
<div class="ratings"><label>Recognize the seed <select class="recognition">{options}</select></label>
<label>Enjoy the result <select class="enjoyment">{options}</select></label></div>
<label>What feels different or memorable?<textarea rows="2" placeholder="Your own words are perfect"></textarea></label>
<a class="download" href="audio/{letter}.mp3" download>Download {letter}</a></article>''')
    terms = [
        ("Melody", "The tune you could hum: its pitches and timing."),
        ("Pitch / contour", "How high or low a sound is / the tune's rising and falling shape."),
        ("Beat", "The underlying pulse you might tap your foot to."),
        ("Tempo", "How fast that pulse moves."),
        ("Rhythm", "The pattern of sounds and pauses, including their lengths."),
        ("Groove", "How timing and accents feel together: bouncy, driving, swinging or relaxed."),
        ("Harmony", "The notes and chords surrounding the tune."),
        ("Timbre", "Sound character: why a violin and trumpet differ on the same note."),
        ("Orchestration", "Which instruments play which parts."),
        ("Dynamics", "Changes in loudness. A crescendo gradually gets louder."),
        ("Phrasing", "The musical sentences, with their breaths and emphasis."),
        ("Texture / form", "How many parts are active / how the piece unfolds and develops."),
    ]
    glossary = "".join(f"<div><dt>{html.escape(t)}</dt><dd>{html.escape(d)}</dd></div>" for t, d in terms)
    page = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>2.009 House Band — Listening round</title><style>
:root{font-family:system-ui,-apple-system,sans-serif;color:#1e2a35;background:#f5f3ed;color-scheme:light}*{box-sizing:border-box}body{margin:0}main{max-width:1100px;margin:auto;padding:38px 24px 70px}.eyebrow{font-weight:750;letter-spacing:.15em;color:#286459;font-size:.8rem}h1{font-size:clamp(2rem,5vw,3.5rem);line-height:1.08;letter-spacing:-.04em;max-width:800px;margin:16px 0}h2{margin:0 0 16px;font-size:1.55rem}h3{margin:0 0 14px;font-size:1.25rem}p{line-height:1.6;max-width:780px}.intro{font-size:1.15rem}.refs,.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}.references{background:#e5ece6;padding:24px;border-radius:18px;margin:30px 0}.refs>div{min-width:0}.refs h3{margin-bottom:8px}.hint{font-size:.9rem;color:#4a5b62}.card{background:#fff;border:1px solid #d8ded9;border-radius:16px;padding:22px;min-width:0}audio{width:100%;display:block;margin:10px 0 14px}summary{cursor:pointer;color:#286459;line-height:1.5}details p{font-size:.9rem}.ratings{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:18px}label{display:block;font-size:.87rem;font-weight:600}select,textarea{display:block;width:100%;font:inherit;background:#fff;color:#1e2a35;border:1px solid #9eaead;border-radius:7px;margin:7px 0 14px;padding:9px}textarea{resize:vertical;font-weight:400}.download{font-size:.85rem;color:#286459}a:focus,summary:focus,button:focus,select:focus,textarea:focus{outline:3px solid #e5a236;outline-offset:3px}.save{margin:26px 0;padding:24px;border:1px solid #becbc4;border-radius:16px;background:#eaf0eb}button{border:0;border-radius:9px;background:#235d50;color:white;font:inherit;font-weight:650;padding:12px 18px;cursor:pointer}#status{min-height:1.3em}.vocabulary{margin-top:36px}dl{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}dt{font-weight:750;margin-bottom:4px}dd{margin:0;line-height:1.5;color:#43525b}footer{border-top:1px solid #ccd5cf;margin-top:32px;padding-top:16px;font-size:.8rem;color:#59646a}footer a{color:inherit}@media(max-width:650px){main{padding:25px 16px 40px}.refs,.grid,dl{grid-template-columns:1fr}.card,.references,.save{padding:18px}.ratings{gap:10px}}
</style></head><body><main>
<div class="eyebrow">MIT 2.009 · HOUSE BAND EXPERIMENT</div><h1>One little idea.<br>Different musical possibilities.</h1>
<p class="intro">Listen to the seed, then explore nine 15-second interpretations. More than one good choice is welcome. No musical knowledge is needed.</p>
<section class="references"><h2>Start with the source</h2><div class="refs"><div><h3>The seed</h3><audio controls preload="metadata" src="audio/Seed.mp3"></audio><p class="hint">Source recording, with leading quiet skipped for playback.</p></div><div><h3>The melody reference</h3><audio controls preload="metadata" src="audio/Guide.mp3"></audio><p class="hint">A plain note check. It simplifies the voice and does not reproduce all its expression.</p></div></div></section>
<h2>Listen in any order</h2><p>Use two separate judgments: <strong>recognition</strong> (1 = no connection, 5 = clearly my seed) and <strong>enjoyment</strong> (1 = not appealing, 5 = would happily keep). Leave either blank if unsure. Open “Musical direction” after listening if you want to see the intended ensemble.</p>
<div class="grid">__CARDS__</div>
<section class="save"><h2>Your overall reaction</h2><label>Which versions feel too similar? Which would you keep?<textarea id="overall" rows="3"></textarea></label><button id="save-feedback" type="button">Download my feedback</button><p class="hint">Nothing is sent or uploaded. Responses stay in this page until you download them; refreshing clears them. You can also share the version letters and comments directly with the project organizer.</p><div id="status" role="status" aria-live="polite"></div></section>
<section class="vocabulary"><h2>A few useful music words</h2><dl>__GLOSSARY__</dl><p class="hint">These are words for discussing what you hear, not controls you need to learn. The current experiment follows estimated notes and their timing. It does not yet transmit the recording's measured loudness changes to the band.</p></section>
<footer>Local experiment; these recordings test possibilities, not a finished student product. Orchestration audio generated locally with Magenta RealTime 2, Google DeepMind / Google LLC, 2026. Model weights: CC BY 4.0 plus model-card usage terms. See ATTRIBUTION.txt for source and method. No source voice is mixed into the orchestrations.</footer>
</main><script>
document.querySelectorAll('audio').forEach(player=>player.addEventListener('play',()=>{document.querySelectorAll('audio').forEach(other=>{if(other!==player)other.pause()})}));
document.getElementById('save-feedback').addEventListener('click',()=>{
const lines=['MIT 2.009 House Band — listening feedback','Recognition: 1 no connection → 5 clearly connected','Enjoyment: 1 not appealing → 5 would happily keep',''];
document.querySelectorAll('[data-track]').forEach(card=>{lines.push('Version '+card.dataset.track,'Recognize seed: '+(card.querySelector('.recognition').value||'Not rated'),'Enjoy result: '+(card.querySelector('.enjoyment').value||'Not rated'),'Comment: '+(card.querySelector('textarea').value||''),'')});
lines.push('Overall: '+document.getElementById('overall').value);
const url=URL.createObjectURL(new Blob([lines.join('\\n')],{type:'text/plain;charset=utf-8'}));const a=document.createElement('a');a.href=url;a.download='House-Band-Feedback.txt';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);document.getElementById('status').textContent='Feedback file prepared. Nothing was sent.';
});
</script></body></html>""".replace("__CARDS__", "".join(rows)).replace("__GLOSSARY__", glossary)
    (out / "index.html").write_text(page)
    (out / "READ-ME.txt").write_text("""MIT 2.009 HOUSE BAND — LISTENING ROUND

Unzip this folder, then open index.html in a web browser. Keep its audio folder beside it.
Or play the MP3 files directly in any music player. No installation or account is needed.
Some phone file-preview apps may not play local HTML audio; use the individual MP3s.

Start with Seed.mp3 and Guide.mp3. Then listen to A through I in any order.
All nine orchestrations are 15 seconds. Source and guide are their own lengths.
Ask two separate questions: Can I recognize the seed? Do I enjoy this?
Also say what feels different, or which versions are too similar. Multiple keepers are welcome.
The optional web form only downloads a text file; it sends nothing and does not retain responses after refresh.

A: funk / closer following. B: funk / higher lead. C: dance-pop.
D: string trio. E: brass and drums. F: marimba and hand drums.
G: jazz quartet with saxophone. H: indie rock. I: cinematic orchestra.
These are intended directions, not verified instrument lists.

The MP3s are listening copies: 192 kb/s, with 1 dB headroom added to limit encoding overshoot.
The original recording is unchanged; only the seed listening copy skips leading quiet.
The melody reference is a plain, simplified note check rather than an expressive performance.
Original 48 kHz WAV masters, controls and technical records remain in the project.

MUSIC-IN-PLAIN-LANGUAGE.md explains the terminology and what this prototype can detect.
ATTRIBUTION.txt identifies the model. This folder was prepared for the project organizer to share; it has not been uploaded or sent.
""")
    (out / "ATTRIBUTION.txt").write_text("""Orchestration audio: local outputs using Magenta RealTime 2 base.
Model: Google DeepMind / Google LLC, 2026.
Official source: https://github.com/magenta/magenta-realtime
Source revision: 694a545e4ba0b88bf1150137b129582166d3e07f (Apache-2.0 code).
Weights: https://huggingface.co/google/magenta-realtime-2
Weights revision: 010aa0dcb0dfd27b24f0ad07b4dad63e8f9521cc.
Weights license: CC BY 4.0 plus MODEL.md usage terms.
License: https://creativecommons.org/licenses/by/4.0/
Terms: https://github.com/magenta/magenta-realtime/blob/694a545e4ba0b88bf1150137b129582166d3e07f/MODEL.md
Changes/process: automatic note extraction from the source recording, locally generated note-conditioned performances, opening trim, 15-second masters, constant gain and 200 ms ending fades. Listening copies are MP3 encodes with an additional -1 dB gain. No original voice is mixed into the orchestrations.
This attribution identifies the model and process; it does not claim the model's weight license governs every generated output.
""")
    shutil.copy2(ROOT / "docs/house-band/MUSIC-IN-PLAIN-LANGUAGE.md", out / "MUSIC-IN-PLAIN-LANGUAGE.md")
    (out / "AUDIO-MANIFEST.json").write_text(
        json.dumps(
            {
                "seed_opening_removed_seconds": opening / 48000,
                "tracks": encodings,
                "feedback": "not collected",
            },
            indent=2,
        )
        + "\n"
    )
    archive = out.with_suffix(".zip")
    with zipfile.ZipFile(archive, "x", compression=zipfile.ZIP_DEFLATED) as bundle:
        for file in sorted(out.rglob("*")):
            if file.is_file():
                bundle.write(file, Path(out.name) / file.relative_to(out))
    with zipfile.ZipFile(archive) as bundle:
        assert bundle.testzip() is None
    print(
        json.dumps(
            {
                "folder": str(out),
                "zip": str(archive),
                "bytes": archive.stat().st_size,
                "tracks": len(encodings),
                "new_orchestrations": 6,
                "source_sha256": media.digest(source),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
