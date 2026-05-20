"""
build.py — Static site generator for gprai.github.io
Run: python build.py
Output: docs/ folder ready for GitHub Pages
"""

import os
import json
import shutil
from pathlib import Path

# ── Output directory ──────────────────────────────────────────────────────────
OUT = Path("docs")
OUT.mkdir(exist_ok=True)
(OUT / "projects").mkdir(exist_ok=True)

# ── Site data (edit this to update content) ───────────────────────────────────
SITE = {
    "name": "Gyan Prakash Rai",
    "tagline": "AWS & Azure Platform Engineer · DevOps · Cloud Infrastructure",
    "email": "gprai86@gmail.com",
  # Optional: add your Calendly link (https://calendly.com/yourname) to enable instant scheduling
  "calendly": "",
  # Optional: form action for an external form endpoint (Formspree, Getform). Leave empty to use mailto fallback.
  "form_action": "",
    "linkedin": "https://www.linkedin.com/in/gyan-prakash-rai-24782413/",
    "github": "https://github.com/gprai",
    "resume": "https://1drv.ms/f/c/768093078700af7a/IgDCyz3vFgDEQ72Q0ExLIeLWAbIhc1mkgmFdLsg6cDKBXhw?e=4TjZaS",
}

CERTIFICATIONS = [
    {"label": "AWS Solutions Architect – Associate", "color": "#FF9900", "icon": "☁"},
    {"label": "AWS Developer – Associate",           "color": "#FF9900", "icon": "☁"},
    {"label": "AWS SysOps Administrator – Associate","color": "#FF9900", "icon": "☁"},
    {"label": "Azure Fundamentals",                  "color": "#0078D4", "icon": "⬡"},
    {"label": "Azure Administrator Associate",       "color": "#0078D4", "icon": "⬡"},
    {"label": "Azure DevOps Engineer Expert",        "color": "#0078D4", "icon": "⬡"},
    {"label": "Azure AI Engineer Associate",         "color": "#0078D4", "icon": "⬡"},
]

STACK = [
    {"category": "Cloud Platforms",           "items": ["AWS", "Azure"]},
    {"category": "Container Orchestration",   "items": ["Kubernetes (EKS/AKS)", "Docker", "Helm", "Karpenter"]},
    {"category": "Infrastructure as Code",    "items": ["Terraform", "ArgoCD", "GitOps"]},
    {"category": "CI/CD & Automation",        "items": ["GitHub Actions", "GitLab CI", "Bash", "Python"]},
    {"category": "Security (DevSecOps)",      "items": ["IAM", "SAST", "Networking", "DevSecOps Best Practices"]},
    {"category": "Observability",             "items": ["Prometheus", "Grafana", "Logging"]},
    {"category": "AI & ML Infrastructure",    "items": ["AWS SageMaker", "Azure AI Services", "AWS Bedrock", "OpenAI APIs"]},
]

PROJECTS = [
    {
        "id": "eks-cicd",
        "title": "Microservices EKS Terraform CI/CD Platform",
        "badge": "Production",
        "summary": "Production-grade Kubernetes platform with a secure, GitOps-ready CI pipeline using GitHub Actions with OIDC authentication — no AWS keys stored in GitHub.",
        "repo": "https://github.com/gprai/microservices-eks-terraform-cicd",
        "doc": "projects/microservices-eks-terraform.html",
        "stack": ["Terraform", "Amazon EKS", "Karpenter", "GitHub Actions", "Helm", "ArgoCD"],
        "highlights": [
            "OIDC-based GitHub Actions → AWS auth (zero long-lived credentials)",
            "Karpenter node autoscaling for cost-efficient workloads",
            "Helm + ArgoCD GitOps continuous delivery",
            "Docker image build → ECR push → Helm value update pipeline",
        ],
    },
    {
        "id": "aws-platform",
        "title": "AWS Platform Engineering",
        "badge": "In Development",
        "summary": "Enterprise-grade AWS platform implementing a secure multi-account landing zone with AWS Control Tower, Organizations, and Terraform-driven governance.",
        "repo": "https://github.com/gprai/aws-platform-engineering",
        "doc": "projects/aws-platform.html",
        "stack": ["AWS Control Tower", "AWS Organizations", "Terraform", "GitHub Actions", "GitOps"],
        "highlights": [
            "Multi-account landing zone with AWS Control Tower",
            "Automated governance, identity, and networking baseline",
            "Terraform modules for repeatable account vending",
            "GitOps-driven policy and compliance automation",
        ],
    },
]

