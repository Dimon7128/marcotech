provider "aws" {
  region = "us-east-1"
}

resource "aws_vpc" "main_vpc" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "main_subnet" {
  vpc_id            = aws_vpc.main_vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-1a"
}

resource "aws_instance" "web_server" {
  ami           = "ami-0d5d9d301c853a04a"
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.main_subnet.id

  tags = {
    Name = "WebServer"
  }
}

resource "aws_security_group" "web_sg" {
  name        = "web_sg"
  description = "Allow web traffic"
  vpc_id      = aws_vpc.main_vpc.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
