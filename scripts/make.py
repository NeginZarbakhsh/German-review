"""Build the German Daily Review site.

Reads phrases.yml, records every phrase with a German voice (slow + normal),
and writes the finished site to the output folder.

Usage: python scripts/make.py <voice.onnx> <phrases.yml> <out-folder>
"""
import sys, os, json, hashlib, unicodedata, wave, shutil, re, subprocess, datetime
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

def mp3_from_wav(src, dest_dir, stem):
    """Turn a recorded WAV into an MP3 with a new name for every new take, so phones never play an old copy."""
    with wave.open(src, "rb") as w:
        rate, pcm = w.getframerate(), w.readframes(w.getnframes())
    enc = lameenc.Encoder()
    enc.set_bit_rate(64); enc.set_in_sample_rate(rate); enc.set_channels(1); enc.set_quality(2)
    name = f"{stem}-{hashlib.md5(pcm).hexdigest()[:8]}.mp3"
    os.makedirs(dest_dir, exist_ok=True)
    open(f"{dest_dir}/{name}", "wb").write(enc.encode(pcm + b"\x00\x00" * int(rate * 0.15)) + enc.flush())
    return name

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

# Every single German word gets its own recording too, so tapping a word in the app plays just that word.
# A word that is already a phrase of its own (e.g. "Hallo") has the same key and reuses that recording.
WORD_RE = re.compile(r"[A-Za-zÄÖÜäöüß]+(?:['’][A-Za-z]+)?")
word_keys = {}
for sec in data["sections"]:
    for g in sec["groups"]:
        if g["kind"] == "cards" or sec["id"] == "sounds":   # Sounds shows single letters, not words
            continue
        for it in g["items"]:
            for w in WORD_RE.findall(it["de"]):
                word_keys.setdefault(w.lower(), (w, key(w)))
for w, k in word_keys.values():
    for name, ls in (("n", 1.0), ("s", 1.4)):
        mp3 = f"{OUT}/audio/{k}_{name}.mp3"
        if os.path.exists(mp3):
            continue
        wav = f"{tmp}/{k}_{name}.wav"
        with wave.open(wav, "wb") as wf:
            voice.synthesize_wav(w, wf, syn_config=SynthesisConfig(length_scale=ls, noise_scale=0.5, noise_w_scale=0.6))
        with wave.open(wav, "rb") as wf:
            rate, pcm = wf.getframerate(), wf.readframes(wf.getnframes())
        pcm += b"\x00\x00" * int(rate * 0.15)
        enc = lameenc.Encoder()
        enc.set_bit_rate(48); enc.set_in_sample_rate(rate); enc.set_channels(1); enc.set_quality(2)
        open(mp3, "wb").write(enc.encode(pcm) + enc.flush())
        count += 1
shutil.rmtree(tmp)

# When was each phrase added? Read the history of phrases.yml (needs the full git history; skipped if missing).
added = {}
try:
    log = subprocess.run(["git", "log", "--reverse", "-p", "--format=@@DATE %as", "--", os.path.relpath(PHRASES, f"{HERE}/..")],
                         cwd=f"{HERE}/..", capture_output=True, text=True, check=True).stdout
    day = None
    for line in log.splitlines():
        if line.startswith("@@DATE "):
            day = line[7:].strip()
        elif line.startswith("+") and "- de:" in line and day:
            de = line.split("- de:", 1)[1].strip().strip("'\"")
            added.setdefault(de, day)
except Exception as e:
    print(f"No history for phrase dates: {e}")
today = datetime.date.today().isoformat()
for sec in data["sections"]:
    for g in sec["groups"]:
        if g["kind"] != "cards":
            for it in g["items"]:
                it["added"] = added.get(str(it["de"]).strip(), today)

# Lines that read several words one by one (e.g. "Abend. acht.") are split into parts, so a person records
# each word only once. A part that is also a phrase of its own (e.g. "acht") reuses that phrase's recording.
singles = {}
for sec in data["sections"]:
    for g in sec["groups"]:
        if g["kind"] != "cards":
            for it in g["items"]:
                if ". " not in it["speak"]:
                    singles.setdefault(it["speak"].rstrip(".!").lower(), it["a"])