SERVICES = [
    {
        "icon": "☁",
        "title": "Cloud & Infrastructure",
        "items": ["AWS & Azure Cloud Architecture", "Infrastructure as Code with Terraform",
                  "Cloud Migration & Optimization", "Networking & IAM Solutions"],
    },
    {
        "icon": "⚙",
        "title": "Kubernetes & Platform Engineering",
        "items": ["Amazon EKS & Azure AKS", "Kubernetes Platform Engineering",
                  "Helm & ArgoCD GitOps", "High Availability Infrastructure"],
    },
    {
        "icon": "🚀",
        "title": "DevOps & Automation",
        "items": ["CI/CD Pipelines", "GitHub Actions & GitLab CI",
                  "Docker Containerisation", "Infrastructure Automation"],
    },
    {
        "icon": "🔒",
        "title": "DevSecOps & Monitoring",
        "items": ["DevSecOps Best Practices", "SAST Security Integration",
                  "Prometheus & Grafana", "Observability & Logging"],
    },
    {
        "icon": "🤖",
        "title": "AI & Automation",
        "items": ["Python & Bash Automation", "AWS SageMaker",
                  "Azure AI Services", "OpenAI API Integrations"],
    },
    {
        "icon": "🧑‍💼",
        "title": "Consulting",
        "items": ["Platform Engineering Consulting", "Cloud Cost Optimisation",
                  "Architecture Reviews", "Technical Documentation"],
    },
]

# ── Shared HTML fragments ─────────────────────────────────────────────────────

