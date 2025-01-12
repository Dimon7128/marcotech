output "public_ec2_public_ip" {
  description = "Public IP of the public EC2 instance"
  value       = aws_instance.ec2["public_ec2"].public_ip
}

output "private_ec2_ips" {
  description = "Private IPs of the private EC2 instances"
  value = {
    for instance, details in aws_instance.ec2 :
    instance => details.private_ip
    if instance != "public_ec2"
  }
}

output "rds_endpoint" {
  description = "RDS Endpoint"
  value       = aws_db_instance.default.endpoint
} 