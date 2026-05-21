"""
build.py — Static site generator for gprai.github.io
Run:    python build.py
Output: docs/  (deploy this via GitHub Pages → gh-pages branch)

── MEDIA ────────────────────────────────────────────────────────────────────
  Drop screenshots  → docs/media/images/   (png/jpg, commit normally)
  Drop demo videos  → docs/media/videos/   (mp4, keep each < 100 MB)
  Then add the filenames to media_images / media_videos in each PROJECTS entry.
─────────────────────────────────────────────────────────────────────────────
"""

import json
from pathlib import Path

OUT = Path("docs")
OUT.mkdir(exist_ok=True)
(OUT / "projects").mkdir(exist_ok=True)
(OUT / "media" / "images").mkdir(parents=True, exist_ok=True)
(OUT / "media" / "videos").mkdir(parents=True, exist_ok=True)

# ═════════════════════════════════════════════════════════════════════════════
#  SITE DATA  ←  edit freely
# ═════════════════════════════════════════════════════════════════════════════
SITE = {
    "name":     "Gyan Prakash Rai",
    "role":     "AWS & Azure Platform Engineer · DevOps · Cloud Infrastructure Specialist",
    "email":    "gprai86@gmail.com",
    "linkedin": "https://www.linkedin.com/in/gyan-prakash-rai-24782413/",
    "github":   "https://github.com/gprai",
    "resume":   "https://1drv.ms/f/c/768093078700af7a/IgDCyz3vFgDEQ72Q0ExLIeLWAbIhc1mkgmFdLsg6cDKBXhw?e=4TjZaS",
    # ← set your real Calendly link here
    "calendly": "https://calendly.com/gprai",
}

ABOUT = {
    "bio": [
        "Cloud & DevOps Engineer with deep expertise in designing and automating scalable, secure, production-grade infrastructure on AWS and Azure. I help engineering teams build reliable cloud platforms using Kubernetes (EKS/AKS), Terraform, CI/CD pipelines, Docker, and GitOps-driven delivery workflows.",
        "I also design <strong style='color:#00e5ff'>AI-ready cloud architectures</strong> for modern workloads including Generative AI and MLOps systems — integrating OpenAI, Azure OpenAI, and AWS Bedrock, as well as building infrastructure for LLM applications, RAG pipelines, and automated ML workflows.",
        "My focus is on building systems that are not only deployed correctly, but are <strong style='color:#00e5ff'>maintainable, observable, and production-safe</strong> — reducing operational overhead and improving release reliability.",
    ],
    "focus": [
        "Platform Engineering","Kubernetes Automation","Cloud Architecture",
        "Infrastructure as Code","DevOps Consulting","Freelance Cloud Projects",
    ],
    "stats": [
        {"n":"7+", "label":"Cloud Certs"},
        {"n":"2",  "label":"Cloud Platforms"},
        {"n":"10+","label":"Core Tools"},
        {"n":"∞",  "label":"Automation"},
    ],
}

CERTIFICATIONS = [
    {"label":"AWS Solutions Architect – Associate","vendor":"AWS",  "color":"#FF9900"},
    {"label":"AWS Developer – Associate",          "vendor":"AWS",  "color":"#FF9900"},
    {"label":"AWS SysOps Administrator – Associate","vendor":"AWS", "color":"#FF9900"},
    {"label":"Azure Fundamentals",                 "vendor":"Azure","color":"#00adef"},
    {"label":"Azure Administrator Associate",      "vendor":"Azure","color":"#00adef"},
    {"label":"Azure DevOps Engineer Expert",       "vendor":"Azure","color":"#00adef"},
    {"label":"Azure AI Engineer Associate",        "vendor":"Azure","color":"#00adef"},
]

STACK = [
    {"cat":"Cloud Platforms",          "icon":"☁", "items":["Amazon Web Services (AWS)","Microsoft Azure"]},
    {"cat":"Container & Orchestration","icon":"⎈", "items":["Kubernetes (EKS / AKS)","Docker","Helm","Karpenter Autoscaling"]},
    {"cat":"Infrastructure as Code",   "icon":"🔧","items":["Terraform","ArgoCD","GitOps Workflows","Helm Charts"]},
    {"cat":"CI/CD & Automation",       "icon":"🚀","items":["GitHub Actions (OIDC)","GitLab CI","Python Automation","Bash Scripting"]},
    {"cat":"Security & DevSecOps",     "icon":"🔒","items":["IAM & RBAC","SAST Scanning","Network Policies","DevSecOps Best Practices"]},
    {"cat":"Observability",            "icon":"📊","items":["Prometheus","Grafana","Centralised Logging","CloudWatch / Azure Monitor"]},
    {"cat":"AI & ML Infrastructure",   "icon":"🤖","items":["AWS SageMaker","Azure AI Services","AWS Bedrock","OpenAI API Integration"]},
    {"cat":"OS & Scripting",           "icon":"💻","items":["Linux (Ubuntu / RHEL)","Python","Bash / Shell","Scripting & Automation"]},
]

# ── PROJECTS ──────────────────────────────────────────────────────────────────
#   featured      → shown in homepage showcase slider
#   status        → "Production" | "In Development"
#   arch_id       → "eks" | "platform"  (keys in ARCH_MAP)
#   media_images  → filenames in docs/media/images/
#   media_videos  → filenames in docs/media/videos/
# ─────────────────────────────────────────────────────────────────────────────
PROJECTS = [
    {
        "id":"eks-cicd","featured":True,"status":"Production",
        "title":"Microservices EKS Terraform CI/CD Platform",
        "short":"Production-grade Kubernetes platform with GitOps CI/CD, OIDC auth and Karpenter — zero AWS keys in GitHub.",
        "summary":"A fully automated, secure CI/CD platform built on Amazon EKS using Terraform for infrastructure provisioning and GitHub Actions for pipeline orchestration. OIDC federation means no long-lived AWS credentials are stored in GitHub. On every commit, Docker images are built, tagged, and pushed to Amazon ECR; Helm values are updated and ArgoCD syncs the change to the cluster automatically.",
        "repo":"https://github.com/gprai/microservices-eks-terraform-cicd",
        "stack":["Terraform","Amazon EKS","Karpenter","GitHub Actions","Helm","ArgoCD","Docker","Amazon ECR"],
        "highlights":[
            "OIDC-based GitHub Actions → AWS auth — zero long-lived credentials stored in GitHub",
            "Karpenter node autoscaling for cost-efficient, right-sized EC2 provisioning",
            "Helm + ArgoCD GitOps — Git is the single source of truth for every deployment",
            "Multi-environment: dev / staging / production namespaces with promotion gates",
            "Private VPC, NAT gateway, security groups, pod-level IRSA roles",
            "Full pipeline: Docker build → ECR push → Helm commit → ArgoCD sync",
        ],
        "arch_id":"eks",
        "media_images":[],   # e.g. ["eks-screen1.png","eks-screen2.png"]
        "media_videos":[],   # e.g. ["eks-demo.mp4"]
    },
    {
        "id":"aws-platform","featured":True,"status":"In Development",
        "title":"AWS Platform Engineering — Multi-Account Landing Zone",
        "short":"Enterprise AWS multi-account landing zone with Control Tower, Organizations, Terraform & GitOps — automated governance at scale.",
        "summary":"Enterprise-grade AWS platform implementing a secure multi-account landing zone using AWS Control Tower and AWS Organizations. Terraform modules handle account vending, baseline networking, IAM, and security controls. GitHub Actions + GitOps drive all changes; centralised CloudTrail, AWS Config, Security Hub, and GuardDuty run across every account.",
        "repo":"https://github.com/gprai/aws-platform-engineering",
        "stack":["AWS Control Tower","AWS Organizations","Terraform","GitHub Actions","IAM Identity Center","SCPs","Security Hub","GuardDuty"],
        "highlights":[
            "Multi-account structure: Management / Log Archive / Audit / Workload accounts",
            "AWS Control Tower guardrails + automated account vending via Terraform modules",
            "Service Control Policies (SCPs) enforcing organisation-wide governance",
            "Centralised CloudTrail, AWS Config, Security Hub aggregator and GuardDuty (org)",
            "IAM Identity Center (SSO) with permission sets mapped to AD groups",
            "Transit Gateway for shared networking across all workload accounts",
        ],
        "arch_id":"platform",
        "media_images":[],
        "media_videos":[],
    },
]

UPCOMING = [
    {"title":"AWS Cost Optimisation Toolkit",      "desc":"Automated rightsizing & reserved instance recommendations via Lambda + Cost Explorer"},
    {"title":"Multi-Cloud Observability Stack",    "desc":"Unified Prometheus + Grafana + Loki spanning AWS and Azure workloads"},
    {"title":"LLM Infra on Bedrock + RAG Pipeline","desc":"Production RAG infrastructure with vector store, embedding pipeline and API gateway"},
    {"title":"Automated Compliance Scanning",      "desc":"CIS benchmark enforcement across EKS clusters using Falco + OPA Gatekeeper"},
]

