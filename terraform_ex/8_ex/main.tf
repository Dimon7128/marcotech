provider "aws" {
  region = "eu-west-3"
}


module "network" {
  source            = "./modules/network"
  region            = var.region
  availability_zone = var.availability_zone
}

module "compute" {
  source       = "./modules/compute"
  region       = var.region
  ami          = var.ami # Replace with your desired AMI ID
  subnet_id    = module.network.subnet_id
  web_sg_id    = module.network.web_sg_id
  agent_sg_id  = module.network.agent_sg_id
  aws_vpc      = module.network.aws_vpc
  key_name     = var.key_name 
}