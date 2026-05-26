// =============================================================================
//  food-tier-app — minimal CI/CD lab infra
//
//  Two EC2s (Blue = staging, Prod = production), one shared security group,
//  one EC2 instance profile (so each EC2 can be managed by SSM), and one
//  IAM role that GitHub Actions assumes via OIDC to run `aws ssm send-command`
//  against those EC2s.
//
//  Two distinct IAM roles — easy to confuse:
//    * EC2 role            → lets the EC2 BE MANAGED BY SSM (outbound to AWS).
//    * GitHub deploy role  → lets GITHUB CALL AWS to issue SSM commands.
//
//  SSM replaces SSH: port 22 is intentionally NOT opened. The SSM Agent on
//  each EC2 calls *out* to AWS over 443, so no inbound key-based access is
//  needed.
// =============================================================================

data "aws_caller_identity" "current" {}

// -----------------------------------------------------------------------------
// 1. Networking — use the default VPC and any default subnet.
// -----------------------------------------------------------------------------

data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
  filter {
    name   = "default-for-az"
    values = ["true"]
  }
}

// -----------------------------------------------------------------------------
// 2. AMI — latest Ubuntu 22.04 LTS amd64 from Canonical.
// -----------------------------------------------------------------------------

data "aws_ami" "ubuntu_22" {
  most_recent = true
  owners      = ["099720109477"] # Canonical's official AWS account.

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
  filter {
    name   = "architecture"
    values = ["x86_64"]
  }
}

// -----------------------------------------------------------------------------
// 3. Security group — 80 / 8000 / 8080 inbound, no SSH.
// -----------------------------------------------------------------------------

resource "aws_security_group" "app" {
  name        = "${var.project_name}-app-sg"
  description = "Inbound HTTP + backend; SSH intentionally closed (deploy via SSM)."
  vpc_id      = data.aws_vpc.default.id

  // We expand var.app_ports into one ingress rule per port — easier to read
  // than CIDR-of-CIDRs trickery and shows up nicely in `terraform plan`.
  dynamic "ingress" {
    for_each = toset(var.app_ports)
    content {
      description = "TCP ${ingress.value} from anywhere"
      from_port   = ingress.value
      to_port     = ingress.value
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }

  // Egress: allow all (default in AWS, but spelled out for clarity).
  egress {
    description = "Allow all outbound"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-app-sg"
  }
}

// =============================================================================
// 4. EC2 role  →  lets the EC2 be MANAGED BY SSM.
//
//   Trusted entity: the EC2 service (the instance assumes this role at boot
//   via the metadata service). The AmazonSSMManagedInstanceCore managed
//   policy gives the SSM Agent the bare minimum it needs to register with
//   SSM and accept commands.
// =============================================================================

data "aws_iam_policy_document" "ec2_assume" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "ec2_ssm" {
  name               = "${var.project_name}-ec2-ssm-role"
  description        = "Role attached to Blue + Prod EC2s so they can be managed by SSM."
  assume_role_policy = data.aws_iam_policy_document.ec2_assume.json
}

resource "aws_iam_role_policy_attachment" "ec2_ssm_core" {
  role       = aws_iam_role.ec2_ssm.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_iam_instance_profile" "ec2" {
  name = "${var.project_name}-ec2-instance-profile"
  role = aws_iam_role.ec2_ssm.name
}

// =============================================================================
// 5. EC2 instances — Blue (staging) and Prod.
//
//   Both share the same AMI, instance profile, security group and user_data.
//   The only differences are the Name / Environment tags. We deliberately do
//   NOT set `key_name` — that guarantees there is no way to SSH in.
// =============================================================================

locals {
  // Read the bootstrap script once and reuse it for both EC2s.
  user_data = file("${path.module}/user_data.sh")
}

resource "aws_instance" "blue" {
  ami                         = data.aws_ami.ubuntu_22.id
  instance_type               = var.instance_type
  subnet_id                   = data.aws_subnets.default.ids[0]
  vpc_security_group_ids      = [aws_security_group.app.id]
  iam_instance_profile        = aws_iam_instance_profile.ec2.name
  associate_public_ip_address = true
  user_data                   = local.user_data

  tags = {
    Name        = "${var.project_name}-blue"
    Environment = "blue"
  }
}

resource "aws_instance" "prod" {
  ami                         = data.aws_ami.ubuntu_22.id
  instance_type               = var.instance_type
  subnet_id                   = data.aws_subnets.default.ids[0]
  vpc_security_group_ids      = [aws_security_group.app.id]
  iam_instance_profile        = aws_iam_instance_profile.ec2.name
  associate_public_ip_address = true
  user_data                   = local.user_data

  tags = {
    Name        = "${var.project_name}-prod"
    Environment = "prod"
  }
}

// =============================================================================
// 6. GitHub Actions OIDC provider (one per AWS account, idempotent).
//
//   GitHub publishes a public OIDC issuer at token.actions.githubusercontent.com.
//   Registering it once in AWS lets GitHub workflows trade their signed
//   workflow JWT for short-lived AWS STS credentials — no long-lived
//   access keys live in GitHub secrets.
// =============================================================================

resource "aws_iam_openid_connect_provider" "github" {
  count = var.create_github_oidc_provider ? 1 : 0

  url            = "https://token.actions.githubusercontent.com"
  client_id_list = ["sts.amazonaws.com"]
  // AWS no longer strictly validates this thumbprint, but the field is
  // required. This value is GitHub's well-known root CA fingerprint.
  thumbprint_list = ["6938fd4d98bab03faadb97b34396831e3780aea1"]
}

// If the provider already exists in your account (from a previous setup),
// flip `create_github_oidc_provider = false` and we'll reference it
// through this data source instead.
data "aws_iam_openid_connect_provider" "github_existing" {
  count = var.create_github_oidc_provider ? 0 : 1
  url   = "https://token.actions.githubusercontent.com"
}

locals {
  github_oidc_provider_arn = var.create_github_oidc_provider ? (
    aws_iam_openid_connect_provider.github[0].arn
    ) : (
    data.aws_iam_openid_connect_provider.github_existing[0].arn
  )
}

// =============================================================================
// 7. GitHub Actions deploy role  →  lets GITHUB CALL AWS for SSM.
//
//   Trust policy: federated principal is the GitHub OIDC provider above,
//   and the `sub` claim is locked to exactly one repo + branch. Any
//   workflow on any other repo (or any other branch in the same repo)
//   will be refused.
//
//   Permissions policy: ssm:SendCommand on the two specific EC2 instance
//   ARNs + the AWS-managed AWS-RunShellScript document, plus the read-only
//   verbs the CD workflow needs to poll command output. No iam:PassRole —
//   SSM runs commands using the EC2's own instance profile, we never
//   pass a role to it.
// =============================================================================

data "aws_iam_policy_document" "github_assume" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRoleWithWebIdentity"]

    principals {
      type        = "Federated"
      identifiers = [local.github_oidc_provider_arn]
    }

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"
      values   = ["sts.amazonaws.com"]
    }

    condition {
      test     = "StringLike"
      variable = "token.actions.githubusercontent.com:sub"
      values   = ["repo:${var.github_org}/${var.github_repo}:ref:refs/heads/${var.github_branch}"]
    }
  }
}