def css() -> str:
    return """
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=DM+Mono:wght@300;400;500&display=swap');

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --bg:        #0f2433; /* lighter than before */
    --surface:   #122933;
    --border:    #23424f;
    --aws:       #FF9900;
    --azure:     #3a9bff;
    --accent:    #2dd4f5; /* softer cyan */
    --text:      #e6f2f8;
    --muted:     #98b9c6;
    --font-head: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
    --font-mono: 'DM Mono', monospace;
  }

  html { scroll-behavior: smooth; }

  body {
    background: linear-gradient(180deg,var(--bg), #0b2028 120%);
    color: var(--text);
    font-family: var(--font-head);
    font-size: 15px;
    line-height: 1.7;
    overflow-x: hidden;
    -webkit-font-smoothing:antialiased; -moz-osx-font-smoothing:grayscale;
  }

  /* ── Noise overlay ── */
  body::before {
    content: '';
    position: fixed; inset: 0; z-index: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.035'/%3E%3C/svg%3E");
    pointer-events: none;
  }

  /* ── Grid lines ── */
  body::after {
    content: '';
    position: fixed; inset: 0; z-index: 0;
    background-image:
      linear-gradient(var(--border) 1px, transparent 1px),
      linear-gradient(90deg, var(--border) 1px, transparent 1px);
    background-size: 60px 60px;
    opacity: 0.35;
    pointer-events: none;
  }

  /* ── Nav ── */
  nav {
    position: fixed; top: 0; left: 0; right: 0; z-index: 100;
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 clamp(1rem, 5vw, 4rem);
    height: 56px;
    background: rgba(9,9,15,0.85);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--border);
  }

  .nav-logo {
    font-family: var(--font-head);
    font-weight: 800;
    font-size: 1.1rem;
    color: var(--accent);
    text-decoration: none;
    letter-spacing: -0.02em;
  }

  .nav-links { display: flex; gap: 2rem; list-style: none; }
  .nav-links a {
    color: var(--muted);
    text-decoration: none;
    font-size: 0.78rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    transition: color .2s;
  }
  .nav-links a:hover { color: var(--accent); }

  /* ── Layout ── */
  main {
    position: relative; z-index: 1;
    padding-top: 56px;
  }

  .section {
    padding: clamp(4rem, 10vw, 8rem) clamp(1rem, 8vw, 8rem);
    max-width: 1200px;
    margin: 0 auto;
  }

  /* ── Section label ── */
  .section-label {
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 1rem;
    display: flex; align-items: center; gap: .75rem;
  }
  .section-label::after {
    content: '';
    flex: 1; max-width: 80px;
    height: 1px;
    background: var(--accent);
    opacity: .4;
  }

  h1, h2, h3 { font-family: var(--font-head); }

  /* ── Hero ── */
  .hero {
    min-height: calc(100vh - 56px);
    display: flex; flex-direction: column; justify-content: center;
    padding: clamp(2rem, 8vw, 6rem) clamp(1rem, 8vw, 8rem);
    position: relative;
  }

  .hero-eyebrow {
    font-size: .7rem;
    letter-spacing: .2em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 1.5rem;
  }

  .hero h1 {
    font-size: clamp(2.2rem, 6vw, 4rem);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.03em;
    color: var(--text);
  }

  .hero h1 .highlight {
    -webkit-text-stroke: 1px var(--accent);
    color: transparent;
  }

  .hero-sub {
    margin-top: 1.5rem;
    font-size: clamp(.85rem, 1.5vw, 1rem);
    color: var(--muted);
    max-width: 540px;
    line-height: 1.8;
  }

  .hero-cta {
    margin-top: 3rem;
    display: flex; gap: 1rem; flex-wrap: wrap;
  }

  .btn {
    display: inline-block;
    padding: .65rem 1.6rem;
    font-family: var(--font-mono);
    font-size: .75rem;
    letter-spacing: .1em;
    text-transform: uppercase;
    text-decoration: none;
    border-radius: 2px;
    transition: all .2s;
    cursor: pointer;
    border: none;
  }

  .btn-primary {
    background: linear-gradient(90deg,var(--accent),#7ce7ff);
    color: #002027;
    font-weight: 500;
  }
  .btn-primary:hover { background: #fff; }

  .btn-outline {
    background: transparent;
    color: var(--text);
    border: 1px solid var(--border);
  }
  .btn-outline:hover { border-color: var(--accent); color: var(--accent); }

  /* ── Cert pills ── */
  .certs { display: flex; flex-wrap: wrap; gap: .65rem; }

  .cert-pill {
    display: flex; align-items: center; gap: .45rem;
    padding: .4rem 1rem;
    border-radius: 2px;
    font-size: .72rem;
    letter-spacing: .05em;
    border: 1px solid;
    transition: transform .15s;
  }
  .cert-pill:hover { transform: translateY(-2px); }

  /* ── Stack grid ── */
  .stack-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1.5px;
    background: var(--border);
    border: 1px solid var(--border);
  }

  .stack-card {
    background: linear-gradient(180deg,var(--surface), #0f2a36);
    padding: 1.8rem;
    transition: background .2s;
  }
  .stack-card:hover { background: #16162a; }

  .stack-card h3 {
    font-size: .85rem;
    letter-spacing: .08em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 1rem;
  }

  .stack-card ul { list-style: none; }
  .stack-card li {
    color: var(--muted);
    font-size: .8rem;
    padding: .25rem 0;
    border-bottom: 1px solid var(--border);
    display: flex; align-items: center; gap: .5rem;
  }
  .stack-card li:last-child { border-bottom: none; }
  .stack-card li::before { content: '→'; color: var(--accent); font-size: .7rem; }

  /* ── Projects ── */
  .project-card {
    border: 1px solid var(--border);
    background: var(--surface);
    padding: 2.5rem;
    margin-bottom: 1.5px;
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 2rem;
    transition: border-color .2s;
    position: relative;
    overflow: hidden;
  }

  .project-card::before {
    content: '';
    position: absolute; left: 0; top: 0; bottom: 0;
    width: 2px;
    background: var(--accent);
    transform: scaleY(0);
    transform-origin: bottom;
    transition: transform .3s;
  }
  .project-card:hover::before { transform: scaleY(1); }
  .project-card:hover { border-color: var(--accent); }

  .project-badge {
    display: inline-block;
    font-size: .6rem;
    letter-spacing: .15em;
    text-transform: uppercase;
    padding: .2rem .6rem;
    border-radius: 1px;
    margin-bottom: .75rem;
  }
  .badge-prod  { background: rgba(0,229,255,.1); color: var(--accent); border: 1px solid rgba(0,229,255,.3); }
  .badge-dev   { background: rgba(255,153,0,.1); color: var(--aws);   border: 1px solid rgba(255,153,0,.3); }

  .project-card h3 {
    font-size: 1.25rem;
    font-weight: 700;
    letter-spacing: -.02em;
    color: var(--text);
    margin-bottom: .75rem;
  }

  .project-summary { color: var(--muted); font-size: .83rem; line-height: 1.8; margin-bottom: 1.5rem; }

  .project-highlights { list-style: none; margin-bottom: 1.5rem; }
  .project-highlights li {
    font-size: .78rem; color: var(--muted);
    padding: .2rem 0;
    display: flex; gap: .5rem;
  }
  .project-highlights li::before { content: '◆'; color: var(--accent); font-size: .5rem; margin-top: .35rem; }

  .tag-list { display: flex; flex-wrap: wrap; gap: .4rem; margin-bottom: 1.5rem; }
  .tag {
    font-size: .65rem;
    letter-spacing: .08em;
    padding: .2rem .55rem;
    border: 1px solid var(--border);
    color: var(--muted);
    border-radius: 1px;
  }

  .project-links { display: flex; gap: .75rem; }

  /* ── Services ── */
  .services-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 1.5px;
    background: var(--border);
    border: 1px solid var(--border);
  }

  .service-card {
    background: linear-gradient(180deg,var(--surface), #0f2a36);
    padding: 2rem;
    transition: background .2s;
  }
  .service-card:hover { background: #16162a; }

  .service-icon { font-size: 1.4rem; margin-bottom: 1rem; }
  .service-card h3 {
    font-size: .95rem;
    font-weight: 700;
    letter-spacing: -.01em;
    color: var(--text);
    margin-bottom: .9rem;
  }

  .service-card ul { list-style: none; }
  .service-card li {
    font-size: .78rem;
    color: var(--muted);
    padding: .3rem 0;
    border-bottom: 1px solid var(--border);
    display: flex; gap: .5rem;
  }
  .service-card li:last-child { border-bottom: none; }
  .service-card li::before { content: '–'; color: var(--accent); }

  /* ── Contact ── */
  .contact-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 1.5px;
    background: var(--border);
    border: 1px solid var(--border);
    margin-bottom: 3rem;
  }

  .contact-card {
    background: linear-gradient(180deg,var(--surface), #0f2a36);
    padding: 2rem;
    text-decoration: none;
    color: inherit;
    transition: background .2s;
    display: block;
  }
  .contact-card:hover { background: #16162a; }
  .contact-card .contact-type {
    font-size: .62rem; letter-spacing: .18em;
    text-transform: uppercase; color: var(--accent);
    margin-bottom: .5rem;
  }
  .contact-card .contact-value { font-size: .88rem; color: var(--text); }

  /* ── Footer ── */
  footer {
    position: relative; z-index: 1;
    border-top: 1px solid var(--border);
    padding: 2rem clamp(1rem, 8vw, 8rem);
    display: flex; justify-content: space-between; align-items: center;
    flex-wrap: wrap; gap: 1rem;
    font-size: .72rem; color: var(--muted);
  }

  /* ── Page heading ── */
  .page-hero {
    padding: 5rem clamp(1rem, 8vw, 8rem) 3rem;
    border-bottom: 1px solid var(--border);
    position: relative; z-index: 1;
    max-width: 1200px; margin: 0 auto;
  }

  .page-hero h1 { font-size: clamp(2rem, 5vw, 3.5rem); font-weight: 800; letter-spacing: -.03em; }
  .page-hero p { color: var(--muted); margin-top: .75rem; max-width: 540px; }

  /* ── Divider ── */
  .divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 0;
  }

  /* ── Responsive ── */
  @media (max-width: 680px) {
    .project-card { grid-template-columns: 1fr; }
    .nav-links { display: none; }
  }
</style>
"""


