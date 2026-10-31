#!/usr/bin/env python3
"""Build the transition site pages from one shared header/footer.

Run from the repo root:  python3 _build/build.py
Writes static HTML into the repo root. All links are relative, so the site
works at any address (GitHub Pages staging, or the root of helenafoulkes.com).
GitHub Pages (Jekyll) does not publish folders starting with "_", so this
script stays private to the repo.

Languages: English is the default and lives at the site root. Spanish copies of the
main pages are written under es/ (e.g. es/team/). English text is in EN below;
Spanish text is in _build/es.py. News, press releases, the privacy policy and the
plan PDFs are English only.
"""
import re
import shutil
import sys
from datetime import date as _date
from html import escape as _esc
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # repo root
sys.path.insert(0, str(Path(__file__).resolve().parent))
from es import ES  # noqa: E402  Spanish text

# Meet the Team: "Leadership Transition Committee" section. Hidden for now; set to True to show it again.
SHOW_COMMITTEE_LEADS = False

# Pages that also have a Spanish version at es/<path>. Every other page is English only.
ES_PAGES = ["", "team/", "plans/", "get-involved/", "get-involved/serve/",
            "get-involved/share-an-idea/", "invitehelena/", "news/"]

# ---------- English text ----------
EN = {
    "proto_label": "Prototype",
    "proto": "Sample design for the transition team's review.",
    "skip": "Skip to content",
    "logo_aria": "Helena Foulkes Transition home",
    "logo_alt": "Helena Buonanno Foulkes, Governor-elect",
    "title_suffix": "Governor-elect Helena Foulkes",
    "nav_home": "Home",
    "nav_team": "Meet the Team",
    "nav_plans": "Plans",
    "nav_news": "News",
    "get_involved_btn": "Get involved",
    "get_involved_menu": "Get Involved",
    "menu": "Menu",
    "lang_group": "Language",
    "contact": "Contact",
    "follow": "Follow",
    "invite_link": "Invite the Governor-elect",
    "built_by": "Built by RI volunteers and funded by Helena Transition",
    "privacy": "Privacy Policy",

    "serve_title": "Serve in the administration",
    "serve_card": "Interested in a role in a state agency or the Governor's Office, or want to volunteer? Submit your interest.",
    "idea_title": "Share your idea",
    "idea_card": "What could the state fix quickly? Tell us the problem and your idea to help Rhode Island work better for everyone.",

    "home_desc": "Welcome from the Helena Foulkes transition team.",
    "home_h1": "Let's get to work.",
    "home_lead": "Helena's transition team is getting the state ready to work for all Rhode Islanders. Raise your hand to serve or share an idea.",
    "home_hero_alt": "Governor-elect Helena Foulkes",
    "home_ways": "Two ways to get involved",

    "team_title": "Team",
    "team_desc": "Governor-elect Helena Foulkes and the transition leadership team.",
    "team_eyebrow": "Meet the Team",
    "team_h1": "The people leading the transition",
    "team_lead": "The Governor-elect and the leadership team preparing the administration for January.",
    "team_photo1_alt": "Helena Foulkes with her husband",
    "team_photo2_alt": "Helena Foulkes talking with a family at a park",
    "team_bio_eyebrow": "Governor-elect Helena Foulkes",
    "team_bio_h2": "Meet Helena",
    "team_bio": [
        "Governor-elect Helena Buonanno Foulkes is a lifelong Rhode Islander, wife of 36 years, mother of four, grandmother, and cancer survivor who rose through the ranks of CVS over 25 years to become president of its retail division.",
        "As President of CVS pharmacy, Helena worked to ensure that consumers got the lowest possible prescription drug prices and removed tobacco products from the shelves—even though tobacco brought in $2 billion in revenue—because she believes that protecting people’s health is more important than profits.",
        "Helena has been working hard to improve our state, partnering with the mayor of Central Falls to improve their public schools, combatting homelessness and domestic violence as a board member and volunteer at non-profits, and meeting regularly with Rhode Islanders about their concerns.",
        "As Governor, Helena will remain committed to making life better for every Rhode Islander.",
    ],
    "team_leaders_h2": "Transition leadership team",
    "email_label": "Email",
    "leaders": [
        ("Bari Harlam", "Transition Co-Chair"),
        ("Mayor Maria Rivera", "Transition Co-Chair"),
        ("David Cicilline", "Transition Co-Chair"),
        ("Caitlin Molina", "Transition Executive Director"),
        ("RJ Kermes", "Transition Deputy Director, Operations"),
        ("Jon Romano", "Senior Advisor"),
    ],
    "team_committee_h2": "Leadership Transition Committee",
    "lead_name": "Name",
    "lead_role": "Current role and organization",

    "gi_title": "Get Involved",
    "gi_desc": "Tell us you want to serve or share an idea.",
    "gi_eyebrow": "Get Involved",
    "gi_h1": "Help build an administration that works",
    "gi_lead": "Tell us you want to serve or share an idea.",
    "gi_about_eyebrow": "About the transition",
    "gi_about_h2": "What guides our work",
    "gi_values": [
        ("Results first", "Residents see real change that measurably improves Rhode Island, lowering costs and expanding opportunity for everyone."),
        ("Open door", "The best ideas come from the residents of Rhode Island and the people who use state services every day. We want to hear from you."),
        ("Ready on day one", "Agency reviews, first-year priorities and key appointments in place by January."),
    ],
    "gi_meet_btn": "Meet the leadership team",
    "gi_action_eyebrow": "Take action",
    "gi_action_h2": "Choose how you'd like to help",

    "form_crumb": "Get Involved",
    "form_next_h2": "What happens next",
    "form_next": "Our team reviews every submission. We'll be in touch to learn more.",
    "form_loading": "Loading the form. If it doesn't appear, make sure JavaScript is on.",
    "idea_page_title": "Share Your Idea",
    "idea_desc": "Share an idea for the first 100 days.",
    "idea_lead": "What could the state fix quickly? Tell us the problem and your idea to help Rhode Island work better for everyone.",
    "idea_label": "Share your idea",
    "serve_page_title": "Serve in the Administration",
    "serve_desc": "Express interest in serving in the administration.",
    "serve_lead": "Interested in a role in a state agency or the Governor's Office, or want to volunteer? Tell us where you'd fit.",
    "serve_label": "Administration interest",
    "serve_note": '<strong>This is not a job application.</strong> Submitting this form does not replace a formal application for employment with the State of Rhode Island (<a href="https://www.ri.gov/employment/" target="_blank" rel="noopener">www.ri.gov/employment/</a>). It only signals your interest in being considered for a future role.',
    "invite_page_title": "Invite the Governor-elect",
    "invite_desc": "Request the Governor-elect for your event.",
    "invite_lead": "Request the Governor-elect or a member of the transition team for your event.",
    "invite_label": "Event request",

    "plans_title": "Plans",
    "plans_desc": "Helena Foulkes's plans for Rhode Island.",
    "plans_eyebrow": "Plans",
    "plans_h1": "Helena’s plans for Rhode Island",
    "plans_lead": "Helena ran a policy-focused campaign on getting things done for Rhode Islanders and improving their lives. These are the plans she will work to implement as Governor.",
    "plans_note": "",
    "plans_btn": "Read the plan",

    "news_title": "News",
    "news_desc": "News from the Helena Foulkes transition.",
    "news_eyebrow": "News",
    "news_h1": "Transition News",
    "news_lead": "Press releases and announcements from the transition.",
    "news_empty": "No press releases yet.",
}
TEXT = {"en": EN, "es": ES}
_missing = sorted(k for k in EN if k not in ES and k != "get_involved_menu")
if _missing:
    raise SystemExit(f"_build/es.py is missing these entries: {', '.join(_missing)}")