for sec in data["sections"]:
    for g in sec["groups"]:
        if g["kind"] != "cards":
            for it in g["items"]:
                bits = [b.strip().rstrip(".!") for b in it["speak"].split(". ")]
                bits = [b for b in bits if b]
                if len(bits) > 1:
                    it["parts"] = [{"w": b, "a": singles.get(b.lower(), key(b))} for b in bits]
                elif bits and singles.get(bits[0].lower(), it["a"]) != it["a"]:
                    it["parts"] = [{"w": bits[0], "a": singles[bits[0].lower()]}]   # e.g. "sechs." in Sounds = the number "sechs"

# People's own recordings, saved by record.html into recordings/<person>/<phrase>.wav
# (recordings/chris = Chris, recordings/negin = Negin)
voices = {"chris": {}, "negin": {}}
tips = {}   # suggestions: recordings/<person>/tips/<phrase>.txt (a note) and/or .wav (how they'd say it)
rec_root = f"{HERE}/../recordings"
if os.path.isdir(rec_root):
    for person in sorted(os.listdir(rec_root)):
        rec_dir = f"{rec_root}/{person}"
        if not os.path.isdir(rec_dir) or not person.isalpha():
            continue
        voices.setdefault(person, {})
        os.makedirs(f"{OUT}/voices/{person}", exist_ok=True)
        for f in sorted(os.listdir(rec_dir)):
            if not f.endswith(".wav"):
                continue
            a = f[:-4]
            try:
                voices[person][a] = mp3_from_wav(f"{rec_dir}/{f}", f"{OUT}/voices/{person}", a)
            except Exception as e:
                print(f"Skipped recording {person}/{f}: {e}")
        tip_dir = f"{rec_dir}/tips"
        if os.path.isdir(tip_dir):
            for f in sorted(os.listdir(tip_dir)):
                a, ext = os.path.splitext(f)
                try:
                    if ext == ".txt":
                        text = open(f"{tip_dir}/{f}", encoding="utf-8").read().strip()[:600]
                        if text:
                            tips.setdefault(person, {}).setdefault(a, {})["text"] = text
                    elif ext == ".wav":
                        tips.setdefault(person, {}).setdefault(a, {})["file"] = "tips/" + mp3_from_wav(f"{tip_dir}/{f}", f"{OUT}/voices/{person}/tips", a)
                except Exception as e:
                    print(f"Skipped tip {person}/{f}: {e}")
for person, recs in voices.items():
    print(f"{person} has recorded {len(recs)} phrases and {len(tips.get(person, {}))} suggestions.")

page_data = json.dumps({"sections": data["sections"], "mistakes": data["mistakes"], "voices": voices, "tips": tips,
                        "wordAudio": {w.lower(): k for w, k in word_keys.values()}}, ensure_ascii=False)
repo = os.environ.get("GITHUB_REPOSITORY", "NeginZarbakhsh/German-review")
owner, name = repo.split("/")
site = f"https://{owner.lower()}.github.io/{name}/"
BUILD = hashlib.md5((page_data + open(f"{HERE}/template.html", encoding="utf-8").read() + open(f"{HERE}/record.html", encoding="utf-8").read()).encode("utf-8")).hexdigest()[:10]
STAMP = datetime.datetime.now(datetime.timezone.utc).strftime("%d %b, %H:%M UTC").lstrip("0")
open(f"{OUT}/version.json", "w").write(json.dumps({"build": BUILD, "stamp": STAMP}))
page = (open(f"{HERE}/template.html", encoding="utf-8").read()
        .replace("__DATA__", page_data).replace("__REPO__", json.dumps(repo)).replace("__SITE__", site)
        .replace("__BUILD__", BUILD).replace("__STAMP__", STAMP))
rec_page = open(f"{HERE}/record.html", encoding="utf-8").read().replace("__DATA__", page_data).replace("__REPO__", json.dumps(repo)).replace("__BUILD__", BUILD).replace("__STAMP__", STAMP)
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
               for it in g["items"] for v in ("n", "s")}) + [f"voices/{p}/{m}" for p, recs in voices.items() for m in recs.values()] \
       + [f"voices/{p}/{t['file']}" for p, ts in tips.items() for t in ts.values() if "file" in t]
files = ["./", "index.html", "manifest.json"] + sorted(os.listdir(f"{HERE}/../static")) + used
version = hashlib.md5((os.path.basename(VOICE) + page + "".join(files)).encode("utf-8")).hexdigest()[:10]
sw = open(f"{HERE}/sw.js", encoding="utf-8").read().replace("__VERSION__", version).replace("__FILES__", json.dumps(files))
open(f"{OUT}/sw.js", "w", encoding="utf-8").write(sw)
print(f"Built site with {count} new recordings.")