def nav(active: str = "") -> str:
    pages = [
        ("Home",        "index.html"),
        ("Stack",       "stack.html"),
        ("Projects",    "projects.html"),
        ("Services",    "services.html"),
        ("Contact",     "contact.html"),
    ]
    links = ""
    for label, href in pages:
        style = 'style="color:var(--accent)"' if label.lower() == active.lower() else ""
        links += f'<li><a href="{href}" {style}>{label}</a></li>\n'
    return f"""
<nav>
  <a class="nav-logo" href="index.html">GPR<span style="color:var(--muted)">.</span></a>
  <ul class="nav-links">{links}</ul>
</nav>
"""


def footer() -> str:
    return f"""
<footer>
  <span>© 2025 Gyan Prakash Rai</span>
  <span>
    <a href="{SITE['github']}" style="color:var(--muted);text-decoration:none;margin-right:1.5rem;">GitHub</a>
    <a href="{SITE['linkedin']}" style="color:var(--muted);text-decoration:none;">LinkedIn</a>
  </span>
</footer>
"""


def page(title: str, body: str, active: str = "", extra_head: str = "") -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{title} · Gyan Prakash Rai</title>
  <meta name="description" content="AWS & Azure Platform Engineer, DevOps, Cloud Infrastructure Specialist"/>
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
  {css()}
  {extra_head}