PH = '<span class="ph">{}</span>'


def ph(text):
    return PH.format(text)


def lang_switch(lang, en_href, es_href, extra=""):
    """EN | ES toggle. The current language is highlighted; the other is a link."""
    if lang == "es":
        en = f'<a href="{en_href}" lang="en" hreflang="en">EN</a>'
        es = '<span aria-current="true" lang="es">ES</span>'
    else:
        en = '<span aria-current="true" lang="en">EN</span>'
        es = f'<a href="{es_href}" lang="es" hreflang="es">ES</a>'
    label = TEXT[lang]["lang_group"]
    return f'<div class="lang{extra}" role="group" aria-label="{label}">{en}{es}</div>'


def page(path, title, body, desc="", forms=False, lang="en"):
    """Write one page. path is the English path (e.g. "team/"); Spanish pages go to es/<path>."""
    t = TEXT[lang]
    out_path = ("es/" + path) if lang == "es" else path
    depth = out_path.count("/")
    pre = "../" * depth                       # back to the site root
    home = pre + ("es/" if lang == "es" else "")  # root of this language
    has_es = path in ES_PAGES
    en_href = pre + path
    # English-only pages: ES goes to the Spanish news page from a press release, otherwise the Spanish home page.
    es_href = pre + "es/" + (path if has_es else ("news/" if path.startswith("news/") else ""))

    def link(p):
        """Link to page p in this language, or to the English page when there's no Spanish one."""
        return (home if p in ES_PAGES else pre) + p

    nav_items = [("", t["nav_home"]), ("team/", t["nav_team"]), ("plans/", t["nav_plans"]), ("news/", t["nav_news"])]
    nav = []
    for href, label in nav_items:
        cur = ' aria-current="page"' if href == path or (href and path.startswith(href)) else ""
        nav.append(f'<a href="{link(href)}"{cur}>{label}</a>')
    nav_html = "\n      ".join(nav)
    gi_cur = ' aria-current="page"' if path.startswith("get-involved/") else ""
    gi_menu = t.get("get_involved_menu", t["get_involved_btn"])
    menu_html = "\n          ".join(nav + [f'<a href="{link("get-involved/")}"{gi_cur}>{gi_menu}</a>'])
    script = f'\n<script src="{pre}assets/forms.js" defer></script>' if forms else ""
    full_title = t["title_suffix"] if not title else f"{title} | {t['title_suffix']}"
    alt = ""
    if has_es:
        alt = (f'\n<link rel="alternate" hreflang="en" href="{en_href}">'
               f'\n<link rel="alternate" hreflang="es" href="{pre}es/{path}">')
    switch = lang_switch(lang, en_href, es_href)
    switch_m = lang_switch(lang, en_href, es_href, " lang-m")
    html = f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{full_title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex, nofollow">{alt}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Semi+Condensed:wght@600;800&family=Montserrat:wght@400;500;700;800&display=swap">
<link rel="stylesheet" href="{pre}assets/site.css">{script}
</head>
<body>
<a class="skip" href="#main">{t["skip"]}</a>
<div class="proto" role="note"><div class="wrap"><b>{t["proto_label"]}</b><span>{t["proto"]}</span></div></div>

<header class="top">
  <div class="wrap">
    <a class="logo" href="{home}" aria-label="{t["logo_aria"]}"><img src="{pre}assets/logo-governor-elect.png" alt="" width="600" height="314"></a>
    <nav class="links" aria-label="Main">
      {nav_html}
      <a class="btn btn-green" href="{link("get-involved/")}"{gi_cur}>{t["get_involved_btn"]}</a>
      {switch}
    </nav>
    <div class="top-right">
      {switch_m}
      <details class="menu">
        <summary>{t["menu"]}</summary>
        <nav class="panel" aria-label="Main">
            {menu_html}
        </nav>
      </details>
    </div>
  </div>
</header>

<main id="main">
{body.replace("{home}", home).replace("{pre}", pre)}
</main>

<footer>
  <div class="wrap">
    <div>
      <a class="logo logo-foot" href="{home}"><img src="{pre}assets/logo-governor-elect.png" alt="{t["logo_alt"]}" width="600" height="314"></a>
    </div>
    <div>
      <h4>{t["contact"]}</h4>
      <p><a href="mailto:info@helenatransition.com">info@helenatransition.com</a></p>
      <p><a href="mailto:press@helenatransition.com">press@helenatransition.com</a></p>
      <p><a href="{link("invitehelena/")}">{t["invite_link"]}</a></p>
      <p>PO Box 6191, Providence, RI 02940</p>
    </div>
    <div>
      <h4>{t["follow"]}</h4>
      <ul>
        <li><a href="https://www.facebook.com/helena4RI" target="_blank" rel="noopener">Facebook</a></li>
        <li><a href="https://www.instagram.com/helenabfoulkes/" target="_blank" rel="noopener">Instagram</a></li>
        <li><a href="https://x.com/HelenaBFoulkes" target="_blank" rel="noopener">X</a></li>
      </ul>
    </div>
    <div class="legal">
      <p class="paid">{t["built_by"]}</p>
      <p><a href="{pre}privacy-policy/">{t["privacy"]}</a></p>
    </div>
  </div>
</footer>
</body>
</html>
"""
    out = ROOT / out_path / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print("wrote", out.relative_to(ROOT.parent))


# ---------- news: one file per press release in _build/news/ ----------
# File name = web address: _build/news/2026-11-04-some-title.txt -> news/2026-11-04-some-title/
# See "How to post a press release" in the README.

NEWS_SRC = ROOT / "_build" / "news"
NEWS_OUT = ROOT / "news"
SLUG_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-[a-z0-9-]+$")


def _fmt_date(d):
    return f"{d.strftime('%b')} {d.day}, {d.year}"


def _inline(text):
    """Escape text, then allow [link text](https://...) links."""
    t = _esc(text)
    return re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+|mailto:[^)\s]+)\)",
                  lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', t)


