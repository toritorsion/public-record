# Content Replacement Guide — PUBLIC RECORD

This file maps every placeholder in the codebase to its location and what needs to be swapped in.

---

## STRIPE PAYMENT LINKS

Replace these placeholder strings with real Stripe Payment Link URLs after you create them in your Stripe dashboard.

| Placeholder | File | Product | Size | Price |
|-------------|------|---------|------|-------|
| `STRIPE_LINK_FIRSTDAY_8x11` | `first-day-print/index.html` | FIRST DAY | 8.5×11″ | $100 |
| `STRIPE_LINK_FIRSTDAY_11x14` | `first-day-print/index.html` | FIRST DAY | 11×14″ | $150 |
| `STRIPE_LINK_FIRSTDAY_13x19` | `first-day-print/index.html` | FIRST DAY | 13×19″ | $225 |
| `STRIPE_LINK_FIRSTDAY_20x30` | `first-day-print/index.html` | FIRST DAY | 20×30″ | $450 |
| `STRIPE_LINK_FIRSTDAY_24x36` | `first-day-print/index.html` | FIRST DAY | 24×36″ (Collector, ltd 9) | $750 |
| `STRIPE_LINK_RESIDUAL_8x11` | `residual-print/index.html` | RESIDUAL | 8.5×11″ | $95 |
| `STRIPE_LINK_RESIDUAL_11x14` | `residual-print/index.html` | RESIDUAL | 11×14″ | $140 |
| `STRIPE_LINK_RESIDUAL_13x19` | `residual-print/index.html` | RESIDUAL | 13×19″ | $210 |
| `STRIPE_LINK_RESIDUAL_20x30` | `residual-print/index.html` | RESIDUAL | 20×30″ | $425 |
| `STRIPE_LINK_RESIDUAL_24x36` | `residual-print/index.html` | RESIDUAL | 24×36″ (Collector, ltd 9) | $700 |

**How to create Stripe Payment Links:**
1. Stripe Dashboard → Products → Add product (one per size/print)
2. Set price, name, and description for each
3. Payment Links → Create Link → choose product
4. Copy the link URL (looks like `https://buy.stripe.com/xxxxxxxxxxxx`)
5. Find and replace the placeholder string in the HTML file

---

## MISSING IMAGES — FIRST DAY GRID

These images are referenced in `first-day/index.html` (Section 9, 3-column grid) but were not available in the asset folder. They show as labeled placeholder boxes. Drop the actual files into `assets/images/first-day/` and the placeholders will automatically be replaced.

| Placeholder | File Needed | Grid Position |
|-------------|-------------|---------------|
| `first-day-trump-wig-kid.jpg` | `assets/images/first-day/first-day-trump-wig-kid.jpg` | Grid slot 2 |
| `first-day-blm-stroller.jpg` | `assets/images/first-day/first-day-blm-stroller.jpg` | Grid slot 3 |
| `first-day-i-am-woman-sign.jpg` | `assets/images/first-day/first-day-i-am-woman-sign.jpg` | Grid slot 4 |
| `first-day-los-crudos-fist.jpg` | `assets/images/first-day/first-day-los-crudos-fist.jpg` | Grid slot 6 |
| `first-day-flower-hand.jpg` | `assets/images/first-day/first-day-flower-hand.jpg` | Grid slot 7 |
| `first-day-flower-police.jpg` | `assets/images/first-day/first-day-flower-police.jpg` | Grid slot 8 |
| `first-day-peace-baby.jpg` | `assets/images/first-day/first-day-peace-baby.jpg` | Grid slot 9 |
| `first-day-street-emptying.jpg` | `assets/images/first-day/first-day-street-emptying.jpg` | Grid slot 14 |

**What to do when you have the files:**
1. Copy each file into `assets/images/first-day/`
2. In `first-day/index.html`, find the `<div class="image-placeholder" data-file="FILENAME.jpg">` block
3. Replace the entire `<div class="image-placeholder">...</div>` with:
   ```html
   <img src="../assets/images/first-day/FILENAME.jpg" alt="Brief description" loading="lazy">
   ```

---

## IMAGE NOTES — RESIDUAL GALLERY

The spec called for `residual_context_RESIDUAL_B-SIDE 01.jpg` (gallery slot 21) — this file was not present.
Currently using `residual_context_RESIDUAL_B-SIDE 02.jpg` in that slot, and `residual_context_RESIDUAL_B-SIDE 04.jpg` in slot 22.

If you locate `residual_context_RESIDUAL_B-SIDE 01.jpg`, copy it to `assets/images/residual/` and update `residual/index.html` grid slot 21.

---

## GITHUB USERNAME

In `docs/github-pages-setup.md` and `docs/cloudflare-dns.md`, replace:
- `YOUR_USERNAME` with your actual GitHub username

---

## OPEN GRAPH IMAGE

For social media sharing previews, add to the `<head>` of each page:
```html
<meta property="og:image" content="https://toritorsion.com/assets/images/heroes/womens-march-chicago-first-day.jpg">
```
Or point to whichever hero image is appropriate per page.
Add this after the other `og:` meta tags when the domain is live.

---

## FAVICON

No favicon is set yet. When ready:
1. Create a small square icon (32×32 or 64×64 PNG) — suggest a bold "PR" in Bebas Neue or a simple geometric mark
2. Save as `assets/images/favicon.png`
3. Add to the `<head>` of every HTML file:
   ```html
   <link rel="icon" type="image/png" href="/assets/images/favicon.png">
   ```

---

## ANALYTICS

When ready to add tracking, add before `</body>` in each page.
- **Plausible** (privacy-focused, recommended): one script tag
- **Google Analytics**: GA4 script tag

See post-launch checklist in the handoff prompt.