</head>
<body>
  {nav(active)}
  <main>{body}</main>
  {footer()}
</body>
</html>
"""


# ── Page builders ─────────────────────────────────────────────────────────────

def build_index():
    typing_words = [
        "AWS &amp; Azure Platform Engineer",
        "Kubernetes · EKS · AKS",
        "Terraform · GitOps · CI/CD",
        "DevSecOps · Observability",
        "AI-Ready Cloud Architecture",
    ]
    typing_js = f"""
<script>
const words = {json.dumps(typing_words)};
let wi = 0, ci = 0, deleting = false;
const el = document.getElementById('typing');
function type() {{
  const w = words[wi];
  el.innerHTML = deleting ? w.slice(0, ci--) : w.slice(0, ci++);
  if (!deleting && ci > w.length) {{ deleting = true; setTimeout(type, 1400); return; }}
  if (deleting && ci < 0) {{ deleting = false; wi = (wi + 1) % words.length; }}
  setTimeout(type, deleting ? 40 : 70);
}}
type();
</script>
"""

    cert_html = ""
    for c in CERTIFICATIONS:
        cert_html += f"""
<div class="cert-pill" style="border-color:{c['color']}44;color:{c['color']}">
  <span>{c['icon']}</span>
  <span>{c['label']}</span>
</div>"""

    # Booking modal + script (injected as a separate string to avoid f-string brace escaping)
    booking_js = '''
<!-- Booking modal and script -->
<div id="bookingModal" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:300;align-items:center;justify-content:center"> 
  <div style="background:var(--surface);max-width:720px;width:94%;padding:1.2rem;border-radius:6px;border:1px solid var(--border)">
    <h3 style="margin:0 0 .5rem">Book a Demo</h3>
    <p style="color:var(--muted);margin:0 0 1rem;font-size:.92rem">Pick a preferred time and tell me briefly about your requirements.</p>
    <form id="bookingForm">
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.6rem">
        <input name="name" placeholder="Your name" required style="padding:.6rem;border-radius:4px;border:1px solid var(--border);background:transparent;color:var(--text)" />
        <input name="email" type="email" placeholder="Email" required style="padding:.6rem;border-radius:4px;border:1px solid var(--border);background:transparent;color:var(--text)" />
      </div>
      <div style="margin-top:.6rem;display:grid;grid-template-columns:1fr 1fr;gap:0.6rem">
        <input name="date" type="date" style="padding:.5rem;border-radius:4px;border:1px solid var(--border);background:transparent;color:var(--text)" />
        <input name="time" type="time" style="padding:.5rem;border-radius:4px;border:1px solid var(--border);background:transparent;color:var(--text)" />
      </div>
      <textarea name="note" placeholder="Brief note (optional)" style="width:100%;margin-top:.6rem;padding:.6rem;border-radius:4px;border:1px solid var(--border);background:transparent;color:var(--text)"></textarea>
      <div style="display:flex;gap:.5rem;margin-top:.8rem;justify-content:flex-end">
        <button type="button" id="bookingCancel" class="btn btn-outline">Cancel</button>
        <button type="submit" class="btn btn-primary">Request Booking</button>
      </div>
    </form>
  </div>
</div>

<script>
document.getElementById('bookBtn').addEventListener('click', function(){
  document.getElementById('bookingModal').style.display = 'flex';
});
document.getElementById('bookingCancel').addEventListener('click', function(){
  document.getElementById('bookingModal').style.display = 'none';
});
document.getElementById('bookingForm').addEventListener('submit', function(e){
  e.preventDefault();
  const f = e.target;
  const data = new FormData(f);
  const name = encodeURIComponent(data.get('name')||'');
  const email = encodeURIComponent(data.get('email')||'');
  // If Calendly is configured, open Calendly with prefilled name/email in a new tab.
  const calendly = __CALENDLY__;
  if (calendly) {
    const url = calendly + (calendly.includes('?') ? '&' : '?') + 'name=' + name + '&email=' + email;
    window.open(url, '_blank');
    document.getElementById('bookingModal').style.display = 'none';
    return;
  }
  // If a form action is configured, POST the form data there.
  const formAction = __FORMACTION__;
  if (formAction) {
    fetch(formAction, { method: 'POST', body: data }).then(()=>{
      alert('Booking request sent — thank you!');
      document.getElementById('bookingModal').style.display = 'none';
    }).catch(()=>{ alert('Unable to send booking request.'); });
    return;
  }
  // Fallback: open mail client with details to owner's email
  const subject = encodeURIComponent('Booking request from ' + (data.get('name')||''));
  const body = encodeURIComponent('Name: ' + (data.get('name')||'') + '\nEmail: ' + (data.get('email')||'') + '\nPreferred: ' + (data.get('date')||'') + ' ' + (data.get('time')||'') + '\n\nNote:\n' + (data.get('note')||''));
  const owner = __OWNER__;
  window.location.href = 'mailto:' + encodeURIComponent(owner) + '?subject=' + subject + '&body=' + body;
});
</script>
'''
    booking_js = booking_js.replace('__CALENDLY__', json.dumps(SITE.get('calendly',''))).replace('__FORMACTION__', json.dumps(SITE.get('form_action',''))).replace('__OWNER__', json.dumps(SITE.get('email','')))

    body = f"""
