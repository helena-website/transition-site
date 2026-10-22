# Helena Foulkes Transition website

Static site for the Helena Foulkes transition: Home, Meet the Team, Get Involved (4 intake forms) and News.
Owned by the `helena-website` GitHub organization. **Prototype: not public until the transition team approves it.**

## How it works
- Plain HTML, CSS and JavaScript. No framework, no server, nothing to install.
- The four forms are Fillout forms embedded on the page. Fillout writes each submission into the transition's Notion workspace:

| Page | Fillout form | Notion database |
|---|---|---|
| `get-involved/share-an-idea/` | Share Your Idea | Ideas |
| `get-involved/invite/` | Invite the Governor-Elect | Event Requests |
| `get-involved/boards/` | Join a Board or Commission | People (Track: Board or Commission) |
| `get-involved/serve/` | Serve in the Administration | People (Track: Administration) |

- Until a Fillout form ID is set, each form page shows a preview that checks fields but sends nothing.

## Files
| Path | What it is |
|---|---|
| `_build/build.py` | Generates every page from one shared header, nav and footer. Edit copy here. |
| `assets/site.css` | All styles. Campaign colors and type. |
| `assets/logo-governor-elect.png` | Logo used in the header and footer. |
| `_build/privacy.html` | Privacy policy and terms text, published at `privacy-policy/`. |
| `assets/forms.js` | Form previews, and the Fillout form IDs (`fillout: ""` per form). |
| `index.html`, `team/`, `get-involved/`, `news/` | Generated pages. Don't edit by hand; rerun the build. |
| `robots.txt` | Blocks search engines while this is a prototype. |

## Common changes
- **Edit text:** change it in `_build/build.py`, then run `python3 _build/build.py` and commit.
- **Connect a form:** in Fillout, open the form → Share → Embed → Standard, and copy the ID from `data-fillout-id="..."`. Paste it into `fillout: ""` for that form in `assets/forms.js`, then commit.
- **Add a news item:** add a line to `NEWS` in `_build/build.py`, rebuild, commit.

## Hosting
- **Staging:** GitHub Pages from the `main` branch, root folder. Settings → Pages.
- **Going live on helenafoulkes.com**, after approval. Pick one:
  1. **The current host serves these files.** Upload everything except `_build/` to the web root.
  2. **Point the domain at GitHub Pages.** Add a `CNAME` file containing `helenafoulkes.com`. Change only the website's DNS records (A/AAAA/CNAME for the root and `www`), as GitHub's custom-domain docs describe. **Do not touch MX or other email records.**
- **Before launch:**
  - Remove the "Prototype" banner, set in `PROTO` in `_build/build.py`.
  - Remove the `noindex` meta tag in `_build/build.py`.
  - Delete `robots.txt`, or change it to allow crawling.
  - Replace every yellow "placeholder" tag with final copy.
  - Confirm the privacy policy (`_build/privacy.html`, copied from helenafoulkes.com/privacy-policy on Oct 22, 2026) and the "Paid for by Helena for RI" line still apply to the transition. Counsel should review both.
