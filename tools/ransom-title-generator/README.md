# Ransom Title Generator

Generates monochrome, transparent masthead titles from the real PNG letters in:

`PUBLIC_RECORD_WE_WERE_THERE_SITE_ASSETS/11_DESIGN ELEMENTS/1RANSOM LETTERS`

## Install

```bash
python3 -m pip install --user Pillow
```

## Run (default titles)

```bash
python3 tools/ransom-title-generator/generate_titles.py
```

Default outputs:

- `assets/generated-titles/residual.png`
- `assets/generated-titles/first-day.png`
- `assets/generated-titles/catalog.png`
- `assets/generated-titles/_options/*.png` (comparison options)
- `assets/generated-titles/manifest.json`
- `preview/ransom-titles.html`

## Generate custom words

```bash
python3 tools/ransom-title-generator/generate_titles.py \
  --title "new-title=NEW TITLE" \
  --title "issue-two=ISSUE TWO" \
  --seed 20260314 \
  --options-per-title 5
```

