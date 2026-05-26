#!/usr/bin/env python3
"""Generate per-store Amazon API privacy policies."""
import os
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
EFFECTIVE_DATE = "May 26, 2026"

STORES = [
    {"slug": "a2e", "store": "A2eshop",                "company": "Avatech Corp.",                    "email": "amz@avatechcorp.us"},
    {"slug": "bat", "store": "Brand Avenue Trading",   "company": "One Brand Avenue Inc.",            "email": "amzops@onebrandavenue.com"},
    {"slug": "fac", "store": "Fancci US",              "company": "Fancci Corp.",                     "email": "amz.team@fancci.us"},
    {"slug": "czy", "store": "Cozey Direct",           "company": "Cozey, LLC",                       "email": "amz@cozeybrand.com"},
    {"slug": "smi", "store": "Schneider Care",         "company": "Schneider Medical Industries",     "email": "ecom@schneidercare.com"},
    {"slug": "she", "store": "SwiftHealth Essentials", "company": "SwiftHealth Essentials",           "email": "amz@swifthealthessentials.com"},
    {"slug": "tsp", "store": "TitanFlex Safety",       "company": "TitanFlex Safety Products",        "email": "amz@titanflexsafety.com"},
    {"slug": "sns", "store": "Safe & Savvy",           "company": "Safe and Savvy, Inc.",             "email": "amz@safesavvy.com"},
    {"slug": "suk", "store": "Schneider UK",           "company": "Schneider UK Enterprises, Ltd.",   "email": "amz@schneiderukenterprises.com", "uk": True},
]

CSS = """
:root { color-scheme: light; --bg: #f5f1e8; --panel: #fffaf2; --text: #1f1f1f; --muted: #5c5448; --accent: #8c4b1f; --border: #d9ccb8; --shadow: 0 18px 40px rgba(67,46,24,0.08); }
* { box-sizing: border-box; }
body { margin: 0; font-family: Georgia, "Times New Roman", serif; background: radial-gradient(circle at top left, rgba(207,171,120,0.2), transparent 28%), linear-gradient(180deg, #f0e5d4 0%, var(--bg) 45%, #efe6d7 100%); color: var(--text); line-height: 1.65; }
main { max-width: 860px; margin: 0 auto; padding: 48px 20px 72px; }
.card { background: var(--panel); border: 1px solid var(--border); border-radius: 24px; box-shadow: var(--shadow); overflow: hidden; }
.hero { padding: 40px 32px 28px; border-bottom: 1px solid var(--border); background: linear-gradient(135deg, rgba(140,75,31,0.08), rgba(140,75,31,0.02)), linear-gradient(180deg, rgba(255,255,255,0.75), rgba(255,250,242,0.95)); }
.eyebrow { margin: 0 0 10px; font-size: 0.8rem; letter-spacing: 0.14em; text-transform: uppercase; color: var(--accent); }
h1 { margin: 0; font-size: clamp(2rem, 4vw, 3.4rem); line-height: 1.05; font-weight: 700; }
.intro { margin: 18px 0 0; max-width: 60ch; color: var(--muted); font-size: 1.05rem; }
.meta { margin-top: 18px; color: var(--muted); font-size: 0.95rem; }
.content { padding: 12px 32px 36px; }
section { padding-top: 18px; }
h2 { margin: 0 0 10px; font-size: 1.2rem; color: var(--accent); }
p { margin: 0 0 14px; }
ul { margin: 0 0 14px 20px; padding: 0; }
li + li { margin-top: 6px; }
.contact { margin-top: 10px; padding: 18px 20px; background: rgba(140,75,31,0.06); border: 1px solid rgba(140,75,31,0.15); border-radius: 16px; }
.dir-list { list-style: none; margin: 0; padding: 0; }
.dir-list li { margin: 0; border-top: 1px solid var(--border); }
.dir-list li:first-child { border-top: 0; }
.dir-list a { display: block; padding: 14px 0; text-decoration: none; color: var(--text); }
.dir-list a:hover { color: var(--accent); }
.dir-list .co { color: var(--muted); font-size: 0.92rem; }
@media (max-width: 640px) { .hero, .content { padding-left: 20px; padding-right: 20px; } main { padding-top: 24px; padding-bottom: 40px; } }
"""

