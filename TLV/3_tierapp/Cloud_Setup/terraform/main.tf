resource "random_password" "rds_password" {
  length  = 16
  special = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

# Store password in Parameter Store
resource "aws_ssm_parameter" "rds_password" {
  name        = "/prod/rds/colordb/password"
  description = "Password for RDS colordb instance"
  type        = "SecureString"
  value       = random_password.rds_password.result
}

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

# Modify the RDS instance to use the password from Parameter Store
resource "aws_db_instance" "default" {
  allocated_storage    = 20
  engine               = "mysql"
  engine_version       = "8.0"
  instance_class       = "db.t3.micro"
  identifier           = "colordb"
  username             = var.db_username
  password             = random_password.rds_password.result
  parameter_group_name = "default.mysql8.0"
  db_subnet_group_name    = aws_db_subnet_group.default.id
  vpc_security_group_ids  = [aws_security_group.rds_sg.id]
  publicly_accessible     = false

  tags = {
    Name = "color-rds"
  }

  skip_final_snapshot = true
}

# Create private subnets for RDS
resource "aws_subnet" "private_subnet_rds_1" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.4.0/24"
  availability_zone = "eu-west-3a"

  tags = {
    Name = "private_subnet_rds_1"
  }
}

resource "aws_subnet" "private_subnet_rds_2" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.5.0/24"
  availability_zone = "eu-west-3b"

  tags = {
    Name = "private_subnet_rds_2"
  }
}

# Create DB subnet group
resource "aws_db_subnet_group" "default" {
  name        = "main-db-subnet-group"
  description = "Database subnet group"
  subnet_ids  = [
    aws_subnet.private_subnet_rds_1.id,
    aws_subnet.private_subnet_rds_2.id
  ]

  tags = {
    Name = "DB subnet group"
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
      name      = "private_ec2_1"
      user_data = "private_ec2_1_setup.sh"
      subnet_id = aws_subnet.private.id
    }
    "private_ec2_2" = {
      name      = "private_ec2_2"
      user_data = "private_ec2_2_setup.sh"
      subnet_id = aws_subnet.private.id
    }
    "private_ec2_3" = {
      name      = "private_ec2_3"
      user_data = "private_ec2_3_setup.sh"
      subnet_id = aws_subnet.private.id
    }
  }
}

# Create the first EC2 instance separately
resource "aws_instance" "private_ec2_1" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.private.id
  key_name      = var.key_name
  
  vpc_security_group_ids = [aws_security_group.private_sg.id]
  iam_instance_profile   = aws_iam_instance_profile.private_profile.name
  
  user_data = templatefile("${path.module}/user_data/private_ec2_1_setup.sh", {})

  tags = {
    Name = "private_ec2_1"
  }
}

# Create the remaining EC2 instances with for_each
locals {
  remaining_ec2_instances = {
    "private_ec2_2" = {
      name      = "private_ec2_2"
      user_data = "private_ec2_2_setup.sh"
      subnet_id = aws_subnet.private.id
    },
    "private_ec2_3" = {
      name      = "private_ec2_3"
      user_data = "private_ec2_3_setup.sh"
      subnet_id = aws_subnet.private.id
    }
  }
}

resource "aws_instance" "remaining_ec2" {
  for_each = local.remaining_ec2_instances
  
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t2.micro"
  subnet_id     = each.value.subnet_id
  key_name      = var.key_name
  
  vpc_security_group_ids = [aws_security_group.private_sg.id]
  iam_instance_profile   = aws_iam_instance_profile.private_profile.name
  
  user_data = templatefile("${path.module}/user_data/${each.value.user_data}", {
    update_color_ip = aws_instance.private_ec2_1.private_ip
  })

  tags = {
    Name = each.value.name
  }
}

# Public EC2 instance for Nginx frontend
resource "aws_instance" "public_ec2" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.public.id
  key_name      = var.key_name
  
  vpc_security_group_ids = [aws_security_group.public_sg.id]
  iam_instance_profile   = aws_iam_instance_profile.public_profile.name
  
  associate_public_ip_address = true

  user_data = templatefile("${path.module}/user_data/1_Proc_init.sh", {
    query_color_ip = aws_instance.remaining_ec2["private_ec2_2"].private_ip
    not_allowed_ip = aws_instance.remaining_ec2["private_ec2_3"].private_ip
  })

  tags = {
    Name = "public_ec2"
  }
}

# Update outputs to include public EC2
output "public_ec2_public_ip" {
  description = "Public IP of the Nginx frontend server"
  value       = aws_instance.public_ec2.public_ip
}

# Get the latest Ubuntu AMI
data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

# Create IAM instance profile
resource "aws_iam_instance_profile" "private_profile" {
  name = "private_ec2_profile"
  role = aws_iam_role.private_role.name
}
