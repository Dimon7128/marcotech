variable "aws_region" {
  description = "AWS Region"
  default     = "eu-west-3"
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
  default     = "ami-09be70e689bddcef5"  # Example AMI for ubuntu in eu-west-3
}

variable "key_name" {
  description = "EC2 Key Pair Name"
}

variable "private_ec2_processes" {
  description = "Map of private EC2 instances to their user data scripts"
  type        = map(string)
  default = {
    "private_ec2_1" = "user_data/2_Proc_init.sh"
    "private_ec2_2" = "user_data/3_Proc_init.sh"
    "private_ec2_3" = "user_data/4_Proc_init.sh"
  }
}
variable "update_color_service_ip" {
  description = "Private IP of the Update Color service (private_ec2_1)"
  type        = string
}

variable "query_color_service_ip" {
  description = "Private IP of the Query Color service (private_ec2_2)"
  type        = string
}

variable "not_allowed_service_ip" {
  description = "Private IP of the Not Allowed service (private_ec2_3)"
  type        = string
}

variable "rds_password_length" {
  description = "Length of the RDS admin password"
  type        = number
  default     = 16
}

variable "rds_password_special" {
  description = "Include special characters in the RDS admin password"
  type        = bool
  default     = true
}

variable "db_username" {
  description = "Username for the RDS instance"
  type        = string
}

variable "db_password" {
  description = "Password for the RDS instance"
  type        = string
  sensitive   = true
}

