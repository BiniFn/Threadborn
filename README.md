# Threadborn

Official static reader and export hub for **Threadborn - Starting Life Beyond the Covenant Door**.

This repository ships the public web experience for the project: a polished single-page reader with chapter browsing, a full cast tab, lore and leaks tabs, project credits, and browser-generated **Collector PDF** and **Styled EPUB** exports.

## Highlights

- Single-file static site with no backend required
- Volume, chapter, character, lore, leaks, drawings, and credits sections
- Full-screen in-browser reader with saved reading progress
- Browser-generated PDF and EPUB downloads with improved styling and credits
- Mobile-friendly layout for phones and desktop
- Ready for both **GitHub Pages** and **Vercel**

## Project Structure

```text
.
├── .github/workflows/pages.yml
├── .nojekyll
├── README.md
└── index.html
```

## Local Preview

Because the site is fully static, you can preview it in either of these simple ways:

1. Open `index.html` directly in your browser.
2. Or serve the folder locally with a tiny static server, for example:

```bash
python3 -m http.server 8080
```

Then visit `http://localhost:8080`.

## Deploy on GitHub Pages

This repo includes a GitHub Pages workflow at [`.github/workflows/pages.yml`](./.github/workflows/pages.yml).

To enable it:

1. Push this repository to GitHub.
2. Open the repository settings.
3. Go to **Pages**.
4. Set the source to **GitHub Actions**.
5. Push again or re-run the workflow.

After that, GitHub Pages should publish the site from the repository automatically.

## Deploy on Vercel

This project is ideal for Vercel's free Hobby plan because it is just static HTML, CSS, and client-side JavaScript.

Recommended setup:

1. Import the GitHub repository into Vercel.
2. Set **Framework Preset** to `Other`.
3. Leave the **Build Command** empty.
4. Leave the **Output Directory** as `.`.
5. Deploy.

If you keep the project static and do **not** add serverless functions, databases, or image optimization pipelines, the site avoids the normal function-memory costs and stays extremely light on the free tier.

## Credits

- **BiniFn** - creator, author, and project owner
- Main channel: [@binifn](https://www.youtube.com/@binifn)
- Roblox channel: [@binirbx](https://www.youtube.com/@binirbx)
- Anime channel: [@binirx](https://www.youtube.com/@binirx)
- GitHub: [BiniFn](https://github.com/BiniFn)

## Notes

- The reader stores progress in browser `localStorage`.
- PDF and EPUB files are generated in the browser on demand.
- The site is intentionally static so it can be deployed cheaply, quickly, and without backend maintenance.