def _body_html(text):
    out = []
    for block in re.split(r"\n\s*\n", text.strip()):
        lines = [l.rstrip() for l in block.strip().splitlines() if l.strip()]
        if not lines:
            continue
        if lines[0].startswith("## "):
            out.append(f"<h3>{_inline(lines[0][3:])}</h3>")
            lines = lines[1:]
            if not lines:
                continue
        if all(l.startswith("- ") for l in lines):
            items = "".join(f"<li>{_inline(l[2:])}</li>" for l in lines)
            out.append(f"<ul>{items}</ul>")
        else:
            out.append(f"<p>{_inline(' '.join(lines))}</p>")
    return "\n        ".join(out)


def load_news():
    items = []
    for f in sorted(NEWS_SRC.glob("*.txt")):
        slug = f.stem
        if not SLUG_RE.match(slug):
            raise SystemExit(f"News file name must look like 2026-11-04-short-title.txt (lowercase, dashes): {f.name}")
        raw = f.read_text(encoding="utf-8")
        if "\n---" not in raw:
            raise SystemExit(f"{f.name}: put a line with --- between the details and the release text")
        meta_txt, body = raw.split("\n---", 1)
        meta = {}
        for line in meta_txt.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip().lower()] = v.strip()
        for k in ("title", "summary"):
            if not meta.get(k):
                raise SystemExit(f"{f.name}: missing '{k}:' line")
        d = _date.fromisoformat(meta.get("date") or slug[:10])
        items.append({
            "slug": slug, "date": d, "title": meta["title"], "summary": meta["summary"],
            "type": meta.get("type", "Press release"),
            "sample": meta.get("placeholder", "").lower() in ("yes", "true"),
            "body": body.lstrip("-").strip(),
        })
    items.sort(key=lambda i: (i["date"], i["slug"]), reverse=True)
    return items


