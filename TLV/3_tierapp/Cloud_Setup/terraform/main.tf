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
  vpc    = null
  domain = "vpc"

  tags = {
    Name = "nat_eip"
  }
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

# Generate a random password for RDS using variables
resource "random_password" "rds_password" {
  length  = var.rds_password_length
  special = var.rds_password_special
}

# Create a Secrets Manager Secret to store the RDS password
resource "aws_secretsmanager_secret" "rds_password_secret" {
  name        = "rds_colordb_password"
  description = "Secret for RDS colordb instance password"

  tags = {
    Environment = "production"
    Application = "color-selector-app"
  }
}

# Add the generated password to the Secrets Manager Secret
resource "aws_secretsmanager_secret_version" "rds_password_secret_version" {
  secret_id     = aws_secretsmanager_secret.rds_password_secret.id
  secret_string = jsonencode({
    username = "admin"
    password = random_password.rds_password.result
  })
}

# Modify the RDS instance to use the secret from Secrets Manager
resource "aws_db_instance" "default" {
  allocated_storage    = 20
  engine               = "mysql"
  engine_version       = "8.0"
  instance_class       = "db.t3.micro"
  identifier           = "colordb"
  username             = var.db_username
  password             = var.db_password
  parameter_group_name = "default.mysql8.0"
  db_subnet_group_name    = aws_db_subnet_group.default.id
  vpc_security_group_ids  = [aws_security_group.rds_sg.id]
  publicly_accessible     = false

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
  ec2_instances = {
    "public_ec2" = {
      user_data = "1_proc_setup.sh"
      role      = "public_role"
    }
    "private_ec2_1" = {
      user_data = "private_ec2_1_setup.sh"
      role      = "private_role"
    }
    "private_ec2_2" = {
      user_data = "private_ec2_2_setup.sh"
      role      = "private_role"
    }
    "private_ec2_3" = {
      user_data = "private_ec2_3_setup.sh"
      role      = "private_role"
    }
  }
}

# EC2 Instances using for_each loop
resource "aws_instance" "ec2" {
  for_each = local.ec2_instances

  ami           = var.ami_id
  instance_type = var.instance_type
  subnet_id     = each.key == "public_ec2" ? aws_subnet.public.id : aws_subnet.private.id
  key_name      = var.key_name

  # Assign different security groups based on instance type
  vpc_security_group_ids = each.key == "public_ec2" ? [aws_security_group.public_sg.id] : [aws_security_group.private_sg.id]

  tags = {
    Name = each.key
  }

  # Associate IAM instance profile based on the role
  iam_instance_profile = local.ec2_instance_profiles[each.value.role].name

  # Assign user data script
  user_data = file("${path.module}/user_data/${each.value.user_data}")
}
