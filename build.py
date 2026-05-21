"""
build.py — Static site generator for gprai.github.io
Run: python build.py
Output: docs/ folder ready for GitHub Pages (gh-pages branch)

NOTES FOR MEDIA (videos/images):
  - Place project screenshots in docs/media/images/
  - Place project demo videos in docs/media/videos/
  - GitHub Pages DOES serve binary assets (images, mp4) — just keep each file < 100 MB
  - Commit them normally: git add docs/media && git commit && git push
  - The HTML references them as /media/images/your-file.png
"""

import json
from pathlib import Path

OUT = Path("docs")
OUT.mkdir(exist_ok=True)
(OUT / "projects").mkdir(exist_ok=True)
(OUT / "media" / "images").mkdir(parents=True, exist_ok=True)
(OUT / "media" / "videos").mkdir(parents=True, exist_ok=True)

# ─────────────────────────────────────────────────────────────────────────────
# SITE DATA  ← edit freely
# ─────────────────────────────────────────────────────────────────────────────
SITE = {
    "name": "Gyan Prakash Rai",
    "role": "AWS & Azure Platform Engineer · DevOps · Cloud Infrastructure Specialist",
    "email": "gprai86@gmail.com",
    "linkedin": "https://www.linkedin.com/in/gyan-prakash-rai-24782413/",
    "github": "https://github.com/gprai",
    "resume": "https://1drv.ms/f/c/768093078700af7a/IgDCyz3vFgDEQ72Q0ExLIeLWAbIhc1mkgmFdLsg6cDKBXhw?e=4TjZaS",
    # ← Replace with your Calendly username: https://calendly.com/YOUR_USERNAME
    "calendly": "https://calendly.com/gprai86",
}

ABOUT = {
    "bio": [
        "Cloud & DevOps Engineer with deep expertise in designing and automating scalable, secure, production-grade infrastructure on AWS and Azure. I help engineering teams build reliable cloud platforms using Kubernetes (EKS/AKS), Terraform, CI/CD pipelines, Docker, and GitOps-driven delivery workflows.",
        "I also design <strong>AI-ready cloud architectures</strong> for modern workloads including Generative AI and MLOps systems — integrating OpenAI, Azure OpenAI, and AWS Bedrock, as well as building infrastructure for LLM applications, RAG pipelines, and automated ML workflows.",
        "My focus is on building systems that are not only deployed correctly, but are <strong>maintainable, observable, and production-safe</strong> — reducing operational overhead and improving release reliability.",
    ],
    "focus": [
        "Platform Engineering", "Kubernetes Automation", "Cloud Architecture",
        "Infrastructure as Code", "DevOps Consulting", "Freelance Cloud Projects",
    ],
    "stats": [
        {"n": "7+",  "label": "Cloud Certs"},
        {"n": "2",   "label": "Cloud Platforms"},
        {"n": "10+", "label": "Core Tools"},
        {"n": "∞",   "label": "Automation"},
    ],
}

CERTIFICATIONS = [
    {"label": "AWS Solutions Architect – Associate", "vendor": "AWS",   "color": "#e07b00"},
    {"label": "AWS Developer – Associate",           "vendor": "AWS",   "color": "#e07b00"},
    {"label": "AWS SysOps Administrator – Associate","vendor": "AWS",   "color": "#e07b00"},
    {"label": "Azure Fundamentals",                  "vendor": "Azure", "color": "#0072c6"},
    {"label": "Azure Administrator Associate",       "vendor": "Azure", "color": "#0072c6"},
    {"label": "Azure DevOps Engineer Expert",        "vendor": "Azure", "color": "#0072c6"},
    {"label": "Azure AI Engineer Associate",         "vendor": "Azure", "color": "#0072c6"},
]

STACK = [
    {"cat": "Cloud Platforms",         "icon": "☁", "items": ["AWS", "Azure"]},
    {"cat": "Container & Orchestration","icon": "⎈", "items": ["Kubernetes (EKS/AKS)", "Docker", "Helm", "Karpenter"]},
    {"cat": "Infrastructure as Code",  "icon": "🔧", "items": ["Terraform", "ArgoCD", "GitOps Workflows"]},
    {"cat": "CI/CD & Automation",      "icon": "🚀", "items": ["GitHub Actions", "GitLab CI", "Python", "Bash Scripting"]},
    {"cat": "Security & DevSecOps",    "icon": "🔒", "items": ["IAM", "SAST", "Networking", "DevSecOps Best Practices"]},
    {"cat": "Observability",           "icon": "📊", "items": ["Prometheus", "Grafana", "Centralised Logging"]},
    {"cat": "AI & ML Infrastructure",  "icon": "🤖", "items": ["AWS SageMaker", "Azure AI Services", "AWS Bedrock", "OpenAI APIs"]},
    {"cat": "OS & Scripting",          "icon": "💻", "items": ["Linux", "Python", "Bash", "Shell Automation"]},
]

# ─── PROJECTS ─────────────────────────────────────────────────────────────────
# featured: shown on home page
# status: "Production" | "In Development"
# arch_svg: inline SVG string (defined below)
# media_images: list of filenames in docs/media/images/  (add yours there)
# media_videos: list of filenames in docs/media/videos/  (add yours there)
# ─────────────────────────────────────────────────────────────────────────────
PROJECTS = [
    {
        "id": "eks-cicd",
        "featured": True,
        "status": "Production",
        "title": "Microservices EKS Terraform CI/CD Platform",
        "short": "Production-grade Kubernetes platform with GitOps-ready CI/CD, OIDC auth and Karpenter autoscaling — zero AWS keys in GitHub.",
        "summary": "A fully automated, secure CI/CD platform built on Amazon EKS using Terraform for infrastructure provisioning and GitHub Actions for pipeline orchestration. The pipeline uses OIDC federation so no long-lived AWS credentials are stored anywhere in GitHub. On every commit, Docker images are built, tagged, and pushed to Amazon ECR, after which Helm values are updated and ArgoCD syncs the change to the cluster.",
        "repo": "https://github.com/gprai/microservices-eks-terraform-cicd",
        "stack": ["Terraform", "Amazon EKS", "Karpenter", "GitHub Actions", "Helm", "ArgoCD", "Docker", "Amazon ECR"],
        "highlights": [
            "OIDC-based GitHub Actions → AWS auth — zero long-lived credentials stored in GitHub",
            "Karpenter node autoscaling for cost-efficient, right-sized EC2 provisioning",
            "Helm + ArgoCD GitOps continuous delivery — Git is the single source of truth",
            "Multi-environment support: dev / staging / production namespaces with promotion gates",
            "Private VPC with NAT gateway, security groups, and pod-level IRSA roles",
            "Docker build → ECR push → Helm values commit → ArgoCD sync — fully automated",
        ],
        "arch_id": "eks",
        "media_images": [],   # e.g. ["eks-screenshot-1.png", "eks-screenshot-2.png"]
        "media_videos": [],   # e.g. ["eks-demo.mp4"]
    },
    {
        "id": "aws-platform",
        "featured": True,
        "status": "In Development",
        "title": "AWS Platform Engineering — Multi-Account Landing Zone",
        "short": "Enterprise AWS multi-account landing zone using Control Tower, Organizations, Terraform and GitOps — automated governance, identity, networking at scale.",
        "summary": "An enterprise-grade AWS platform implementing a secure multi-account landing zone using AWS Control Tower and AWS Organizations. Terraform modules handle account vending, baseline networking, IAM, and security controls. GitHub Actions + GitOps drive all changes, with centralised CloudTrail, AWS Config, Security Hub, and GuardDuty across every account.",
        "repo": "https://github.com/gprai/aws-platform-engineering",
        "stack": ["AWS Control Tower", "AWS Organizations", "Terraform", "GitHub Actions", "IAM Identity Center", "SCPs", "Security Hub", "GuardDuty"],
        "highlights": [
            "Multi-account structure: Management / Log Archive / Audit / Workload accounts",
            "AWS Control Tower guardrails + automated account vending via Terraform",
            "Service Control Policies (SCPs) enforcing organisation-wide governance",
            "Centralised CloudTrail, AWS Config, Security Hub aggregator and GuardDuty",
            "IAM Identity Center (SSO) with permission sets mapped to AD groups",
            "Transit Gateway for shared networking across all workload accounts",
        ],
        "arch_id": "platform",
        "media_images": [],
        "media_videos": [],
    },
]