SERVICES = [
    {"icon":"☁","title":"Cloud & Infrastructure",
     "items":["AWS & Azure Architecture","Terraform Infrastructure as Code","Cloud Migration & Optimisation","Networking & IAM Solutions"]},
    {"icon":"⎈","title":"Kubernetes & Platform Engineering",
     "items":["Amazon EKS & Azure AKS","Kubernetes Platform Engineering","Helm & ArgoCD GitOps","High Availability Design"]},
    {"icon":"🚀","title":"DevOps & Automation",
     "items":["CI/CD Pipelines","GitHub Actions & GitLab CI","Docker Containerisation","Infrastructure Automation"]},
    {"icon":"🔒","title":"DevSecOps & Monitoring",
     "items":["DevSecOps Best Practices","SAST Security Integration","Prometheus & Grafana","Observability & Logging"]},
    {"icon":"🤖","title":"AI & Automation",
     "items":["Python & Bash Automation","AWS SageMaker","Azure AI Services","OpenAI API Integrations"]},
    {"icon":"🧑‍💼","title":"Consulting",
     "items":["Platform Engineering Consulting","Cloud Cost Optimisation","Architecture Reviews","Technical Documentation"]},
]

# ═════════════════════════════════════════════════════════════════════════════
#  ARCHITECTURE SVGs  (light background so they're legible inside dark cards)
# ═════════════════════════════════════════════════════════════════════════════
def arch_eks() -> str:
    return """
<svg viewBox="0 0 900 400" xmlns="http://www.w3.org/2000/svg"
     style="width:100%;border-radius:8px;background:#f0f4fa;border:1px solid #c8d4e8">
  <defs>
    <marker id="ah" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#2563eb"/></marker>
    <marker id="ag" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#16a34a"/></marker>
    <marker id="ap" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#9333ea"/></marker>
    <marker id="ao" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#f97316"/></marker>
  </defs>
  <text x="16" y="18" font-family="sans-serif" font-size="10" font-weight="700" fill="#0f172a">EKS · GitHub Actions OIDC · ArgoCD GitOps Pipeline</text>
  <rect x="14" y="30" width="112" height="64" rx="7" fill="#dbeafe" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="70" y="52" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="700" fill="#1e40af">👨‍💻 Dev</text>
  <text x="70" y="66" text-anchor="middle" font-family="sans-serif" font-size="8" fill="#2563eb">git push</text>
  <text x="70" y="80" text-anchor="middle" font-family="sans-serif" font-size="8" fill="#2563eb">feature branch</text>
  <rect x="170" y="20" width="150" height="84" rx="7" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.5"/>
  <text x="245" y="40" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="700" fill="#166534">⚙ GitHub Actions</text>
  <text x="245" y="55" text-anchor="middle" font-family="sans-serif" font-size="8" fill="#15803d">OIDC → AssumeRole</text>
  <text x="245" y="68" text-anchor="middle" font-family="sans-serif" font-size="8" fill="#15803d">Docker build &amp; tag</text>
  <text x="245" y="81" text-anchor="middle" font-family="sans-serif" font-size="8" fill="#15803d">Push to ECR</text>
  <text x="245" y="97" text-anchor="middle" font-family="sans-serif" font-size="8" fill="#15803d">Update Helm values</text>
  <rect x="372" y="30" width="112" height="64" rx="7" fill="#fff7ed" stroke="#f97316" stroke-width="1.5"/>
  <text x="428" y="52" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="700" fill="#9a3412">📦 ECR</text>
  <text x="428" y="67" text-anchor="middle" font-family="sans-serif" font-size="8" fill="#ea580c">Container Registry</text>
  <text x="428" y="82" text-anchor="middle" font-family="sans-serif" font-size="8" fill="#ea580c">Image:sha-abc123</text>
  <rect x="170" y="152" width="150" height="58" rx="7" fill="#faf5ff" stroke="#9333ea" stroke-width="1.5"/>
  <text x="245" y="173" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="700" fill="#6b21a8">⎈ Helm Values</text>
  <text x="245" y="188" text-anchor="middle" font-family="sans-serif" font-size="8" fill="#9333ea">Git repo · image tag</text>
  <text x="245" y="203" text-anchor="middle" font-family="sans-serif" font-size="8" fill="#9333ea">environment configs</text>
  <rect x="372" y="152" width="112" height="58" rx="7" fill="#fff0f6" stroke="#db2777" stroke-width="1.5"/>
  <text x="428" y="173" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="700" fill="#9d174d">🔄 ArgoCD</text>
  <text x="428" y="188" text-anchor="middle" font-family="sans-serif" font-size="8" fill="#db2777">Poll for drift</text>
  <text x="428" y="203" text-anchor="middle" font-family="sans-serif" font-size="8" fill="#db2777">Sync to cluster</text>
  <rect x="528" y="14" width="354" height="376" rx="10" fill="#f1f5fb" stroke="#3b82f6" stroke-width="2" stroke-dasharray="6,3"/>
  <text x="705" y="32" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="700" fill="#1e40af">Amazon EKS Cluster</text>
  <rect x="544" y="42" width="130" height="48" rx="5" fill="#ecfdf5" stroke="#10b981" stroke-width="1.5"/>
  <text x="609" y="62" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="700" fill="#065f46">⚡ Karpenter</text>
  <text x="609" y="77" text-anchor="middle" font-family="sans-serif" font-size="8" fill="#059669">Node Autoscaling</text>
  <rect x="544" y="106" width="316" height="88" rx="5" fill="#eff6ff" stroke="#93c5fd"/>
  <text x="702" y="123" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="700" fill="#1e40af">Workload Namespaces</text>
  <rect x="554" y="130" width="82" height="52" rx="4" fill="#bfdbfe" stroke="#60a5fa"/>
  <text x="595" y="151" text-anchor="middle" font-family="sans-serif" font-size="8" font-weight="600" fill="#1e40af">dev</text>
  <text x="595" y="165" text-anchor="middle" font-family="sans-serif" font-size="7" fill="#2563eb">Pods · Svc · Ingress</text>
  <rect x="646" y="130" width="82" height="52" rx="4" fill="#bfdbfe" stroke="#60a5fa"/>
  <text x="687" y="151" text-anchor="middle" font-family="sans-serif" font-size="8" font-weight="600" fill="#1e40af">staging</text>
  <text x="687" y="165" text-anchor="middle" font-family="sans-serif" font-size="7" fill="#2563eb">Pods · Svc · Ingress</text>
  <rect x="738" y="130" width="104" height="52" rx="4" fill="#93c5fd" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="790" y="151" text-anchor="middle" font-family="sans-serif" font-size="8" font-weight="700" fill="#1e3a8a">production</text>
  <text x="790" y="165" text-anchor="middle" font-family="sans-serif" font-size="7" fill="#1e3a8a">Pods · HPA · PDB</text>
  <rect x="544" y="210" width="316" height="58" rx="5" fill="#fefce8" stroke="#eab308"/>
  <text x="702" y="228" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="700" fill="#713f12">VPC — Private Subnets</text>
  <text x="612" y="248" text-anchor="middle" font-family="sans-serif" font-size="8" fill="#854d0e">NAT Gateway</text>
  <text x="702" y="248" text-anchor="middle" font-family="sans-serif" font-size="8" fill="#854d0e">Security Groups</text>
  <text x="804" y="248" text-anchor="middle" font-family="sans-serif" font-size="8" fill="#854d0e">ALB Ingress</text>
  <rect x="544" y="284" width="316" height="50" rx="5" fill="#fff1f2" stroke="#f43f5e"/>
  <text x="702" y="304" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="700" fill="#9f1239">IAM + OIDC Identity Provider</text>
  <text x="702" y="322" text-anchor="middle" font-family="sans-serif" font-size="8" fill="#e11d48">IRSA · AssumeRoleWithWebIdentity · Pod-level roles</text>
  <rect x="544" y="350" width="152" height="18" rx="4" fill="#f0fdf4" stroke="#10b981"/>
  <text x="620" y="363" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#166534">Prometheus · Grafana · Alerts</text>
  <rect x="706" y="350" width="152" height="18" rx="4" fill="#faf5ff" stroke="#9333ea"/>
  <text x="782" y="363" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#6b21a8">CloudWatch · Container Insights</text>
  <line x1="126" y1="62" x2="168" y2="62" stroke="#16a34a" stroke-width="1.5" marker-end="url(#ag)"/>
  <line x1="320" y1="62" x2="370" y2="62" stroke="#f97316" stroke-width="1.5" marker-end="url(#ao)"/>
  <line x1="245" y1="104" x2="245" y2="150" stroke="#9333ea" stroke-width="1.5" marker-end="url(#ap)"/>
  <line x1="320" y1="181" x2="370" y2="181" stroke="#2563eb" stroke-width="1.5" marker-end="url(#ah)"/>
  <line x1="484" y1="181" x2="526" y2="155" stroke="#db2777" stroke-width="1.5" marker-end="url(#ah)"/>
  <line x1="428" y1="94" x2="542" y2="150" stroke="#f97316" stroke-width="1.4" stroke-dasharray="5,3" marker-end="url(#ao)"/>
</svg>"""