NEWS = load_news()


def news_list(items, empty="No press releases yet."):
    if not items:
        return f'      <li><div></div><div><p>{empty}</p></div></li>'
    out = []
    for i in items:
        tag = f' {ph("Sample")}' if i["sample"] else ""
        out.append(f"""      <li><div class="when">{_fmt_date(i["date"])}</div><div><span class="tag">{_esc(i["type"])}</span><h3><a href="{{pre}}news/{i["slug"]}/">{_esc(i["title"])}</a></h3><p>{_esc(i["summary"])}{tag}</p></div></li>""")
    return "\n".join(out)


def release_page(i):
    note = f'\n        <p class="note warn">Sample press release. Placeholder text, not a real announcement.</p>' if i["sample"] else ""
    return f"""  <section class="hero slim">
    <div class="wrap">
      <p class="eyebrow"><a href="{{pre}}news/" style="color:inherit">News</a> / {_esc(i["type"])}</p>
      <h1>{_esc(i["title"])}</h1>
      <p class="lead">{_fmt_date(i["date"])}</p>
    </div>
  </section>

  <section class="band">
    <div class="wrap">
      <div class="prose release">{note}
        {_body_html(i["body"])}
        <p class="release-back"><a href="{{pre}}news/">&larr; All news</a></p>
      </div>
    </div>
  </section>
"""


