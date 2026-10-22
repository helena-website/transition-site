#!/usr/bin/env python3
"""Build the transition site pages from one shared header/footer.

Run from the repo root:  python3 _build/build.py
Writes static HTML into the repo root. All links are relative, so the site
works at any address (GitHub Pages staging, or the root of helenafoulkes.com).
GitHub Pages (Jekyll) does not publish folders starting with "_", so this
script stays private to the repo.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # repo root

PROTO = "Sample design for the transition team's review."

NAV = [
    ("", "Home"),
    ("team/", "Meet the Team"),
    ("plans/", "Plans"),
    ("endorsements/", "Endorsements"),
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
        cur = ' aria-current="page"' if href == path else ""
        nav.append(f'<a href="{pre}{href}"{cur}>{label}</a>')
    nav_html = "\n      ".join(nav)
    gi_cur = ' aria-current="page"' if path.startswith("get-involved/") else ""
    menu_html = "\n          ".join(nav + [f'<a href="{pre}get-involved/"{gi_cur}>Get Involved</a>'])
    script = f'\n<script src="{pre}assets/forms.js" defer></script>' if forms else ""
    full_title = "Helena Foulkes Transition" if not title else f"{title} | Helena Foulkes Transition"
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
      <p><a href="mailto:info@helenafoulkes.com">info@helenafoulkes.com</a></p>
      <p>Press: <a href="mailto:press@helenafoulkes.com">press@helenafoulkes.com</a></p>
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
      <p class="paid">Paid for by Helena for RI</p>
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

ACTIONS = [
    ("share-an-idea/", "Share your idea", "Policy team",
     "Have a fix for something state government could do better? Send it to the team building the first-year agenda."),
    ("invite/", "Invite the Governor-Elect", "Scheduling",
     "Request the Governor-Elect or a member of the team for your event, meeting or community gathering."),
    ("boards/", "Join a board or commission", "Personnel",
     "Rhode Island's boards and commissions shape policy across the state. Tell us where you'd like to serve."),
    ("serve/", "Serve in the administration", "Personnel",
     "Interested in a role in a state agency or the Governor's Office? Submit your interest and résumé."),
]


def action_cards(pre_to_gi):
    cards = []
    for href, title, who, text in ACTIONS:
        cards.append(f"""      <div class="card">
        <h3>{title}</h3>
        <p>{text}</p>
        <div class="spacer"></div>
        <a class="btn btn-blue" href="{pre_to_gi}{href}">{title}</a>
      </div>""")
    return "\n".join(cards)


NEWS = [
    ("Nov 4, 2026", "Press release", "Governor-Elect Foulkes announces transition leadership team",
     "Co-chairs and senior advisors who will guide the transition through Inauguration Day."),
    ("Nov 10, 2026", "Committee announcement", "Transition policy committees named",
     "Eight committees will review state agencies and recommend first-year priorities."),
    ("Dec 1, 2026", "Cabinet rollout", "First cabinet appointments announced",
     "The Governor-Elect names the first members of her cabinet."),
]


def news_list(items):
    out = []
    for when, tag, title, text in items:
        out.append(f"""      <li><div class="when">{when}</div><div><span class="tag">{tag}</span><h3><a href="#">{title}</a></h3><p>{text} {ph("Sample")}</p></div></li>""")
    return "\n".join(out)


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
        <h1>Thank you, Rhode Island.</h1>
        <p class="lead">Thank you to everyone who knocked doors, made calls and cast a ballot. Now the work begins. The transition team is getting ready for day one, and we want your ideas and your help.</p>
        <div class="ctas">
          <a class="btn btn-green" href="{{pre}}get-involved/">Get involved</a>
          <a class="btn btn-ghost" href="{{pre}}team/">Meet the Governor-Elect</a>
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
        <p class="eyebrow">Get involved</p>
        <h2>Four ways to help build the administration</h2>
        <p>Every submission goes to the team responsible for it, and every one is read.</p>
      </div>
      <div class="cards">
{action_cards("{pre}get-involved/")}
      </div>
    </div>
  </section>

"""

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
        <p class="eyebrow">Leadership</p>
        <h2>Transition leadership team</h2>
        <p>Names and titles to come with the leadership announcement. {ph("TBD")}</p>
      </div>
      <div class="people">
        <div class="person"><div class="portrait" role="img" aria-label="Photo placeholder">Photo</div><h3>Name TBD</h3><p>Transition Co-Chair</p></div>
        <div class="person"><div class="portrait" role="img" aria-label="Photo placeholder">Photo</div><h3>Name TBD</h3><p>Transition Co-Chair</p></div>
        <div class="person"><div class="portrait" role="img" aria-label="Photo placeholder">Photo</div><h3>Name TBD</h3><p>Executive Director</p></div>
        <div class="person"><div class="portrait" role="img" aria-label="Photo placeholder">Photo</div><h3>Name TBD</h3><p>Policy Director</p></div>
      </div>
    </div>
  </section>
