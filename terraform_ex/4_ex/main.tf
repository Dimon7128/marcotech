provider "aws" {
  region = "us-west-2"
}

module "vpc" {
  source = "./modules/vpc"
  vpc_cidr = var.vpc_cidr
  public_subnet_cidr = var.public_subnet_cidr
  private_subnet_cidr = var.private_subnet_cidr
}

module "ec2" {
  source = "./modules/ec2"
  instance_type = var.instance_type
  ami = var.ami
  subnet_id = module.vpc.public_subnet_id
  security_group_id = module.vpc.security_group_id
}