def head(title: str) -> str:
    return ("""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="noindex, nofollow, noarchive, nosnippet, noimageindex, notranslate">
  <meta name="googlebot" content="noindex, nofollow, noarchive, nosnippet, noimageindex, notranslate">
  <meta name="bingbot" content="noindex, nofollow, noarchive, nosnippet, noimageindex, notranslate">
  <meta name="google" content="notranslate">
  <meta name="ai" content="noai, noimageai">
  <title>""" + title + """</title>
  <style>""" + CSS + """</style>
</head>
<body>
  <main>
    <article class="card">""")

UK_SECTION = """
        <section>
          <h2>10. UK Data Protection (UK GDPR)</h2>
          <p>
            For the operation of the UK Amazon selling and advertising
            account, {company} acts as the data controller within the meaning
            of the UK General Data Protection Regulation (UK GDPR) and the
            Data Protection Act 2018. Lawful bases for processing include
            legitimate interests in operating the business, contractual
            necessity, and consent where required.
          </p>
          <p>
            UK and EEA data subjects have rights of access, rectification,
            erasure, restriction, objection, and portability with respect to
            their personal data. To exercise these rights or for any privacy
            inquiries, contact us at the email below. You also have the right
            to lodge a complaint with the UK Information Commissioner's
            Office (ICO) at <code>ico.org.uk</code>.
          </p>
        </section>
"""

