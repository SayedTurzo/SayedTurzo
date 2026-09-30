# Make it yours

`profile.json` is the content source for both the GitHub profile and playable portfolio. Do not edit generated README sections or `site/profile.json` directly.

## Professional portfolio content

The root website is your primary portfolio. `portfolio` should point to `https://sayedturzo.github.io/`; `previousPortfolio` records the original Google Sites source and `publisher` points to your Google Play catalogue.

- `games`: published game cards. `images` is an array of local screenshot paths; optional `youtubeId` supplies the trailer. Clicking a card opens its gallery, trailer and platform button.
- `demonstrations`: `{ "title": "Project name", "category": "Multiplayer", "youtubeId": "VIDEO_ID" }`. Search and categories update automatically. Videos load only when opened; closing the dialog stops playback.
- `archiveProjects`: `{ "title": "Project name", "description": "Short overview", "images": ["assets/sources/my-image.webp"] }`. Keep unavailable historical projects here with images or verified video IDs, without broken outbound URLs.
- `experience`: company, role, `dates` and detail. `education`, `portrait`, `heroImage`, `specialties`, `phone` and `cvUrl` control the professional profile sections.

Store new media inside `assets/sources/`. Edit page markup in `site/index.template.html`; `site/index.html` is generated. Rebuild, review locally and publish with the existing workflows. The builder publishes CSS, JavaScript modules and JSON together under a content-hashed release directory, preventing cached files from different updates from mixing. Run `python scripts/check_release.py` to check this. `PORTFOLIO_SOURCES.md` documents provenance and import limitations; `portfolio-evidence.json` preserves original source media and titles. Import scripts use BeautifulSoup and Pillow and run explicitly, not as part of the regular build. Review imported content before replacing curated `profile.json`.

## Add a game

Copy an entry in `games`. Give it a unique, lowercase, hyphenated `id`, a `title`, `platform`, `description`, `url` and `accent`. Set `featured: true` to put it in the README showcase. Featured games are arranged in pairs. All games appear on the companion site and filter automatically by platform.

For real game artwork, save an image inside the repo and add `coverImage`, for example `"coverImage": "assets/sources/my-game.png"`. The generator creates the framed README card and the site uses the original artwork. The two Roblox games use public thumbnails fetched from Roblox. Other games use title cards. Refresh Roblox thumbnails with `python scripts/fetch_roblox_covers.py` when you want to (requires internet access).

## Change your information or style

- Edit `bio`, `headline`, contacts, `skills`, `experience`, or `worlds` in `profile.json`.
- Edit `theme.accent`, `theme.secondary`, and `theme.background` for your colours.
- Edit `site/styles.css` for layout and motion, `scripts/build_profile.py` for the GIF and README layout.
- Set `heroEffect` to `"glitch"` for the animated portrait or `"none"` for the clean image. The effect pauses offscreen and respects reduced-motion preferences; timing and scanline strength are in the portrait rules at the end of `site/styles.css`.
- The GIF uses original procedural animation. Regeneration produces a 48-frame loop with your current name and headline.

Rebuild locally with Python and Pillow:

```sh
python scripts/build_profile.py
```

Preview using a local web server (fetch and JS modules need HTTP):

```sh
python -m http.server 8000 --directory site
```

Open `http://localhost:8000`. Game controls: arrows/WASD, swipe, or direction buttons. Space pauses while the canvas is focused. Scrolling the game out of view or changing tabs pauses it. Best score is stored only on the visitor's device.

Validate game rules with `node scripts/check-game.mjs`. Optional browser checks use Playwright (`node scripts/check-browser.cjs`) against the running local server, with Microsoft Edge by default on Windows. Set `BROWSER_CHANNEL` for another installed browser. Screenshots are saved to `tmp/qa`.

## Make it live on GitHub

The main public portfolio is published at `https://sayedturzo.github.io/` through the separate [SayedTurzo.github.io repository](https://github.com/SayedTurzo/SayedTurzo.github.io). Its **Publish root portfolio** workflow builds this repository's latest source. It checks hourly; for an immediate update after editing this repository, run that workflow manually. Keep all content and design edits in this repository.

The project-site copy is published at `https://sayedturzo.github.io/SayedTurzo/`. Its deployment setup is:

1. Push the changes to `main`.
2. In repository **Settings → Pages → Build and deployment**, select **GitHub Actions** as the source.
3. Run **Publish playable portfolio** in Actions if it has not run automatically. The project-site URL is `https://sayedturzo.github.io/SayedTurzo/`; `siteUrl` points README play links to the main root-domain portfolio.
4. Run **Profile refresh** once to generate the real contribution snake. It then refreshes daily. It needs repository Contents write permission; branch protection may require a different publishing strategy.

The Pages workflow verifies the deployed page, then sets `sitePublished: true` and regenerates the README to activate its Play links. Keep that flag false until deployment is verified; false shows setup information instead of a broken public game link. The workflows share a concurrency group to prevent overlapping generated-content commits. The contribution snake has a labelled first-run placeholder until Profile refresh runs. The animation uses [Platane/snk](https://github.com/Platane/snk); it is separate from the visitor's playable Snake game. Private activity visibility follows GitHub's profile settings.

README supports images and links; JavaScript games run on the companion GitHub Pages site. No build framework, API keys, tracking, or application backend is required.