def arch_platform() -> str:
    return """
<svg viewBox="0 0 900 470" xmlns="http://www.w3.org/2000/svg"
     style="width:100%;border-radius:8px;background:#f0f4fa;border:1px solid #c8d4e8">
  <defs>
    <marker id="bh" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#2563eb"/></marker>
    <marker id="bg" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#f97316"/></marker>
    <marker id="bv" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#9333ea"/></marker>
  </defs>
  <text x="16" y="18" font-family="sans-serif" font-size="10" font-weight="700" fill="#0f172a">AWS Multi-Account Landing Zone — Control Tower + Organizations + Terraform GitOps</text>
  <rect x="14" y="28" width="870" height="432" rx="11" fill="none" stroke="#f97316" stroke-width="2" stroke-dasharray="8,4"/>
  <text x="30" y="46" font-family="sans-serif" font-size="9" font-weight="700" fill="#c2410c">AWS Organizations (Root)</text>
  <rect x="28" y="52" width="148" height="90" rx="7" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.5"/>
  <text x="102" y="71" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="700" fill="#166534">⚙ Terraform</text>
  <text x="102" y="86" text-anchor="middle" font-family="sans-serif" font-size="8" fill="#16a34a">GitHub Actions CI</text>
  <text x="102" y="99" text-anchor="middle" font-family="sans-serif" font-size="8" fill="#16a34a">GitOps · IaC Modules</text>
  <text x="102" y="112" text-anchor="middle" font-family="sans-serif" font-size="8" fill="#16a34a">Account Vending</text>
  <text x="102" y="131" text-anchor="middle" font-family="sans-serif" font-size="8" fill="#16a34a">Baseline Deployment</text>
  <rect x="348" y="52" width="200" height="90" rx="7" fill="#fff7ed" stroke="#f97316" stroke-width="2"/>
  <text x="448" y="71" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="700" fill="#9a3412">Management Account</text>
  <text x="448" y="87" text-anchor="middle" font-family="sans-serif" font-size="8" fill="#c2410c">AWS Control Tower</text>
  <text x="448" y="100" text-anchor="middle" font-family="sans-serif" font-size="8" fill="#c2410c">Account Vending · Guardrails</text>
  <text x="448" y="113" text-anchor="middle" font-family="sans-serif" font-size="8" fill="#c2410c">SCPs · Consolidated Billing</text>
  <text x="448" y="131" text-anchor="middle" font-family="sans-serif" font-size="8" fill="#c2410c">IAM Identity Center (SSO)</text>
  <line x1="176" y1="97" x2="346" y2="97" stroke="#16a34a" stroke-width="1.5" marker-end="url(#bh)"/>
  <rect x="28" y="182" width="238" height="118" rx="7" fill="#fff1f2" stroke="#f43f5e" stroke-width="1.5"/>
  <text x="147" y="200" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="700" fill="#9f1239">Security OU</text>
  <rect x="38" y="208" width="102" height="80" rx="5" fill="#fee2e2" stroke="#f87171"/>
  <text x="89" y="227" text-anchor="middle" font-family="sans-serif" font-size="8" font-weight="700" fill="#991b1b">Log Archive</text>
  <text x="89" y="242" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#b91c1c">CloudTrail (org)</text>
  <text x="89" y="255" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#b91c1c">S3 Access Logs</text>
  <text x="89" y="268" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#b91c1c">Config Snapshots</text>
  <text x="89" y="281" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#b91c1c">Glacier Archive</text>
  <rect x="150" y="208" width="106" height="80" rx="5" fill="#fee2e2" stroke="#f87171"/>
  <text x="203" y="227" text-anchor="middle" font-family="sans-serif" font-size="8" font-weight="700" fill="#991b1b">Audit Account</text>
  <text x="203" y="242" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#b91c1c">Security Hub</text>
  <text x="203" y="255" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#b91c1c">GuardDuty</text>
  <text x="203" y="268" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#b91c1c">AWS Config</text>
  <text x="203" y="281" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#b91c1c">Inspector v2</text>
  <rect x="280" y="182" width="600" height="118" rx="7" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="580" y="200" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="700" fill="#1e40af">Workloads OU</text>
  <rect x="290" y="208" width="174" height="80" rx="5" fill="#dbeafe" stroke="#60a5fa"/>
  <text x="377" y="227" text-anchor="middle" font-family="sans-serif" font-size="8" font-weight="700" fill="#1e40af">Dev Account</text>
  <text x="377" y="242" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#2563eb">VPC · Private Subnets</text>
  <text x="377" y="255" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#2563eb">EKS Dev Cluster</text>
  <text x="377" y="268" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#2563eb">IAM Roles · SCPs</text>
  <text x="377" y="281" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#2563eb">Cost Allocation Tags</text>
  <rect x="474" y="208" width="174" height="80" rx="5" fill="#dbeafe" stroke="#60a5fa"/>
  <text x="561" y="227" text-anchor="middle" font-family="sans-serif" font-size="8" font-weight="700" fill="#1e40af">Staging Account</text>
  <text x="561" y="242" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#2563eb">VPC · Private Subnets</text>
  <text x="561" y="255" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#2563eb">EKS Staging</text>
  <text x="561" y="268" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#2563eb">IAM Roles · SCPs</text>
  <text x="561" y="281" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#2563eb">Integration Tests</text>
  <rect x="658" y="208" width="212" height="80" rx="5" fill="#bfdbfe" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="764" y="227" text-anchor="middle" font-family="sans-serif" font-size="8" font-weight="700" fill="#1e3a8a">Production Account</text>
  <text x="764" y="242" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#1e40af">VPC · Private Subnets</text>
  <text x="764" y="255" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#1e40af">EKS Prod · Multi-AZ</text>
  <text x="764" y="268" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#1e40af">IAM Roles · SCPs · WAF</text>
  <text x="764" y="281" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#1e40af">Backups · DR Policy</text>
  <rect x="28" y="320" width="560" height="128" rx="7" fill="#faf5ff" stroke="#9333ea" stroke-width="1.5"/>
  <text x="308" y="338" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="700" fill="#6b21a8">Shared Services OU</text>
  <rect x="38" y="346" width="126" height="90" rx="5" fill="#ede9fe" stroke="#a78bfa"/>
  <text x="101" y="365" text-anchor="middle" font-family="sans-serif" font-size="8" font-weight="700" fill="#5b21b6">Networking</text>
  <text x="101" y="380" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#7c3aed">Transit Gateway</text>
  <text x="101" y="393" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#7c3aed">Route53 · DNS</text>
  <text x="101" y="406" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#7c3aed">VPC Peering</text>
  <text x="101" y="419" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#7c3aed">Direct Connect</text>
  <rect x="174" y="346" width="126" height="90" rx="5" fill="#ede9fe" stroke="#a78bfa"/>
  <text x="237" y="365" text-anchor="middle" font-family="sans-serif" font-size="8" font-weight="700" fill="#5b21b6">Identity (SSO)</text>
  <text x="237" y="380" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#7c3aed">IAM Identity Center</text>
  <text x="237" y="393" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#7c3aed">Permission Sets</text>
  <text x="237" y="406" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#7c3aed">AD Integration</text>
  <text x="237" y="419" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#7c3aed">MFA Enforcement</text>
  <rect x="310" y="346" width="126" height="90" rx="5" fill="#ede9fe" stroke="#a78bfa"/>
  <text x="373" y="365" text-anchor="middle" font-family="sans-serif" font-size="8" font-weight="700" fill="#5b21b6">DevOps Tooling</text>
  <text x="373" y="380" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#7c3aed">CodeArtifact</text>
  <text x="373" y="393" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#7c3aed">ECR (shared)</text>
  <text x="373" y="406" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#7c3aed">S3 Artifacts</text>
  <text x="373" y="419" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#7c3aed">Secrets Manager</text>
  <rect x="446" y="346" width="130" height="90" rx="5" fill="#ede9fe" stroke="#a78bfa"/>
  <text x="511" y="365" text-anchor="middle" font-family="sans-serif" font-size="8" font-weight="700" fill="#5b21b6">Observability</text>
  <text x="511" y="380" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#7c3aed">CloudWatch (org)</text>
  <text x="511" y="393" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#7c3aed">Security Hub agg.</text>
  <text x="511" y="406" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#7c3aed">GuardDuty (org)</text>
  <text x="511" y="419" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#7c3aed">Config Aggregator</text>
  <rect x="602" y="320" width="272" height="128" rx="7" fill="#fefce8" stroke="#eab308" stroke-width="1.5"/>
  <text x="738" y="338" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="700" fill="#713f12">Governance Layer</text>
  <text x="738" y="355" text-anchor="middle" font-family="sans-serif" font-size="8" fill="#854d0e">Service Control Policies (SCPs)</text>
  <text x="738" y="370" text-anchor="middle" font-family="sans-serif" font-size="8" fill="#854d0e">AWS Config + Conformance Packs</text>
  <text x="738" y="385" text-anchor="middle" font-family="sans-serif" font-size="8" fill="#854d0e">CloudTrail (org-wide, immutable)</text>
  <text x="738" y="400" text-anchor="middle" font-family="sans-serif" font-size="8" fill="#854d0e">Security Hub Aggregator</text>
  <text x="738" y="415" text-anchor="middle" font-family="sans-serif" font-size="8" fill="#854d0e">GuardDuty (org-wide)</text>
  <text x="738" y="430" text-anchor="middle" font-family="sans-serif" font-size="8" fill="#854d0e">AWS Budgets + Cost Explorer</text>
  <line x1="448" y1="142" x2="178" y2="180" stroke="#f97316" stroke-width="1.4" marker-end="url(#bg)"/>
  <line x1="448" y1="142" x2="460" y2="180" stroke="#f97316" stroke-width="1.4" marker-end="url(#bg)"/>
  <line x1="448" y1="142" x2="308" y2="318" stroke="#9333ea" stroke-width="1.3" stroke-dasharray="5,3" marker-end="url(#bv)"/>
  <line x1="448" y1="142" x2="720" y2="318" stroke="#eab308" stroke-width="1.3" stroke-dasharray="5,3" marker-end="url(#bh)"/>
</svg>"""

