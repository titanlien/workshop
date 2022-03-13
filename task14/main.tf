module "s3-bucket" {
  source  = "cloudposse/s3-bucket/aws"
  version = "0.49.0"
  enabled = true

  acl                           = "private"
  block_public_policy           = false
  block_public_acls             = false
  user_enabled                  = false
  versioning_enabled            = false
  lifecycle_configuration_rules = local.lifecycle_configuration_rules

  name      = var.bucket_name
  namespace = var.namespace
  stage     = var.env
}
