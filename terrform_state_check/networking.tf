# resource "aws_vpc" "my_vpc" {
#   cidr_block = "10.0.0.0/16"
# }

# resource "aws_subnet" "my_subnet" {
#   vpc_id            = aws_vpc.my_vpc.id
#   cidr_block        = "10.0.1.0/24"
#   availability_zone = "eu-west-3a"
# }

# resource "aws_security_group" "my_sg" {
#   name        = "allow-private-comm"
#   vpc_id      = aws_vpc.my_vpc.id

#   ingress {
#     from_port   = 0
#     to_port     = 65535
#     protocol    = "tcp"
#     cidr_blocks = [aws_vpc.my_vpc.cidr_block]
#   }

#   egress {
#     from_port   = 0
#     to_port     = 65535
#     protocol    = "tcp"
#     cidr_blocks = ["0.0.0.0/0"]
#   }
# }
