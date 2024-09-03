variable "region" {
  description = "The AWS region where resources will be created"
  type        = string
  default     = "eu-west-3"
}

variable "availability_zone" {
  description = "The Availability Zone within the selected region"
  type        = string
  default     = "eu-west-3a"
}

variable "ami" {
  description = "The ID of the AMI to use for the EC2 instances"
  type        = string
  default     = "ami-0abcdef1234567890"  # Replace with your desired AMI ID
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "subnet_cidr" {
  description = "CIDR block for the subnet"
  type        = string
  default     = "10.0.1.0/24"
}

variable "key_name" {
  description = "Name of the PEM key"
  type = string 
  default = "dimipimi.pem"
}