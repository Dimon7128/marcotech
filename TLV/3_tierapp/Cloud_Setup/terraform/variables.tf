variable "aws_region" {
  description = "AWS Region"
  default     = "us-east-1"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidr" {
  description = "CIDR block for the Public Subnet"
  default     = "10.0.1.0/24"
}

variable "private_subnet_cidr" {
  description = "CIDR block for the Private Subnet"
  default     = "10.0.2.0/24"
}

variable "instance_type" {
  description = "EC2 Instance Type"
  default     = "t2.micro"
}

variable "ami_id" {
  description = "AMI ID for EC2 Instances"
  default     = "ami-0c94855ba95c71c99"  # Example AMI for Amazon Linux 2 in us-east-1
}

variable "key_name" {
  description = "EC2 Key Pair Name"
}

variable "private_ec2_processes" {
  description = "Map of private EC2 instances to their user data scripts"
  type        = map(string)
  default = {
    "private_ec2_1" = "private_ec2_1_setup.sh"
    "private_ec2_2" = "private_ec2_2_setup.sh"
    "private_ec2_3" = "private_ec2_3_setup.sh"
  }
}