resource "aws_security_group" "public_sg" {
  name_prefix = "public_sg_"
  description = "Security group for public EC2 instance"
  vpc_id      = aws_vpc.main.id

  lifecycle {
    create_before_destroy = true
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }


  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "public_sg"
  }
}

resource "aws_security_group" "private_sg" {
  name        = "private_sg"
  description = "Allow internal communication from Public SG and necessary ports"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "Allow Nginx to Update Color Service"
    from_port   = 5001
    to_port     = 5001
    protocol    = "tcp"
    security_groups = [aws_security_group.public_sg.id]
  }

  ingress {
    description = "Allow Nginx to Query Color Service"
    from_port   = 5002
    to_port     = 5002
    protocol    = "tcp"
    security_groups = [aws_security_group.public_sg.id]
  }

  ingress {
    description = "Allow Nginx to Not Allowed Service"
    from_port   = 5003
    to_port     = 5003
    protocol    = "tcp"
    security_groups = [aws_security_group.public_sg.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "rds_sg" {
  name        = "rds_sg"
  description = "Allow MySQL access from Private SG"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "MySQL"
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    security_groups = [aws_security_group.private_sg.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}