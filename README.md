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

## How it works

`scripts/make.py` records every phrase with the Piper German voice (Thorsten), slow and normal,
and builds the page from `scripts/template.html`. GitHub Actions runs it on every change
(`.github/workflows/publish.yml`).