<section class="hero">
  <p class="hero-eyebrow">Cloud · DevOps · Platform Engineering</p>
  <h1>Gyan<br/><span class="highlight">Prakash Rai</span></h1>
  <p class="hero-sub">
    <span id="typing" style="color:var(--accent)"></span><span style="color:var(--accent);animation:blink 1s step-end infinite">_</span>
    <br/><br/>
    Designing and automating scalable, secure, production-grade infrastructure
    on AWS and Azure — with Kubernetes, Terraform, CI/CD, and GitOps at the core.
  </p>
  <div class="hero-cta">
    <a href="projects.html" class="btn btn-primary">View Projects</a>
    <a href="services.html" class="btn btn-outline">Services</a>
    <a href="contact.html" class="btn btn-outline">Contact</a>
    <button id="bookBtn" class="btn btn-primary" style="background:transparent;border:1px solid rgba(255,255,255,.06);">Book a Demo</button>
  </div>
</section>

<hr class="divider"/>

<section class="section">
  <p class="section-label">Certifications</p>
  <div class="certs">{cert_html}</div>
</section>

<hr class="divider"/>

<section class="section">
  <p class="section-label">About</p>
  <p style="max-width:680px;color:var(--muted);line-height:2;font-size:.88rem">
    Cloud &amp; DevOps Engineer specialising in designing and automating scalable, secure,
    production-grade infrastructure on AWS and Azure. I help teams build reliable cloud
    platforms using Kubernetes (EKS/AKS), Terraform, CI/CD pipelines, Docker, and
    GitOps-driven delivery workflows.
    <br/><br/>
    I also design <strong style="color:var(--text)">AI-ready cloud architectures</strong>
    for modern workloads, including Generative AI and MLOps systems — integrating
    OpenAI, Azure OpenAI, AWS Bedrock, and building infrastructure for LLM applications
    and RAG pipelines.
  </p>
</section>
<style>@keyframes blink{{0%,100%{{opacity:1}}50%{{opacity:0}}}}</style>
{typing_js}
{booking_js}
"""
    return page("Home", body, active="Home")


def build_stack():
    cards = ""
    for s in STACK:
        items = "".join(f"<li>{i}</li>" for i in s["items"])
        cards += f"""
<div class="stack-card">
  <h3>{s['category']}</h3>
  <ul>{items}</ul>
</div>"""

    body = f"""
<div class="page-hero">
  <p class="section-label">Tech Stack</p>
  <h1>Tools &amp; Technologies</h1>
  <p>The full stack I work with day-to-day across cloud, platform, security, and AI.</p>