ARCH_MAP = {"eks": arch_eks, "platform": arch_platform}

# ═════════════════════════════════════════════════════════════════════════════
#  CSS  — Dark navy theme matching the live site screenshot
# ═════════════════════════════════════════════════════════════════════════════
def css() -> str:
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@300;400;500&display=swap');

*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}

:root{
  /* ── exact palette from the screenshot ── */
  --bg:       #0a1628;
  --bg2:      #0d1e35;
  --surface:  #112240;
  --surface2: #162d4e;
  --border:   #1e3a5f;
  --border2:  #264d7a;
  --cyan:     #00e5ff;
  --cyan2:    #00b4cc;
  --aws:      #FF9900;
  --azure:    #00adef;
  --violet:   #7c5cbf;
  --green:    #00c896;
  --text:     #e2eaf5;
  --sub:      #a8bdd4;
  --muted:    #6b8aaa;
  --light:    #3d5a7a;
  --head:     'Outfit',sans-serif;
  --mono:     'JetBrains Mono',monospace;
  --r:        10px;
  --glow:     0 0 20px rgba(0,229,255,.12);
  --sh:       0 2px 12px rgba(0,0,0,.35);
  --sh2:      0 8px 32px rgba(0,0,0,.5),0 0 0 1px var(--border);
}

html{scroll-behavior:smooth}
body{
  background:var(--bg);
  color:var(--text);
  font-family:var(--head);
  font-size:15px;
  line-height:1.65;
  overflow-x:hidden;
}

/* ── grid bg ── */
body::after{
  content:'';position:fixed;inset:0;z-index:-1;pointer-events:none;
  background-image:
    linear-gradient(rgba(0,229,255,.04) 1px,transparent 1px),
    linear-gradient(90deg,rgba(0,229,255,.04) 1px,transparent 1px);
  background-size:48px 48px;
}

/* ── subtle glow top-right ── */
body::before{
  content:'';position:fixed;top:-20%;right:-10%;z-index:-1;
  width:600px;height:600px;
  background:radial-gradient(circle,rgba(0,80,160,.18),transparent 70%);
  pointer-events:none;
}

/* ─────── NAV ─────── */
nav{
  position:fixed;top:0;left:0;right:0;z-index:300;
  display:flex;align-items:center;justify-content:space-between;gap:1rem;
  padding:0 clamp(1.2rem,4vw,4rem);height:58px;
  background:rgba(10,22,40,.92);
  backdrop-filter:blur(20px);
  border-bottom:1px solid var(--border);
}
.nav-logo{
  font-family:var(--head);font-weight:900;font-size:1.2rem;
  color:var(--cyan);text-decoration:none;letter-spacing:-.04em;
}
.nav-logo span{color:var(--muted)}
.nav-links{display:flex;gap:0;list-style:none}
.nav-links a{
  color:var(--muted);text-decoration:none;font-size:.82rem;font-weight:500;
  padding:.35rem .9rem;border-radius:6px;transition:all .18s;letter-spacing:.01em;
  text-transform:uppercase;font-size:.72rem;letter-spacing:.1em;
}
.nav-links a:hover,.nav-links a.active{color:var(--cyan);background:rgba(0,229,255,.06)}
.nav-book{
  display:inline-flex;align-items:center;gap:.35rem;
  padding:.38rem 1.1rem;font-family:var(--head);font-size:.75rem;font-weight:700;
  background:transparent;color:var(--cyan);
  border:1.5px solid var(--cyan);border-radius:6px;cursor:pointer;
  letter-spacing:.06em;text-transform:uppercase;
  transition:all .18s;white-space:nowrap;
}
.nav-book:hover{background:rgba(0,229,255,.1);box-shadow:0 0 16px rgba(0,229,255,.2)}

main{padding-top:58px}

/* ─────── LAYOUT ─────── */
.section{padding:clamp(2.5rem,6vw,5rem) clamp(1.2rem,5vw,4rem);max-width:1200px;margin:0 auto}
.sec-label{
  font-family:var(--mono);font-size:.62rem;letter-spacing:.24em;text-transform:uppercase;
  color:var(--cyan);margin-bottom:.75rem;
  display:flex;align-items:center;gap:.6rem;
}
.sec-label::after{content:'';height:1px;width:36px;background:var(--cyan);opacity:.4}
h1,h2,h3,h4{font-family:var(--head)}

/* ─────── DIVIDER ─────── */
hr.div{border:none;border-top:1px solid var(--border);margin:0}

/* ─────── BUTTONS ─────── */
.btn{
  display:inline-flex;align-items:center;gap:.4rem;
  padding:.55rem 1.4rem;font-family:var(--head);font-size:.82rem;font-weight:600;
  text-decoration:none;border-radius:7px;transition:all .18s;cursor:pointer;border:none;white-space:nowrap;
}
.btn-p{
  background:transparent;color:var(--cyan);
  border:1.5px solid var(--cyan);
  letter-spacing:.04em;
}
.btn-p:hover{background:rgba(0,229,255,.1);box-shadow:0 0 18px rgba(0,229,255,.22);transform:translateY(-1px)}
.btn-v{background:rgba(124,92,191,.22);color:#c4a8ff;border:1.5px solid var(--violet)}
.btn-v:hover{background:rgba(124,92,191,.35);transform:translateY(-1px)}
.btn-o{background:var(--surface);color:var(--sub);border:1px solid var(--border2)}
.btn-o:hover{border-color:var(--cyan);color:var(--cyan);transform:translateY(-1px)}
.btn-aws{background:rgba(255,153,0,.12);color:var(--aws);border:1px solid rgba(255,153,0,.3)}
.btn-aws:hover{background:rgba(255,153,0,.22);transform:translateY(-1px)}

/* ─────── HERO ─────── */
.hero{
  display:grid;grid-template-columns:1fr 400px;gap:3rem;align-items:center;
  padding:clamp(2rem,6vw,5rem) clamp(1.2rem,5vw,4rem);
  max-width:1200px;margin:0 auto;min-height:calc(100vh - 58px);
}
.eyebrow{
  display:inline-flex;align-items:center;gap:.5rem;
  font-family:var(--mono);font-size:.65rem;letter-spacing:.16em;text-transform:uppercase;
  color:var(--cyan);background:rgba(0,229,255,.07);border:1px solid rgba(0,229,255,.2);
  padding:.3rem .9rem;border-radius:20px;margin-bottom:1.2rem;
}
.hero h1{
  font-size:clamp(2.8rem,6vw,4.6rem);font-weight:900;line-height:1.04;
  letter-spacing:-.04em;color:var(--text);margin-bottom:1.1rem;
}
.hero h1 em{
  font-style:normal;
  -webkit-text-stroke:2px var(--cyan);
  color:transparent;
}
.hero-sub{font-size:.96rem;color:var(--sub);max-width:460px;line-height:1.85;margin-bottom:2rem}
.hero-sub strong{color:var(--cyan)}
.hero-cta{display:flex;gap:.75rem;flex-wrap:wrap;margin-bottom:2.2rem}
.hero-stats{display:flex;gap:2rem;flex-wrap:wrap}
.stat-n{font-family:var(--head);font-size:1.6rem;font-weight:900;color:var(--text);line-height:1}
.stat-n span{color:var(--cyan)}
.stat-l{font-family:var(--mono);font-size:.6rem;color:var(--muted);margin-top:.18rem;letter-spacing:.06em;text-transform:uppercase}

/* ─────── HERO PANEL ─────── */
.hero-panel{
  background:var(--surface);border:1px solid var(--border2);border-radius:14px;
  padding:1.4rem;position:relative;overflow:hidden;
  box-shadow:var(--sh2),var(--glow);
}
.hero-panel::before{
  content:'';position:absolute;top:-50px;right:-50px;
  width:180px;height:180px;
  background:radial-gradient(circle,rgba(0,229,255,.1),transparent 70%);
  pointer-events:none;
}
.panel-label{
  font-family:var(--mono);font-size:.58rem;letter-spacing:.2em;text-transform:uppercase;
  color:var(--muted);margin-bottom:.55rem;
}
.tech-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:.4rem;margin-bottom:1rem}
.tech-chip{
  display:flex;align-items:center;gap:.3rem;
  background:var(--bg2);border:1px solid var(--border);border-radius:6px;
  padding:.38rem .45rem;font-family:var(--mono);font-size:.62rem;color:var(--sub);
  transition:all .16s;
}
.tech-chip:hover{border-color:var(--cyan);color:var(--cyan);background:rgba(0,229,255,.05)}
.tech-chip .dot{width:6px;height:6px;border-radius:50%;flex-shrink:0}
.pipeline{display:flex;align-items:center;gap:0;overflow-x:auto}
.pipe-step{
  flex:1;min-width:0;text-align:center;padding:.45rem .2rem;
  background:var(--bg2);border:1px solid var(--border);font-size:.6rem;font-weight:600;
  color:var(--sub);font-family:var(--mono);line-height:1.3;
}
.pipe-step:first-child{border-radius:6px 0 0 6px}
.pipe-step:last-child{border-radius:0 6px 6px 0}
.pipe-step .icon{font-size:.85rem;display:block;margin-bottom:.12rem}
.pipe-arrow{color:var(--cyan);font-size:.7rem;flex-shrink:0}

