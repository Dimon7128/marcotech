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

resource "aws_instance" "public_ec2" {
  ami           = var.ami_id
  instance_type = var.instance_type
  subnet_id     = aws_subnet.public.id
  key_name      = var.key_name

  security_groups = [aws_security_group.public_sg.name]

  tags = {
    Name = "public-ec2"
  }

  user_data = file("${path.module}/user_data/public_ec2_setup.sh")
}

resource "aws_instance" "private_ec2" {
  for_each = var.private_ec2_processes

  ami           = var.ami_id
  instance_type = var.instance_type
  subnet_id     = aws_subnet.private.id
  key_name      = var.key_name

  security_groups = [aws_security_group.private_sg.name]

  tags = {
    Name = each.key
  }

  user_data = file("${path.module}/user_data/${each.value}")
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