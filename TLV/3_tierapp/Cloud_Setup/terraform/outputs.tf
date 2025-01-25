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
  description = "Private IP of EC2 instance 1 (Update Color Service)"
  value       = aws_instance.private_ec2_1.private_ip
}

output "private_ec2_2_ip" {
  description = "Private IP of EC2 instance 2 (Query Color Service)"
  value       = aws_instance.remaining_ec2["private_ec2_2"].private_ip
}

output "private_ec2_3_ip" {
  description = "Private IP of EC2 instance 3 (Not Allowed Service)"
  value       = aws_instance.remaining_ec2["private_ec2_3"].private_ip
}

# If you need all remaining EC2 IPs in a map format
output "all_remaining_ec2_ips" {
  description = "Private IPs of all remaining EC2 instances"
  value = {
    for instance, details in aws_instance.remaining_ec2 :
    instance => details.private_ip
  }
} 