# Plans from helenafoulkes.com/plans (Oct 22, 2026). PDFs are copied into plans/files/ so they
# keep working after the campaign site is replaced. Links are relative to the plans/ page.
PLANS = [
    ("Healthcare", "July 6", "Reimagining Rhode Island Healthcare",
     "Making Quality, Affordable Healthcare Accessible for All Rhode Islanders",
     "files/Reimagining-Rhode-Island-Healthcare.pdf"),
    ("Jobs/Economy", "June 4", "Believe in Rhode Island Part 3",
     "Creating & Growing Good-Paying Jobs",
     "files/Believe-in-Rhode-Island-Creating-Growing-Good-Paying-Jobs.pdf"),
    ("Jobs/Economy", "May 20", "Believe in Rhode Island Part 2",
     "Childcare and Transportation for Working Families",
     "files/Childcare-Transportation.pdf"),
    ("Jobs/Economy", "May 13", "Believe in Rhode Island Part 1",
     "$100 Million Proposal for Career and Technical Education",
     "files/Classroom-to-Career.pdf"),
    ("Energy", "April 2", "No False Choices",
     "Affordable Utility Bills and a Clean Energy Future",
     "files/No-False-Choices.pdf"),
    ("Housing", "March 2", "The Rhode Home Program",
     "Increasing Supply and Making Housing Affordable for all Rhode Islanders",
     "files/The-Rhode-Home-Program.pdf"),
    ("RIDOT Reform", "January 13", "Never Again: Accountability and Expertise to Stop the Next Bridge Disaster",
     "A Plan to Create the Office of Safety and Accountability, Putting Taxpayers and Safety Ahead of Contractor Profits",
     "files/Department-of-Transportation.pdf"),
    ("Ethics Reform", "January 12", "You Shouldn\u2019t Have to Know a Guy",
     "Ensuring the State House Works for All Rhode Islanders, Not Just the Insiders",
     "files/You-Shouldnt-Have-to-Know-a-Guy.pdf"),
]


def plan_cards(t, lang):
    out = []
    for i, (cat, date, title, desc, url) in enumerate(PLANS):
        if lang == "es":
            cat, title, desc = t["plans"][i]
        out.append(f"""      <div class="card">
        <p class="who">{cat}</p>
        <h3>{title}</h3>
        <p>{desc}</p>
        <div class="spacer"></div>
        <a class="btn btn-blue" href="{{pre}}plans/{url}" target="_blank" rel="noopener"{' hreflang="en"' if lang == "es" else ""}>{t["plans_btn"]}</a>
      </div>""")
    return "\n".join(out)