"""

GET_INVOLVED = f"""  <section class="hero slim">
    <div class="wrap">
      <p class="eyebrow">Get Involved</p>
      <h1>Help build an administration that works</h1>
      <p class="lead">Share an idea, invite the Governor-Elect to your community, or tell us you want to serve.</p>
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


def form_page(key, eyebrow, title, lead, side_title, side_html, label):
    return f"""  <section class="hero slim">
    <div class="wrap">
      <p class="eyebrow"><a href="{{pre}}get-involved/" style="color:inherit">Get Involved</a> / {eyebrow}</p>
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
    "Tell the policy team what state government should do better, and how.",
    "What happens next",
    """<p>Our team reviews every submission. We'll be in touch if we'd like to learn more.</p>""",
    "Share your idea")

INVITE = form_page(
    "event", "Invite the Governor-Elect", "Invite the Governor-Elect",
    "Request the Governor-Elect or a member of the transition team for your event.",
    "What happens next",
    """<p>Our team reviews every submission. We'll be in touch if we'd like to learn more.</p>""",
    "Event request")

BOARDS = form_page(
    "boards", "Boards and commissions", "Join a board or commission",
    "Interested in being considered for a board or commission? Tell us where you'd fit.",
    "What happens next",
    """<p>Our team reviews every submission. We'll be in touch if we'd like to learn more.</p>""",
    "Board and commission interest")

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
      <p class="lead">Press releases, committee announcements and cabinet appointments.</p>
    </div>
  </section>

  <section class="band">
    <div class="wrap">
      <ul class="news">
{news_list(NEWS[::-1])}
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

# Endorsements from helenafoulkes.com/endorsements (Oct 22, 2026), stored in _build/endorsements.json.
import json as _json
from html import escape as _esc
ENDORSEMENTS = _json.loads((ROOT / "_build" / "endorsements.json").read_text(encoding="utf-8"))


def endorsement_sections():
    order = []
    for e in ENDORSEMENTS:
        if e["section"] not in order:
            order.append(e["section"])
    out = []
    for sec in order:
        items = [e for e in ENDORSEMENTS if e["section"] == sec]
        if all(e.get("img") for e in items):
            cards = "\n".join(
                f'''        <figure class="endorser"><img src="{{pre}}assets/img/endorsements/{e["img"]}" alt="" width="320" height="320" loading="lazy"><figcaption>{_esc(e["name"])}</figcaption></figure>'''
                for e in items)
            body = f'<div class="endorsers">\n{cards}\n      </div>'
        else:
            lis = "\n".join(f"        <li>{_esc(e['name'])}</li>" for e in items)
            body = f'<ul class="committees">\n{lis}\n      </ul>'
        out.append(f'''  <section class="band{" soft" if len(out) % 2 else ""}">
    <div class="wrap">
      <div class="sec-head"><h2>{_esc(sec)}</h2></div>
      {body}
    </div>
  </section>''')
    return "\n\n".join(out)


ENDORSEMENTS_PAGE = f"""  <section class="hero slim">
    <div class="wrap">
      <h1>Endorsements</h1>
    </div>
  </section>

{endorsement_sections()}
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

if __name__ == "__main__":
    page("", "", HOME, "Welcome from the Helena Foulkes transition team.")
    page("team/", "Meet the Team", TEAM, "Governor-Elect Helena Foulkes and the transition leadership team.")
    page("get-involved/", "Get Involved", GET_INVOLVED, "Share an idea, invite the Governor-Elect, or tell us you want to serve.")
    page("get-involved/share-an-idea/", "Share Your Idea", IDEA, "Send an idea to the transition policy team.", forms=True)
    page("get-involved/invite/", "Invite the Governor-Elect", INVITE, "Request the Governor-Elect for your event.", forms=True)
    page("get-involved/boards/", "Join a Board or Commission", BOARDS, "Express interest in a board or commission appointment.", forms=True)
    page("get-involved/serve/", "Serve in the Administration", SERVE, "Express interest in serving in the administration.", forms=True)
    page("plans/", "Plans", PLANS_PAGE, "Helena Foulkes's plans for Rhode Island.")
    page("endorsements/", "Endorsements", ENDORSEMENTS_PAGE, "Leaders, unions and organizations endorsing Helena Foulkes.")
    page("privacy-policy/", "Privacy Policy", PRIVACY_PAGE, "Privacy Policy and Terms of Use.")
    page("news/", "News", NEWS_PAGE, "News from the Helena Foulkes transition.")