SERVICES = [
    {"icon": "☁", "title": "Cloud & Infrastructure",
     "items": ["AWS & Azure Architecture", "Terraform Infrastructure as Code", "Cloud Migration & Optimisation", "Networking & IAM Solutions"]},
    {"icon": "⎈", "title": "Kubernetes & Platform Engineering",
     "items": ["Amazon EKS & Azure AKS", "Kubernetes Platform Engineering", "Helm & ArgoCD GitOps", "High Availability Design"]},
    {"icon": "🚀", "title": "DevOps & Automation",
     "items": ["CI/CD Pipelines", "GitHub Actions & GitLab CI", "Docker Containerisation", "Infrastructure Automation"]},
    {"icon": "🔒", "title": "DevSecOps & Monitoring",
     "items": ["DevSecOps Best Practices", "SAST Security Integration", "Prometheus & Grafana", "Observability & Logging"]},
    {"icon": "🤖", "title": "AI & Automation",
     "items": ["Python & Bash Automation", "AWS SageMaker", "Azure AI Services", "OpenAI API Integrations"]},
    {"icon": "🧑‍💼", "title": "Consulting",
     "items": ["Platform Engineering Consulting", "Cloud Cost Optimisation", "Architecture Reviews", "Technical Documentation"]},
]

# ─────────────────────────────────────────────────────────────────────────────
# ARCHITECTURE SVGs
# ─────────────────────────────────────────────────────────────────────────────

def arch_eks() -> str:
    return """
<svg viewBox="0 0 900 400" xmlns="http://www.w3.org/2000/svg"
     style="width:100%;max-width:900px;border-radius:10px;background:#f8fafc;border:1px solid #e2e8f0">
  <defs>
    <marker id="ah" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L7,3 z" fill="#2563eb"/>
    </marker>
    <marker id="ag" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L7,3 z" fill="#16a34a"/>
    </marker>
    <marker id="ap" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L7,3 z" fill="#9333ea"/>
    </marker>
  </defs>

  <!-- Title -->
  <text x="16" y="20" font-family="'Segoe UI',sans-serif" font-size="11" font-weight="700" fill="#0f172a">
    Microservices EKS · GitHub Actions OIDC · ArgoCD GitOps Pipeline
  </text>

  <!-- Developer -->
  <rect x="14" y="34" width="110" height="62" rx="8" fill="#dbeafe" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="69" y="57" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="700" fill="#1e40af">👨‍💻 Dev</text>
  <text x="69" y="72" text-anchor="middle" font-family="sans-serif" font-size="9" fill="#2563eb">git push</text>
  <text x="69" y="85" text-anchor="middle" font-family="sans-serif" font-size="9" fill="#2563eb">feature branch</text>

  <!-- GitHub Actions -->
  <rect x="170" y="22" width="150" height="86" rx="8" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.5"/>
  <text x="245" y="44" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="700" fill="#166534">⚙ GitHub Actions</text>
  <text x="245" y="59" text-anchor="middle" font-family="sans-serif" font-size="8.5" fill="#15803d">OIDC → AssumeRole</text>
  <text x="245" y="73" text-anchor="middle" font-family="sans-serif" font-size="8.5" fill="#15803d">Docker build &amp; tag</text>
  <text x="245" y="87" text-anchor="middle" font-family="sans-serif" font-size="8.5" fill="#15803d">Push to ECR</text>
  <text x="245" y="101" text-anchor="middle" font-family="sans-serif" font-size="8.5" fill="#15803d">Update Helm values</text>

  <!-- ECR -->
  <rect x="372" y="34" width="110" height="62" rx="8" fill="#fff7ed" stroke="#f97316" stroke-width="1.5"/>
  <text x="427" y="57" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="700" fill="#9a3412">📦 ECR</text>
  <text x="427" y="73" text-anchor="middle" font-family="sans-serif" font-size="8.5" fill="#ea580c">Container Registry</text>
  <text x="427" y="86" text-anchor="middle" font-family="sans-serif" font-size="8.5" fill="#ea580c">Image:sha-abc123</text>

  <!-- Helm Values Repo -->
  <rect x="170" y="155" width="150" height="56" rx="8" fill="#faf5ff" stroke="#9333ea" stroke-width="1.5"/>
  <text x="245" y="177" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="700" fill="#6b21a8">⎈ Helm Values</text>
  <text x="245" y="193" text-anchor="middle" font-family="sans-serif" font-size="8.5" fill="#9333ea">Git repo · image tag</text>
  <text x="245" y="207" text-anchor="middle" font-family="sans-serif" font-size="8.5" fill="#9333ea">environment configs</text>

  <!-- ArgoCD -->
  <rect x="372" y="155" width="110" height="56" rx="8" fill="#fff0f6" stroke="#db2777" stroke-width="1.5"/>
  <text x="427" y="177" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="700" fill="#9d174d">🔄 ArgoCD</text>
  <text x="427" y="193" text-anchor="middle" font-family="sans-serif" font-size="8.5" fill="#db2777">Poll for drift</text>
  <text x="427" y="207" text-anchor="middle" font-family="sans-serif" font-size="8.5" fill="#db2777">Sync to cluster</text>

  <!-- EKS cluster boundary -->
  <rect x="530" y="16" width="350" height="370" rx="12" fill="#f1f5fb" stroke="#3b82f6" stroke-width="2" stroke-dasharray="7,3"/>
  <text x="705" y="36" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="700" fill="#1e40af">Amazon EKS Cluster</text>

  <!-- Karpenter -->
  <rect x="547" y="46" width="130" height="50" rx="6" fill="#ecfdf5" stroke="#10b981" stroke-width="1.5"/>
  <text x="612" y="67" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="700" fill="#065f46">⚡ Karpenter</text>
  <text x="612" y="82" text-anchor="middle" font-family="sans-serif" font-size="8.5" fill="#059669">Node Autoscaling</text>

  <!-- Namespaces -->
  <rect x="547" y="112" width="310" height="90" rx="6" fill="#eff6ff" stroke="#93c5fd"/>
  <text x="702" y="130" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="700" fill="#1e40af">Workload Namespaces</text>
  <rect x="557" y="138" width="82" height="52" rx="4" fill="#bfdbfe" stroke="#60a5fa"/>
  <text x="598" y="158" text-anchor="middle" font-family="sans-serif" font-size="8.5" font-weight="600" fill="#1e40af">dev</text>
  <text x="598" y="172" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#2563eb">Pods · Services</text>
  <text x="598" y="183" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#2563eb">Ingress</text>
  <rect x="648" y="138" width="82" height="52" rx="4" fill="#bfdbfe" stroke="#60a5fa"/>
  <text x="689" y="158" text-anchor="middle" font-family="sans-serif" font-size="8.5" font-weight="600" fill="#1e40af">staging</text>
  <text x="689" y="172" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#2563eb">Pods · Services</text>
  <text x="689" y="183" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#2563eb">Ingress</text>
  <rect x="739" y="138" width="100" height="52" rx="4" fill="#93c5fd" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="789" y="158" text-anchor="middle" font-family="sans-serif" font-size="8.5" font-weight="700" fill="#1e3a8a">production</text>
  <text x="789" y="172" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#1e3a8a">Pods · Services</text>
  <text x="789" y="183" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#1e3a8a">HPA · PDB</text>

  <!-- VPC -->
  <rect x="547" y="218" width="310" height="62" rx="6" fill="#fefce8" stroke="#eab308"/>
  <text x="702" y="237" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="700" fill="#713f12">VPC — Private Subnets</text>
  <text x="617" y="257" text-anchor="middle" font-family="sans-serif" font-size="8" fill="#854d0e">NAT Gateway</text>
  <text x="702" y="257" text-anchor="middle" font-family="sans-serif" font-size="8" fill="#854d0e">Security Groups</text>
  <text x="800" y="257" text-anchor="middle" font-family="sans-serif" font-size="8" fill="#854d0e">ALB Ingress</text>

  <!-- IRSA / IAM -->
  <rect x="547" y="296" width="310" height="52" rx="6" fill="#fff1f2" stroke="#f43f5e"/>
  <text x="702" y="316" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="700" fill="#9f1239">IAM + OIDC Identity Provider</text>
  <text x="702" y="333" text-anchor="middle" font-family="sans-serif" font-size="8" fill="#e11d48">IRSA · Pod-level AWS roles · AssumeRoleWithWebIdentity</text>

  <!-- Monitoring -->
  <rect x="547" y="362" width="145" height="18" rx="4" fill="#f0fdf4" stroke="#10b981"/>
  <text x="619" y="375" text-anchor="middle" font-family="sans-serif" font-size="8" fill="#166534">Prometheus · Grafana · Alerts</text>
  <rect x="702" y="362" width="155" height="18" rx="4" fill="#faf5ff" stroke="#9333ea"/>
  <text x="779" y="375" text-anchor="middle" font-family="sans-serif" font-size="8" fill="#6b21a8">CloudWatch · Container Insights</text>

  <!-- Arrows -->
  <line x1="124" y1="65" x2="168" y2="65" stroke="#16a34a" stroke-width="1.5" marker-end="url(#ag)"/>
  <line x1="320" y1="65" x2="370" y2="65" stroke="#ea580c" stroke-width="1.5" marker-end="url(#ah)"/>
  <line x1="245" y1="108" x2="245" y2="153" stroke="#9333ea" stroke-width="1.5" marker-end="url(#ap)"/>
  <line x1="320" y1="183" x2="370" y2="183" stroke="#2563eb" stroke-width="1.5" marker-end="url(#ah)"/>
  <line x1="482" y1="183" x2="528" y2="155" stroke="#db2777" stroke-width="1.5" marker-end="url(#ah)"/>
  <line x1="427" y1="96" x2="545" y2="155" stroke="#f97316" stroke-width="1.5" stroke-dasharray="5,3" marker-end="url(#ah)"/>
</svg>"""


