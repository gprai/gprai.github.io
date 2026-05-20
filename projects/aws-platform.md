# AWS Platform Engineering
Enterprise-grade AWS platform engineering project implementing a secure multi-account landing zone using AWS Control Tower, AWS Organizations, Terraform, GitHub Actions, and GitOps principles for automated governance, security, identity, networking, and scalable cloud foundation deployment.

# AWS Multi-Account Landing Zone Platform on AWS using Control Tower, Terraform & GitOps

Enterprise-grade AWS Landing Zone / Cloud Foundation Platform built using:

- AWS Control Tower
- AWS Organizations
- Terraform
- GitHub Actions
- GitOps principles
- IAM Identity Center
- Security Guardrails
- Enterprise Governance Automation

---

# Overview

This project demonstrates the implementation of a production-grade AWS Cloud Foundation / Landing Zone architecture designed for enterprise-scale cloud adoption.

The platform provides:

- Multi-account AWS governance
- Centralized identity and access management
- Security baselines
- Logging and auditing
- Organizational governance
- CI/CD-driven infrastructure automation
- Terraform-based account provisioning
- GitOps workflows
- Enterprise-ready cloud foundation architecture

The architecture follows AWS best practices for:

- Security
- Governance
- Scalability
- Operational excellence
- Infrastructure automation

---

# Key Objectives

This platform was designed to solve the following enterprise challenges:

- Secure separation of environments using isolated AWS accounts
- Centralized governance across all AWS accounts
- Standardized account provisioning
- Automated infrastructure lifecycle management
- Secure CI/CD pipelines using GitHub OIDC federation
- Scalable landing zone architecture
- Security and compliance enforcement
- Cloud cost visibility and governance
- Infrastructure consistency through Infrastructure as Code

---

# Architecture Overview

The platform follows a multi-account AWS organizational model.

```text
AWS Organization
│
├── Management Account
│
├── Security OU
│   ├── Audit Account
│   └── Log Archive Account
│
├── Infrastructure OU
│   └── Shared Services Account
│
├── Workloads OU
│   ├── Dev Account
│   ├── Stage Account
│   └── Prod Account
│
└── Sandbox OU
    └── Playground Account
```
---
![alt text](image.png)
---
---

# Why Multi-Account Architecture?

Instead of hosting everything inside a single AWS account, enterprises isolate workloads into multiple AWS accounts for:

## Security Isolation

Compromise in one environment does not directly impact another.

```text
Dev Account Compromise
        ≠
Production Compromise
```

---

## IAM Separation

Fine-grained access control between:

- Developers
- Platform Engineers
- Security Teams
- Operations Teams

---

## Billing Separation

Each AWS account maintains independent cost visibility and budgeting.

---

## Quota Isolation

AWS quotas are account-scoped.

Separate accounts prevent:

- noisy-neighbor problems
- quota exhaustion
- resource contention

---

## Compliance & Governance

Different environments require:

- different security controls
- different SCPs
- different monitoring baselines

---

# Platform Components

## Governance Layer

- AWS Organizations
- Organizational Units (OUs)
- Service Control Policies (SCPs)
- Tag Policies
- Centralized Billing

---

## Identity Layer

- AWS IAM Identity Center
- Permission Sets
- Role-based Access Control (RBAC)
- Cross-account access management
- GitHub OIDC federation

---

## Security Layer

- AWS CloudTrail
- AWS Config
- AWS KMS
- Amazon CloudWatch
- AWS Security Hub
- Amazon GuardDuty
- Centralized log archival

---

## Networking Layer

- Hub-and-spoke networking architecture
- Shared services networking
- Centralized DNS
- Shared ingress/egress design
- Transit Gateway-ready architecture

---

## Automation Layer

- Terraform
- GitHub Actions
- GitOps workflows
- Remote state management
- Automated account provisioning
- CI/CD-driven infrastructure deployment

---

# Repository Structure

```text
aws-platform-engineering/
├── bootstrap/
├── organizations/
├── control-tower/
├── identity/
├── security/
├── networking/
├── workloads/
├── modules/
└── .github/workflows/
```

---

# Bootstrap Layer

Bootstrap is the foundational setup required before Terraform can manage infrastructure.

The bootstrap phase provisions:

- Terraform backend S3 bucket
- DynamoDB state locking table
- IAM execution roles
- GitHub OIDC federation
- KMS encryption keys

---

# Terraform Remote State

Terraform state is stored remotely using:

- Amazon S3
- DynamoDB state locking

This enables:

- team collaboration
- safe concurrent deployments
- CI/CD integration
- infrastructure drift detection

Example backend configuration:

```hcl
terraform {
  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "organizations/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
  }
}
```

---

# CI/CD Architecture

Infrastructure deployments are fully automated using GitHub Actions.

Deployment flow:

```text
Git Push
    ↓
Terraform Validate
    ↓
Terraform Plan
    ↓
Security Scan
    ↓
Approval
    ↓
Terraform Apply
```

---

# GitHub OIDC Federation

This project uses GitHub OIDC federation instead of static AWS credentials.

Benefits:

- no long-term AWS keys
- temporary credentials
- improved security posture
- enterprise-grade CI/CD authentication

Authentication flow:

```text
GitHub Actions
      ↓
OIDC Token
      ↓
AWS IAM Role
      ↓
Temporary Credentials
```

---

# Terraform Automation

