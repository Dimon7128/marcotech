# output "public_ec2_public_ip" {
#   description = "Public IP of the public EC2 instance"
#   value       = aws_instance.ec2["public_ec2"].public_ip
# }

# output "private_ec2_ips" {
#   description = "Private IPs of the private EC2 instances"
#   value = {
#     for instance, details in aws_instance.ec2 :
#     instance => details.private_ip
#     if instance != "public_ec2"
#   }
# }

output "rds_endpoint" {
  description = "RDS Endpoint"
  value       = aws_db_instance.default.endpoint
}

output "private_ec2_1_ip" {
  description = "Private IP of EC2 instance 1"
  value       = aws_instance.private_ec2_1.private_ip
}

output "private_ec2_2_ip" {
  description = "Private IP of EC2 instance 2"
  value       = aws_instance.private_ec2_2.private_ip
}

output "private_ec2_3_ip" {
  description = "Private IP of EC2 instance 3"
  value       = aws_instance.private_ec2_3.private_ip
}

output "all_private_ec2_ips" {
  description = "Map of all private EC2 instance IPs"
  value = {
    private_ec2_1 = aws_instance.private_ec2_1.private_ip
    private_ec2_2 = aws_instance.private_ec2_2.private_ip
    private_ec2_3 = aws_instance.private_ec2_3.private_ip
  }
} 