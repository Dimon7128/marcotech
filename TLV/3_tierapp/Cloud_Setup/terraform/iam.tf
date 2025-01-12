# IAM Role for Public EC2 Instance
resource "aws_iam_role" "public_role" {
  name = "public_ec2_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = {
        Service = "ec2.amazonaws.com"
      },
      Action = "sts:AssumeRole"
    }]
  })
}

# IAM Role for Private EC2 Instances
resource "aws_iam_role" "private_role" {
  name = "private_ec2_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = {
        Service = "ec2.amazonaws.com"
      },
      Action = "sts:AssumeRole"
    }]
  })
}

# IAM Policy for Public EC2 (if needed)
resource "aws_iam_policy" "public_policy" {
  name        = "public_ec2_policy"
  description = "Policy for Public EC2 instances"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      # Define necessary permissions
    ]
  })
}

# IAM Policy for Private EC2 Instances (e.g., access Secrets Manager)
resource "aws_iam_policy" "private_policy" {
  name        = "private_ec2_policy"
  description = "Policy for Private EC2 instances to access Secrets Manager"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow",
        Action   = [
          "secretsmanager:GetSecretValue",
          "secretsmanager:DescribeSecret"
        ],
        Resource = aws_secretsmanager_secret.rds_password_secret.arn
      },
      {
        Effect   = "Allow",
        Action   = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

# Attach Policies to Roles
resource "aws_iam_role_policy_attachment" "public_attach" {
  role       = aws_iam_role.public_role.name
  policy_arn = aws_iam_policy.public_policy.arn
}

resource "aws_iam_role_policy_attachment" "private_attach" {
  role       = aws_iam_role.private_role.name
  policy_arn = aws_iam_policy.private_policy.arn
}

# IAM Instance Profiles
resource "aws_iam_instance_profile" "public_instance_profile" {
  name = "public_ec2_instance_profile"
  role = aws_iam_role.public_role.name
}

resource "aws_iam_instance_profile" "private_instance_profile" {
  name = "private_ec2_instance_profile"
  role = aws_iam_role.private_role.name
}

# Mapping of Roles to Instance Profiles for easy reference
locals {
  ec2_instance_profiles = {
    "public_role"  = aws_iam_instance_profile.public_instance_profile
    "private_role" = aws_iam_instance_profile.private_instance_profile
  }
}