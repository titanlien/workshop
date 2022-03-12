output "route53_for_task1" {
  value = aws_route53_record.task1.fqdn
}

output "clb_dns_name" {
  value       = aws_elb.task1.dns_name
  description = "The domain name of the task1 load balancer"
}

output "spot_instance_private_ip" {
  value = module.worker.spot_instance_private_ip
}