# ---------- shared content ----------

# The two forms promoted across the site (Home, Get Involved). Serve comes first.
# Invite the Governor-elect (invitehelena/) is linked only from the footer Contact section.
# Join a Board or Commission (get-involved/boards/) stays live but is not linked anywhere, and is English only.
def action_cards(t):
    cards = []
    for href, title, text, primary in (
        ("serve/", t["serve_title"], t["serve_card"], True),
        ("share-an-idea/", t["idea_title"], t["idea_card"], False),
    ):
        cls = "card primary" if primary else "card"
        btn = "btn-green" if primary else "btn-blue"
        cards.append(f"""      <div class="{cls}">
        <h3>{title}</h3>
        <p>{text}</p>
        <div class="spacer"></div>
        <a class="btn {btn}" href="{{home}}get-involved/{href}">{title}</a>
      </div>""")
    return "\n".join(cards)


# ---------- pages (each takes t = the text for one language) ----------

def home_page(t):
    return f"""  <section class="hero split photo">
    <div class="wrap">
      <div>
        <h1>{t["home_h1"]}</h1>
        <p class="lead">{t["home_lead"]}</p>
        <div class="ctas">
          <a class="btn btn-green" href="{{home}}get-involved/serve/">{t["serve_title"]}</a>
          <a class="btn btn-ghost" href="{{home}}get-involved/share-an-idea/">{t["idea_title"]}</a>
        </div>
      </div>
      <div class="hero-photo">
        <img src="{{pre}}assets/img/helena-hero.webp" alt="{t["home_hero_alt"]}" width="665" height="900">
      </div>
    </div>
  </section>

  <section class="band lav">
    <div class="wrap">
      <div class="sec-head">
        <h2>{t["home_ways"]}</h2>
      </div>
      <div class="cards">
{action_cards(t)}
      </div>
    </div>
  </section>

"""


# Leadership photos, in the same order as "leaders" in EN and ES. Only Caitlin shows an email.
LEADER_PHOTOS = ["bari-harlam", "maria-rivera", "david-cicilline", "caitlin-molina", "rj-kermes", "jon-romano"]
LEADER_EMAILS = {"caitlin-molina": "caitlin@helenatransition.com"}


def leaders(t):
    if len(t["leaders"]) != len(LEADER_PHOTOS):
        raise SystemExit(f'"leaders" has {len(t["leaders"])} people but LEADER_PHOTOS has {len(LEADER_PHOTOS)} photos')
    out = []
    for (name, title), img in zip(t["leaders"], LEADER_PHOTOS):
        email = LEADER_EMAILS.get(img)
        mail = f'\n          <p class="email"><a href="mailto:{email}">{t["email_label"]}</a></p>' if email else ""
        out.append(f"""        <div class="person">
          <img class="portrait" src="{{pre}}assets/img/team/{img}.webp" alt="{name}" width="480" height="480" loading="lazy">
          <h3>{name}</h3>
          <p class="role">{title}</p>{mail}
        </div>""")
    return "\n".join(out)


