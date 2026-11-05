# German Daily Review

My German notes with a German voice for every phrase.
Open it at **https://neginzarbakhsh.github.io/German-review/**

## Add or change a phrase

1. Open `phrases.yml` on GitHub and tap the pencil (Edit).
2. Copy an existing phrase and change it. A phrase looks like this:

```yaml
    - de: Wie heißt du?          # the German
      say: vee **HAIST** doo     # how to say it; **CAPITALS** = stressed part (shown in orange)
      fa: وی هایست دو             # Persian spelling (optional)
      en: What's your name?      # meaning
      words:                     # word-by-word meanings (optional)
      - [wie, how]
      - [heißt, are called]
      tip: A short note.         # optional
```

3. Keep the spaces at the start of each line the same as the phrase above it.
4. Tap **Commit changes**. After about 2 minutes the page updates, with the new phrase recorded.

To add a mistake to “Watch out”, add a line under `mistakes:` like
`- [what I wrote, correct spelling, why]`.

## Today's review

The blue box at the top picks phrases for you each day: up to 10 new ones, plus the ones due again.
Tap **Got it** or **Again**. Phrases you know come back after 1, 3, 7, 14 and 30 days; phrases you forget come back tomorrow.
Progress is saved on the phone you use.

## Voices

The ▶ button plays the main voice. The switch at the top picks which one:

- **iPhone** (default): the German voice built into the phone. Download **Anna (Premium)** in
  Settings › Accessibility › Spoken Content › Voices › German for the most natural sound.
- **Standard**: the computer voice recorded when the page is built.

Phrases Chris has recorded also get a separate **🎤 Chris** button that plays his recording.

### Record yourself

Open **https://neginzarbakhsh.github.io/German-review/record.html?who=negin** (or tap
“Record yourself and compare with Chris” in the app). Each phrase has **▶ Chris** to hear him,
then you record and **Listen to me** to compare. Saved takes appear in the app as **🎤 Me**,
and Chris sees a **▶ Negin** button on his recording page. Your recordings go into `recordings/negin/`.

### Chris's recording page

Chris records at **https://neginzarbakhsh.github.io/German-review/record.html**.
Each saved recording goes into `recordings/chris/` and appears in the app about 2 minutes later.

The page needs an access code, made once by Negin:

1. Go to https://github.com/settings/personal-access-tokens/new
2. Name: `Chris recordings`. Expiration: 1 year.
3. Repository access: **Only select repositories** → `German-review`.
4. Permissions → Repository permissions → **Contents: Read and write**.
5. Generate the token, copy it, and send it to Chris privately. He pastes it once on the recording page.

The code can only change files in this one repository. To stop it working, delete it on the same settings page.

## How it works

`scripts/make.py` records every phrase with the Piper German voice (Thorsten), slow and normal,
and builds the page from `scripts/template.html`. GitHub Actions runs it on every change
(`.github/workflows/publish.yml`).
