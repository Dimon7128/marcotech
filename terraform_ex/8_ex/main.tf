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
  region       = "eu-west-3"
  ami          = "ami-0abcdef1234567890" # Replace with your desired AMI ID
  subnet_id    = module.network.aws_subnet.main.id
  web_sg_id    = module.network.aws_security_group.web_sg.id
  agent_sg_id  = module.network.aws_security_group.agent_sg.id
  master_sg_id = module.network.aws_security_group.master_sg.id
}
