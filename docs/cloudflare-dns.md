# Cloudflare DNS Migration — toritorsion.com → GitHub Pages

## Before you do this

- Confirm GitHub Pages is working at `https://YOUR_USERNAME.github.io/public-record/`
- Have your GitHub Pages URL ready
- Keep Squarespace active until DNS is confirmed working (allow a day or two of overlap)

## Step 1: Add custom domain in GitHub

1. Go to your `public-record` repo on GitHub
2. Settings → Pages
3. Under **Custom domain**: type `toritorsion.com`
4. Click Save
5. GitHub will create a `CNAME` file in your repo automatically

## Step 2: Log into Cloudflare

Go to https://dash.cloudflare.com and select your `toritorsion.com` domain.

## Step 3: Update DNS records

In Cloudflare DNS, delete or update any existing A records pointing to Squarespace.
Then add these GitHub Pages A records:

| Type | Name | Content | Proxy |
|------|------|---------|-------|
| A | @ | 185.199.108.153 | DNS only (gray cloud) |
| A | @ | 185.199.109.153 | DNS only (gray cloud) |
| A | @ | 185.199.110.153 | DNS only (gray cloud) |
| A | @ | 185.199.111.153 | DNS only (gray cloud) |
| CNAME | www | YOUR_USERNAME.github.io | DNS only (gray cloud) |

**Important**: Set to "DNS only" (not proxied) for GitHub Pages to work correctly with HTTPS.

## Step 4: Wait for DNS propagation

DNS changes can take 1-48 hours to fully propagate. Usually much faster through Cloudflare.

You can check propagation at: https://dnschecker.org/

## Step 5: Verify HTTPS

Once propagated, GitHub will automatically provision an SSL certificate (via Let's Encrypt).
In GitHub Settings → Pages, you'll see "Your site is published at https://toritorsion.com"

Make sure **Enforce HTTPS** is checked in GitHub Settings → Pages.

## Step 6: Cancel Squarespace

Only cancel Squarespace AFTER:
- `toritorsion.com` resolves to your GitHub Pages site
- HTTPS is working
- You've tested all pages

Squarespace billing renews March 22. Cancel before that date.

## If you want www to redirect to non-www

In Cloudflare, use a **Page Rule** or **Redirect Rule**:
- Match: `www.toritorsion.com/*`
- Redirect to: `https://toritorsion.com/$1` (301 permanent)

## Notes

- Cloudflare free plan is sufficient for this
- The "DNS only" setting is required — GitHub Pages HTTPS doesn't work through Cloudflare's proxy (orange cloud)
- If you previously used Cloudflare's proxy for Squarespace, you may need to turn it off
