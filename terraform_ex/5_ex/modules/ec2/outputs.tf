output "instance_id" {
  value = aws_instance.web.id
}
output "public_id" {
  value = aws_instance.web.public_ip
}
