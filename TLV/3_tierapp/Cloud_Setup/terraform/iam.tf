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
  description = "Policy for public EC2 instances"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ssm:GetParameter",
          "ssm:GetParameters"
        ]
        Resource = [
          aws_ssm_parameter.rds_password.arn
        ]
      }
    ]
  })
}

# IAM Policy for Private EC2 Instances (e.g., access Secrets Manager)
resource "aws_iam_policy" "private_policy" {
  name        = "private_ec2_policy"
  description = "Policy for private EC2 instances"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ssm:GetParameter",
          "ssm:GetParameters"
        ]
        Resource = aws_ssm_parameter.rds_password.arn
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

# IAM instance profile for public EC2
resource "aws_iam_instance_profile" "public_profile" {
  name = "public_ec2_profile"
  role = aws_iam_role.public_role.name
}

# Attach policy to public role
resource "aws_iam_role_policy_attachment" "public_policy_attachment" {
  policy_arn = aws_iam_policy.public_policy.arn
  role       = aws_iam_role.public_role.name
}

# Add SSM policy attachment for public role
resource "aws_iam_role_policy_attachment" "public_ssm_policy" {
  role       = aws_iam_role.public_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

# Add SSM policy attachment for private role
resource "aws_iam_role_policy_attachment" "private_ssm_policy" {
  role       = aws_iam_role.private_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}