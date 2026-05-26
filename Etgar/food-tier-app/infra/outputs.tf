// outputs.tf — everything you might want from `terraform output`.
//
// `github_actions_secrets` at the bottom is shaped exactly like the
// GitHub Secrets the CD workflow expects — copy/paste-friendly.

// --- Blue EC2 ---------------------------------------------------------------

output "blue_instance_id" {
  description = "EC2 instance ID of the Blue (staging) server."
  value       = aws_instance.blue.id
}

output "blue_public_ip" {
  description = "Public IPv4 address of the Blue server."
  value       = aws_instance.blue.public_ip
}

output "blue_public_dns" {
  description = "Public DNS hostname of the Blue server."
  value       = aws_instance.blue.public_dns
}

// --- Prod EC2 ---------------------------------------------------------------

output "prod_instance_id" {
  description = "EC2 instance ID of the Prod (production) server."
  value       = aws_instance.prod.id
}

output "prod_public_ip" {
  description = "Public IPv4 address of the Prod server."
  value       = aws_instance.prod.public_ip
}

output "prod_public_dns" {
  description = "Public DNS hostname of the Prod server."
  value       = aws_instance.prod.public_dns
}

// --- IAM (EC2 side — for SSM management) -----------------------------------

output "ec2_ssm_role_name" {
  description = "IAM role attached to both EC2s for SSM management."
  value       = aws_iam_role.ec2_ssm.name
}

output "ec2_instance_profile_name" {
  description = "Instance profile wrapping the EC2 SSM role."
  value       = aws_iam_instance_profile.ec2.name
}

// --- IAM (GitHub side — for OIDC deploy role) ------------------------------

output "github_actions_deploy_role_name" {
  description = "Name of the role GitHub Actions assumes via OIDC."
  value       = aws_iam_role.github_deploy.name
}

output "github_actions_deploy_role_arn" {
  description = "ARN of the role GitHub Actions assumes via OIDC."
  value       = aws_iam_role.github_deploy.arn
}

// --- Misc -------------------------------------------------------------------

output "aws_region" {
  description = "AWS region the lab is deployed in."
  value       = var.aws_region
}

// --- GitHub Secrets bundle --------------------------------------------------
//
// Paste these values into Settings → Secrets and variables → Actions of
// the repo named in var.github_repo. Names match those expected by the
// food-tier-cd-deploy.yml workflow.

output "github_actions_secrets" {
  description = "Values to paste into GitHub repo secrets (names match the CD workflow)."
  value = {
    AWS_REGION           = var.aws_region
    AWS_DEPLOY_ROLE_ARN  = aws_iam_role.github_deploy.arn
    BLUE_EC2_INSTANCE_ID = aws_instance.blue.id
    PROD_EC2_INSTANCE_ID = aws_instance.prod.id
    BLUE_EC2_HOST        = aws_instance.blue.public_dns
    PROD_EC2_HOST        = aws_instance.prod.public_dns
  }
}
