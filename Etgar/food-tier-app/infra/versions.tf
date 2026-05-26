// versions.tf — pin Terraform and the AWS provider.
//
// Pinning matters because untrusted provider versions can introduce
// breaking changes between `terraform plan` runs on different machines.
// We keep the floor low enough to work with Terraform 1.5+.

terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.60"
    }
  }
}