/* ─────── CERT STRIP ─────── */
.cert-strip{display:flex;flex-wrap:wrap;gap:.5rem}
.cert{
  display:flex;align-items:center;gap:.4rem;padding:.32rem .9rem;
  border-radius:20px;font-size:.72rem;font-weight:500;border:1px solid;
  background:var(--surface);transition:transform .14s,box-shadow .14s;
}
.cert:hover{transform:translateY(-2px);box-shadow:var(--glow)}

/* ─────── ABOUT ─────── */
.about-grid{display:grid;grid-template-columns:3fr 2fr;gap:3rem;align-items:start}
.about-text p{font-size:.9rem;color:var(--sub);line-height:1.9;margin-bottom:1rem}
.focus-wrap{display:flex;flex-wrap:wrap;gap:.4rem;margin-top:1rem}
.focus-tag{
  font-family:var(--mono);font-size:.65rem;padding:.28rem .75rem;
  background:rgba(0,229,255,.07);border:1px solid rgba(0,229,255,.2);
  color:var(--cyan);border-radius:20px;
}
.skill-bars{display:flex;flex-direction:column;gap:.65rem}
.skill-row{display:flex;flex-direction:column;gap:.22rem}
.skill-top{display:flex;justify-content:space-between;font-family:var(--mono);font-size:.68rem;color:var(--sub)}
.skill-bar{height:4px;background:var(--border);border-radius:3px;overflow:hidden}
.skill-fill{height:100%;border-radius:3px;background:linear-gradient(90deg,var(--cyan),var(--violet))}

/* ─────── VIDEO SHOWCASE ─────── */
.showcase{
  background:var(--bg2);border-top:1px solid var(--border);border-bottom:1px solid var(--border);
  padding:clamp(2.5rem,5vw,4.5rem) clamp(1.2rem,5vw,4rem);
}
.showcase-inner{max-width:1200px;margin:0 auto}
.slides-wrap{position:relative;overflow:hidden;border-radius:14px}
.slides{display:flex;transition:transform .55s cubic-bezier(.4,0,.2,1)}
.slide{
  min-width:100%;background:var(--surface);border:1px solid var(--border2);
  border-radius:14px;padding:2.5rem;
  display:grid;grid-template-columns:1fr 1fr;gap:2.5rem;align-items:center;
  box-shadow:var(--sh2),var(--glow);
}
.slide-label{
  font-family:var(--mono);font-size:.6rem;letter-spacing:.2em;text-transform:uppercase;
  color:var(--cyan);margin-bottom:.6rem;
}
.slide h3{font-size:1.3rem;font-weight:800;letter-spacing:-.025em;color:var(--text);margin-bottom:.6rem}
.slide p{font-size:.85rem;color:var(--sub);line-height:1.8;margin-bottom:1rem}
.slide-tags{display:flex;flex-wrap:wrap;gap:.35rem;margin-bottom:1rem}
.slide-screen{
  background:var(--bg2);border:1px solid var(--border);border-radius:10px;
  aspect-ratio:16/9;display:flex;align-items:center;justify-content:center;
  font-size:2.5rem;position:relative;overflow:hidden;
}
.slide-screen-inner{text-align:center}
.slide-screen-label{font-family:var(--mono);font-size:.7rem;color:var(--muted);margin-top:.5rem;display:block}
/* animated blinking dot on "live" badge */
.live-dot{
  display:inline-block;width:7px;height:7px;border-radius:50%;background:#00c896;
  margin-right:.35rem;animation:pulse-green 1.5s ease-in-out infinite;
}
@keyframes pulse-green{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.5;transform:scale(.7)}}
.slide-status{
  display:inline-flex;align-items:center;
  font-family:var(--mono);font-size:.62rem;letter-spacing:.1em;text-transform:uppercase;
  padding:.2rem .65rem;border-radius:20px;margin-bottom:.6rem;
}
.s-prod{background:rgba(0,200,150,.1);color:#00c896;border:1px solid rgba(0,200,150,.25)}
.s-dev{ background:rgba(255,153,0,.1);color:var(--aws);border:1px solid rgba(255,153,0,.25)}
/* slider controls */
.slide-controls{display:flex;align-items:center;justify-content:center;gap:1rem;margin-top:1.2rem}
.slide-dot{
  width:8px;height:8px;border-radius:50%;background:var(--border2);
  border:none;cursor:pointer;transition:all .2s;padding:0;
}
.slide-dot.active{background:var(--cyan);box-shadow:0 0 8px rgba(0,229,255,.5)}
.slide-nav{
  background:var(--surface);border:1px solid var(--border2);color:var(--sub);
  border-radius:6px;padding:.3rem .7rem;cursor:pointer;font-size:.9rem;
  transition:all .18s;
}
.slide-nav:hover{border-color:var(--cyan);color:var(--cyan)}

/* upcoming cards (inside showcase) */
.upcoming-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:.7rem;margin-top:1.4rem}
.upcoming-card{
  background:var(--surface);border:1px solid var(--border);border-radius:10px;
  padding:1.1rem;transition:all .18s;
}
.upcoming-card:hover{border-color:var(--cyan);box-shadow:var(--glow)}
.uc-badge{
  font-family:var(--mono);font-size:.57rem;letter-spacing:.14em;text-transform:uppercase;
  color:var(--aws);background:rgba(255,153,0,.08);border:1px solid rgba(255,153,0,.2);
  padding:.16rem .5rem;border-radius:10px;display:inline-block;margin-bottom:.55rem;
}
.uc-title{font-size:.88rem;font-weight:700;color:var(--text);margin-bottom:.3rem}
.uc-desc{font-size:.75rem;color:var(--muted);line-height:1.65}

/* ─────── FEATURED CARDS (home) ─────── */
.feat-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:1rem}
.feat-card{
  background:var(--surface);border:1px solid var(--border);border-radius:12px;
  padding:1.5rem;transition:all .2s;position:relative;overflow:hidden;
}
.feat-card::before{
  content:'';position:absolute;left:0;top:0;bottom:0;width:2px;
  background:linear-gradient(to bottom,var(--cyan),var(--violet));
  transform:scaleY(0);transform-origin:bottom;transition:transform .28s;
}
.feat-card:hover{border-color:var(--border2);box-shadow:var(--sh2),var(--glow);transform:translateY(-2px)}
.feat-card:hover::before{transform:scaleY(1)}
.feat-badge{
  display:inline-block;font-family:var(--mono);font-size:.58rem;
  letter-spacing:.14em;text-transform:uppercase;padding:.18rem .65rem;
  border-radius:20px;margin-bottom:.7rem;
}
.b-prod{background:rgba(0,200,150,.08);color:#00c896;border:1px solid rgba(0,200,150,.22)}
.b-dev {background:rgba(255,153,0,.08);color:var(--aws);border:1px solid rgba(255,153,0,.22)}
.feat-card h3{font-size:1rem;font-weight:700;letter-spacing:-.018em;color:var(--text);margin-bottom:.5rem}
.feat-card p{font-size:.8rem;color:var(--sub);line-height:1.72;margin-bottom:.9rem}
.feat-tags{display:flex;flex-wrap:wrap;gap:.3rem;margin-bottom:.9rem}
.tag{font-family:var(--mono);font-size:.6rem;padding:.18rem .5rem;border:1px solid var(--border2);color:var(--muted);border-radius:5px;background:var(--bg2)}

/* ─────── STACK PAGE ─────── */
.stack-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:.85rem}
.stack-card{
  background:var(--surface);border:1px solid var(--border);border-radius:12px;
  padding:1.4rem;transition:all .2s;
}
.stack-card:hover{border-color:var(--border2);box-shadow:var(--sh2),var(--glow);transform:translateY(-2px)}
.stack-head{display:flex;align-items:center;gap:.55rem;margin-bottom:.9rem}
.stack-icon{
  width:34px;height:34px;background:rgba(0,229,255,.08);border:1px solid rgba(0,229,255,.18);
  border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:1.1rem;flex-shrink:0;
}
.stack-head h3{font-family:var(--mono);font-size:.68rem;font-weight:500;letter-spacing:.12em;text-transform:uppercase;color:var(--cyan)}
.stack-card ul{list-style:none}
.stack-card li{
  font-size:.82rem;color:var(--sub);padding:.26rem 0;
  border-bottom:1px solid var(--border);display:flex;align-items:center;gap:.45rem;
}
.stack-card li:last-child{border-bottom:none}
.stack-card li::before{content:'›';color:var(--cyan);flex-shrink:0;font-size:.9rem}