def arch_platform() -> str:
    return """
<svg viewBox="0 0 900 480" xmlns="http://www.w3.org/2000/svg"
     style="width:100%;max-width:900px;border-radius:10px;background:#f8fafc;border:1px solid #e2e8f0">
  <defs>
    <marker id="bh" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L7,3 z" fill="#2563eb"/>
    </marker>
    <marker id="bg" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L7,3 z" fill="#f97316"/>
    </marker>
  </defs>

  <text x="16" y="20" font-family="'Segoe UI',sans-serif" font-size="11" font-weight="700" fill="#0f172a">
    AWS Multi-Account Landing Zone — Control Tower + Organizations + Terraform GitOps
  </text>

  <!-- Outer: AWS Organizations -->
  <rect x="14" y="30" width="870" height="440" rx="12" fill="none" stroke="#f97316" stroke-width="2" stroke-dasharray="9,4"/>
  <text x="28" y="50" font-family="sans-serif" font-size="10" font-weight="700" fill="#c2410c">AWS Organizations (Root)</text>

  <!-- Terraform/GitOps -->
  <rect x="28" y="56" width="148" height="88" rx="8" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.5"/>
  <text x="102" y="76" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="700" fill="#166534">⚙ Terraform</text>
  <text x="102" y="91" text-anchor="middle" font-family="sans-serif" font-size="8.5" fill="#16a34a">GitHub Actions CI</text>
  <text x="102" y="105" text-anchor="middle" font-family="sans-serif" font-size="8.5" fill="#16a34a">GitOps · IaC Modules</text>
  <text x="102" y="119" text-anchor="middle" font-family="sans-serif" font-size="8.5" fill="#16a34a">Account Vending</text>
  <text x="102" y="133" text-anchor="middle" font-family="sans-serif" font-size="8.5" fill="#16a34a">Baseline Deployment</text>

  <!-- Management Account -->
  <rect x="350" y="56" width="196" height="88" rx="8" fill="#fff7ed" stroke="#f97316" stroke-width="2"/>
  <text x="448" y="76" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="700" fill="#9a3412">Management Account</text>
  <text x="448" y="93" text-anchor="middle" font-family="sans-serif" font-size="9" fill="#c2410c">AWS Control Tower</text>
  <text x="448" y="108" text-anchor="middle" font-family="sans-serif" font-size="8.5" fill="#c2410c">Account Vending · Guardrails</text>
  <text x="448" y="122" text-anchor="middle" font-family="sans-serif" font-size="8.5" fill="#c2410c">SCPs · Consolidated Billing</text>
  <text x="448" y="136" text-anchor="middle" font-family="sans-serif" font-size="8.5" fill="#c2410c">IAM Identity Center (SSO)</text>

  <!-- Arrow Terraform → Mgmt -->
  <line x1="176" y1="100" x2="348" y2="100" stroke="#16a34a" stroke-width="1.5" marker-end="url(#bh)"/>

  <!-- Security OU -->
  <rect x="28" y="186" width="238" height="120" rx="8" fill="#fff1f2" stroke="#f43f5e" stroke-width="1.5"/>
  <text x="147" y="206" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="700" fill="#9f1239">Security OU</text>
  <!-- Log Archive -->
  <rect x="38" y="213" width="100" height="80" rx="5" fill="#fee2e2" stroke="#f87171"/>
  <text x="88" y="232" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="700" fill="#991b1b">Log Archive</text>
  <text x="88" y="247" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#b91c1c">CloudTrail (org)</text>
  <text x="88" y="259" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#b91c1c">S3 Access Logs</text>
  <text x="88" y="271" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#b91c1c">Config Snapshots</text>
  <text x="88" y="285" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#b91c1c">Glacier Archive</text>
  <!-- Audit -->
  <rect x="148" y="213" width="108" height="80" rx="5" fill="#fee2e2" stroke="#f87171"/>
  <text x="202" y="232" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="700" fill="#991b1b">Audit Account</text>
  <text x="202" y="247" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#b91c1c">Security Hub</text>
  <text x="202" y="259" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#b91c1c">GuardDuty</text>
  <text x="202" y="271" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#b91c1c">AWS Config</text>
  <text x="202" y="285" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#b91c1c">Inspector v2</text>

  <!-- Workloads OU -->
  <rect x="282" y="186" width="596" height="120" rx="8" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="580" y="206" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="700" fill="#1e40af">Workloads OU</text>
  <!-- Dev -->
  <rect x="292" y="213" width="172" height="80" rx="5" fill="#dbeafe" stroke="#60a5fa"/>
  <text x="378" y="232" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="700" fill="#1e40af">Dev Account</text>
  <text x="378" y="247" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#2563eb">VPC · Private Subnets</text>
  <text x="378" y="259" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#2563eb">EKS Dev Cluster</text>
  <text x="378" y="271" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#2563eb">IAM Roles · SCPs</text>
  <text x="378" y="283" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#2563eb">Cost Allocation Tags</text>
  <!-- Staging -->
  <rect x="474" y="213" width="172" height="80" rx="5" fill="#dbeafe" stroke="#60a5fa"/>
  <text x="560" y="232" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="700" fill="#1e40af">Staging Account</text>
  <text x="560" y="247" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#2563eb">VPC · Private Subnets</text>
  <text x="560" y="259" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#2563eb">EKS Staging</text>
  <text x="560" y="271" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#2563eb">IAM Roles · SCPs</text>
  <text x="560" y="283" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#2563eb">Integration Tests</text>
  <!-- Prod -->
  <rect x="656" y="213" width="212" height="80" rx="5" fill="#bfdbfe" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="762" y="232" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="700" fill="#1e3a8a">Production Account</text>
  <text x="762" y="247" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#1e40af">VPC · Private Subnets</text>
  <text x="762" y="259" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#1e40af">EKS Prod · Multi-AZ</text>
  <text x="762" y="271" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#1e40af">IAM Roles · SCPs · WAF</text>
  <text x="762" y="283" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#1e40af">Backups · DR Policy</text>

  <!-- Shared Services OU -->
  <rect x="28" y="328" width="568" height="130" rx="8" fill="#faf5ff" stroke="#9333ea" stroke-width="1.5"/>
  <text x="312" y="348" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="700" fill="#6b21a8">Shared Services OU</text>
  <rect x="38" y="356" width="130" height="90" rx="5" fill="#ede9fe" stroke="#a78bfa"/>
  <text x="103" y="376" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="700" fill="#5b21b6">Networking</text>
  <text x="103" y="392" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#7c3aed">Transit Gateway</text>
  <text x="103" y="404" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#7c3aed">Route 53 · DNS</text>
  <text x="103" y="416" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#7c3aed">VPC Peering</text>
  <text x="103" y="428" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#7c3aed">Direct Connect</text>
  <rect x="178" y="356" width="130" height="90" rx="5" fill="#ede9fe" stroke="#a78bfa"/>
  <text x="243" y="376" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="700" fill="#5b21b6">Identity (SSO)</text>
  <text x="243" y="392" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#7c3aed">IAM Identity Center</text>
  <text x="243" y="404" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#7c3aed">Permission Sets</text>
  <text x="243" y="416" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#7c3aed">AD Integration</text>
  <text x="243" y="428" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#7c3aed">MFA Enforcement</text>
  <rect x="318" y="356" width="130" height="90" rx="5" fill="#ede9fe" stroke="#a78bfa"/>
  <text x="383" y="376" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="700" fill="#5b21b6">DevOps Tooling</text>
  <text x="383" y="392" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#7c3aed">CodeArtifact</text>
  <text x="383" y="404" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#7c3aed">ECR (shared)</text>
  <text x="383" y="416" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#7c3aed">S3 Artifacts</text>
  <text x="383" y="428" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#7c3aed">Secrets Manager</text>
  <rect x="458" y="356" width="128" height="90" rx="5" fill="#ede9fe" stroke="#a78bfa"/>
  <text x="522" y="376" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="700" fill="#5b21b6">Observability</text>
  <text x="522" y="392" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#7c3aed">CloudWatch (org)</text>
  <text x="522" y="404" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#7c3aed">Security Hub agg.</text>
  <text x="522" y="416" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#7c3aed">GuardDuty (org)</text>
  <text x="522" y="428" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#7c3aed">Config Aggregator</text>

  <!-- Governance -->
  <rect x="610" y="328" width="268" height="130" rx="8" fill="#fefce8" stroke="#eab308" stroke-width="1.5"/>
  <text x="744" y="348" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="700" fill="#713f12">Governance Layer</text>
  <text x="744" y="366" text-anchor="middle" font-family="sans-serif" font-size="8.5" fill="#854d0e">Service Control Policies (SCPs)</text>
  <text x="744" y="382" text-anchor="middle" font-family="sans-serif" font-size="8.5" fill="#854d0e">AWS Config Rules + Conformance Packs</text>
  <text x="744" y="398" text-anchor="middle" font-family="sans-serif" font-size="8.5" fill="#854d0e">CloudTrail (org-wide, immutable)</text>
  <text x="744" y="414" text-anchor="middle" font-family="sans-serif" font-size="8.5" fill="#854d0e">Security Hub Aggregator</text>
  <text x="744" y="430" text-anchor="middle" font-family="sans-serif" font-size="8.5" fill="#854d0e">GuardDuty (org-wide delegation)</text>
  <text x="744" y="446" text-anchor="middle" font-family="sans-serif" font-size="8.5" fill="#854d0e">AWS Budgets + Cost Explorer</text>

  <!-- Arrows Mgmt → OUs -->
  <line x1="448" y1="144" x2="180" y2="184" stroke="#f97316" stroke-width="1.5" marker-end="url(#bg)"/>
  <line x1="448" y1="144" x2="460" y2="184" stroke="#f97316" stroke-width="1.5" marker-end="url(#bg)"/>
  <line x1="448" y1="144" x2="310" y2="326" stroke="#9333ea" stroke-width="1.4" stroke-dasharray="5,3" marker-end="url(#bh)"/>
  <line x1="448" y1="144" x2="720" y2="326" stroke="#eab308" stroke-width="1.4" stroke-dasharray="5,3" marker-end="url(#bh)"/>
</svg>"""