def team_page(t):
    bio = "\n".join(f"        <p>{p}</p>" for p in t["team_bio"])
    committee = "\n".join(
        f"""        <li><strong>{t["lead_name"]}</strong><span>{t["lead_role"]}</span></li>""" for _ in range(6))
    committee_section = f"""
  <section class="band">
    <div class="wrap">
      <div class="sec-head">
        <h2>{t["team_committee_h2"]}</h2>
      </div>
      <ul class="leads">
{committee}
      </ul>
    </div>
  </section>
""" if SHOW_COMMITTEE_LEADS else ""
    return f"""  <section class="hero slim">
    <div class="wrap">
      <p class="eyebrow">{t["team_eyebrow"]}</p>
      <h1>{t["team_h1"]}</h1>
      <p class="lead">{t["team_lead"]}</p>
    </div>
  </section>

  <section class="band">
    <div class="wrap bio">
      <div class="bio-photos">
        <img class="bio-photo" src="{{pre}}assets/img/helena-and-husband.webp" alt="{t["team_photo1_alt"]}" width="1000" height="620">
        <img class="bio-photo" src="{{pre}}assets/img/helena-at-park.webp" alt="{t["team_photo2_alt"]}" width="1000" height="667">
      </div>
      <div class="prose">
        <p class="eyebrow" style="color:var(--green)">{t["team_bio_eyebrow"]}</p>
        <h2 style="font-size:clamp(32px,4.6vw,48px);color:var(--blue);margin-bottom:18px">{t["team_bio_h2"]}</h2>
{bio}
      </div>
    </div>
  </section>

  <section class="band soft">
    <div class="wrap">
      <div class="sec-head">
        <h2>{t["team_leaders_h2"]}</h2>
      </div>
      <div class="people">
{leaders(t)}
      </div>
    </div>
  </section>
{committee_section}"""


def get_involved_page(t):
    values = "\n".join(f"        <li><h3>{h}</h3><p>{p}</p></li>" for h, p in t["gi_values"])
    return f"""  <section class="hero slim">
    <div class="wrap">
      <p class="eyebrow">{t["gi_eyebrow"]}</p>
      <h1>{t["gi_h1"]}</h1>
      <p class="lead">{t["gi_lead"]}</p>
    </div>
  </section>

  <section class="band">
    <div class="wrap">
      <div class="sec-head">
        <p class="eyebrow">{t["gi_about_eyebrow"]}</p>
        <h2>{t["gi_about_h2"]}</h2>
      </div>
      <ul class="values">
{values}
      </ul>
      <p style="margin-top:32px"><a class="btn btn-line" href="{{home}}team/">{t["gi_meet_btn"]}</a></p>
    </div>
  </section>

  <section class="band lav" id="forms">
    <div class="wrap">
      <div class="sec-head">
        <p class="eyebrow">{t["gi_action_eyebrow"]}</p>
        <h2>{t["gi_action_h2"]}</h2>
      </div>
      <div class="cards">
{action_cards(t)}
      </div>
    </div>
  </section>
"""


def form_page(t, lang, key, eyebrow, title, lead, side_html, label, crumb=True):
    trail = f'<a href="{{home}}get-involved/" style="color:inherit">{t["form_crumb"]}</a> / {eyebrow}' if crumb else eyebrow
    return f"""  <section class="hero slim">
    <div class="wrap">
      <p class="eyebrow">{trail}</p>
      <h1>{title}</h1>
      <p class="lead">{lead}</p>
    </div>
  </section>

  <section class="band lav">
    <div class="wrap form-layout">
      <div class="form-side">
        <h2 style="font-size:clamp(28px,3.6vw,38px);color:var(--blue);margin-bottom:14px">{t["form_next_h2"]}</h2>
        {side_html}
      </div>
      <div data-form="{key}" data-lang="{lang}" data-label="{label}">
        <p class="note">{t["form_loading"]}</p>
      </div>
    </div>
  </section>
"""


def idea_page(t, lang):
    return form_page(t, lang, "idea", t["idea_title"], t["idea_title"], t["idea_lead"],
                     f"<p>{t['form_next']}</p>", t["idea_label"])


def invite_page(t, lang):
    return form_page(t, lang, "event", t["invite_page_title"], t["invite_page_title"], t["invite_lead"],
                     f"<p>{t['form_next']}</p>", t["invite_label"], crumb=False)


def serve_page(t, lang):
    return form_page(t, lang, "serve", t["serve_title"], t["serve_title"], t["serve_lead"],
                     f"""<p>{t['form_next']}</p>
        <p class="note" style="margin-top:20px">{t['serve_note']}</p>""", t["serve_label"])


