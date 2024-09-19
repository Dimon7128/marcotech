
provider "aws" {
  region = "eu-west-3" # Replace with your desired region
}

# data "terraform_remote_state" "backend" {
#   backend = "local"

#   config = {
#     path = "./backend/terraform.tfstate" # Path to the first Terraform state
#   }
# }

terraform {
  backend "s3" {
    bucket         = "my-terraform-state-bucket11111"
    key            = "terraform/state"
    region         = "eu-west-3"
    dynamodb_table = "terraform-state-lock"
    encrypt        = true
  }
}

resource "aws_instance" "example" {
  ami           = "ami-04a92520784b93e73" # Example AMI
  instance_type = "t2.micro"
}