ARCH_MAP = {"eks": arch_eks, "platform": arch_platform}

# ─────────────────────────────────────────────────────────────────────────────
# CSS — refined light theme, editorial/card-based, compact & dense
# ─────────────────────────────────────────────────────────────────────────────
def css() -> str:
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,300;12..96,400;12..96,500;12..96,600;12..96,700;12..96,800&family=Fira+Code:wght@300;400;500&display=swap');

*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}

:root{
  --bg:#eef2f8;
  --surface:#ffffff;
  --surface2:#f4f7fc;
  --border:#dde3ef;
  --border2:#c8d0e4;
  --aws:#d97706;
  --azure:#0064b5;
  --accent:#1d4ed8;
  --accent-h:#1e40af;
  --violet:#6d28d9;
  --green:#15803d;
  --text:#0a1628;
  --sub:#374151;
  --muted:#64748b;
  --light:#94a3b8;
  --head:'Bricolage Grotesque',sans-serif;
  --mono:'Fira Code',monospace;
  --r:10px;
  --sh:0 2px 10px rgba(29,78,216,.07),0 1px 3px rgba(10,22,40,.06);
  --sh2:0 8px 28px rgba(29,78,216,.12),0 2px 8px rgba(10,22,40,.08);
}

html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--text);font-family:var(--head);font-size:14.5px;line-height:1.65;overflow-x:hidden}

/* ── subtle grid bg ── */
body::after{
  content:'';position:fixed;inset:0;z-index:-1;pointer-events:none;
  background-image:linear-gradient(var(--border) 1px,transparent 1px),linear-gradient(90deg,var(--border) 1px,transparent 1px);
  background-size:44px 44px;opacity:.28;
}

/* ── NAV ── */
nav{
  position:fixed;top:0;left:0;right:0;z-index:200;
  display:flex;align-items:center;justify-content:space-between;gap:1rem;
  padding:0 clamp(1rem,4vw,3.5rem);height:54px;
  background:rgba(238,242,248,.94);backdrop-filter:blur(18px);
  border-bottom:1px solid var(--border2);box-shadow:var(--sh);
}
.nav-logo{font-family:var(--head);font-weight:800;font-size:1.1rem;color:var(--accent);text-decoration:none;letter-spacing:-.03em}
.nav-logo span{color:var(--muted)}
.nav-links{display:flex;gap:0;list-style:none}
.nav-links a{
  color:var(--muted);text-decoration:none;font-size:.8rem;font-weight:500;
  padding:.32rem .78rem;border-radius:6px;transition:all .16s;letter-spacing:.01em;
}
.nav-links a:hover,.nav-links a.active{color:var(--accent);background:rgba(29,78,216,.08)}
.nav-book{
  display:inline-flex;align-items:center;gap:.35rem;
  padding:.35rem 1rem;font-family:var(--head);font-size:.78rem;font-weight:700;
  background:var(--accent);color:#fff;border:none;border-radius:7px;cursor:pointer;
  box-shadow:0 2px 8px rgba(29,78,216,.28);transition:all .16s;white-space:nowrap;
}
.nav-book:hover{background:var(--accent-h);transform:translateY(-1px)}

main{padding-top:54px}

/* ── LAYOUT ── */
.wrap{max-width:1180px;margin:0 auto;padding:0 clamp(1rem,5vw,3.5rem)}
.section{padding:clamp(2.5rem,6vw,5rem) clamp(1rem,5vw,3.5rem);max-width:1180px;margin:0 auto}
.sec-label{
  font-family:var(--mono);font-size:.62rem;font-weight:500;
  letter-spacing:.22em;text-transform:uppercase;color:var(--accent);
  margin-bottom:.7rem;display:flex;align-items:center;gap:.6rem;
}
.sec-label::after{content:'';height:1px;width:40px;background:var(--accent);opacity:.35}

h1,h2,h3,h4{font-family:var(--head)}