def policy_html(store: dict) -> str:
    company = store["company"]
    email = store["email"]
    is_uk = store.get("uk", False)
    contact_num = "11" if is_uk else "10"
    title = f"{company} – Amazon API Privacy Policy"
    uk_block = UK_SECTION.format(company=company) if is_uk else ""
    return f"""{head(title)}
      <header class="hero">
        <p class="eyebrow">Privacy Notice</p>
        <h1>{company}</h1>
        <p class="intro">
          {company} uses an internal application to access, analyze, report
          on, and operate its authorized Amazon selling and advertising
          accounts.
        </p>
        <p class="meta">Effective Date: {EFFECTIVE_DATE}</p>
      </header>

      <div class="content">
        <section>
          <p>
            This Privacy Policy explains how information is handled when this
            application is connected to Amazon services on behalf of
            {company}, including Login with Amazon, the Amazon Selling
            Partner API (SP-API), and the Amazon Ads API.
          </p>
        </section>

        <section>
          <h2>1. Information We Collect</h2>
          <p>
            When the Amazon selling account and/or Amazon Ads account
            belonging to {company} is authorized for use with this
            application, the following information may be accessed and
            processed:
          </p>
          <ul>
            <li>Amazon seller and Ads account and profile identifiers (seller ID, marketplace ID, advertising profile ID)</li>
            <li>Orders, shipments, returns, refunds, and settlement reports</li>
            <li>Sales and traffic reports, inventory, catalog listings, and pricing data</li>
            <li>Brand Analytics, coupons, promotions, and competitive pricing reports</li>
            <li>Advertising campaigns, ad groups, keywords, targeting, and performance reports</li>
            <li>OAuth refresh tokens used to call the SP-API and Ads API on behalf of {company}</li>
            <li>Basic contact information provided directly to {company}, if any</li>
          </ul>
          <p>
            We do not collect or store any Amazon password through this
            application. Personally Identifiable Information (PII) contained
            in Amazon orders (such as buyer names, addresses, or phone
            numbers) is not retained beyond what is strictly required to
            operate authorized workflows, and is handled in accordance with
            Amazon's Data Protection Policy and Acceptable Use Policy.
          </p>
        </section>

        <section>
          <h2>2. How We Use Information</h2>
          <p>This information is used only to:</p>
          <ul>
            <li>connect to the authorized Amazon selling and advertising accounts of {company},</li>
            <li>retrieve orders, settlements, inventory, advertising data, and other reports,</li>
            <li>monitor store and campaign performance,</li>
            <li>support reporting and internal analysis,</li>
            <li>improve store operations, campaign management, and optimization workflows,</li>
            <li>maintain, debug, and secure the application.</li>
          </ul>
          <p>
            Amazon Selling Partner and Amazon Ads data are not used for any
            purpose unrelated to the operation, reporting, management, or
            optimization of the authorized accounts of {company}.
          </p>
        </section>

        <section>
          <h2>3. Who Can Use This Tool</h2>
          <p>
            This application is intended only for private internal use by
            {company} in connection with its own authorized Amazon selling
            and advertising accounts.
          </p>
        </section>

        <section>
          <h2>4. Data Sharing</h2>
          <p>
            We do not sell Amazon Selling Partner data, Amazon Ads data, or
            personal information.
          </p>
          <p>Information may be shared only when necessary:</p>
          <ul>
            <li>with hosting, cloud, analytics, or technical service providers who support operation of the application,</li>
            <li>when required by law, regulation, legal process, or governmental request,</li>
            <li>to protect the security, integrity, or lawful operation of the application.</li>
          </ul>
        </section>

        <section>
          <h2>5. Data Retention</h2>
          <p>
            Data is retained only for as long as reasonably necessary to
            operate the application, maintain reporting history, support
            optimization workflows, comply with legal obligations, and
            resolve disputes.
          </p>
          <p>
            When data is no longer needed, it will be deleted or anonymized
            where reasonably practical.
          </p>
        </section>

        <section>
          <h2>6. Data Security</h2>
          <p>
            Reasonable administrative, technical, and organizational
            safeguards are used to protect information from unauthorized
            access, disclosure, alteration, or destruction.
          </p>
          <p>
            However, no method of electronic transmission or storage is
            completely secure, and absolute security cannot be guaranteed.
          </p>
        </section>

        <section>
          <h2>7. Third-Party Services</h2>
          <p>
            This application interacts with third-party services provided by
            Amazon, including Login with Amazon, the Amazon Selling Partner
            API, and the Amazon Ads API. Use of those services is also
            subject to Amazon's own terms, notices, and policies, including
            the Amazon Services API Developer Agreement, the Amazon
            Acceptable Use Policy, and the Amazon Data Protection Policy.
          </p>
        </section>

        <section>
          <h2>8. Your Choices</h2>
          <p>
            To stop allowing this application to access the Amazon selling
            or advertising account of {company}, access can be revoked at
            any time through Seller Central (Apps &amp; Services &rarr;
            Manage Your Apps), through the relevant Amazon Ads account
            settings, or by contacting {company} at the email below.
          </p>
        </section>

        <section>
          <h2>9. Changes to This Privacy Policy</h2>
          <p>
            This Privacy Policy may be updated from time to time. Any updates
            will be posted at this URL, and the Effective Date above will be
            revised accordingly.
          </p>
        </section>
{uk_block}
        <section>
          <h2>{contact_num}. Contact</h2>
          <div class="contact">
            <p><strong>Company:</strong> {company}</p>
            <p><strong>Email:</strong> {email}</p>
          </div>
        </section>
      </div>
    </article>
  </main>
</body>
</html>
"""

def index_html() -> str:
    items = "\n".join(
        f'          <li><a href="{s["slug"]}/"><strong>{s["store"]}</strong><br><span class="co">{s["company"]}</span></a></li>'
        for s in STORES
    )
    return f"""{head("Amazon API Privacy Policies")}
      <header class="hero">
        <p class="eyebrow">Privacy Notices</p>
        <h1>Amazon API Privacy Policies</h1>
        <p class="intro">
          Per-account privacy notices for Amazon Selling Partner API and
          Amazon Ads API integrations. Each store's notice describes how
          information is handled when its Amazon accounts are authorized
          for use with the corresponding internal application.
        </p>
        <p class="meta">Effective Date: {EFFECTIVE_DATE}</p>
      </header>
      <div class="content">
        <section>
          <ul class="dir-list">
{items}
          </ul>
        </section>
      </div>
    </article>
  </main>
</body>
</html>
"""

def main():
    for s in STORES:
        d = ROOT / s["slug"]
        d.mkdir(exist_ok=True)
        (d / "index.html").write_text(policy_html(s), encoding="utf-8")
        print(f"wrote {s['slug']}/index.html  ({s['company']})")
    (ROOT / "index.html").write_text(index_html(), encoding="utf-8")
    print("wrote index.html (directory)")

if __name__ == "__main__":
    main()
