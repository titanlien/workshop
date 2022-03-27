output "bucket_domain_name" {
  value = module.s3-bucket.bucket_domain_name
}

output "final_whitelist_ips" {
  value = local.whitelistIPs
}