</div>
<section class="section">
  <div class="stack-grid">{cards}</div>
</section>
"""
    return page("Stack", body, active="Stack")


def build_projects():
    cards = ""
    for p in PROJECTS:
        badge_cls = "badge-prod" if p["badge"] == "Production" else "badge-dev"
        highlights = "".join(f"<li>{h}</li>" for h in p["highlights"])
        tags = "".join(f'<span class="tag">{t}</span>' for t in p["stack"])
        cards += f"""
<div class="project-card">
  <div>
    <span class="project-badge {badge_cls}">{p['badge']}</span>
    <h3>{p['title']}</h3>
    <p class="project-summary">{p['summary']}</p>
    <ul class="project-highlights">{highlights}</ul>
    <div class="tag-list">{tags}</div>
    <div class="project-links">
      <a href="{p['repo']}" class="btn btn-outline" target="_blank" rel="noopener">GitHub Repo ↗</a>
      <a href="{p['doc']}" class="btn btn-outline">Full Docs →</a>
    </div>
  </div>
</div>"""

    body = f"""
<div class="page-hero">
  <p class="section-label">Projects</p>
  <h1>Featured Work</h1>
  <p>Production-grade cloud and platform engineering projects.</p>
</div>
<section class="section">
  {cards}
</section>
"""
    return page("Projects", body, active="Projects")


def build_services():
    cards = ""
    for s in SERVICES:
        items = "".join(f"<li>{i}</li>" for i in s["items"])
        cards += f"""
<div class="service-card">
  <div class="service-icon">{s['icon']}</div>
  <h3>{s['title']}</h3>
  <ul>{items}</ul>
</div>"""

    body = f"""
<div class="page-hero">
  <p class="section-label">Services</p>
  <h1>What I Offer</h1>
  <p>End-to-end cloud engineering, DevOps, and platform consulting.</p>
</div>
<section class="section">
  <div class="services-grid">{cards}</div>
  <div style="margin-top:3rem;padding:2.5rem;border:1px solid var(--border);background:var(--surface)">
    <p class="section-label">Get Started</p>
    <h2 style="font-size:1.6rem;letter-spacing:-.02em;margin-bottom:1rem">Ready to build something?</h2>
    <p style="color:var(--muted);max-width:480px;margin-bottom:1.5rem;font-size:.85rem;line-height:1.8">
      Whether you need a full cloud platform build, a CI/CD overhaul, or a one-off architecture review —
      let's talk.
    </p>
    <a href="contact.html" class="btn btn-primary">Get in Touch</a>
  </div>
</section>
"""
    return page("Services", body, active="Services")


def build_contact():
    contacts = [
        ("Email",    SITE["email"],    f"mailto:{SITE['email']}"),
        ("LinkedIn", "linkedin.com/in/gyan-prakash-rai-24782413", SITE["linkedin"]),
        ("GitHub",   "github.com/gprai", SITE["github"]),
        ("Resume",   "View / Download PDF", SITE["resume"]),
    ]
    cards = ""
    for ctype, val, href in contacts:
        cards += f"""
<a class="contact-card" href="{href}" target="_blank" rel="noopener">
  <div class="contact-type">{ctype}</div>
  <div class="contact-value">{val} ↗</div>
</a>"""

    body = f"""
<div class="page-hero">
  <p class="section-label">Contact</p>
  <h1>Let's Connect</h1>
  <p>Available for freelance projects, consulting, and full-time opportunities.</p>
</div>
<section class="section">
  <div class="contact-grid">{cards}</div>
  <p style="color:var(--muted);font-size:.78rem">
    Preferred contact: email or LinkedIn. I typically respond within 24 hours.
  </p>
