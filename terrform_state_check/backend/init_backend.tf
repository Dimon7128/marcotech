provider "aws" {
  region = "eu-west-3" 
}

# terraform {
#   backend "s3" {
#     bucket         = "my-terraform-state-bucket11111"
#     key            = "terraform/state"
#     region         = "eu-west-3"
#     dynamodb_table = "terraform-state-lock"
#     encrypt        = true
#   }
# }

resource "aws_s3_bucket" "terraform_state_bucket" {
  bucket = "my-terraform-state-bucket11111" 
}
resource "aws_dynamodb_table" "terraform_state_lock" {
  name         = "terraform-state-lock"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}

output "s3_bucket_name" {
  value = aws_s3_bucket.terraform_state_bucket.id
}

output "dynamodb_table_name" {
  value = aws_dynamodb_table.terraform_state_lock.id
}