# English only (unlinked).
BOARDS = form_page(
    EN, "en", "boards", "Committees", "Join a committee",
    "Interested in being considered for a committee? Tell us where you'd fit.",
    f"<p>{EN['form_next']}</p>", "Committee interest")


def plans_page(t, lang):
    note = f'\n      <p class="note" style="margin-bottom:28px">{t["plans_note"]}</p>' if t["plans_note"] else ""
    return f"""  <section class="hero slim">
    <div class="wrap">
      <p class="eyebrow">{t["plans_eyebrow"]}</p>
      <h1>{t["plans_h1"]}</h1>
      <p class="lead">{t["plans_lead"]}</p>
    </div>
  </section>

  <section class="band soft">
    <div class="wrap">{note}
      <div class="cards">
{plan_cards(t, lang)}
      </div>
    </div>
  </section>
"""


def news_page(t, lang):
    # The list of press releases is always English (lang="en" on Spanish pages).
    list_lang = ' lang="en"' if lang == "es" else ""
    return f"""  <section class="hero slim">
    <div class="wrap">
      <p class="eyebrow">{t["news_eyebrow"]}</p>
      <h1>{t["news_h1"]}</h1>
      <p class="lead">{t["news_lead"]}</p>
    </div>
  </section>

  <section class="band">
    <div class="wrap">
      <ul class="news"{list_lang}>
{news_list(NEWS, t["news_empty"])}
      </ul>
    </div>
  </section>
"""

PRIVACY_PAGE = f"""  <section class="hero slim">
    <div class="wrap">
      <h1>Privacy Policy</h1>
    </div>
  </section>

  <section class="band">
    <div class="wrap legal-text">
{(ROOT / "_build" / "privacy.html").read_text(encoding="utf-8")}
    </div>
  </section>
"""



def redirect(path, target):
    """Small page that forwards an old address to its new one."""
    out = ROOT / path / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex, nofollow"><meta http-equiv="refresh" content="0; url={target}"><link rel="canonical" href="{target}"><title>Moved</title></head><body><p>This page has moved: <a href="{target}">continue</a>.</p></body></html>
""", encoding="utf-8")
    print("wrote", out.relative_to(ROOT.parent), "->", target)


def build_news():
    keep = {i["slug"] for i in NEWS}
    for i in NEWS:
        page(f"news/{i['slug']}/", _esc(i["title"]), release_page(i), _esc(i["summary"]))
    # Remove pages for releases whose file was deleted.
    for d in NEWS_OUT.iterdir():
        if d.is_dir() and SLUG_RE.match(d.name) and d.name not in keep:
            shutil.rmtree(d)
            print("removed", d.relative_to(ROOT.parent))



def build_lang(lang):
    t = TEXT[lang]
    page("", "", home_page(t), t["home_desc"], lang=lang)
    page("team/", t["team_title"], team_page(t), t["team_desc"], lang=lang)
    page("get-involved/", t["gi_title"], get_involved_page(t), t["gi_desc"], lang=lang)
    page("get-involved/share-an-idea/", t["idea_page_title"], idea_page(t, lang), t["idea_desc"], forms=True, lang=lang)
    page("invitehelena/", t["invite_page_title"], invite_page(t, lang), t["invite_desc"], forms=True, lang=lang)
    page("get-involved/serve/", t["serve_page_title"], serve_page(t, lang), t["serve_desc"], forms=True, lang=lang)
    page("plans/", t["plans_title"], plans_page(t, lang), t["plans_desc"], lang=lang)
    page("news/", t["news_title"], news_page(t, lang), t["news_desc"], lang=lang)


if __name__ == "__main__":
    build_lang("en")
    build_lang("es")
    redirect("get-involved/invite/", "../../invitehelena/")
    page("get-involved/boards/", "Join a Committee", BOARDS, "Express interest in serving on a committee.", forms=True)
    page("privacy-policy/", "Privacy Policy", PRIVACY_PAGE, "Privacy Policy and Terms of Use.")
    build_news()