</section>
"""
    return page("Contact", body, active="Contact")


def build_project_doc(project_id: str) -> str:
    p = next(x for x in PROJECTS if x["id"] == project_id)
    badge_cls = "badge-prod" if p["badge"] == "Production" else "badge-dev"
    highlights = "".join(
        f'<li style="color:var(--muted);font-size:.85rem;padding:.4rem 0;border-bottom:1px solid var(--border);display:flex;gap:.6rem">'
        f'<span style="color:var(--accent)">◆</span>{h}</li>'
        for h in p["highlights"]
    )
    tags = "".join(f'<span class="tag">{t}</span>' for t in p["stack"])

    # If this is the AWS Platform project, try to include the project's README and architecture image
    extra_html = ""
    if project_id == 'aws-platform':
      readme_path = Path('..') / 'aws-platform-engineering' / 'README.md'
      img_src = Path('..') / 'aws-platform-engineering' / 'image.png'
      try:
        if readme_path.exists():
          raw = readme_path.read_text(encoding='utf-8')
          # Minimal markdown -> HTML conversion (headers and lists)
          lines = raw.splitlines()
          out_lines = []
          in_list = False
          for L in lines:
            if L.startswith('### '):
              out_lines.append(f"<h3>{L[4:].strip()}</h3>")
              continue
            if L.startswith('## '):
              out_lines.append(f"<h2>{L[3:].strip()}</h2>")
              continue
            if L.startswith('# '):
              out_lines.append(f"<h1>{L[2:].strip()}</h1>")
              continue
            if L.startswith('- '):
              if not in_list:
                out_lines.append('<ul>')
                in_list = True
              out_lines.append(f"<li>{L[2:].strip()}</li>")
              continue
            else:
              if in_list:
                out_lines.append('</ul>')
                in_list = False
            # horizontal rules
            if L.strip().startswith('---'):
              out_lines.append('<hr/>')
              continue
            # code block fence -> wrap in pre (very simple)
            out_lines.append(f"<p style='color:var(--muted);line-height:1.7'>{L}</p>")
          if in_list:
            out_lines.append('</ul>')
          extra_html = '<div style="margin-top:2rem">' + '\n'.join(out_lines) + '</div>'
        if img_src.exists():
          # copy image into docs/projects
          dst = OUT / 'projects' / 'aws-platform.png'
          dst.parent.mkdir(parents=True, exist_ok=True)
          shutil.copyfile(img_src, dst)
          extra_html = f"<div style=\"margin-top:1.2rem;max-width:100%;\"><img src=\"projects/aws-platform.png\" alt=\"architecture\" style=\"width:100%;border:1px solid var(--border);border-radius:6px;\"/></div>" + extra_html
      except Exception:
        extra_html = ''

    body = f"""
<div class="page-hero">
  <a href="projects.html" style="font-size:.75rem;color:var(--muted);text-decoration:none;display:inline-block;margin-bottom:1rem">← Back to Projects</a>
  <span class="project-badge {badge_cls}" style="display:inline-block;margin-bottom:.75rem">{p['badge']}</span>
  <h1>{p['title']}</h1>
  <p>{p['summary']}</p>
</div>
<section class="section">
  <div style="display:grid;grid-template-columns:2fr 1fr;gap:3rem;align-items:start">
    <div>
      <p class="section-label">Overview</p>
      <p style="color:var(--muted);font-size:.88rem;line-height:2;margin-bottom:2rem">{p['summary']}</p>
      <p class="section-label">Key Highlights</p>
      <ul style="list-style:none">{highlights}</ul>
    </div>
    <div>
      <div style="border:1px solid var(--border);padding:1.8rem;background:var(--surface)">
        <p class="section-label">Stack</p>
        <div class="tag-list" style="flex-direction:column">{tags}</div>
        <div style="margin-top:1.5rem;padding-top:1.5rem;border-top:1px solid var(--border)">
          <a href="{p['repo']}" class="btn btn-primary" target="_blank" rel="noopener" style="width:100%;text-align:center;display:block">
            View on GitHub ↗
          </a>
        </div>
      </div>
    </div>
  </div>
</section>
"""
    return page(p["title"], body, active="Projects")


# ── Build all pages ───────────────────────────────────────────────────────────

def build():
    pages = {
        OUT / "index.html":           build_index(),
        OUT / "stack.html":           build_stack(),
        OUT / "projects.html":        build_projects(),
        OUT / "services.html":        build_services(),
        OUT / "contact.html":         build_contact(),
        OUT / "projects" / "microservices-eks-terraform.html": build_project_doc("eks-cicd"),
        OUT / "projects" / "aws-platform.html":                build_project_doc("aws-platform"),
    }

    for path, content in pages.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"  ✓  {path}")

    print(f"\nBuild complete → {OUT}/")


if __name__ == "__main__":
    build()
