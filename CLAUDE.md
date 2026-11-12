# German Daily Review

Negin's personal app for learning beginner German (A1). She photographs her handwritten notes and asks for them to be added.
Live at https://neginzarbakhsh.github.io/German-review/ — every push to `main` rebuilds and publishes it (about 2 minutes).

## How it works

- `phrases.yml` — **all the content.** Sections → groups → phrases. Adding or fixing phrases happens here.
- `scripts/template.html` — the main app (Negin's view). Data is injected at build time as `DATA`.
- `scripts/record.html` — Chris's recording page (`record.html?who=chris`). Chris is German; he records native audio.
- `scripts/make.py` — the build: records every phrase with the Piper German voice (slow + normal), converts people's recordings, writes `site/`.
- `scripts/sw.js` — offline support. `version.json` makes open pages reload when a newer build exists.
- `.github/workflows/publish.yml` — builds on push to `main` and publishes to the `gh-pages` branch.
- Every German word in a phrase also gets its own recording automatically (tap a word in the app to hear it and see its meaning from `words`). Nothing to add in `phrases.yml` for this.
- `recordings/chris/`, `recordings/negin/` — real recordings saved from the pages (WAV). `recordings/<person>/tips/` = Chris's suggestions (`.txt` note and/or `.wav`).
  **Never add, delete or overwrite files here unless Negin asks.** They are real voices.

## Adding a handwritten page

1. Read the photo carefully. Fix her spelling in the German you add, and add each slip to `mistakes:` as `[what she wrote, correct, short why]`.
2. Don't repeat phrases already in `phrases.yml` (search first). Reference them in a note or card instead.
3. Put new material in a new section (or the section it clearly belongs to). Keep the section order sensible for a beginner.
4. Every phrase needs:
   - `de` (German), `en` (meaning), `say` (English-style pronunciation, stressed part in `**CAPS**`), `fa` (Persian spelling of the sound)
   - `words` for word-by-word meanings of anything new, e.g. `- [woher, where from]`
   - optional `tip` (one short line, e.g. a sound rule: ch after a = throaty خ, ei = eye, ie = ee, w = v, z = ts, final g = k, final d = t)
   - `speak` only when the spoken text should differ from `de`
5. Lines that read several items (dialogue lines, example word lists) should use `speak: "Part one. Part two."` — the build splits on `". "` so Chris records each part once and parts that already exist are reused.
6. Grammar tables use `kind: conj`; explanation boxes use `kind: cards` with `title` + `body` (simple HTML allowed).
7. Answer her questions written on the page (e.g. “explain this”) in a card or tip, and in your reply.

Style: short, plain English; she is a beginner and a native Persian speaker. Use du/Sie labels as “(friendly)” / “(polite)”.

## Check before pushing

```bash
pip install piper-tts==1.8.0 pyyaml lameenc==1.9.0
curl -sSL -o voice.tgz https://github.com/rhasspy/piper/releases/download/v0.0.2/voice-de-thorsten-low.tar.gz && mkdir -p voice && tar xzf voice.tgz -C voice
python scripts/make.py voice/de-thorsten-low.onnx phrases.yml site   # must finish without errors
cd site && python -m http.server 8000                               # open http://localhost:8000
```

- `python -c "import yaml;yaml.safe_load(open('phrases.yml'))"` must pass (quote values that start with `**` or contain `: `).
- On Chris's page (`record.html?who=chris`, “All” tab) no phrase or word may appear twice.
- Layout: a home screen (Today's review, stats, search, Lessons list, More) and one lesson per page with Back, a lesson picker, and Previous/Next at the bottom. The address keeps the place (`#numbers`). Each section in `phrases.yml` is one lesson, in file order.
- App extras (don't remove): search, tap-a-word, My progress (practice calendar, known per lesson), listening cards in the daily review, pauses after each phrase in Play all.
- Every phrase card shows the same 5 buttons: Standard · Phone · Chris · Me · Record. Practice mode shows only Me · Record.
- Don't change the UI unless asked; Negin cares a lot about a clean, consistent layout.

## Publishing

Commit to `main` and push. The workflow publishes in about 2 minutes; pages update themselves on next open.
Negin's links: app `…/German-review/`; Chris's page `…/German-review/record.html?who=chris` (his access code is added by Negin, never commit it).

Negin doesn't want to see when phrases were added (no “New” badges, timelines or “added this week”).
