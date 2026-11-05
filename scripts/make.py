"""Build the German Daily Review site.

Reads phrases.yml, records every phrase with a German voice (slow + normal),
and writes the finished site to the output folder.

Usage: python scripts/make.py <voice.onnx> <phrases.yml> <out-folder>
"""
import sys, os, json, hashlib, unicodedata, wave, shutil
import yaml, lameenc
from piper.voice import PiperVoice
from piper.config import SynthesisConfig

VOICE, PHRASES, OUT = sys.argv[1:4]
HERE = os.path.dirname(os.path.abspath(__file__))

# Stress fixes where the voice's dictionary is wrong (IPA before -> after)
STRESS_FIXES = {"viːdɜzˈeːən": "vˈiːdɜzeːən"}  # Wiedersehen: stress on Wie

data = yaml.safe_load(open(PHRASES, encoding="utf-8"))

voice = PiperVoice.load(VOICE)
IDS = voice.config.phoneme_id_map
_orig = voice.phonemize
def phonemize(text):
    out = []
    for sent in _orig(text):
        s = unicodedata.normalize("NFC", "".join(sent))  # keeps the soft ch in "ich" as one sound
        for a, b in STRESS_FIXES.items():
            s = s.replace(a, b)
        fitted = []
        for ch in s:  # use whichever form of each sound this voice knows
            fitted.extend([ch] if ch in IDS else list(unicodedata.normalize("NFD", ch)))
        out.append(fitted)
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
                with wave.open(wav, "rb") as w:
                    rate, pcm = w.getframerate(), w.readframes(w.getnframes())
                pcm += b"\x00\x00" * int(rate * 0.15)  # short pause at the end
                enc = lameenc.Encoder()
                enc.set_bit_rate(48); enc.set_in_sample_rate(rate); enc.set_channels(1); enc.set_quality(2)
                open(mp3, "wb").write(enc.encode(pcm) + enc.flush())
                count += 1
shutil.rmtree(tmp)

# Chris's own recordings (saved by record.html into recordings/chris/<phrase>.wav)
chris = {}
rec_dir = f"{HERE}/../recordings/chris"
os.makedirs(f"{OUT}/voices/chris", exist_ok=True)
if os.path.isdir(rec_dir):
    for f in sorted(os.listdir(rec_dir)):
        if not f.endswith(".wav"):
            continue
        a = f[:-4]
        try:
            with wave.open(f"{rec_dir}/{f}", "rb") as w:
                rate, pcm = w.getframerate(), w.readframes(w.getnframes())
            enc = lameenc.Encoder()
            enc.set_bit_rate(64); enc.set_in_sample_rate(rate); enc.set_channels(1); enc.set_quality(2)
            open(f"{OUT}/voices/chris/{a}.mp3", "wb").write(enc.encode(pcm + b"\x00\x00" * int(rate * 0.15)) + enc.flush())
            chris[a] = f"{a}.mp3"
        except Exception as e:
            print(f"Skipped recording {f}: {e}")
print(f"Chris has recorded {len(chris)} phrases.")

page_data = json.dumps({"sections": data["sections"], "mistakes": data["mistakes"], "chris": chris}, ensure_ascii=False)
page = open(f"{HERE}/template.html", encoding="utf-8").read().replace("__DATA__", page_data)
repo = os.environ.get("GITHUB_REPOSITORY", "NeginZarbakhsh/German-review")
rec_page = open(f"{HERE}/record.html", encoding="utf-8").read().replace("__DATA__", page_data).replace("__REPO__", json.dumps(repo))
open(f"{OUT}/record.html", "w", encoding="utf-8").write(rec_page)
open(f"{OUT}/index.html", "w", encoding="utf-8").write(page)
for f in os.listdir(f"{HERE}/../static"):
    shutil.copy(f"{HERE}/../static/{f}", f"{OUT}/{f}")
json.dump({"name": "German Daily Review", "short_name": "Deutsch", "start_url": ".", "scope": ".", "display": "standalone",
           "background_color": "#f2f4f8", "theme_color": "#2347c5",
           "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
                     {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"},
                     {"src": "icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}]},
          open(f"{OUT}/manifest.json", "w"))

# Offline: cache the page, icons and every recording that is in use
used = sorted({f"audio/{it['a']}_{v}.mp3" for sec in data["sections"] for g in sec["groups"] if g["kind"] != "cards"
               for it in g["items"] for v in ("n", "s")}) + [f"voices/chris/{m}" for m in chris.values()]
files = ["./", "index.html", "manifest.json"] + sorted(os.listdir(f"{HERE}/../static")) + used
version = hashlib.md5((os.path.basename(VOICE) + page + "".join(files)).encode("utf-8")).hexdigest()[:10]
sw = open(f"{HERE}/sw.js", encoding="utf-8").read().replace("__VERSION__", version).replace("__FILES__", json.dumps(files))
open(f"{OUT}/sw.js", "w", encoding="utf-8").write(sw)
print(f"Built site with {count} new recordings.")
