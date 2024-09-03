# provider "aws" {
#   region = var.region
# }

resource "aws_instance" "web" {
  ami             = var.ami
  instance_type   = "t2.micro"
  subnet_id       = var.subnet_id
  security_groups = [var.web_sg_id]
  key_name        = var.key_name
}

resource "aws_instance" "agent" {
  ami           = var.ami
  instance_type = "t2.small"
  subnet_id     = var.subnet_id
  security_groups = [var.agent_sg_id]
  key_name      = var.key_name
}

resource "aws_instance" "master" {
  ami             = var.ami
  instance_type   = "t3.medium"
  subnet_id       = var.subnet_id
  security_groups = [aws_security_group.master_sg.id]
  key_name        = var.key_name
}

resource "aws_security_group" "master_sg" {
  name        = "master_sg"
  description = "Security group for Jenkins Master"
  vpc_id      =  var.aws_vpc

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 50000
    to_port     = 50000
    protocol    = "tcp"
    cidr_blocks = [aws_instance.agent.private_ip]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}