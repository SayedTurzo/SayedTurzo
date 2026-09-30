# Make it yours

`profile.json` is the content source for both the GitHub profile and playable portfolio. Do not edit generated README sections or `site/profile.json` directly.

## Add a game

Copy an entry in `games`. Give it a unique, lowercase, hyphenated `id`, a `title`, `platform`, `description`, `url`, `accent` and `symbol`. Set `featured: true` to put it in the README showcase. Keep three featured games for a balanced row. All games appear on the companion site and filter automatically by platform.

The current covers are original abstract title cards, not screenshots of the games. To use real screenshots, change the cover generator or replace generated covers and stop regenerating those covers in `scripts/build_profile.py`.

## Change your information or style

- Edit `bio`, `headline`, contacts, `skills`, `experience`, or `worlds` in `profile.json`.
- Edit `theme.accent`, `theme.secondary`, and `theme.background` for your colours.
- Edit `site/styles.css` for layout and motion, `scripts/build_profile.py` for the GIF and README layout.
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

1. Push the changes to `main`.
2. In repository **Settings → Pages → Build and deployment**, select **GitHub Actions** as the source.
3. Run **Publish playable portfolio** in Actions if it has not run automatically. The expected URL is `https://sayedturzo.github.io/SayedTurzo/`; update `siteUrl` if the deployed URL differs.
4. Run **Profile refresh** once to generate the real contribution snake. It then refreshes daily. It needs repository Contents write permission; branch protection may require a different publishing strategy.

Until those workflows run successfully, the playable link is not live and the snake has a clearly labelled first-run placeholder. The contribution animation uses [Platane/snk](https://github.com/Platane/snk); it is an animation of GitHub activity, separate from the visitor's playable Snake game. Private activity visibility follows GitHub's profile settings.

README supports images and links; JavaScript games run on the companion GitHub Pages site. No build framework, API keys, tracking, or application backend is required.
