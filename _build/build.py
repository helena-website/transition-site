#!/usr/bin/env python3
"""Build the transition site pages from one shared header/footer.

Run from the repo root:  python3 _build/build.py
Writes static HTML into the repo root. All links are relative, so the site
works at any address (GitHub Pages staging, or the root of helenafoulkes.com).
GitHub Pages (Jekyll) does not publish folders starting with "_", so this
script stays private to the repo.
"""
import re
import shutil
from datetime import date as _date
from html import escape as _esc
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # repo root

PROTO = "Sample design for the transition team's review."

NAV = [
    ("", "Home"),
    ("team/", "Meet the Team"),
    ("plans/", "Plans"),
    ("news/", "News"),
]

PH = '<span class="ph">{}</span>'


def ph(text):
    return PH.format(text)


def page(path, title, body, desc="", forms=False):
    depth = path.count("/")
    pre = "../" * depth
    nav = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == path or (href and path.startswith(href)) else ""
        nav.append(f'<a href="{pre}{href}"{cur}>{label}</a>')
    nav_html = "\n      ".join(nav)
    gi_cur = ' aria-current="page"' if path.startswith("get-involved/") else ""
    menu_html = "\n          ".join(nav + [f'<a href="{pre}get-involved/"{gi_cur}>Get Involved</a>'])
    script = f'\n<script src="{pre}assets/forms.js" defer></script>' if forms else ""
    full_title = "Helena Foulkes, Governor-Elect" if not title else f"{title} | Helena Foulkes, Governor-Elect"
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{full_title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex, nofollow">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Semi+Condensed:wght@600;800&family=Montserrat:wght@400;500;700;800&display=swap">
<link rel="stylesheet" href="{pre}assets/site.css">{script}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="proto" role="note"><div class="wrap"><b>Prototype</b><span>{PROTO}</span></div></div>

<header class="top">
  <div class="wrap">
    <a class="logo" href="{pre}" aria-label="Helena Foulkes Transition home"><img src="{pre}assets/logo-governor-elect.png" alt="" width="600" height="314"></a>
    <nav class="links" aria-label="Main">
      {nav_html}
      <a class="btn btn-green" href="{pre}get-involved/"{gi_cur}>Get involved</a>
    </nav>
    <details class="menu">
      <summary>Menu</summary>
      <nav class="panel" aria-label="Main">
          {menu_html}
      </nav>
    </details>
  </div>
</header>

<main id="main">
{body.replace("{pre}", pre)}
</main>

<footer>
  <div class="wrap">
    <div>
      <a class="logo logo-foot" href="{pre}"><img src="{pre}assets/logo-governor-elect.png" alt="Helena Buonanno Foulkes, Governor-Elect" width="600" height="314"></a>
    </div>
    <div>
      <h4>Contact</h4>
      <p><a href="mailto:info@helenatransition.com">info@helenatransition.com</a></p>
      <p><a href="mailto:press@helenatransition.com">press@helenatransition.com</a></p>
      <p><a href="{pre}invitehelena/">Invite the Governor-Elect</a></p>
      <p>PO Box 6191, Providence, RI 02940</p>
    </div>
    <div>
      <h4>Follow</h4>
      <ul>
        <li><a href="https://www.facebook.com/helena4RI" target="_blank" rel="noopener">Facebook</a></li>
        <li><a href="https://www.instagram.com/helenabfoulkes/" target="_blank" rel="noopener">Instagram</a></li>
        <li><a href="https://x.com/HelenaBFoulkes" target="_blank" rel="noopener">X</a></li>
      </ul>
    </div>
    <div class="legal">
      <p class="paid">Built by RI volunteers and funded by Helena Transition</p>
      <p><a href="{pre}privacy-policy/">Privacy Policy</a></p>
    </div>
  </div>
</footer>
</body>
</html>
"""
    out = ROOT / path / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print("wrote", out.relative_to(ROOT.parent))


# ---------- shared content ----------

# The two forms promoted across the site (Home, Get Involved, footer). Serve comes first.
# Invite the Governor-Elect (invitehelena/) is linked only from the footer Contact section.
# Join a Board or Commission (get-involved/boards/) stays live but is not linked anywhere.
ACTIONS = [
    ("serve/", "Serve in the administration",
     "Interested in a role in a state agency or the Governor's Office? Submit your interest and résumé.", True),
    ("share-an-idea/", "Share your idea",
     "What could the state fix quickly? Tell us the problem and your idea to help Rhode Island work better for everyone.", False),
]


def action_cards(pre_to_gi):
    cards = []
    for href, title, text, primary in ACTIONS:
        cls = "card primary" if primary else "card"
        btn = "btn-green" if primary else "btn-blue"
        cards.append(f"""      <div class="{cls}">
        <h3>{title}</h3>
        <p>{text}</p>
        <div class="spacer"></div>
        <a class="btn {btn}" href="{pre_to_gi}{href}">{title}</a>
      </div>""")
    return "\n".join(cards)


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


def news_list(items):
    if not items:
        return '      <li><div></div><div><p>No press releases yet.</p></div></li>'
    out = []
    for i in items:
        tag = f' {ph("Sample")}' if i["sample"] else ""
        out.append(f"""      <li><div class="when">{_fmt_date(i["date"])}</div><div><span class="tag">{_esc(i["type"])}</span><h3><a href="{i["slug"]}/">{_esc(i["title"])}</a></h3><p>{_esc(i["summary"])}{tag}</p></div></li>""")
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


def plan_cards():
    out = []
    for cat, date, title, desc, url in PLANS:
        out.append(f"""      <div class="card">
        <p class="who">{cat}</p>
        <h3>{title}</h3>
        <p>{desc}</p>
        <div class="spacer"></div>
        <a class="btn btn-blue" href="{url}" target="_blank" rel="noopener">Read the plan</a>
      </div>""")
    return "\n".join(out)


# ---------- pages ----------

HOME = f"""  <section class="hero split photo">
    <div class="wrap">
      <div>
        <h1>Let's get to work.</h1>
        <p class="lead">Helena's transition team is getting the state ready to work for all Rhode Islanders. Raise your hand to serve or share an idea.</p>
        <div class="ctas">
          <a class="btn btn-green" href="{{pre}}get-involved/serve/">Serve in the administration</a>
          <a class="btn btn-ghost" href="{{pre}}get-involved/share-an-idea/">Share your idea</a>
        </div>
      </div>
      <div class="hero-photo">
        <img src="{{pre}}assets/img/helena-hero.webp" alt="Governor-Elect Helena Foulkes" width="665" height="900">
      </div>
    </div>
  </section>

  <section class="band lav">
    <div class="wrap">
      <div class="sec-head">
        <h2>Two ways to get involved</h2>
      </div>
      <div class="cards">
{action_cards("{pre}get-involved/")}
      </div>
    </div>
  </section>

"""


def leader(name, title, img, email=""):
    mail = f'\n          <p class="email"><a href="mailto:{email}">Email</a></p>' if email else ""
    return f"""        <div class="person">
          <img class="portrait" src="{{pre}}assets/img/team/{img}.webp" alt="{name}" width="480" height="480" loading="lazy">
          <h3>{name}</h3>
          <p class="role">{title}</p>{mail}
        </div>"""


LEADERS = "\n".join([
    leader("Bari Harlam", "Transition Chair", "bari-harlam"),
    leader("Mayor Maria Rivera", "Transition Chair", "maria-rivera"),
    leader("David Cicilline", "Transition Chair", "david-cicilline"),
    leader("Caitlin Molina", "Transition Executive Director", "caitlin-molina", "caitlin@helenatransition.com"),
    leader("RJ Kermes", "Transition Deputy Director, Operations", "rj-kermes"),
])

COMMITTEE_LEADS = "\n".join(
    """        <li><strong>Name</strong><span>Current role and organization</span></li>"""
    for _ in range(6))

TEAM = f"""  <section class="hero slim">
    <div class="wrap">
      <p class="eyebrow">Meet the Team</p>
      <h1>The people leading the transition</h1>
      <p class="lead">The Governor-Elect and the leadership team preparing the administration for January.</p>
    </div>
  </section>

  <section class="band">
    <div class="wrap bio">
      <div class="bio-photos">
        <img class="bio-photo" src="{{pre}}assets/img/helena-and-husband.webp" alt="Helena Foulkes with her husband" width="1000" height="620">
        <img class="bio-photo" src="{{pre}}assets/img/helena-at-park.webp" alt="Helena Foulkes talking with a family at a park" width="1000" height="667">
      </div>
      <div class="prose">
        <p class="eyebrow" style="color:var(--green)">Governor-Elect</p>
        <h2 style="font-size:clamp(32px,4.6vw,48px);color:var(--blue);margin-bottom:18px">Meet Helena</h2>
        <p>Helena Buonanno Foulkes is a lifelong Rhode Islander, wife of 36 years, mother of four, grandmother, and cancer survivor who rose through the ranks of CVS over 25 years to become president of its retail division.</p>
        <p>As President of CVS pharmacy, Helena worked to ensure that consumers got the lowest possible prescription drug prices and removed tobacco products from the shelves\u2014even though tobacco brought in $2 billion in revenue\u2014because she believes that protecting people\u2019s health is more important than profits.</p>
        <p>Since coming just short in the 2022 race for governor, Helena has been working hard to improve our state, including partnering with the mayor of Central Falls to improve their public schools and combatting homelessness and domestic violence as a board member and volunteer at Rhode Island non-profits. Helena regularly holds community gatherings at people\u2019s homes to hear directly from Rhode Islanders about their concerns.</p>
        <p>Helena is a compassionate, experienced and effective leader. Now, she\u2019s committed to making life better for every Rhode Islander.</p>
      </div>
    </div>
  </section>

  <section class="band soft">
    <div class="wrap">
      <div class="sec-head">
        <h2>Transition leadership team</h2>
      </div>
      <div class="people">
{LEADERS}
      </div>
    </div>
  </section>

  <section class="band">
    <div class="wrap">
      <div class="sec-head">
        <h2>Leadership Transition Committee</h2>
      </div>
      <ul class="leads">
{COMMITTEE_LEADS}
      </ul>
    </div>
  </section>
"""

GET_INVOLVED = f"""  <section class="hero slim">
    <div class="wrap">
      <p class="eyebrow">Get Involved</p>
      <h1>Help build an administration that works</h1>
      <p class="lead">Tell us you want to serve, or share an idea for the first 100 days.</p>
    </div>
  </section>

  <section class="band">
    <div class="wrap">
      <div class="sec-head">
        <p class="eyebrow">About the transition</p>
        <h2>What guides our work</h2>
      </div>
      <ul class="values">
        <li><h3>Results first</h3><p>Measure success by what changes for Rhode Islanders, not by press releases.</p></li>
        <li><h3>Open door</h3><p>The best ideas come from people who use state services every day. We want to hear from them.</p></li>
        <li><h3>Ready on day one</h3><p>Agency reviews, first-year priorities and key appointments in place by January 5.</p></li>
      </ul>
      <p style="margin-top:32px"><a class="btn btn-line" href="{{pre}}team/">Meet the leadership team</a></p>
    </div>
  </section>

  <section class="band lav" id="forms">
    <div class="wrap">
      <div class="sec-head">
        <p class="eyebrow">Take action</p>
        <h2>Choose how you'd like to help</h2>
      </div>
      <div class="cards">
{action_cards("")}
      </div>
    </div>
  </section>
"""


def form_page(key, eyebrow, title, lead, side_title, side_html, label, crumb=True):
    trail = f'<a href="{{pre}}get-involved/" style="color:inherit">Get Involved</a> / {eyebrow}' if crumb else eyebrow
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
        <h2 style="font-size:clamp(28px,3.6vw,38px);color:var(--blue);margin-bottom:14px">{side_title}</h2>
        {side_html}
      </div>
      <div data-form="{key}" data-label="{label}">
        <p class="note">Loading the form. If it doesn't appear, make sure JavaScript is on.</p>
      </div>
    </div>
  </section>
"""


IDEA = form_page(
    "idea", "Share your idea", "Share your idea",
    "What could the state fix quickly? Tell us the problem and your idea to help Rhode Island work better for everyone.",
    "What happens next",
    """<p>Our team reviews every submission. We'll be in touch if we'd like to learn more.</p>""",
    "Share your idea")

INVITE = form_page(
    "event", "Invite the Governor-Elect", "Invite the Governor-Elect",
    "Request the Governor-Elect or a member of the transition team for your event.",
    "What happens next",
    """<p>Our team reviews every submission. We'll be in touch if we'd like to learn more.</p>""",
    "Event request", crumb=False)

BOARDS = form_page(
    "boards", "Committees", "Join a committee",
    "Interested in being considered for a committee? Tell us where you'd fit.",
    "What happens next",
    """<p>Our team reviews every submission. We'll be in touch if we'd like to learn more.</p>""",
    "Committee interest")

SERVE = form_page(
    "serve", "Serve in the administration", "Serve in the administration",
    "Interested in a role in a state agency or the Governor's Office? Tell us where you'd fit.",
    "What happens next",
    """<p>Our team reviews every submission. We'll be in touch if we'd like to learn more.</p>
        <p class="note" style="margin-top:20px"><strong>This is not a job application.</strong> Submitting this form does not replace a formal application for employment with the State of Rhode Island (<a href="https://www.ri.gov/employment/" target="_blank" rel="noopener">www.ri.gov/employment/</a>). It only signals your interest in being considered for a future role.</p>""",
    "Administration interest")

NEWS_PAGE = f"""  <section class="hero slim">
    <div class="wrap">
      <p class="eyebrow">News</p>
      <h1>Transition news</h1>
      <p class="lead">Press releases and announcements from the transition.</p>
    </div>
  </section>

  <section class="band">
    <div class="wrap">
      <ul class="news">
{news_list(NEWS)}
      </ul>
    </div>
  </section>
"""

PLANS_PAGE = f"""  <section class="hero slim">
    <div class="wrap">
      <p class="eyebrow">Plans</p>
      <h1>Helena\u2019s plans for Rhode Island</h1>
      <p class="lead">Helena ran a policy-focused campaign on getting things done for Rhode Islanders and improving their lives. These are the plans she will work to implement as governor.</p>
    </div>
  </section>

  <section class="band soft">
    <div class="wrap">
      <div class="cards">
{plan_cards()}
      </div>
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
    page("news/", "News", NEWS_PAGE, "News from the Helena Foulkes transition.")
    keep = {i["slug"] for i in NEWS}
    for i in NEWS:
        page(f"news/{i['slug']}/", _esc(i["title"]), release_page(i), _esc(i["summary"]))
    # Remove pages for releases whose file was deleted.
    for d in NEWS_OUT.iterdir():
        if d.is_dir() and SLUG_RE.match(d.name) and d.name not in keep:
            shutil.rmtree(d)
            print("removed", d.relative_to(ROOT.parent))


if __name__ == "__main__":
    page("", "", HOME, "Welcome from the Helena Foulkes transition team.")
    page("team/", "Meet the Team", TEAM, "Governor-Elect Helena Foulkes and the transition leadership team.")
    page("get-involved/", "Get Involved", GET_INVOLVED, "Serve in the administration, or share an idea for the first 100 days.")
    page("get-involved/share-an-idea/", "Share Your Idea", IDEA, "Share an idea for the first 100 days.", forms=True)
    page("invitehelena/", "Invite the Governor-Elect", INVITE, "Request the Governor-Elect for your event.", forms=True)
    redirect("get-involved/invite/", "../../invitehelena/")
    page("get-involved/boards/", "Join a Committee", BOARDS, "Express interest in serving on a committee.", forms=True)
    page("get-involved/serve/", "Serve in the Administration", SERVE, "Express interest in serving in the administration.", forms=True)
    page("plans/", "Plans", PLANS_PAGE, "Helena Foulkes's plans for Rhode Island.")
    page("privacy-policy/", "Privacy Policy", PRIVACY_PAGE, "Privacy Policy and Terms of Use.")
    build_news()
