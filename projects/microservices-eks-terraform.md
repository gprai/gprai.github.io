# GitHub Actions CI: Build & Push UI Microservice to AWS ECR

Production-grade Kubernetes platform to **secure, GitOps-ready CI pipeline** using GitHub Actions with **OIDC authentication** (no AWS keys stored in GitHub!). The pipeline automatically builds, tags, and pushes Docker images to Amazon ECR, then updates Helm values to trigger ArgoCD deployments.

---

## Prerequisites

Before starting, ensure you have:

- [x] AWS CLI configured with appropriate permissions
- [x] GitHub repository with `ui` microservice code
- [x] Basic understanding of Docker, ECR, and Helm
- [x] GitHub Actions enabled in your repository

---

## What This Pipeline Achieves
```
Code Change -> GitHub Actions -> Build Image -> Push to ECR -> Update Helm Values -> ArgoCD Deploys
```

**Key Features:**
- **Secure OIDC authentication** (no long-lived AWS credentials)
- **Dual tagging strategy** (`latest` + `sha-commit`)
- **GitOps-ready** (auto-updates Helm values)
- **Fast, automated CI** triggered on code changes

### GitOps Full Flow (DevOps CI and CD combined flow)
```
Developer Pushes Code to src/ui/src/**
            |
            | (1) Triggers GitHub Actions workflow
            v
    GitHub Actions Runner
            |
            | (2) Builds Docker image
            | (3) Pushes to ECR with tags: latest + sha-a1b2c3d
            | (4) Updates chart/values-ui.yaml (tag: sha-a1b2c3d)
            | (5) Commits and pushes to Git
            v
       Git Repository (main branch)
            |
            | (6) ArgoCD polls Git every 3 minutes
            v
      ArgoCD Detects Change
            |
            | (7) Syncs and deploys new image
            v
        EKS Cluster (Running Pods)
```
## Summary

You've successfully built a **production-ready CI pipeline** with:

- **Zero secrets stored in GitHub** (OIDC-based authentication)
- **Immutable image tagging** (SHA-based versioning)
- **GitOps-ready workflow** (auto-updates Helm values)
- **Fast, automated builds** (triggers on code changes)
- **ECR integration** (secure, private container registry)

---

