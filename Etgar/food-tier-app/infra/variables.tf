// variables.tf — knobs you can change without editing the main resources.

variable "aws_region" {
  description = "AWS region the lab is deployed in."
  type        = string
  default     = "il-central-1"
}

variable "instance_type" {
  description = "EC2 instance type for both Blue and Prod."
  type        = string
  default     = "t3.micro"
}

variable "project_name" {
  description = "Short name baked into resource names and tags."
  type        = string
  default     = "food-tier"
}

// --- GitHub OIDC --------------------------------------------------------
//
// These three values shape the trust policy of the GitHub deploy role.
// The condition restricts the role to be assumed *only* by workflows
// running on `github_branch` of `github_org/github_repo` — even another
// branch in the same repo cannot assume it. That is the whole point of
// using OIDC instead of long-lived AWS keys.

variable "github_org" {
  description = "GitHub organisation or user that owns the repo (e.g. \"my-org\")."
  type        = string
}

variable "github_repo" {
  description = "GitHub repository name (e.g. \"marcotech\")."
  type        = string
}

variable "github_branch" {
  description = "Branch allowed to assume the deploy role (typically \"main\")."
  type        = string
  default     = "main"
}

variable "create_github_oidc_provider" {
  description = <<-EOT
    Set to false if the GitHub OIDC provider already exists in this AWS
    account (it is one-per-account). When false, the deploy role's trust
    policy points at the existing provider found via a data source.
  EOT
  type        = bool
  default     = true
}

// --- Optional knobs -----------------------------------------------------

variable "app_ports" {
  description = <<-EOT
    TCP ports opened to 0.0.0.0/0 on the EC2s. Port 22 is intentionally
    NOT in this list — deployment uses SSM, never SSH.
      - 80   : nginx, if you change compose to publish frontend on 80
      - 8000 : FastAPI backend (matches docker-compose.yml)
      - 8080 : current frontend port (matches docker-compose.yml)
  EOT
  type        = list(number)
  default     = [80, 8000, 8080]
}
