# Helena Foulkes Transition website

Static site for the Helena Foulkes transition: Home, Meet the Team, Plans, Get Involved and News.
Owned by the `helena-website` GitHub organization. **Prototype: not public until the transition team approves it.**

## How it works
- Plain HTML, CSS and JavaScript. No framework, no server, nothing to install.
- The forms are Fillout forms embedded on the page. Fillout writes each submission into the transition's Notion workspace:

| Page | Fillout form | Notion database | Where it's linked |
|---|---|---|---|
| `get-involved/serve/` | Serve in the Administration | People (Track: Administration) | Home, Get Involved, footer |
| `get-involved/share-an-idea/` | Share Your Idea | Ideas | Home, Get Involved, footer |
| `invitehelena/` | Invite the Governor-Elect | Event Requests | Footer Contact section only |
| `get-involved/boards/` | Join a Committee (Board or Commission) | People (Track: Board or Commission) | Not linked. Live at its address. |

- `get-involved/invite/` is a redirect to `invitehelena/`, so old links still work.
- Until a Fillout form ID is set, each form page shows a preview that checks fields but sends nothing.

## Files
| Path | What it is |
|---|---|
| `_build/build.py` | Generates every page from one shared header, nav and footer. Edit copy here. |
| `_build/news/` | One text file per press release. See "How to post a press release." |
| `assets/site.css` | All styles. Campaign colors and type. |
| `assets/logo-governor-elect.png` | Logo used in the header and footer. |
| `assets/img/` | Photos: Helena cutout for the home hero, Helena and her husband for Meet the Team. |
| `plans/files/` | The 8 plan PDFs, copied from helenafoulkes.com so they keep working after cutover. |
| `_build/privacy.html` | Privacy policy and terms text, published at `privacy-policy/`. |
| `assets/forms.js` | Form previews, and the Fillout form IDs (`fillout: ""` per form). |
| `index.html`, `team/`, `get-involved/`, `invitehelena/`, `news/` | Generated pages. Don't edit by hand; rerun the build. |
| `robots.txt` | Blocks search engines while this is a prototype. |

## How to post a press release
Each press release is one text file. Its page and its spot on the News page are made from that file.

1. **Make the file.** In GitHub, open the `_build/news/` folder and click **Add file → Create new file**.
2. **Name it** with the release date and a short title, all lowercase, words joined by dashes, ending in `.txt`:
   `2026-11-12-cabinet-picks.txt`
   The name becomes the web address: `news/2026-11-12-cabinet-picks/`.
3. **Fill in the top lines, then `---`, then the release text.** Copy this:
   ```
   title: Governor-Elect Foulkes names first cabinet picks
   date: 2026-11-12
   type: Press release
   summary: One sentence that shows on the News page.
   ---
   PROVIDENCE, RI: First paragraph of the release.

   Leave a blank line between paragraphs.

   ## A heading looks like this

   - A bulleted line starts with a dash and a space
   - Links look like this: [press@helenafoulkes.com](mailto:press@helenafoulkes.com)
   ```
   `type` is the small label above the title. It can be left out; it defaults to "Press release."
4. **Click Commit changes.**
5. **Rebuild the site.** The new page doesn't appear until the build runs. Ask Scott (or the transition's Claude) to run `python3 _build/build.py` and commit. This takes a minute.

To fix a release, edit its file and rebuild. To take one down, delete its file and rebuild; its page is removed too.
The News page lists releases newest first, by `date`.

The sample release (`2026-11-04-sample-release.txt`) has `placeholder: yes`, which marks it as a sample. Delete that file before launch.

## Common changes
- **Edit text:** change it in `_build/build.py`, then run `python3 _build/build.py` and commit.
- **Connect a form:** in Fillout, open the form → Share → Embed → Standard, and copy the ID from `data-fillout-id="..."`. Paste it into `fillout: ""` for that form in `assets/forms.js`, then commit.

## Hosting
- **Staging:** GitHub Pages from the `main` branch, root folder. Settings → Pages.
- **Going live**, after approval. The plan is helenatransition.com. Pick one:
  1. **Point the domain at GitHub Pages.** Add a `CNAME` file containing the domain. Change only the website's DNS records (A/AAAA/CNAME for the root and `www`), as GitHub's custom-domain docs describe. **Do not touch MX or other email records.**
  2. **Another host serves these files.** Upload everything except `_build/` to the web root.
- **Before launch:**
  - Remove the "Prototype" banner, set in `PROTO` in `_build/build.py`.
  - Remove the `noindex` meta tag in `_build/build.py`.
  - Delete `robots.txt`, or change it to allow crawling.
  - Replace every yellow "placeholder" tag with final copy, and delete the sample press release.
  - Update the privacy policy (`_build/privacy.html`, copied from helenafoulkes.com/privacy-policy on Oct 22, 2026, effective 9/5/2025). It is with counsel for an update.
  - Confirm the footer line "Built by RI volunteers and funded by Helena Transition" with counsel.
