"""Build the German Daily Review site.

Reads phrases.yml, records every phrase with a German voice (slow + normal),
and writes the finished site to the output folder.

Usage: python scripts/make.py <voice.onnx> <phrases.yml> <out-folder>
"""
import sys, os, json, hashlib, subprocess, unicodedata, wave, shutil
import yaml
from piper.voice import PiperVoice
from piper.config import SynthesisConfig

VOICE, PHRASES, OUT = sys.argv[1:4]
HERE = os.path.dirname(os.path.abspath(__file__))

# Stress fixes where the voice's dictionary is wrong (IPA before -> after)
STRESS_FIXES = {"viːdɜzˈeːən": "vˈiːdɜzeːən"}  # Wiedersehen: stress on Wie

data = yaml.safe_load(open(PHRASES, encoding="utf-8"))

voice = PiperVoice.load(VOICE)
_orig = voice.phonemize
def phonemize(text):
    out = []
    for sent in _orig(text):
        s = unicodedata.normalize("NFC", "".join(sent))  # keeps the soft ch in "ich" as one sound
        for a, b in STRESS_FIXES.items():
            s = s.replace(a, b)
        out.append(list(s))
    return out
voice.phonemize = phonemize

def key(t):
    return hashlib.md5(t.encode("utf-8")).hexdigest()[:8]

os.makedirs(f"{OUT}/audio", exist_ok=True)
tmp = f"{OUT}/_tmp"; os.makedirs(tmp, exist_ok=True)
count = 0
for sec in data["sections"]:
    for g in sec["groups"]:
        if g["kind"] == "cards":
            continue
        for it in g["items"]:
            it.setdefault("words", [])
            it.setdefault("tip", None)
            text = it.get("speak") or it["de"].rstrip("!")
            it["speak"] = text
            it["a"] = k = key(text)
            for name, ls in (("n", 1.0), ("s", 1.5)):
                mp3 = f"{OUT}/audio/{k}_{name}.mp3"
                if os.path.exists(mp3):
                    continue
                wav = f"{tmp}/{k}_{name}.wav"
                with wave.open(wav, "wb") as w:
                    voice.synthesize_wav(text, w, syn_config=SynthesisConfig(length_scale=ls, noise_scale=0.5, noise_w_scale=0.6))
                subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-af", "apad=pad_dur=0.15",
                                "-ac", "1", "-ar", "22050", "-b:a", "40k", mp3], check=True)
                count += 1
shutil.rmtree(tmp)

page = open(f"{HERE}/template.html", encoding="utf-8").read()
page = page.replace("__DATA__", json.dumps({"sections": data["sections"], "mistakes": data["mistakes"]}, ensure_ascii=False))
open(f"{OUT}/index.html", "w", encoding="utf-8").write(page)
json.dump({"name": "German Daily Review", "short_name": "Deutsch", "start_url": ".", "display": "standalone",
           "background_color": "#f2f4f8", "theme_color": "#2347c5"}, open(f"{OUT}/manifest.json", "w"))
print(f"Built site with {count} new recordings.")