The platform uses Terraform to provision:

- AWS Organizations
- Organizational Units
- AWS Accounts
- SCPs
- IAM Roles
- Logging infrastructure
- Security baselines
- Networking components

Example AWS account creation:

```hcl
resource "aws_organizations_account" "dev" {
  name      = "DevAccount"
  email     = "aws-dev@company.com"
  parent_id = aws_organizations_organizational_unit.workloads.id
}
```

---

# Service Control Policies (SCPs)

SCPs enforce organization-wide governance policies.

Examples:

- Restrict root usage
- Deny public S3 buckets
- Restrict AWS regions
- Enforce encryption
- Prevent disabling CloudTrail

Example SCP:

```hcl
resource "aws_organizations_policy" "deny_root" {
  name = "DenyRootUsage"

  content = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Deny"
      Action = "*"
      Resource = "*"
      Condition = {
        StringLike = {
          "aws:PrincipalArn" = "*root*"
        }
      }
    }]
  })

  type = "SERVICE_CONTROL_POLICY"
}
```

---

# AWS Control Tower Integration

AWS Control Tower provides:

- Landing zone governance
- Account Factory
- Guardrails
- Logging baselines
- Account lifecycle governance

Architecture relationship:

```text
AWS Organizations = Account Engine
Control Tower     = Governance Layer
Terraform         = Automation Engine
AFT               = GitOps Account Provisioning
```

---

# Account Factory for Terraform (AFT)

This platform is designed to support:

## AWS Control Tower Account Factory for Terraform (AFT)

AFT enables:

- GitOps account vending
- Automated account provisioning
- Baseline customization
- Enterprise account lifecycle automation

Provisioning flow:

```text
GitHub Actions
       ↓
Terraform
       ↓
AFT
       ↓
Control Tower
       ↓
AWS Organizations
       ↓
AWS Account Provisioned
```

---

# Example AFT Account Request

```hcl
module "dev_account" {
  source = "./modules/aft-account-request"

  control_tower_parameters = {
    AccountEmail = "aws-dev@company.com"
    AccountName  = "DevAccount"
    ManagedOrganizationalUnit = "Workloads"
    SSOUserEmail = "admin@company.com"
    SSOUserFirstName = "Cloud"
    SSOUserLastName  = "Admin"
  }

  account_tags = {
    environment = "dev"
    owner       = "platform-team"
  }
}
```

---

# Security Architecture

Security controls implemented:

- AWS CloudTrail organization trails
- Centralized log archival
- AWS Config compliance monitoring
- AWS Security Hub
- Amazon GuardDuty
- KMS encryption
- IAM least privilege
- SCP governance
- Cross-account role management

---

# Observability & Monitoring

Monitoring stack:

- Amazon CloudWatch
- Centralized logging
- Organization-wide CloudTrail
- Security findings aggregation
- Compliance visibility

---

# Networking Architecture

Recommended enterprise networking model:

- Hub-and-spoke networking
- Shared services VPC
- Centralized DNS
- Shared ingress/egress
- Transit Gateway-ready design

---

# Recommended Learning / Deployment Progression

## Phase 1 — Organizations & Governance

- AWS Organizations
- OUs
- SCPs
- Account provisioning

---

## Phase 2 — Identity & Access

- IAM Identity Center
- Permission Sets
- Cross-account access

---

## Phase 3 — Security Baselines

- CloudTrail
- Config
- Security Hub
- GuardDuty

---

## Phase 4 — Networking Foundation

- Shared networking
- DNS
- Transit Gateway architecture

---

## Phase 5 — Control Tower & AFT

- Landing zone governance
- Account Factory
- GitOps account vending

---

# Cost Optimization Notes

This platform can be deployed in:

- learning/lab mode
- production enterprise mode

Recommended low-cost learning setup:

- single AWS region
- minimal accounts
- no NAT Gateway
- limited logging retention
- minimal security services

Approximate learning cost:

```text
~$10–20/month
```

---

# Key Engineering Concepts Demonstrated

This project demonstrates expertise in:

- AWS Platform Engineering
- Landing Zone Architecture
- Enterprise Governance
- Multi-account AWS Architecture
- Infrastructure as Code
- GitOps Workflows
- Terraform Automation
- AWS Security Governance
- CI/CD Engineering
- Cloud Foundation Engineering

---

# Technologies Used

| Category | Technologies |
|---|---|
| Cloud | AWS |
| Governance | AWS Organizations, Control Tower |
| IaC | Terraform |
| CI/CD | GitHub Actions |
| Identity | IAM Identity Center |
| Security | CloudTrail, Config, Security Hub |
| Monitoring | CloudWatch |
| State Management | S3 + DynamoDB |
| Authentication | GitHub OIDC |
| Automation | AFT |

---

# Future Enhancements

Planned enhancements:

- Full AFT integration
- Automated account vending workflows
- EKS platform integration
- Shared services platform
- Security Lake integration
- Centralized SIEM integration
- Policy-as-Code (OPA/Sentinel)
- FinOps automation
- Advanced networking automation

---

# Final Notes

This repository demonstrates how modern enterprises build:

- secure AWS foundations
- scalable governance platforms
- automated landing zones
- GitOps-driven cloud platforms

using Infrastructure as Code and enterprise automation principles.

The architecture reflects real-world cloud platform engineering practices used in large-scale AWS environments.