/* ── BUTTONS ── */
.btn{
  display:inline-flex;align-items:center;gap:.4rem;
  padding:.55rem 1.3rem;font-family:var(--head);font-size:.82rem;font-weight:600;
  text-decoration:none;border-radius:7px;transition:all .16s;cursor:pointer;border:none;white-space:nowrap;
}
.btn-p{background:var(--accent);color:#fff;box-shadow:0 2px 10px rgba(29,78,216,.25)}
.btn-p:hover{background:var(--accent-h);transform:translateY(-1px);box-shadow:0 4px 16px rgba(29,78,216,.35)}
.btn-v{background:var(--violet);color:#fff;box-shadow:0 2px 10px rgba(109,40,217,.22)}
.btn-v:hover{background:#5b21b6;transform:translateY(-1px)}
.btn-o{background:var(--surface);color:var(--sub);border:1.5px solid var(--border2);box-shadow:var(--sh)}
.btn-o:hover{border-color:var(--accent);color:var(--accent);transform:translateY(-1px)}

/* ── HERO ── */
.hero{
  display:grid;grid-template-columns:1fr 420px;gap:2.5rem;align-items:center;
  padding:clamp(1.5rem,5vw,4rem) clamp(1rem,5vw,3.5rem);
  max-width:1180px;margin:0 auto;min-height:calc(100vh - 54px);
}
.eyebrow{
  display:inline-flex;align-items:center;gap:.45rem;
  font-family:var(--mono);font-size:.7rem;font-weight:500;letter-spacing:.12em;text-transform:uppercase;
  color:var(--accent);background:rgba(29,78,216,.09);border:1px solid rgba(29,78,216,.18);
  padding:.28rem .8rem;border-radius:20px;margin-bottom:1.1rem;
}
.hero h1{
  font-size:clamp(2.4rem,5.8vw,4.2rem);font-weight:800;line-height:1.06;
  letter-spacing:-.035em;color:var(--text);margin-bottom:1rem;
}
.hero h1 em{
  font-style:normal;
  background:linear-gradient(130deg,var(--accent),var(--violet));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}
.hero-sub{font-size:.95rem;color:var(--muted);max-width:470px;line-height:1.8;margin-bottom:1.8rem}
.hero-cta{display:flex;gap:.7rem;flex-wrap:wrap;margin-bottom:2rem}
.hero-stats{display:flex;gap:1.8rem;flex-wrap:wrap}
.stat-n{font-family:var(--head);font-size:1.5rem;font-weight:800;color:var(--text);line-height:1}
.stat-n span{color:var(--accent)}
.stat-l{font-family:var(--mono);font-size:.65rem;color:var(--muted);margin-top:.15rem;letter-spacing:.04em}

/* ── HERO PANEL ── */
.hero-panel{
  position:relative;background:var(--surface);border:1px solid var(--border2);
  border-radius:14px;padding:1.5rem;box-shadow:var(--sh2);overflow:hidden;
}
.hero-panel::before{
  content:'';position:absolute;top:-60px;right:-60px;width:200px;height:200px;
  background:radial-gradient(circle,rgba(29,78,216,.12),transparent 70%);pointer-events:none;
}
.tech-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:.5rem;margin-bottom:1rem}
.tech-chip{
  display:flex;align-items:center;gap:.35rem;
  background:var(--surface2);border:1px solid var(--border);border-radius:7px;
  padding:.4rem .55rem;font-family:var(--mono);font-size:.68rem;color:var(--sub);
  transition:all .16s;cursor:default;
}
.tech-chip:hover{border-color:var(--accent);color:var(--accent);background:rgba(29,78,216,.05)}
.tech-chip .dot{width:7px;height:7px;border-radius:50%;flex-shrink:0}

.pipeline{display:flex;align-items:center;gap:0;margin-top:.75rem;overflow-x:auto}
.pipe-step{
  flex:1;min-width:0;text-align:center;padding:.5rem .3rem;
  background:var(--surface2);border:1px solid var(--border);font-size:.65rem;font-weight:600;
  color:var(--sub);font-family:var(--mono);line-height:1.3;
}
.pipe-step:first-child{border-radius:7px 0 0 7px}
.pipe-step:last-child{border-radius:0 7px 7px 0}
.pipe-arrow{color:var(--accent);font-size:.75rem;flex-shrink:0;padding:0 1px}
.pipe-step .icon{font-size:.9rem;display:block;margin-bottom:.15rem}

.panel-label{font-family:var(--mono);font-size:.6rem;letter-spacing:.18em;text-transform:uppercase;color:var(--light);margin-bottom:.5rem}

/* ── CERT STRIP ── */
.cert-strip{display:flex;flex-wrap:wrap;gap:.5rem}
.cert{
  display:flex;align-items:center;gap:.4rem;
  padding:.32rem .8rem;border-radius:20px;font-size:.72rem;font-weight:600;
  border:1.5px solid;background:var(--surface);box-shadow:var(--sh);
  transition:transform .14s,box-shadow .14s;
}
.cert:hover{transform:translateY(-2px);box-shadow:var(--sh2)}

/* ── FEATURED PROJECTS (home) ── */
.feat-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:1rem}
.feat-card{
  background:var(--surface);border:1px solid var(--border2);border-radius:var(--r);
  padding:1.4rem;box-shadow:var(--sh);transition:all .18s;position:relative;overflow:hidden;
}
.feat-card::before{
  content:'';position:absolute;left:0;top:0;bottom:0;width:3px;
  background:linear-gradient(to bottom,var(--accent),var(--violet));
  transform:scaleY(0);transform-origin:bottom;transition:transform .25s;
}
.feat-card:hover{box-shadow:var(--sh2);transform:translateY(-2px)}
.feat-card:hover::before{transform:scaleY(1)}
.feat-badge{
  display:inline-block;font-family:var(--mono);font-size:.6rem;font-weight:500;
  letter-spacing:.14em;text-transform:uppercase;padding:.18rem .6rem;
  border-radius:20px;margin-bottom:.65rem;
}
.b-prod{background:rgba(29,78,216,.09);color:var(--accent);border:1px solid rgba(29,78,216,.22)}
.b-dev{background:rgba(217,119,6,.09);color:var(--aws);border:1px solid rgba(217,119,6,.22)}
.feat-card h3{font-size:.97rem;font-weight:700;letter-spacing:-.018em;margin-bottom:.5rem;color:var(--text)}
.feat-card p{font-size:.8rem;color:var(--muted);line-height:1.7;margin-bottom:.9rem}
.feat-tags{display:flex;flex-wrap:wrap;gap:.3rem;margin-bottom:.9rem}
.tag{font-family:var(--mono);font-size:.62rem;padding:.18rem .5rem;border:1px solid var(--border);color:var(--muted);border-radius:5px;background:var(--surface2)}

/* ── STACK ── */
.stack-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:.8rem}
.stack-card{
  background:var(--surface);border:1px solid var(--border);border-radius:var(--r);
  padding:1.3rem;box-shadow:var(--sh);transition:all .18s;
}
.stack-card:hover{box-shadow:var(--sh2);transform:translateY(-2px)}
.stack-card-head{display:flex;align-items:center;gap:.5rem;margin-bottom:.8rem}
.stack-card-head h3{font-family:var(--mono);font-size:.7rem;font-weight:500;letter-spacing:.1em;text-transform:uppercase;color:var(--accent)}
.stack-card ul{list-style:none}
.stack-card li{
  font-size:.8rem;color:var(--muted);padding:.22rem 0;
  border-bottom:1px solid var(--surface2);display:flex;align-items:center;gap:.4rem;
}
.stack-card li:last-child{border-bottom:none}
.stack-card li::before{content:'›';color:var(--accent);flex-shrink:0}

/* ── PROJECT DETAIL CARDS ── */
.proj-card{
  background:var(--surface);border:1px solid var(--border2);border-radius:14px;
  padding:2rem;margin-bottom:1.5rem;box-shadow:var(--sh);
}
.proj-card:hover{box-shadow:var(--sh2)}
.proj-card h2{font-size:1.4rem;font-weight:800;letter-spacing:-.025em;margin-bottom:.6rem}
.proj-summary{font-size:.88rem;color:var(--muted);line-height:1.85;margin-bottom:1.2rem}
.proj-hl{list-style:none;margin-bottom:1.2rem}
.proj-hl li{
  font-size:.82rem;color:var(--sub);padding:.26rem 0;
  border-bottom:1px solid var(--surface2);display:flex;gap:.5rem;align-items:flex-start;
}
.proj-hl li:last-child{border-bottom:none}
.proj-hl li::before{content:'◆';color:var(--accent);font-size:.45rem;margin-top:.45rem;flex-shrink:0}

/* ── ARCH BOX ── */
.arch-box{
  margin-top:1.5rem;padding:1.2rem;
  background:var(--surface2);border:1px solid var(--border);border-radius:10px;
}
.arch-box h4{font-family:var(--mono);font-size:.68rem;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);margin-bottom:.4rem}
.arch-box p{font-size:.78rem;color:var(--muted);margin-bottom:.8rem;line-height:1.6}

/* ── MEDIA SECTION ── */
.media-box{
  margin-top:1.2rem;padding:1.2rem;
  background:var(--surface2);border:1px solid var(--border);border-radius:10px;
}
.media-box h4{font-family:var(--mono);font-size:.68rem;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:var(--violet);margin-bottom:.8rem}
.media-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:.7rem}
.media-img{width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:7px;border:1px solid var(--border);box-shadow:var(--sh)}
.media-video{width:100%;border-radius:7px;border:1px solid var(--border);box-shadow:var(--sh)}
.media-empty{
  border:2px dashed var(--border2);border-radius:8px;padding:1.5rem;
  text-align:center;font-family:var(--mono);font-size:.72rem;color:var(--light);line-height:1.8;
}

