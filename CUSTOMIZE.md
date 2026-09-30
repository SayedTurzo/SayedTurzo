# Make it yours

`profile.json` is the content source for both the GitHub profile and playable portfolio. Do not edit generated README sections or `site/profile.json` directly.

## Add a game

Copy an entry in `games`. Give it a unique, lowercase, hyphenated `id`, a `title`, `platform`, `description`, `url` and `accent`. Set `featured: true` to put it in the README showcase. Featured games are arranged in pairs. All games appear on the companion site and filter automatically by platform.

For real game artwork, save an image inside the repo and add `coverImage`, for example `"coverImage": "assets/sources/my-game.png"`. The generator creates the framed README card and the site uses the original artwork. The two Roblox games use public thumbnails fetched from Roblox. Other games use title cards. Refresh Roblox thumbnails with `python scripts/fetch_roblox_covers.py` when you want to (requires internet access).

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

The Pages workflow verifies the deployed page, then sets `sitePublished: true` and regenerates the README to activate its Play links. Keep that flag false until deployment is verified; false shows setup information instead of a broken public game link. The workflows share a concurrency group to prevent overlapping generated-content commits. The contribution snake has a labelled first-run placeholder until Profile refresh runs. The animation uses [Platane/snk](https://github.com/Platane/snk); it is separate from the visitor's playable Snake game. Private activity visibility follows GitHub's profile settings.

README supports images and links; JavaScript games run on the companion GitHub Pages site. No build framework, API keys, tracking, or application backend is required.
