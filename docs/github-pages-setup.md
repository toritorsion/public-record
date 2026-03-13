# GitHub Pages Setup — PUBLIC RECORD

## Step 1: Initialize git repo

Open Terminal and run:

```bash
cd /Users/torsion/Sites/public-record
git init
git add .
git commit -m "Initial build — PUBLIC RECORD launch"
```

## Step 2: Create GitHub repository

1. Go to https://github.com/new
2. Repository name: `public-record`
   - Or use `toritorsion.github.io` if you want this as your root GitHub Pages site (then skip `/public-record/` from all URLs)
3. Set to **Public**
4. Do NOT initialize with README (you already have one)
5. Click **Create repository**

## Step 3: Push to GitHub

GitHub will show you commands after creation. Run:

```bash
git remote add origin https://github.com/YOUR_USERNAME/public-record.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

## Step 4: Enable GitHub Pages

1. Go to your repo on GitHub
2. Click **Settings** tab
3. Scroll to **Pages** in the left sidebar
4. Under **Source**: select `Deploy from a branch`
5. Branch: `main`, folder: `/ (root)`
6. Click **Save**

GitHub will build and deploy. Takes 1-3 minutes.

## Step 5: View your live site

Your site will be live at:
```
https://YOUR_USERNAME.github.io/public-record/
```

If you used `toritorsion.github.io` as repo name:
```
https://toritorsion.github.io/
```

## Step 6: Future updates

After any code changes:

```bash
git add .
git commit -m "Your description of changes"
git push
```

GitHub Pages auto-redeploys within 1-2 minutes.

## Notes

- GitHub Pages is free for public repos
- The `PUBLIC_RECORD_WE_WERE_THERE_SITE_ASSETS` folder is large — add it to `.gitignore` before your first push so it doesn't get pushed to GitHub
- See `.gitignore` in project root