resource "aws_iam_role" "github_deploy" {
  name               = "${var.project_name}-github-actions-deploy-role"
  description        = "Assumed by GitHub Actions via OIDC to run SSM commands against the EC2s."
  assume_role_policy = data.aws_iam_policy_document.github_assume.json
}

data "aws_iam_policy_document" "github_deploy_permissions" {
  // Allow SendCommand only against:
  //   * the two specific EC2 instance ARNs, AND
  //   * the AWS-RunShellScript document.
  // Both have to be in the Resource list for SendCommand — IAM requires
  // BOTH the document and the target instance to be authorised.
  statement {
    sid     = "AllowSendCommandToSpecificInstances"
    effect  = "Allow"
    actions = ["ssm:SendCommand"]
    resources = [
      aws_instance.blue.arn,
      aws_instance.prod.arn,
      "arn:aws:ssm:${var.aws_region}::document/AWS-RunShellScript",
    ]
  }

  // Read-only verbs — needed to poll command status + collect stdout.
  // No resource-level scoping is supported for these, so "*" is the
  // tightest we can do.
  statement {
    sid    = "AllowReadingCommandResults"
    effect = "Allow"
    actions = [
      "ssm:GetCommandInvocation",
      "ssm:ListCommandInvocations",
      "ssm:ListCommands",
    ]
    resources = ["*"]
  }

  // Lets the workflow's `aws sts get-caller-identity` / discovery work.
  // These are also resource-level-scoping-unfriendly.
  statement {
    sid    = "AllowDescribingEC2"
    effect = "Allow"
    actions = [
      "ec2:DescribeInstances",
      "ec2:DescribeInstanceStatus",
    ]
    resources = ["*"]
  }
}

resource "aws_iam_role_policy" "github_deploy" {
  name   = "${var.project_name}-github-deploy-policy"
  role   = aws_iam_role.github_deploy.id
  policy = data.aws_iam_policy_document.github_deploy_permissions.json
}