/* ─────── SERVICES PAGE ─────── */
.svc-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:.9rem}
.svc-card{
  background:var(--surface);border:1px solid var(--border);border-radius:12px;
  padding:1.6rem;transition:all .2s;
}
.svc-card:hover{border-color:var(--border2);box-shadow:var(--sh2),var(--glow);transform:translateY(-2px)}
.svc-icon-wrap{
  width:42px;height:42px;background:rgba(0,229,255,.08);border:1px solid rgba(0,229,255,.18);
  border-radius:10px;display:flex;align-items:center;justify-content:center;
  font-size:1.25rem;margin-bottom:.9rem;
}
.svc-card h3{font-size:1rem;font-weight:700;color:var(--text);margin-bottom:.8rem}
.svc-card ul{list-style:none}
.svc-card li{
  font-size:.82rem;color:var(--sub);padding:.26rem 0;
  border-bottom:1px solid var(--border);display:flex;align-items:center;gap:.45rem;
}
.svc-card li:last-child{border-bottom:none}
.svc-card li::before{content:'–';color:var(--cyan);flex-shrink:0}

/* ─────── CONTACT PAGE ─────── */
.contact-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:.85rem;margin-bottom:2rem}
.contact-card{
  background:var(--surface);border:1px solid var(--border);border-radius:12px;
  padding:1.5rem;text-decoration:none;color:inherit;transition:all .2s;display:block;
}
.contact-card:hover{border-color:var(--cyan);box-shadow:var(--glow);transform:translateY(-2px)}
.cc-type{font-family:var(--mono);font-size:.6rem;letter-spacing:.18em;text-transform:uppercase;color:var(--cyan);margin-bottom:.45rem}
.cc-val{font-size:.88rem;font-weight:600;color:var(--text)}

/* ─────── PROJECTS PAGE ─────── */
.proj-card{
  background:var(--surface);border:1px solid var(--border);border-radius:14px;
  padding:2.2rem;margin-bottom:1.5rem;box-shadow:var(--sh);transition:box-shadow .2s;
}
.proj-card:hover{box-shadow:var(--sh2),var(--glow)}
.proj-card h2{font-size:1.4rem;font-weight:800;letter-spacing:-.025em;color:var(--text);margin-bottom:.65rem}
.proj-summary{font-size:.88rem;color:var(--sub);line-height:1.85;margin-bottom:1.2rem}
.proj-hl{list-style:none;margin-bottom:1.2rem}
.proj-hl li{
  font-size:.83rem;color:var(--sub);padding:.28rem 0;
  border-bottom:1px solid var(--border);display:flex;gap:.5rem;align-items:flex-start;
}
.proj-hl li:last-child{border-bottom:none}
.proj-hl li::before{content:'◆';color:var(--cyan);font-size:.44rem;margin-top:.46rem;flex-shrink:0}
.arch-box{
  margin-top:1.4rem;padding:1.2rem;
  background:var(--bg2);border:1px solid var(--border);border-radius:10px;
}
.arch-box h4{font-family:var(--mono);font-size:.65rem;font-weight:500;letter-spacing:.16em;text-transform:uppercase;color:var(--cyan);margin-bottom:.4rem}
.arch-box p{font-size:.78rem;color:var(--muted);margin-bottom:.8rem;line-height:1.6}
.media-box{
  margin-top:1.1rem;padding:1.2rem;
  background:var(--bg2);border:1px solid var(--border);border-radius:10px;
}
.media-box h4{font-family:var(--mono);font-size:.65rem;font-weight:500;letter-spacing:.16em;text-transform:uppercase;color:var(--violet);margin-bottom:.75rem}
.media-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:.65rem}
.media-img{width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:7px;border:1px solid var(--border)}
.media-video{width:100%;border-radius:7px;border:1px solid var(--border)}
.media-empty{
  border:1.5px dashed var(--border2);border-radius:8px;padding:1.4rem;
  text-align:center;font-family:var(--mono);font-size:.7rem;color:var(--muted);line-height:1.85;
}
.media-empty code{color:var(--cyan);background:rgba(0,229,255,.06);padding:.1rem .35rem;border-radius:4px}

/* ─────── PAGE HERO ─────── */
.page-hero{
  padding:3.5rem clamp(1.2rem,5vw,4rem) 2.2rem;
  max-width:1200px;margin:0 auto;border-bottom:1px solid var(--border);
}
.page-hero h1{font-size:clamp(2rem,4.2vw,3rem);font-weight:900;letter-spacing:-.035em;color:var(--text)}
.page-hero p{color:var(--sub);margin-top:.5rem;max-width:500px;font-size:.9rem}