/* ── SERVICES ── */
.svc-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:.9rem}
.svc-card{
  background:var(--surface);border:1px solid var(--border);border-radius:var(--r);
  padding:1.4rem;box-shadow:var(--sh);transition:all .18s;
}
.svc-card:hover{box-shadow:var(--sh2);transform:translateY(-2px)}
.svc-icon{font-size:1.3rem;margin-bottom:.7rem}
.svc-card h3{font-size:.94rem;font-weight:700;margin-bottom:.7rem}
.svc-card ul{list-style:none}
.svc-card li{font-size:.79rem;color:var(--muted);padding:.22rem 0;border-bottom:1px solid var(--surface2);display:flex;gap:.4rem}
.svc-card li:last-child{border-bottom:none}
.svc-card li::before{content:'–';color:var(--accent);flex-shrink:0}

/* ── CONTACT ── */
.cta-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:.8rem;margin-bottom:2rem}
.cta-card{
  background:var(--surface);border:1px solid var(--border);border-radius:var(--r);
  padding:1.4rem;text-decoration:none;color:inherit;box-shadow:var(--sh);
  transition:all .18s;display:block;
}
.cta-card:hover{box-shadow:var(--sh2);transform:translateY(-2px);border-color:var(--accent)}
.cta-type{font-family:var(--mono);font-size:.6rem;letter-spacing:.16em;text-transform:uppercase;color:var(--accent);margin-bottom:.4rem}
.cta-val{font-size:.86rem;font-weight:600;color:var(--text)}

/* ── PAGE HERO ── */
.page-hero{
  padding:3.5rem clamp(1rem,5vw,3.5rem) 2rem;
  max-width:1180px;margin:0 auto;border-bottom:1px solid var(--border);
}
.page-hero h1{font-size:clamp(1.9rem,4vw,2.9rem);font-weight:800;letter-spacing:-.03em}
.page-hero p{color:var(--muted);margin-top:.5rem;max-width:500px;font-size:.9rem}

/* ── ABOUT GRID (home) ── */
.about-grid{display:grid;grid-template-columns:3fr 2fr;gap:2.5rem;align-items:start}
.about-text p{font-size:.88rem;color:var(--muted);line-height:1.9;margin-bottom:.9rem}
.about-focus{display:flex;flex-wrap:wrap;gap:.4rem;margin-top:1rem}
.focus-tag{
  font-family:var(--mono);font-size:.68rem;padding:.28rem .7rem;
  background:rgba(29,78,216,.07);border:1px solid rgba(29,78,216,.2);
  color:var(--accent);border-radius:20px;font-weight:500;
}
.skill-bars{display:flex;flex-direction:column;gap:.6rem}
.skill-row{display:flex;flex-direction:column;gap:.22rem}
.skill-top{display:flex;justify-content:space-between;font-size:.74rem;font-weight:600;color:var(--sub)}
.skill-bar{height:5px;background:var(--border);border-radius:3px;overflow:hidden}
.skill-fill{height:100%;border-radius:3px;background:linear-gradient(90deg,var(--accent),var(--violet))}

/* ── CALENDLY MODAL ── */
.cal-overlay{
  display:none;position:fixed;inset:0;z-index:500;
  background:rgba(10,22,40,.55);backdrop-filter:blur(8px);
  align-items:center;justify-content:center;padding:1rem;
}
.cal-overlay.open{display:flex}
.cal-modal{
  background:var(--surface);border:1px solid var(--border2);border-radius:16px;
  width:100%;max-width:700px;max-height:90vh;overflow:hidden;
  box-shadow:0 24px 60px rgba(29,78,216,.18);position:relative;
  display:flex;flex-direction:column;
  animation:slideUp .22s ease;
}
@keyframes slideUp{from{transform:translateY(18px);opacity:0}to{transform:translateY(0);opacity:1}}
.cal-header{
  display:flex;align-items:center;justify-content:space-between;
  padding:1.2rem 1.5rem;border-bottom:1px solid var(--border);
  background:var(--surface2);flex-shrink:0;
}
.cal-header h2{font-size:1.05rem;font-weight:800;letter-spacing:-.02em}
.cal-header p{font-size:.78rem;color:var(--muted);margin-top:.15rem}
.cal-close{
  background:none;border:none;cursor:pointer;
  font-size:1.3rem;color:var(--muted);line-height:1;padding:.2rem;
}
.cal-close:hover{color:var(--text)}
.cal-body{flex:1;overflow:hidden;min-height:480px;position:relative}
.cal-body iframe{width:100%;height:100%;min-height:480px;border:none}
.cal-loading{
  position:absolute;inset:0;display:flex;flex-direction:column;
  align-items:center;justify-content:center;gap:1rem;font-size:.85rem;color:var(--muted);
}
.spinner{width:28px;height:28px;border:3px solid var(--border2);border-top-color:var(--accent);border-radius:50%;animation:spin .7s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}

/* ── FOOTER ── */
footer{
  background:var(--surface);border-top:1px solid var(--border2);
  padding:1.5rem clamp(1rem,5vw,3.5rem);
  display:flex;justify-content:space-between;align-items:center;
  flex-wrap:wrap;gap:.75rem;font-size:.76rem;color:var(--muted);margin-top:3rem;
}

hr.div{border:none;border-top:1px solid var(--border)}

@media(max-width:820px){
  .hero{grid-template-columns:1fr}
  .hero-panel{display:none}
  .about-grid{grid-template-columns:1fr}
}
@media(max-width:540px){
  .feat-grid,.svc-grid,.stack-grid{grid-template-columns:1fr}
  .nav-links{display:none}
  .tech-grid{grid-template-columns:repeat(2,1fr)}
}
</style>
"""

# ─────────────────────────────────────────────────────────────────────────────
# CALENDLY MODAL
# ─────────────────────────────────────────────────────────────────────────────
def calendly_modal() -> str:
    url = SITE["calendly"]
    return f"""
<div class="cal-overlay" id="calModal">
  <div class="cal-modal">
    <div class="cal-header">
      <div>
        <h2>📅 Book a Meeting</h2>
        <p>Schedule a cloud / platform engineering consultation — powered by Calendly</p>
      </div>
      <button class="cal-close" onclick="closeCal()" aria-label="Close">✕</button>
    </div>
    <div class="cal-body">
      <div class="cal-loading" id="calLoad">
        <div class="spinner"></div>
        Loading Calendly…
      </div>
      <iframe
        id="calFrame"
        src="{url}?embed_domain=gprai.github.io&embed_type=Inline&hide_gdpr_banner=1"
        title="Book a meeting"
        onload="document.getElementById('calLoad').style.display='none'"
      ></iframe>
    </div>
  </div>
</div>

<script>
function openCal(){{
  document.getElementById('calModal').classList.add('open');
  document.body.style.overflow='hidden';
}}
function closeCal(){{
  document.getElementById('calModal').classList.remove('open');
  document.body.style.overflow='';
}}
document.getElementById('calModal').addEventListener('click',function(e){{
  if(e.target===this)closeCal();
}});
document.addEventListener('keydown',function(e){{if(e.key==='Escape')closeCal();}});
</script>
"""

# ─────────────────────────────────────────────────────────────────────────────
# NAV / FOOTER / PAGE SHELL
# ─────────────────────────────────────────────────────────────────────────────
def nav(active="") -> str:
    links = [("Home","index.html"),("Stack","stack.html"),("Projects","projects.html"),
             ("Services","services.html"),("Contact","contact.html")]
    items = "".join(
        f'<li><a href="/{h}" {"class=\"active\"" if l.lower()==active.lower() else ""}>{l}</a></li>'
        for l,h in links
    )
    return f"""
<nav>
  <a class="nav-logo" href="/index.html">GPR<span>.</span></a>
  <ul class="nav-links">{items}</ul>
  <button class="nav-book" onclick="openCal()">📅 Book a Call</button>
</nav>"""

def footer_frag() -> str:
    return f"""
<footer>
  <span>© 2025 Gyan Prakash Rai · Cloud & Platform Engineer</span>
  <span style="display:flex;gap:1.2rem;flex-wrap:wrap">
    <a href="{SITE['github']}" style="color:var(--muted);text-decoration:none" target="_blank">GitHub</a>
    <a href="{SITE['linkedin']}" style="color:var(--muted);text-decoration:none" target="_blank">LinkedIn</a>
    <a href="mailto:{SITE['email']}" style="color:var(--muted);text-decoration:none">{SITE['email']}</a>
  </span>
