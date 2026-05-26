# Init CI - Nginx Continuous Deployment

## Project Overview

This project demonstrates a full CI/CD pipeline for deploying a simple Nginx web server on an AWS EC2 instance.

- **Phase 1 (Manual Setup):** Launch an Ubuntu EC2 instance (t2.micro), install Nginx, and configure it to serve two routes (`/file1` and `/file2`) that return distinct HTML pages.
- **Phase 2 (Verification):** Validate routing by browsing to `http://<EC2_IP>/file1` and `http://<EC2_IP>/file2` to confirm each returns its expected content.
- **Phase 3 (CD Automation):** Automate deployment with GitHub Actions so that any push to the repository automatically syncs HTML and Nginx config files to the EC2 instance and reloads Nginx.

## DevOps Concepts

### Webhooks

GitHub uses webhooks to notify external services (like a GitHub Actions runner) when events occur in a repository. When a `push` event happens, GitHub sends an HTTP POST request to the configured endpoint, which triggers the CI/CD workflow to run.

### SSH Authentication

The GitHub Actions runner authenticates to the EC2 instance using an SSH key pair. The private key is stored as a GitHub Secret and injected at runtime, allowing the runner to establish a secure, passwordless connection to the server.

### OIDC (OpenID Connect)

OIDC allows GitHub Actions to request short-lived, automatically rotated credentials from AWS instead of relying on long-lived Access Keys stored as secrets. This significantly reduces the risk of credential leakage, since the tokens expire quickly and are scoped to the specific workflow run.

## Repository Structure

```
Etgar/Init_CI/
├── html/
│   ├── index1.html
│   └── index2.html
├── nginx/
│   └── nginx.conf
└── README.md

.github/workflows/
└── deploy.yml
```

## Required GitHub Secrets

Before the pipeline can deploy, add these secrets in your GitHub repo under **Settings > Secrets and variables > Actions**:

| Secret Name    | Description                                      |
|----------------|--------------------------------------------------|
| `EC2_HOST`     | Public IP address of your EC2 instance           |
| `EC2_USER`     | SSH username (typically `ubuntu` for Ubuntu AMIs) |
| `EC2_SSH_KEY`  | Full contents of your `.pem` private key file    |

## Security Approaches Comparison

This project uses **SSH keys** for simplicity. Below is a summary of more secure alternatives to consider for production.

### SSH Key (Current)
- Private key stored as a GitHub Secret, runner connects to EC2 over port 22.
- Simple setup, but the key is **long-lived** and port 22 must be open.
- **Risk:** if the secret leaks, the attacker has persistent access until the key is revoked.

### AWS Access Keys
- `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY` stored as GitHub Secrets.
- Enables AWS API calls (S3, SSM, CodeDeploy) but credentials are **permanent** until rotated.
- **Risk:** #1 source of cloud breaches -- keys accidentally committed to repos are found by scanners in minutes.

### OIDC + SSH (Hybrid)
- OIDC replaces AWS Access Keys with **short-lived tokens** (~1 hour, auto-rotated).
- SSH key is still used for direct EC2 access, so port 22 remains open.
- **Benefit:** eliminates long-lived AWS credentials; SSH key is the only remaining secret.

### OIDC + SSM (Gold Standard)
- OIDC for AWS auth + AWS Systems Manager (SSM) to execute commands on EC2.
- **Zero secrets** to manage, **zero inbound ports** -- no SSH, no port 22.
- The runner calls `aws ssm send-command` via HTTPS API; the SSM Agent on EC2 executes it.
- Full audit trail in CloudTrail and SSM Run Command history.
- **Trade-off:** highest setup complexity (OIDC provider + IAM roles + EC2 instance role + SSM Agent).

### Summary Table

| Approach | Secrets | Open Ports | Credential Lifetime | Complexity |
|----------|---------|------------|---------------------|------------|
| SSH Key | 1 (key) | 22 | Permanent | Low |
| AWS Access Keys | 2 (key ID + secret) | None | Permanent | Low |
| OIDC + SSH | 1 (SSH key) | 22 | AWS: ~1h / SSH: permanent | Medium |
| OIDC + SSM | 0 | None | ~1 hour, auto-rotated | High |

### Recommended Progression
1. **Learning** -- SSH key (this project)
2. **Next step** -- OIDC + SSH (learn OIDC without changing deployment method)
3. **Production** -- OIDC + SSM (zero secrets, zero open ports, full audit trail)