/* ─────── CALENDLY MODAL ─────── */
.cal-overlay{
  display:none;position:fixed;inset:0;z-index:500;
  background:rgba(0,0,0,.7);backdrop-filter:blur(10px);
  align-items:center;justify-content:center;padding:1rem;
}
.cal-overlay.open{display:flex}
.cal-modal{
  background:var(--surface);border:1px solid var(--border2);border-radius:16px;
  width:100%;max-width:700px;max-height:90vh;overflow:hidden;
  box-shadow:0 32px 80px rgba(0,0,0,.7),0 0 0 1px var(--border2),var(--glow);
  position:relative;display:flex;flex-direction:column;
  animation:slideUp .22s ease;
}
@keyframes slideUp{from{transform:translateY(16px);opacity:0}to{transform:translateY(0);opacity:1}}
.cal-header{
  display:flex;align-items:center;justify-content:space-between;
  padding:1.2rem 1.5rem;border-bottom:1px solid var(--border);
  background:var(--bg2);flex-shrink:0;
}
.cal-header h2{font-size:1rem;font-weight:800;color:var(--text)}
.cal-header p{font-size:.78rem;color:var(--muted);margin-top:.15rem}
.cal-close{background:none;border:none;cursor:pointer;font-size:1.3rem;color:var(--muted);transition:color .16s}
.cal-close:hover{color:var(--cyan)}
.cal-body{flex:1;min-height:480px;position:relative}
.cal-body iframe{width:100%;height:100%;min-height:480px;border:none;background:#fff}
.cal-loading{
  position:absolute;inset:0;display:flex;flex-direction:column;
  align-items:center;justify-content:center;gap:1rem;font-size:.85rem;color:var(--muted);
  background:var(--surface);
}
.spinner{width:26px;height:26px;border:2.5px solid var(--border2);border-top-color:var(--cyan);border-radius:50%;animation:spin .6s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}

/* ─────── FOOTER ─────── */
footer{
  background:var(--bg2);border-top:1px solid var(--border);
  padding:1.6rem clamp(1.2rem,5vw,4rem);
  display:flex;justify-content:space-between;align-items:center;
  flex-wrap:wrap;gap:.75rem;font-size:.76rem;color:var(--muted);margin-top:3rem;
}
footer a{color:var(--muted);text-decoration:none;transition:color .16s}
footer a:hover{color:var(--cyan)}

@media(max-width:860px){
  .hero{grid-template-columns:1fr}.hero-panel{display:none}
  .slide{grid-template-columns:1fr}
  .about-grid{grid-template-columns:1fr}
}
@media(max-width:520px){
  .feat-grid,.svc-grid,.stack-grid,.contact-grid{grid-template-columns:1fr}
  .nav-links{display:none}
  .tech-grid{grid-template-columns:repeat(2,1fr)}
}
</style>
"""

# ═════════════════════════════════════════════════════════════════════════════
#  CALENDLY MODAL
# ═════════════════════════════════════════════════════════════════════════════
def calendly_modal() -> str:
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
      <iframe id="calFrame"
        src="{SITE['calendly']}?embed_domain=gprai.github.io&embed_type=Inline&hide_gdpr_banner=1&background_color=112240&text_color=e2eaf5&primary_color=00e5ff"
        title="Book a meeting"
        onload="document.getElementById('calLoad').style.display='none'"></iframe>
    </div>
  </div>
</div>
<script>
function openCal(){{document.getElementById('calModal').classList.add('open');document.body.style.overflow='hidden'}}
function closeCal(){{document.getElementById('calModal').classList.remove('open');document.body.style.overflow=''}}
document.getElementById('calModal').addEventListener('click',function(e){{if(e.target===this)closeCal()}})
document.addEventListener('keydown',function(e){{if(e.key==='Escape')closeCal()}})
</script>"""

# ═════════════════════════════════════════════════════════════════════════════
#  NAV / FOOTER / PAGE SHELL
# ═════════════════════════════════════════════════════════════════════════════
def nav(active="") -> str:
    links = [("Home","index.html"),("Stack","stack.html"),
             ("Projects","projects.html"),("Services","services.html"),("Contact","contact.html")]
    items = "".join(
        f'<li><a href="/{h}" {"class=\"active\"" if l.lower()==active.lower() else ""}>{l}</a></li>'
        for l,h in links)
    return f"""<nav>
  <a class="nav-logo" href="/index.html">GPR<span>.</span></a>
  <ul class="nav-links">{items}</ul>
  <button class="nav-book" onclick="openCal()">📅 Book a Demo</button>
</nav>"""

def foot() -> str:
    return f"""<footer>
  <span>© 2025 Gyan Prakash Rai · Cloud &amp; Platform Engineer</span>
  <span style="display:flex;gap:1.3rem;flex-wrap:wrap">
    <a href="{SITE['github']}" target="_blank">GitHub</a>
    <a href="{SITE['linkedin']}" target="_blank">LinkedIn</a>
    <a href="mailto:{SITE['email']}">{SITE['email']}</a>
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
  {foot()}
</body>
</html>"""

# ═════════════════════════════════════════════════════════════════════════════
#  PAGE: HOME
# ═════════════════════════════════════════════════════════════════════════════
def build_index() -> str:
    typing_words = [
        "AWS & Azure Platform Engineer",
        "Kubernetes · EKS · AKS · Karpenter",
        "Terraform · GitOps · CI/CD",
        "DevSecOps · Observability",
        "AI-Ready Cloud Architecture",
    ]
    chips = [
        ("#FF9900","AWS EKS"),("#00adef","Azure AKS"),("#7c5cbf","Terraform"),
        ("#00c896","GitHub Actions"),("#00e5ff","ArgoCD"),("#FF9900","Karpenter"),
        ("#db2777","Docker · Helm"),("#f59e0b","Prometheus"),("#7c5cbf","Bedrock"),
    ]
    chip_html = "".join(
        f'<div class="tech-chip"><span class="dot" style="background:{c}"></span>{lbl}</div>'
        for c,lbl in chips)
    certs_html = "".join(
        f'<div class="cert" style="border-color:{c["color"]}55;color:{c["color"]}">'
        f'{"☁" if c["vendor"]=="AWS" else "⬡"}&nbsp;{c["label"]}</div>'
        for c in CERTIFICATIONS)
    stats_html = "".join(
        f'<div><div class="stat-n">{s["n"]}<span>.</span></div>'
        f'<div class="stat-l">{s["label"]}</div></div>'
        for s in ABOUT["stats"])
    bio_html = "".join(f'<p>{b}</p>' for b in ABOUT["bio"])
    focus_html = "".join(f'<span class="focus-tag">{f}</span>' for f in ABOUT["focus"])
    skills = [
        ("Cloud (AWS & Azure)",95),("Kubernetes / EKS / AKS",90),
        ("Terraform / IaC",90),("CI/CD & GitOps",88),
        ("DevSecOps",82),("AI Infra / MLOps",75),
    ]
    bars_html = "".join(
        f'<div class="skill-row"><div class="skill-top"><span>{n}</span><span>{v}%</span></div>'
        f'<div class="skill-bar"><div class="skill-fill" style="width:{v}%"></div></div></div>'
        for n,v in skills)

    # — featured project cards
    feat_html = ""
    for p in PROJECTS:
        if not p.get("featured"): continue
        bc = "b-prod" if p["status"]=="Production" else "b-dev"
        tags = "".join(f'<span class="tag">{t}</span>' for t in p["stack"][:5])
        feat_html += f"""<div class="feat-card">
  <span class="feat-badge {bc}">{p['status']}</span>
  <h3>{p['title']}</h3>
  <p>{p['short']}</p>
  <div class="feat-tags">{tags}</div>
  <a href="/projects.html#{p['id']}" class="btn btn-p" style="font-size:.75rem;padding:.42rem 1rem">Full Details →</a>
</div>"""

    # — video showcase slides
    slides_html = ""
    dots_html = ""
    for i, p in enumerate(PROJECTS):
        bc = "s-prod" if p["status"]=="Production" else "s-dev"
        dot_cls = "active" if i==0 else ""
        dots_html += f'<button class="slide-dot {dot_cls}" onclick="goSlide({i})" aria-label="Slide {i+1}"></button>'
        tags = "".join(f'<span class="tag">{t}</span>' for t in p["stack"][:6])
        screen_content = ""
        if p["media_videos"]:
            vf = p["media_videos"][0]
            screen_content = f'<video style="width:100%;height:100%;object-fit:cover;border-radius:10px" autoplay muted loop playsinline><source src="/media/videos/{vf}" type="video/mp4"/></video>'
        elif p["media_images"]:
            imgf = p["media_images"][0]
            screen_content = f'<img src="/media/images/{imgf}" alt="{p["title"]}" style="width:100%;height:100%;object-fit:cover;border-radius:10px"/>'
        else:
            icon = "⎈" if "eks" in p["id"] else "☁"
            screen_content = f"""<div class="slide-screen-inner">
  <div style="font-size:3.5rem">{icon}</div>
  <span class="slide-screen-label" style="margin-top:.6rem;display:block;color:var(--muted);font-size:.68rem">
    Add video/image in build.py<br/>docs/media/videos/ or docs/media/images/
  </span>
</div>"""
        slides_html += f"""<div class="slide">
  <div>
    <div class="slide-label">{'Completed Project' if p['status']=='Production' else 'Upcoming Project'}</div>
    <div class="slide-status {bc}"><span class="live-dot"></span>{p['status']}</div>
    <h3>{p['title']}</h3>
    <p>{p['short']}</p>
    <div class="slide-tags">{tags}</div>
    <div style="display:flex;gap:.65rem;flex-wrap:wrap">
      <a href="/projects.html#{p['id']}" class="btn btn-p" style="font-size:.74rem;padding:.4rem .9rem">Full Details →</a>
      <a href="{p['repo']}" class="btn btn-o" target="_blank" style="font-size:.74rem;padding:.4rem .9rem">GitHub ↗</a>
    </div>
  </div>
  <div class="slide-screen">{screen_content}</div>
</div>"""

    upcoming_html = "".join(
        f'<div class="upcoming-card"><span class="uc-badge">Planned</span>'
        f'<div class="uc-title">{u["title"]}</div>'
        f'<div class="uc-desc">{u["desc"]}</div></div>'
        for u in UPCOMING)

    return page("Home", f"""
<!-- ═══ HERO ═══ -->
<section class="hero">
  <div>
    <div class="eyebrow">🚀 Open for Consulting &amp; Freelance</div>
    <h1>Gyan<br/>Prakash <em>Rai</em></h1>
    <p class="hero-sub">
      <span id="ty" style="color:var(--cyan);font-weight:600"></span><span style="color:var(--cyan);animation:blink 1s step-end infinite">_</span>
      <br/><br/>
      Building scalable, secure, <strong>production-grade cloud infrastructure</strong> on AWS &amp; Azure — with Kubernetes, Terraform, CI/CD and GitOps at the core.
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
    <div class="panel-label" style="margin-top:.9rem">GitOps CI/CD Pipeline</div>
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
<style>@keyframes blink{{0%,100%{{opacity:1}}50%{{opacity:0}}}}</style>
<script>
const W={json.dumps(typing_words)};
let wi=0,ci=0,dl=false;
const el=document.getElementById('ty');
function t(){{const w=W[wi];el.textContent=dl?w.slice(0,ci--):w.slice(0,ci++);
  if(!dl&&ci>w.length){{dl=true;setTimeout(t,1200);return;}}
  if(dl&&ci<0){{dl=false;wi=(wi+1)%W.length;}}setTimeout(t,dl?35:68);}}
t();
</script>

<hr class="div"/>

<!-- ═══ CERTIFICATIONS ═══ -->
<section class="section">
  <p class="sec-label">Certifications</p>
  <h2 style="font-size:1.3rem;font-weight:800;letter-spacing:-.02em;margin-bottom:1.1rem;color:var(--text)">7 Cloud Certifications — AWS &amp; Azure</h2>
  <div class="cert-strip">{certs_html}</div>
</section>

<hr class="div"/>

<!-- ═══ ABOUT ═══ -->
<section class="section">
  <p class="sec-label">About</p>
  <div class="about-grid">
    <div class="about-text">
      <h2 style="font-size:1.55rem;font-weight:900;letter-spacing:-.03em;margin-bottom:1.1rem;color:var(--text)">
        Cloud-native infrastructure,<br/><span style="color:var(--cyan)">built for production.</span>
      </h2>
      {bio_html}
      <div class="focus-wrap">{focus_html}</div>
      <div style="margin-top:1.5rem;display:flex;gap:.75rem;flex-wrap:wrap">
        <a href="/contact.html" class="btn btn-p">Get in Touch</a>
        <a href="{SITE['resume']}" class="btn btn-o" target="_blank">Resume ↗</a>
        <button class="btn btn-v" onclick="openCal()">📅 Book a Demo</button>
      </div>
    </div>
    <div class="skill-bars">{bars_html}</div>
  </div>
</section>

<hr class="div"/>

<!-- ═══ VIDEO / PROJECT SHOWCASE ═══ -->
<div class="showcase">
  <div class="showcase-inner">
    <p class="sec-label">Project Showcase</p>
    <h2 style="font-size:1.35rem;font-weight:900;letter-spacing:-.02em;margin-bottom:1.4rem;color:var(--text)">
      Completed &amp; Upcoming Projects
    </h2>
    <div class="slides-wrap">
      <div class="slides" id="slides">{slides_html}</div>
    </div>
    <div class="slide-controls">
      <button class="slide-nav" onclick="prevSlide()">‹</button>
      {dots_html}
      <button class="slide-nav" onclick="nextSlide()">›</button>
    </div>
    <div style="margin-top:2rem">
      <p class="sec-label" style="margin-bottom:.8rem">Upcoming</p>
      <div class="upcoming-grid">{upcoming_html}</div>
    </div>
  </div>
</div>
<script>
let cur=0;
const total={len(PROJECTS)};
function goSlide(n){{
  cur=n;
  document.getElementById('slides').style.transform='translateX(-'+n*100+'%)';
  document.querySelectorAll('.slide-dot').forEach((d,i)=>d.classList.toggle('active',i===n));
}}
function nextSlide(){{goSlide((cur+1)%total)}}
function prevSlide(){{goSlide((cur-1+total)%total)}}
setInterval(()=>nextSlide(),6000);
</script>

<hr class="div"/>

<!-- ═══ FEATURED PROJECTS ═══ -->
<section class="section">
  <div style="display:flex;align-items:baseline;justify-content:space-between;gap:1rem;margin-bottom:1.2rem;flex-wrap:wrap">
    <div>
      <p class="sec-label">Featured Projects</p>
      <h2 style="font-size:1.3rem;font-weight:900;letter-spacing:-.02em;color:var(--text)">Production-grade Cloud Work</h2>
    </div>
    <a href="/projects.html" class="btn btn-o" style="font-size:.76rem">All Projects →</a>
  </div>
  <div class="feat-grid">{feat_html}</div>
</section>
""", active="Home")

# ═════════════════════════════════════════════════════════════════════════════
#  PAGE: STACK
# ═════════════════════════════════════════════════════════════════════════════
def build_stack() -> str:
    cards = "".join(
        f'<div class="stack-card">'
        f'<div class="stack-head"><div class="stack-icon">{s["icon"]}</div><h3>{s["cat"]}</h3></div>'
        f'<ul>{"".join(f"<li>{i}</li>" for i in s["items"])}</ul>'
        f'</div>' for s in STACK)
    return page("Stack", f"""
<div class="page-hero">
  <p class="sec-label">Tech Stack</p>
  <h1>Tools &amp; Technologies</h1>
  <p>Full stack I work with day-to-day across cloud, platform engineering, security, and AI/ML.</p>
</div>
<section class="section">
  <div class="stack-grid">{cards}</div>
</section>
""", active="Stack")

# ═════════════════════════════════════════════════════════════════════════════
#  PAGE: PROJECTS
# ═════════════════════════════════════════════════════════════════════════════
def build_projects() -> str:
    cards = ""
    for p in PROJECTS:
        bc = "b-prod" if p["status"]=="Production" else "b-dev"
        hl  = "".join(f"<li>{h}</li>" for h in p["highlights"])
        tags = "".join(f'<span class="tag">{t}</span>' for t in p["stack"])
        arch_svg = ARCH_MAP[p["arch_id"]]()

        img_html = "".join(
            f'<img class="media-img" src="/media/images/{f}" alt="{p["title"]}" loading="lazy"/>'
            for f in p["media_images"])
        vid_html = "".join(
            f'<video class="media-video" controls preload="metadata">'
            f'<source src="/media/videos/{f}" type="video/mp4"/>Your browser does not support video.</video>'
            for f in p["media_videos"])

        if img_html or vid_html:
            media_inner = f'<div class="media-grid">{img_html}{vid_html}</div>'
        else:
            media_inner = f"""<div class="media-empty">
  No media yet — drop images into <code>docs/media/images/</code> or videos into <code>docs/media/videos/</code>,
  then add the filenames to <code>media_images</code> / <code>media_videos</code> in <strong>build.py</strong> and re-run.
</div>"""

        cards += f"""<div class="proj-card" id="{p['id']}">
  <span class="feat-badge {bc}">{p['status']}</span>
  <h2>{p['title']}</h2>
  <p class="proj-summary">{p['summary']}</p>
  <ul class="proj-hl">{hl}</ul>
  <div class="feat-tags" style="margin-bottom:1.1rem">{tags}</div>
  <div style="display:flex;gap:.7rem;flex-wrap:wrap;margin-bottom:.5rem">
    <a href="{p['repo']}" class="btn btn-p" target="_blank">GitHub Repo ↗</a>
  </div>
  <div class="arch-box">
    <h4>🗺 Architecture Diagram</h4>
    <p>{p['short']}</p>
    {arch_svg}
  </div>
  <div class="media-box">
    <h4>📸 Screenshots &amp; Demo Videos</h4>
    {media_inner}
  </div>
</div>"""

    return page("Projects", f"""
<div class="page-hero">
  <p class="sec-label">Projects</p>
  <h1>Featured Work</h1>
  <p>Production-grade cloud and platform engineering with full architecture diagrams.</p>
</div>
<section class="section">{cards}</section>
""", active="Projects")

# ═════════════════════════════════════════════════════════════════════════════
#  PAGE: SERVICES
# ═════════════════════════════════════════════════════════════════════════════
def build_services() -> str:
    cards = "".join(
        f'<div class="svc-card">'
        f'<div class="svc-icon-wrap">{s["icon"]}</div>'
        f'<h3>{s["title"]}</h3>'
        f'<ul>{"".join(f"<li>{i}</li>" for i in s["items"])}</ul>'
        f'</div>' for s in SERVICES)
    return page("Services", f"""
<div class="page-hero">
  <p class="sec-label">Services</p>
  <h1>What I Offer</h1>
  <p>End-to-end cloud engineering, DevOps, and platform consulting.</p>
</div>
<section class="section">
  <div class="svc-grid">{cards}</div>
  <div style="margin-top:2rem;padding:2rem;background:var(--surface);border:1px solid var(--border2);border-radius:14px;box-shadow:var(--sh2),var(--glow)">
    <p class="sec-label">Ready to start?</p>
    <h2 style="font-size:1.4rem;font-weight:900;letter-spacing:-.025em;margin-bottom:.7rem;color:var(--text)">Let's build something great.</h2>
    <p style="color:var(--sub);max-width:460px;margin-bottom:1.3rem;font-size:.88rem;line-height:1.85">
      Full cloud platform, CI/CD overhaul, or a one-off architecture review — let's talk.
    </p>
    <div style="display:flex;gap:.75rem;flex-wrap:wrap">
      <button class="btn btn-v" onclick="openCal()">📅 Book a Demo Call</button>
      <a href="/contact.html" class="btn btn-o">Contact Me</a>
    </div>
  </div>
</section>
""", active="Services")

# ═════════════════════════════════════════════════════════════════════════════
#  PAGE: CONTACT
# ═════════════════════════════════════════════════════════════════════════════
def build_contact() -> str:
    links = [
        ("Email",    SITE["email"],    f"mailto:{SITE['email']}"),
        ("LinkedIn", "linkedin.com/in/gyan-prakash-rai-24782413", SITE["linkedin"]),
        ("GitHub",   "github.com/gprai", SITE["github"]),
        ("Resume",   "View / Download PDF", SITE["resume"]),
    ]
    cards = "".join(
        f'<a class="contact-card" href="{h}" target="_blank" rel="noopener">'
        f'<div class="cc-type">{t}</div><div class="cc-val">{v} ↗</div></a>'
        for t,v,h in links)
    return page("Contact", f"""
<div class="page-hero">
  <p class="sec-label">Contact</p>
  <h1>Let's Connect</h1>
  <p>Available for freelance, consulting, and full-time opportunities.</p>
</div>
<section class="section">
  <div class="contact-grid">{cards}</div>
  <div style="background:var(--surface);border:1px solid var(--border2);border-radius:14px;padding:2rem;box-shadow:var(--sh2),var(--glow);max-width:520px">
    <p class="sec-label">Schedule a call</p>
    <h2 style="font-size:1.2rem;font-weight:900;margin-bottom:.5rem;color:var(--text)">Prefer a scheduled meeting?</h2>
    <p style="color:var(--sub);font-size:.86rem;margin-bottom:1.2rem;line-height:1.8">
      Use the Calendly widget to pick a time that works. I confirm within 24 hours.
    </p>
    <button class="btn btn-p" onclick="openCal()">📅 Open Booking Calendar</button>
  </div>
</section>
""", active="Contact")

# ═════════════════════════════════════════════════════════════════════════════
#  BUILD
# ═════════════════════════════════════════════════════════════════════════════
def build():
    pages = {
        OUT/"index.html":    build_index(),
        OUT/"stack.html":    build_stack(),
        OUT/"projects.html": build_projects(),
        OUT/"services.html": build_services(),
        OUT/"contact.html":  build_contact(),
    }
    for path, html in pages.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(html, encoding="utf-8")
        print(f"  ✓  {path}")
    (OUT/"media"/"images"/"README.md").write_text(
        "# Screenshots\nDrop .png/.jpg here, add filenames to media_images in build.py\n")
    (OUT/"media"/"videos"/"README.md").write_text(
        "# Demo Videos\nDrop .mp4 here (< 100 MB each), add filenames to media_videos in build.py\n")
    print(f"\nBuild complete → {OUT}/")

if __name__ == "__main__":
    build()