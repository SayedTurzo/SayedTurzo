# Profile link audit

Checked on September 30, 2026 (Asia/Dhaka). HTTP checks were followed by browser checks for failed listings, Google Sites, and LinkedIn. The removed links no longer appear in the README or portfolio content.

| Removed destination | Observed failure |
| --- | --- |
| Spaceholic! | Google Play HTTP 404; browser displays Not Found |
| Burgerology | Google Play HTTP 404; browser displays Not Found |
| Shark Attack | Google Play HTTP 404; browser displays Not Found |
| War Troops 1917 | Google Play HTTP 404; browser displays Not Found |
| Met City | Redirects away from the project to an unrelated numbered domain; browser cannot load the project |
| E-Gold City | DNS resolution fails; browser reports ERR_NAME_NOT_RESOLVED |
| Nanoverse | HTTPS certificate validation fails (self-signed certificate); not bypassed |

Kept: both Roblox game pages (HTTP 200 with matching game titles), the published root portfolio (HTTP 200), GitHub (HTTP 200), and the Google Sites portfolio (HTTP 200 with visible portfolio content).

LinkedIn responds with an authentication wall in the browser and blocks automated requests (HTTP 999). Kept as a sign-in-dependent social link, not classified as a broken destination. The exact profile content could not be independently verified behind that sign-in requirement.

Email links were checked for matching address syntax; no email was sent and inbox delivery was not tested. The Neon Snake link opens the working arcade section of the root portfolio.

Run `python scripts/check_links.py` for a read-only audit of the current configured links. It writes `tmp/link-audit.json`. A blocked request or sign-in page alone is not proof that a link is broken.
