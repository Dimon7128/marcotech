# provider "aws" {
#   region = var.region
# }

resource "aws_instance" "web" {
  ami                          = var.ami
  instance_type                = "t2.micro"
  subnet_id                    = var.subnet_id
  security_groups              = [var.web_sg_id]
  key_name                     = var.key_name
  associate_public_ip_address  = true

  tags = {
    Name = "WebServer"
  }
}

resource "aws_instance" "agent" {
  ami                          = var.ami
  instance_type                = "t2.small"
  subnet_id                    = var.subnet_id
  security_groups              = [var.agent_sg_id]
  key_name                     = var.key_name
  associate_public_ip_address  = true

  tags = {
    Name = "JenkinsAgent"
  }
}

resource "aws_instance" "master" {
  ami                          = var.ami
  instance_type                = "t3.medium"
  subnet_id                    = var.subnet_id
  security_groups              = [var.master_sg_id]
  key_name                     = var.key_name
  associate_public_ip_address  = true

  tags = {
    Name = "JenkinsMaster"
  }

}
