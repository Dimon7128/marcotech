output "public_ec2_public_ip" {
  description = "Public IP of the public EC2 instance"
  value       = aws_instance.public_ec2.public_ip
}

output "private_ec2_ids" {
  description = "IDs of the private EC2 instances"
  value       = aws_instance.private_ec2[*].id
}

output "rds_endpoint" {
  description = "RDS Endpoint"
  value       = aws_db_instance.default.endpoint
} 