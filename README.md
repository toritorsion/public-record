# PUBLIC RECORD — We Were There

A documentary print publication by Tori "Torsion" Howard.

Two fine art prints from Chicago:

- **FIRST DAY** — Women's March, Chicago, January 21, 2017
- **RESIDUAL** — Logan Square monument with "FIGHT FASCISM" graffiti, November 11, 2024

## Stack

Vanilla HTML / CSS / JS. No build tools, no frameworks. Static files, GitHub Pages.

## Structure

```
index.html              → Home / We Were There
first-day/              → FIRST DAY feature page
residual/               → RESIDUAL feature page
first-day-print/        → FIRST DAY print purchase
residual-print/         → RESIDUAL print purchase
assets/
  css/main.css          → Full design system
  js/main.js            → Nav, lazy loading
  js/inspect.js         → Image hover zoom
  images/               → All site images
docs/
  github-pages-setup.md
  cloudflare-dns.md
  content-replacement-guide.md
```

## To deploy

See `docs/github-pages-setup.md`

## Pending after launch

- Swap Stripe Payment Link placeholders (see `docs/content-replacement-guide.md`)
- Add 8 missing First Day grid images (see `docs/content-replacement-guide.md`)
- Point toritorsion.com via Cloudflare (see `docs/cloudflare-dns.md`)
- Cancel Squarespace before March 22, 2026