</footer>"""

def page(title, body, active="") -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <title>{title} · Gyan Prakash Rai</title>
  <meta name="description" content="AWS & Azure Platform Engineer — Kubernetes, Terraform, CI/CD, GitOps, DevSecOps"/>
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
  {css()}
</head>
<body>
  {nav(active)}
  {calendly_modal()}
  <main>{body}</main>
  {footer_frag()}
</body>
</html>"""

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: INDEX
# ─────────────────────────────────────────────────────────────────────────────
def build_index() -> str:
    typing_words = [
        "AWS & Azure Platform Engineer",
        "Kubernetes · EKS · AKS · Karpenter",
        "Terraform · GitOps · CI/CD",
        "DevSecOps · Observability",
        "AI-Ready Cloud Architecture",
    ]
    chips = [
        ("#FF9900","AWS EKS"),("#0072c6","Azure AKS"),("#6d28d9","Terraform"),
        ("#15803d","GitHub Actions"),("#1d4ed8","ArgoCD"),("#d97706","Karpenter"),
        ("#db2777","Docker · Helm"),("#0ea5e9","Prometheus"),("#7c3aed","AWS Bedrock"),
    ]
    chip_html = "".join(
        f'<div class="tech-chip"><span class="dot" style="background:{c}"></span>{lbl}</div>'
        for c,lbl in chips
    )
    certs_html = "".join(
        f'<div class="cert" style="border-color:{c["color"]};color:{c["color"]}">'
        f'{"☁" if c["vendor"]=="AWS" else "⬡"}&nbsp;{c["label"]}</div>'
        for c in CERTIFICATIONS
    )
    stats_html = "".join(
        f'<div><div class="stat-n">{s["n"]}<span>.</span></div><div class="stat-l">{s["label"]}</div></div>'
        for s in ABOUT["stats"]
    )
    # Featured projects
    feat_html = ""
    for p in PROJECTS:
        if not p.get("featured"):
            continue
        bc = "b-prod" if p["status"]=="Production" else "b-dev"
        tags = "".join(f'<span class="tag">{t}</span>' for t in p["stack"][:5])
        feat_html += f"""
<div class="feat-card">
  <span class="feat-badge {bc}">{p['status']}</span>
  <h3>{p['title']}</h3>
  <p>{p['short']}</p>
  <div class="feat-tags">{tags}</div>
  <a href="/projects.html#{p['id']}" class="btn btn-o" style="font-size:.76rem;padding:.42rem 1rem">
    Full Details →
  </a>
</div>"""
    # About focus
    focus_html = "".join(f'<span class="focus-tag">{f}</span>' for f in ABOUT["focus"])
    skills = [
        ("Cloud (AWS & Azure)", 95),("Kubernetes & EKS/AKS", 90),
        ("Terraform / IaC", 90),("CI/CD & GitOps", 88),
        ("DevSecOps", 82),("AI Infra / MLOps", 75),
    ]
    bars_html = "".join(
        f'<div class="skill-row"><div class="skill-top"><span>{n}</span><span>{v}%</span></div>'
        f'<div class="skill-bar"><div class="skill-fill" style="width:{v}%"></div></div></div>'
        for n,v in skills
    )
    bio_html = "".join(f'<p>{b}</p>' for b in ABOUT["bio"])

    return page("Home", f"""
<!-- HERO -->
<section class="hero">
  <div>
    <div class="eyebrow">🚀 Open for Consulting &amp; Freelance</div>
    <h1>Gyan Prakash<br/><em>Rai</em></h1>
    <p class="hero-sub">
      <span id="ty" style="color:var(--accent);font-weight:600"></span><span style="color:var(--accent);animation:blink 1s step-end infinite">_</span>
      <br/><br/>
      Building scalable, secure, production-grade cloud infrastructure on AWS &amp; Azure — with Kubernetes, Terraform, CI/CD and GitOps at the core.
    </p>
    <div class="hero-cta">
      <a href="/projects.html" class="btn btn-p">View Projects</a>
      <button class="btn btn-v" onclick="openCal()">📅 Book a Demo</button>
      <a href="/services.html" class="btn btn-o">Services</a>
    </div>
    <div class="hero-stats">{stats_html}</div>
  </div>

  <div class="hero-panel">
    <div class="panel-label">Core Tech Stack</div>
    <div class="tech-grid">{chip_html}</div>
    <div class="panel-label" style="margin-top:.8rem">GitOps CI/CD Pipeline</div>
    <div class="pipeline">
      <div class="pipe-step"><span class="icon">👨‍💻</span>Push</div>
      <div class="pipe-arrow">›</div>
      <div class="pipe-step"><span class="icon">⚙</span>Actions</div>
      <div class="pipe-arrow">›</div>
      <div class="pipe-step"><span class="icon">📦</span>ECR</div>
      <div class="pipe-arrow">›</div>
      <div class="pipe-step"><span class="icon">⎈</span>Helm</div>
      <div class="pipe-arrow">›</div>
      <div class="pipe-step"><span class="icon">🔄</span>ArgoCD</div>
      <div class="pipe-arrow">›</div>
      <div class="pipe-step"><span class="icon">☸</span>EKS</div>
    </div>
  </div>
</section>

<hr class="div"/>

<!-- CERTS -->
<section class="section">
  <p class="sec-label">Certifications</p>
  <h2 style="font-size:1.35rem;font-weight:800;letter-spacing:-.02em;margin-bottom:1.1rem">7 Cloud Certifications — AWS &amp; Azure</h2>
  <div class="cert-strip">{certs_html}</div>
</section>

<hr class="div"/>

<!-- ABOUT -->
<section class="section">
  <p class="sec-label">About</p>
  <div class="about-grid">
    <div class="about-text">
      <h2 style="font-size:1.5rem;font-weight:800;letter-spacing:-.025em;margin-bottom:1rem">
        Cloud-native infrastructure,<br/>built for production.
      </h2>
      {bio_html}
      <div class="about-focus">{focus_html}</div>
      <div style="margin-top:1.4rem;display:flex;gap:.7rem;flex-wrap:wrap">
        <a href="/contact.html" class="btn btn-p">Get in Touch</a>
        <a href="{SITE['resume']}" class="btn btn-o" target="_blank" rel="noopener">Resume ↗</a>
        <button class="btn btn-v" onclick="openCal()">📅 Book a Call</button>
      </div>
    </div>
    <div class="skill-bars">{bars_html}</div>
  </div>
</section>

<hr class="div"/>

<!-- FEATURED PROJECTS -->
<section class="section">
  <div style="display:flex;align-items:baseline;justify-content:space-between;gap:1rem;margin-bottom:1.2rem;flex-wrap:wrap">
    <div>
      <p class="sec-label">Featured Projects</p>
      <h2 style="font-size:1.35rem;font-weight:800;letter-spacing:-.02em">Production-grade Cloud Work</h2>
    </div>
    <a href="/projects.html" class="btn btn-o" style="font-size:.78rem">All Projects →</a>
  </div>
  <div class="feat-grid">{feat_html}</div>
</section>

<hr class="div"/>

<!-- UPCOMING -->
<section class="section">
  <p class="sec-label">Upcoming</p>
  <h2 style="font-size:1.35rem;font-weight:800;letter-spacing:-.02em;margin-bottom:1.2rem">On the Roadmap</h2>
  <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:.8rem">
    {"".join(f'''<div style="background:var(--surface);border:1px solid var(--border);border-radius:var(--r);padding:1.2rem;box-shadow:var(--sh)">
      <span style="font-family:var(--mono);font-size:.58rem;letter-spacing:.14em;text-transform:uppercase;color:var(--light);background:var(--surface2);padding:.15rem .5rem;border-radius:10px">Planned</span>
      <div style="font-size:.9rem;font-weight:700;margin-top:.6rem;margin-bottom:.35rem;color:var(--text)">{t}</div>
      <div style="font-size:.78rem;color:var(--muted)">{d}</div>
    </div>''' for t,d in [
      ("AWS Cost Optimisation Toolkit","Automated rightsizing and reserved instance recommendations using Lambda + Cost Explorer"),
      ("Multi-Cloud Observability Stack","Unified Prometheus + Grafana + Loki stack spanning both AWS and Azure workloads"),
      ("LLM Infra on Bedrock + RAG Pipeline","Production-ready RAG infrastructure with vector store, embedding pipeline and API gateway"),
      ("Automated Compliance Scanning","CIS benchmark enforcement across EKS clusters using Falco + OPA Gatekeeper"),
    ])}
  </div>
</section>

<style>@keyframes blink{{0%,100%{{opacity:1}}50%{{opacity:0}}}}</style>
<script>
const W={json.dumps(typing_words)};
let wi=0,ci=0,dl=false;
const el=document.getElementById('ty');
function t(){{
  const w=W[wi];
  el.textContent=dl?w.slice(0,ci--):w.slice(0,ci++);
  if(!dl&&ci>w.length){{dl=true;setTimeout(t,1300);return;}}
  if(dl&&ci<0){{dl=false;wi=(wi+1)%W.length;}}
  setTimeout(t,dl?36:68);
}}
t();
</script>
""", active="Home")


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: STACK
# ─────────────────────────────────────────────────────────────────────────────
def build_stack() -> str:
    cards = "".join(
        f'<div class="stack-card"><div class="stack-card-head"><span>{s["icon"]}</span><h3>{s["cat"]}</h3></div>'
        f'<ul>{"".join(f"<li>{i}</li>" for i in s["items"])}</ul></div>'
        for s in STACK
    )
    return page("Stack", f"""
<div class="page-hero">
  <p class="sec-label">Tech Stack</p>
  <h1>Tools &amp; Technologies</h1>
  <p>Full stack I work with across cloud, platform engineering, security, and AI/ML.</p>
</div>
<section class="section"><div class="stack-grid">{cards}</div></section>
""", active="Stack")


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: PROJECTS
# ─────────────────────────────────────────────────────────────────────────────
def build_projects() -> str:
    cards = ""
    for p in PROJECTS:
        bc = "b-prod" if p["status"]=="Production" else "b-dev"
        hl = "".join(f"<li>{h}</li>" for h in p["highlights"])
        tags = "".join(f'<span class="tag">{t}</span>' for t in p["stack"])
        arch_svg = ARCH_MAP[p["arch_id"]]()

        # Media section
        img_html = "".join(
            f'<img class="media-img" src="/media/images/{f}" alt="{p["title"]} screenshot" loading="lazy"/>'
            for f in p["media_images"]
        )
        vid_html = "".join(
            f'<video class="media-video" controls preload="metadata">'
            f'<source src="/media/videos/{f}" type="video/mp4"/>Your browser does not support video.</video>'
            for f in p["media_videos"]
        )
        has_media = img_html or vid_html
        if has_media:
            media_sec = f'<div class="media-box"><h4>📸 Screenshots &amp; Demo Videos</h4><div class="media-grid">{img_html}{vid_html}</div></div>'
        else:
            media_sec = f"""<div class="media-box">
  <h4>📸 Screenshots &amp; Demo Videos</h4>
  <div class="media-empty">
    No media added yet.<br/>
    Drop images into <code>docs/media/images/</code> and videos into <code>docs/media/videos/</code><br/>
    then add filenames to the <code>media_images</code> / <code>media_videos</code> lists in <strong>build.py</strong> and re-run the build.
  </div>
</div>"""

        cards += f"""
<div class="proj-card" id="{p['id']}">
  <span class="feat-badge {bc}">{p['status']}</span>
  <h2>{p['title']}</h2>
  <p class="proj-summary">{p['summary']}</p>
  <ul class="proj-hl">{hl}</ul>
  <div class="feat-tags" style="margin-bottom:1.1rem">{tags}</div>
  <div style="display:flex;gap:.7rem;flex-wrap:wrap;margin-bottom:.5rem">
    <a href="{p['repo']}" class="btn btn-p" target="_blank" rel="noopener">GitHub Repo ↗</a>
  </div>
  <div class="arch-box">
    <h4>🗺 Architecture Diagram</h4>
    <p style="font-size:.78rem;color:var(--muted);margin-bottom:.8rem">{p['summary'][:120]}…</p>
    {arch_svg}
  </div>
  {media_sec}
</div>"""

    return page("Projects", f"""
<div class="page-hero">
  <p class="sec-label">Projects</p>
  <h1>Featured Work</h1>
  <p>Production-grade cloud and platform engineering with full architecture diagrams and media.</p>
</div>
<section class="section">{cards}</section>
""", active="Projects")


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: SERVICES
# ─────────────────────────────────────────────────────────────────────────────
def build_services() -> str:
    cards = "".join(
        f'<div class="svc-card"><div class="svc-icon">{s["icon"]}</div><h3>{s["title"]}</h3>'
        f'<ul>{"".join(f"<li>{i}</li>" for i in s["items"])}</ul></div>'
        for s in SERVICES
    )
    return page("Services", f"""
<div class="page-hero">
  <p class="sec-label">Services</p>
  <h1>What I Offer</h1>
  <p>End-to-end cloud engineering, DevOps, and platform consulting.</p>
</div>
<section class="section">
  <div class="svc-grid">{cards}</div>
  <div style="margin-top:2rem;padding:2rem;background:linear-gradient(135deg,rgba(29,78,216,.06),rgba(109,40,217,.06));border:1px solid var(--border2);border-radius:12px;box-shadow:var(--sh)">
    <p class="sec-label">Get started</p>
    <h2 style="font-size:1.4rem;font-weight:800;letter-spacing:-.02em;margin-bottom:.6rem">Ready to build something great?</h2>
    <p style="color:var(--muted);max-width:460px;margin-bottom:1.2rem;font-size:.86rem;line-height:1.8">
      Whether it's a full cloud platform, CI/CD overhaul, or a one-off architecture review — let's talk.
    </p>
    <div style="display:flex;gap:.7rem;flex-wrap:wrap">
      <button class="btn btn-v" onclick="openCal()">📅 Book a Demo Call</button>
      <a href="/contact.html" class="btn btn-o">Contact Me</a>
    </div>
  </div>
</section>
""", active="Services")


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: CONTACT
# ─────────────────────────────────────────────────────────────────────────────
def build_contact() -> str:
    links = [
        ("Email", SITE["email"], f"mailto:{SITE['email']}"),
        ("LinkedIn", "linkedin.com/in/gyan-prakash-rai-24782413", SITE["linkedin"]),
        ("GitHub", "github.com/gprai", SITE["github"]),
        ("Resume", "View / Download PDF", SITE["resume"]),
    ]
    cards = "".join(
        f'<a class="cta-card" href="{h}" target="_blank" rel="noopener">'
        f'<div class="cta-type">{t}</div><div class="cta-val">{v} ↗</div></a>'
        for t,v,h in links
    )
    return page("Contact", f"""
<div class="page-hero">
  <p class="sec-label">Contact</p>
  <h1>Let's Connect</h1>
  <p>Available for freelance, consulting, and full-time opportunities.</p>
</div>
<section class="section">
  <div class="cta-grid">{cards}</div>
  <div style="background:var(--surface);border:1px solid var(--border2);border-radius:12px;padding:2rem;box-shadow:var(--sh);max-width:520px">
    <p class="sec-label">Schedule a call</p>
    <h2 style="font-size:1.2rem;font-weight:800;margin-bottom:.5rem">Prefer a scheduled meeting?</h2>
    <p style="color:var(--muted);font-size:.84rem;margin-bottom:1.1rem;line-height:1.75">
      Use the Calendly booking widget to pick a time that works for you. I confirm within 24 hours.
    </p>
    <button class="btn btn-p" onclick="openCal()">📅 Open Booking Calendar</button>
  </div>
</section>
""", active="Contact")


# ─────────────────────────────────────────────────────────────────────────────
# BUILD
# ─────────────────────────────────────────────────────────────────────────────
def build():
    pages = {
        OUT / "index.html":    build_index(),
        OUT / "stack.html":    build_stack(),
        OUT / "projects.html": build_projects(),
        OUT / "services.html": build_services(),
        OUT / "contact.html":  build_contact(),
    }
    for path, html in pages.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(html, encoding="utf-8")
        print(f"  ✓  {path}")
    # Write a placeholder README inside media folders
    (OUT / "media" / "images" / "README.md").write_text(
        "# Project Screenshots\n\nDrop `.png` / `.jpg` screenshots here.\n"
        "Then add the filenames to the `media_images` list in `build.py`.\n", encoding="utf-8")
    (OUT / "media" / "videos" / "README.md").write_text(
        "# Project Demo Videos\n\nDrop `.mp4` demo videos here (keep each < 100 MB).\n"
        "Then add the filenames to the `media_videos` list in `build.py`.\n", encoding="utf-8")
    print(f"\nBuild complete → {OUT}/")

if __name__ == "__main__":
    build()
