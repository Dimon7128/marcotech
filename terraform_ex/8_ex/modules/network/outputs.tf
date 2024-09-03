
  output "subnet_id" {
  value = aws_subnet.main.id
}

output "web_sg_id" {
  value = aws_security_group.web_sg.id
}

output "agent_sg_id" {
  value = aws_security_group.agent_sg.id
}

output "aws_vpc" {
    value = aws_vpc.main.id
}

# output "master_sg_id" {
#   value = aws_security_group.master_sg.id
# }
