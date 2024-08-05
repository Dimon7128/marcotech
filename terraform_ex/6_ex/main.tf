provider "aws" {
  region = "us-west-2"
}

module "network" {
  source = "./modules/vp"
  vpc_cidr = var.vpc_cidr
  public_subnet_cidr = var.public_subnet_cidr
  private_subnet_cidr = var.private_subnet_cidr
}

module "compute" {
  source = "./modules/ec2"
  instance_type = var.instance_type
  ami = var.ami
  subnet_id = module.network.public_subnet_id
  security_group_id = module.network.security_group_id
  key_name = var.key_name
}
