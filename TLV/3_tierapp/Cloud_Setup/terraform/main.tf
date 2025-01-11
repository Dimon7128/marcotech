resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr

  tags = {
    Name = "main-vpc"
  }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "main-igw"
  }
}

resource "aws_subnet" "public" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.public_subnet_cidr
  map_public_ip_on_launch = true

  tags = {
    Name = "public-subnet"
  }
}

resource "aws_subnet" "private" {
  vpc_id     = aws_vpc.main.id
  cidr_block = var.private_subnet_cidr

  tags = {
    Name = "private-subnet"
  }
}

resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "public-rt"
  }
}

resource "aws_route_table_association" "public_assoc" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public_rt.id
}

resource "aws_eip" "nat_eip" {
  vpc = true
}

resource "aws_nat_gateway" "nat_gw" {
  allocation_id = aws_eip.nat_eip.id
  subnet_id     = aws_subnet.public.id

  tags = {
    Name = "main-nat-gw"
  }
}

resource "aws_route_table" "private_rt" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat_gw.id
  }

  tags = {
    Name = "private-rt"
  }
}

resource "aws_route_table_association" "private_assoc" {
  subnet_id      = aws_subnet.private.id
  route_table_id = aws_route_table.private_rt.id
}

resource "aws_db_instance" "default" {
  allocated_storage    = 20
  engine               = "mysql"
  engine_version       = "8.0"
  instance_class       = "db.t2.micro"
  name                 = "colordb"
  username             = "admin"
  password             = "YourSecurePassword123"
  parameter_group_name = "default.mysql8.0"
  db_subnet_group_name = aws_db_subnet_group.default.id
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  publicly_accessible  = false

  tags = {
    Name = "color-rds"
  }

  skip_final_snapshot = true
}

resource "aws_db_subnet_group" "default" {
  name       = "main-db-subnet-group"
  subnet_ids = [aws_subnet.private.id]

  tags = {
    Name = "main-db-subnet-group"
  }
}

# Local variables to capture private IPs of backend EC2 instances
locals {
  update_color_ip  = aws_instance.private_ec2_1.private_ip
  query_color_ip   = aws_instance.private_ec2_2.private_ip
  not_allowed_ip   = aws_instance.private_ec2_3.private_ip

  nginx_config = templatefile("${path.module}/templates/nginx.conf.tpl", {
    update_color_ip = local.update_color_ip
    query_color_ip  = local.query_color_ip
    not_allowed_ip  = local.not_allowed_ip
  })
}

# Public EC2 Instance with Nginx Configuration
resource "aws_instance" "public_ec2" {
  ami           = var.ami_id
  instance_type = var.instance_type
  subnet_id     = aws_subnet.public.id
  key_name      = var.key_name

  security_groups = [aws_security_group.public_sg.name]

  tags = {
    Name = "public-ec2"
  }

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install -y nginx

              # Deploy Nginx configuration
              echo '${replace(local.nginx_config, "\n", "\n")}' > /etc/nginx/nginx.conf

              # Start and enable Nginx
              systemctl enable nginx
              systemctl start nginx
              EOF
}

# Private EC2 Instances
resource "aws_instance" "private_ec2_1" {
  ami           = var.ami_id
  instance_type = var.instance_type
  subnet_id     = aws_subnet.private.id
  key_name      = var.key_name

  security_groups = [aws_security_group.private_sg.name]

  tags = {
    Name = "private-ec2-1"
  }

  user_data = file("${path.module}/user_data/private_ec2_1_setup.sh")
}

resource "aws_instance" "private_ec2_2" {
  ami           = var.ami_id
  instance_type = var.instance_type
  subnet_id     = aws_subnet.private.id
  key_name      = var.key_name

  security_groups = [aws_security_group.private_sg.name]

  tags = {
    Name = "private-ec2-2"
  }

  user_data = file("${path.module}/user_data/private_ec2_2_setup.sh")
}

resource "aws_instance" "private_ec2_3" {
  ami           = var.ami_id
  instance_type = var.instance_type
  subnet_id     = aws_subnet.private.id
  key_name      = var.key_name

  security_groups = [aws_security_group.private_sg.name]

  tags = {
    Name = "private-ec2-3"
  }

  user_data = file("${path.module}/user_data/private_ec2_3_setup.sh")
}