// providers.tf — AWS provider configuration.
//
// The region comes from var.aws_region (set in terraform.tfvars or via
// the TF_VAR_aws_region environment variable). Default tags are applied
// to every resource that supports them — handy for cost tracking and
// "what is this thing?" questions later.

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project   = "food-tier-app"
      ManagedBy = "terraform"
    }
  }
}
